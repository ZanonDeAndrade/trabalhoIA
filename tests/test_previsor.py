"""O serviço de previsão deve montar exatamente as mesmas variáveis usadas no treinamento."""
from __future__ import annotations


import pandas as pd
import pytest

from src.common import CatalogoEquipes, ErroApi, carregar_partidas
from src.data_split import criar_features_diferenciais
from src.predictor import ServicoPrevisao


@pytest.fixture(scope="module")
def servico():
    df = carregar_partidas()
    return ServicoPrevisao(df, CatalogoEquipes(df))


@pytest.fixture(scope="module")
def completo():
    df, _ = criar_features_diferenciais(carregar_partidas())
    return df


def test_atributos_do_servico_sao_identicos_aos_do_conjunto_de_treino(servico, completo):
    amostra = completo[completo["utilizavel_ml"] == 1].sample(40, random_state=7)
    for _, r in amostra.iterrows():
        x = servico.atributos_confronto(r["home_team"], r["away_team"], r["data_partida"].to_pydatetime()).iloc[0]
        for coluna in servico.colunas_entrada:
            if coluna in ("home_team", "away_team", "dia_semana"):
                assert x[coluna] == r[coluna], coluna
            elif pd.isna(r[coluna]):
                assert pd.isna(x[coluna]), coluna
            else:
                assert x[coluna] == pytest.approx(r[coluna], abs=1e-9), coluna


def test_o_proprio_jogo_nao_entra_nos_atributos(servico, completo):
    """Mesmos atributos mesmo que o placar da partida consultada fosse outro: só jogos anteriores são lidos."""
    r = completo[(completo["utilizavel_ml"] == 1) & (completo["temporada"] == 2023)].iloc[5]
    original = servico.atributos_confronto(r["home_team"], r["away_team"], r["data_partida"].to_pydatetime())
    servico.df.loc[servico.df["id_partida"] == r["id_partida"], ["home_team_score", "away_team_score"]] = [8, 8]
    try:
        alterado = servico.atributos_confronto(r["home_team"], r["away_team"], r["data_partida"].to_pydatetime())
    finally:
        servico.df.loc[servico.df["id_partida"] == r["id_partida"], ["home_team_score", "away_team_score"]] = [r["home_team_score"], r["away_team_score"]]
    pd.testing.assert_frame_equal(original, alterado)


def test_previsao_retrospectiva_devolve_resultado_real_e_probabilidades_validas(servico):
    resposta = servico.prever(None, None, id_partida=1461)
    p = resposta["probabilities"]
    assert set(p) == {"home_win", "draw", "away_win"}
    assert all(0 <= v <= 1 for v in p.values()) and sum(p.values()) == pytest.approx(1, abs=1e-3)
    assert resposta["prediction"] == max(p, key=p.get)
    assert resposta["actual"]["score"] == "3 x 0"
    assert resposta["reference"]["hypothetical"] is False
    assert resposta["actual"]["used_in_training"] is False


def test_previsao_hipotetica_usa_historico_ate_a_ultima_partida(servico):
    resposta = servico.prever("flamengo", "palmeiras")
    assert resposta["reference"]["hypothetical"] is True
    assert resposta["reference"]["history_until"] == "2023-12-06"
    assert resposta["reference"]["date"] == "2023-12-07"
    assert len(resposta["home_team_form"]["last_five"]) == 5
    assert resposta["head_to_head"]["matches"] == 8


def test_forma_recente_corresponde_aos_ultimos_jogos_reais(servico):
    resposta = servico.prever("flamengo", "palmeiras")
    df = servico.df
    fla = df[(df["home_team"] == "CR Flamengo") | (df["away_team"] == "CR Flamengo")].tail(5)
    esperado = []
    for _, j in fla.iterrows():
        gp, gc = (j["home_team_score"], j["away_team_score"]) if j["home_team"] == "CR Flamengo" else (j["away_team_score"], j["home_team_score"])
        esperado.append("V" if gp > gc else "E" if gp == gc else "D")
    assert resposta["home_team_form"]["last_five"] == esperado


def test_datas_de_referencia_sao_validadas(servico):
    with pytest.raises(ErroApi) as e:
        servico.prever("flamengo", "palmeiras", data="07/12/2023")
    assert e.value.status == 400
    with pytest.raises(ErroApi) as e:
        servico.prever("flamengo", "palmeiras", data="2030-01-01")
    assert e.value.status == 422
    with pytest.raises(ErroApi) as e:
        servico.prever("flamengo", "palmeiras", data="2023-06-01", hora=30)
    assert e.value.status == 400


def test_equipe_sem_jogos_na_temporada_de_referencia_e_recusada(servico):
    with pytest.raises(ErroApi) as e:
        servico.prever("sport", "flamengo")
    assert e.value.status == 422 and e.value.codigo == "historico_insuficiente"


def test_data_no_passado_recalcula_o_historico_daquela_data(servico):
    a = servico.prever("flamengo", "palmeiras", data="2022-06-01")
    b = servico.prever("flamengo", "palmeiras", data="2023-12-07")
    assert a["reference"]["history_until"] < b["reference"]["history_until"]
    assert a["home_team_form"] != b["home_team_form"]


def test_equipes_iguais_sao_recusadas(servico):
    with pytest.raises(ErroApi) as e:
        servico.prever("flamengo", "flamengo")
    assert e.value.codigo == "equipes_iguais"


def test_elegibilidade_reflete_temporada_de_referencia(servico):
    por_id = {e["id"]: e for e in servico.equipes()}
    assert por_id["flamengo"]["eligible"] is True
    assert por_id["sport"]["eligible"] is False and por_id["sport"]["reason"]
    assert sum(e["eligible"] for e in por_id.values()) == 20  # clubes que disputaram 2023
