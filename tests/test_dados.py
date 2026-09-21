"""Carga do CSV, datas, temporada, público, listas JSON, cartões e variável-alvo."""
from __future__ import annotations

import json

import pandas as pd
import pytest

from src import data_analysis as da
from src.common import sha256_texto
from src.data_split import CLASSES

COLUNAS_ORIGINAIS = [
    "home_team", "away_team", "home_team_score", "away_team_score", "game_date", "stadium", "public", "ref",
    "yellow_cards_home", "red_cards_home", "gols_home", "yellow_cards_away", "red_cards_away", "gols_away",
    "sec_card_home", "sec_card_away", "link",
]


def test_csv_original_tem_a_forma_esperada(bruto):
    assert bruto.shape == (1520, 17)
    assert list(bruto.columns) == COLUNAS_ORIGINAIS


def test_csv_original_esta_preservado_desde_o_treinamento():
    """O hash do CSV (sem diferença de fim de linha) deve ser o registrado nos metadados: o original não foi alterado."""
    meta = json.loads((da.RAIZ_PROJETO / "models" / "metadata.json").read_text(encoding="utf-8"))
    assert sha256_texto(da.CSV_ORIGINAL) == meta["sha256_csv_original"]


def test_estrutura_das_temporadas_e_equipes(processado):
    df, _ = processado
    assert df["temporada"].value_counts().sort_index().to_dict() == {2020: 380, 2021: 380, 2022: 380, 2023: 380}
    assert pd.concat([df["home_team"], df["away_team"]]).nunique() == 26
    assert df["link"].is_unique
    assert not df.duplicated(subset=["home_team", "away_team", "data_partida"]).any()


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("25 de fevereiro de 2021 21:30", pd.Timestamp("2021-02-25 21:30")),
        ("8 de agosto de 2020 16:00", pd.Timestamp("2020-08-08 16:00")),
        ("1 de março de 2023 09:05", pd.Timestamp("2023-03-01 09:05")),
    ],
)
def test_converte_datas_em_portugues(texto, esperado):
    assert da.converter_data_ptbr(pd.Series([texto])).iloc[0] == esperado


def test_converte_todos_os_meses_em_portugues():
    resultado = da.converter_data_ptbr(pd.Series([f"10 de {m} de 2021 10:00" for m in da.MAPA_MESES]))
    assert resultado.dt.month.tolist() == list(range(1, 13))


def test_data_invalida_vira_nat_sem_erro():
    serie = pd.Series(["31 de fevereiro de 2021 10:00", "10 de abril 2021", "10 de xpto de 2021 10:00"])
    assert da.converter_data_ptbr(serie).isna().all()


def test_nenhuma_data_da_base_ficou_sem_conversao(processado):
    df, aux = processado
    assert aux["datas_nao_interpretadas"] == 0
    assert df["data_partida"].min() == pd.Timestamp("2020-08-08 16:00") or df["data_partida"].min().year == 2020
    assert df["data_partida"].max().year == 2023


def test_temporada_vem_do_link_e_nao_do_ano_da_data(processado):
    df, aux = processado
    assert aux["temporadas_nao_extraidas"] == 0
    virada = df[(df["temporada"] == 2020) & (df["ano_calendario"] == 2021)]
    assert len(virada) > 0  # jogos da temporada 2020 disputados em 2021
    vasco_goias = df[(df["home_team"] == "CR Vasco da Gama") & (df["data_partida"].dt.strftime("%Y-%m-%d") == "2021-02-25")]
    assert vasco_goias["temporada"].iloc[0] == 2020


def test_extrai_temporada_de_link_codificado():
    link = "https://x/pt_BR/soccer/brasileir%C3%A3o-s%C3%A9rie-a-2022/abc/match/view/xyz"
    assert da.extrair_temporada(pd.Series([link])).iloc[0] == 2022


@pytest.mark.parametrize(
    "texto,esperado",
    [("12.345", 12345), ("999", 999), ("1.234.567", 1234567)],
)
def test_publico_com_ponto_de_milhar(texto, esperado):
    valores, inesperados = da.converter_publico(pd.Series([texto]))
    assert valores.iloc[0] == esperado and inesperados == 0


def test_publico_no_data_e_ausente_nao_zero(processado):
    valores, inesperados = da.converter_publico(pd.Series(["No data", "1.000"]))
    assert pd.isna(valores.iloc[0]) and valores.iloc[1] == 1000 and inesperados == 0
    df, _ = processado
    assert df["publico"].isna().sum() == 613  # documentado na EDA
    assert (df["publico"].dropna() > 0).all()


def test_listas_json_validas_e_vazias():
    assert da.converter_lista_json('[{"player": "A", "minute": "17\'"}]') == [{"player": "A", "minute": "17'"}]
    assert da.converter_lista_json("[]") == []


def test_lista_json_invalida_nao_executa_codigo():
    registro: list = []
    perigoso = "__import__('os').system('touch /tmp/pwned_ia2')"
    assert da.converter_lista_json(perigoso, "col", 0, registro) == []
    assert registro and "JSON inválido" in registro[0]["motivo"]
    from pathlib import Path
    assert not Path("/tmp/pwned_ia2").exists()


def test_lista_json_com_elementos_invalidos_e_registrada():
    registro: list = []
    assert da.converter_lista_json('[{"a": 1}, 5]', "col", 3, registro) == [{"a": 1}]
    assert registro[0]["motivo"] == "elementos que não são objetos"


def test_toda_lista_json_da_base_e_valida(processado):
    _, aux = processado
    assert len(aux["inconsistencias_json"]) == 0


def test_eventos_e_cartoes_batem_com_as_listas(processado, bruto_texto):
    df, aux = processado
    for lado, sufixo in (("home", "mandante"), ("away", "visitante")):
        assert (df[f"amarelos_{sufixo}"] == aux["listas"][f"yellow_cards_{lado}"].map(len)).all()
        assert (df[f"vermelhos_diretos_{sufixo}"] == aux["listas"][f"red_cards_{lado}"].map(len)).all()
        assert (df[f"segundos_amarelos_{sufixo}"] == aux["listas"][f"sec_card_{lado}"].map(len)).all()
        assert (df[f"expulsoes_{sufixo}"] == df[f"vermelhos_diretos_{sufixo}"] + df[f"segundos_amarelos_{sufixo}"]).all()
        penais = aux["listas"][f"gols_{lado}"].map(lambda l: sum(1 for g in l if g.get("penal") == 1))
        contra = aux["listas"][f"gols_{lado}"].map(lambda l: sum(1 for g in l if g.get("cont") == 1))
        assert (df[f"penaltis_convertidos_{sufixo}"] == penais).all()
        assert (df[f"gols_contra_{sufixo}"] == contra).all()
    assert (df["total_amarelos"] == df["amarelos_mandante"] + df["amarelos_visitante"]).all()


def test_variavel_alvo_vem_do_placar(processado):
    df, _ = processado
    assert set(df["resultado"].unique()) == set(CLASSES)
    diferenca = df["home_team_score"] - df["away_team_score"]
    assert (df.loc[diferenca > 0, "resultado"] == "home_win").all()
    assert (df.loc[diferenca == 0, "resultado"] == "draw").all()
    assert (df.loc[diferenca < 0, "resultado"] == "away_win").all()
    assert df["resultado_codigo"].map({0: "home_win", 1: "draw", 2: "away_win"}).equals(df["resultado"])
    assert df["resultado"].value_counts().to_dict() == {"home_win": 691, "draw": 427, "away_win": 402}


def test_placares_sao_validos(processado):
    df, _ = processado
    assert df[["home_team_score", "away_team_score"]].notna().all().all()
    assert (df[["home_team_score", "away_team_score"]] >= 0).all().all()
    assert (df["total_gols"] == df["home_team_score"] + df["away_team_score"]).all()


def test_base_processada_do_repositorio_bate_com_o_reprocessamento(processado):
    """O CSV processado versionado deve ser reproduzível a partir do original."""
    df, _ = processado
    salvo = pd.read_csv(da.CSV_PROCESSADO, parse_dates=["data_partida"])
    assert len(salvo) == len(df)
    colunas = ["id_partida", "temporada", "resultado", "pontos_media_ultimos_5_mandante", "utilizavel_ml"]
    for c in colunas:
        pd.testing.assert_series_equal(salvo[c].reset_index(drop=True), df[c].reset_index(drop=True), check_dtype=False, check_names=False)
