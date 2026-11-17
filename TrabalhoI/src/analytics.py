"""Estatísticas descritivas servidas pela API, calculadas sempre sobre a base processada real."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np
import pandas as pd

from src.common import CatalogoEquipes, ErroApi
from src.data_analysis import construir_tabela_longa

TEMPORADAS_VALIDAS = {"all", "2020", "2021", "2022", "2023"}
MANDOS_VALIDOS = {"all", "home", "away"}
MIN_JOGOS_RANKING = 10
TAMANHO_MAXIMO_PAGINA = 50


def _numero(valor: Any, casas: int = 2) -> float | None:
    return None if pd.isna(valor) else round(float(valor), casas)


class Analises:
    def __init__(self, partidas: pd.DataFrame, catalogo: CatalogoEquipes):
        self.df = partidas
        self.catalogo = catalogo
        longa = construir_tabela_longa(partidas)
        longa = longa.merge(
            partidas[["id_partida", "amarelos_mandante", "amarelos_visitante", "expulsoes_mandante", "expulsoes_visitante"]],
            on="id_partida",
        )
        eh_mandante = longa["mando"] == "mandante"
        longa["amarelos"] = np.where(eh_mandante, longa["amarelos_mandante"], longa["amarelos_visitante"])
        longa["expulsoes"] = np.where(eh_mandante, longa["expulsoes_mandante"], longa["expulsoes_visitante"])
        self.longa = longa.drop(columns=["amarelos_mandante", "amarelos_visitante", "expulsoes_mandante", "expulsoes_visitante"])
        self.temporadas = sorted(int(t) for t in partidas["temporada"].unique())
        self._cache_visao = lru_cache(maxsize=256)(self._visao_geral)
        self._cache_graficos = lru_cache(maxsize=256)(self._graficos)

    # ------------------------------------------------------------------ #
    # Filtros
    # ------------------------------------------------------------------ #
    def validar_filtros(self, temporada: str = "all", equipe: str = "all", mando: str = "all") -> tuple[str, str | None, str]:
        if temporada not in TEMPORADAS_VALIDAS:
            raise ErroApi(400, "parametro_invalido", "season deve ser 'all' ou um ano entre 2020 e 2023.")
        if mando not in MANDOS_VALIDOS:
            raise ErroApi(400, "parametro_invalido", "venue deve ser 'all', 'home' ou 'away'.")
        oficial = None if equipe in ("all", "", None) else self.catalogo.resolver(equipe)
        return temporada, oficial, mando

    def recorte(self, temporada: str, oficial: str | None, mando: str) -> pd.DataFrame:
        df = self.df
        if temporada != "all":
            df = df[df["temporada"] == int(temporada)]
        if oficial is not None:
            if mando == "home":
                df = df[df["home_team"] == oficial]
            elif mando == "away":
                df = df[df["away_team"] == oficial]
            else:
                df = df[(df["home_team"] == oficial) | (df["away_team"] == oficial)]
        return df  # o mando só tem efeito quando há uma equipe selecionada

    # ------------------------------------------------------------------ #
    # Indicadores
    # ------------------------------------------------------------------ #
    def visao_geral(self, temporada="all", equipe="all", mando="all") -> dict[str, Any]:
        return self._cache_visao(*self.validar_filtros(temporada, equipe, mando))

    def _visao_geral(self, temporada: str, oficial: str | None, mando: str) -> dict[str, Any]:
        d = self.recorte(temporada, oficial, mando)
        n = len(d)
        base = {
            "total_matches": n,
            "seasons": sorted(int(t) for t in d["temporada"].unique()),
            "teams": int(pd.concat([d["home_team"], d["away_team"]]).nunique()) if n else 0,
            "first_date": str(d["data_partida"].min())[:10] if n else None,
            "last_date": str(d["data_partida"].max())[:10] if n else None,
        }
        if n == 0:
            return {**base, "total_goals": 0, "goals_average": 0.0, "total_yellow_cards": 0, "yellow_cards_average": 0.0,
                    "total_red_cards": 0, "red_cards_average": 0.0, "home_win_percentage": 0.0, "draw_percentage": 0.0,
                    "away_win_percentage": 0.0, "attendance_average": None, "matches_with_attendance": 0,
                    "matches_without_attendance": 0}
        gols = int(d["total_gols"].sum())
        publico = d["publico"].dropna()
        return {
            **base,
            "total_goals": gols,
            "goals_average": round(gols / n, 2),
            "total_yellow_cards": int(d["total_amarelos"].sum()),
            "yellow_cards_average": round(float(d["total_amarelos"].mean()), 2),
            "total_red_cards": int(d["total_expulsoes"].sum()),
            "red_cards_average": round(float(d["total_expulsoes"].mean()), 2),
            "home_win_percentage": round(float((d["resultado"] == "home_win").mean()), 4),
            "draw_percentage": round(float((d["resultado"] == "draw").mean()), 4),
            "away_win_percentage": round(float((d["resultado"] == "away_win").mean()), 4),
            "attendance_average": int(round(publico.mean())) if len(publico) else None,
            "matches_with_attendance": int(len(publico)),
            "matches_without_attendance": int(n - len(publico)),
        }

    def graficos(self, temporada="all", equipe="all", mando="all") -> dict[str, Any]:
        return self._cache_graficos(*self.validar_filtros(temporada, equipe, mando))

    def _graficos(self, temporada: str, oficial: str | None, mando: str) -> dict[str, Any]:
        d = self.recorte(temporada, oficial, mando)
        n = len(d)
        vazio = {"result_distribution": [], "results_by_season": [], "goals_by_season": [], "cards_by_season": [],
                 "attendance_by_season": [], "top_winners": [], "top_goals": [], "top_cards": [],
                 "rankings_available": oficial is None}
        if n == 0:
            return vazio

        distribuicao = [
            {"name": nome, "value": round(float((d["resultado"] == classe).mean()) * 100, 1), "count": int((d["resultado"] == classe).sum())}
            for classe, nome in (("home_win", "Mandante"), ("draw", "Empate"), ("away_win", "Visitante"))
        ]
        por_temporada = d.groupby("temporada")
        resultados_temp = [
            {"season": str(t), "home_win": int((g["resultado"] == "home_win").sum()),
             "draw": int((g["resultado"] == "draw").sum()), "away_win": int((g["resultado"] == "away_win").sum())}
            for t, g in por_temporada
        ]
        gols_temp = [{"season": str(t), "goals_average": round(float(g["total_gols"].mean()), 2), "matches": int(len(g))}
                     for t, g in por_temporada]
        cartoes_temp = [{"season": str(t), "yellow": round(float(g["total_amarelos"].mean()), 2),
                         "red": round(float(g["total_expulsoes"].mean()), 2)} for t, g in por_temporada]
        publico_temp = [
            {"season": str(t), "attendance_average": int(round(g["publico"].mean())) if g["publico"].notna().any() else None,
             "matches_with_attendance": int(g["publico"].notna().sum()), "matches": int(len(g))}
            for t, g in por_temporada
        ]

        top_v, top_g, top_c = [], [], []
        if oficial is None:  # rankings só fazem sentido comparando várias equipes
            longa = self.longa[self.longa["id_partida"].isin(d["id_partida"])]
            agg = longa.groupby("equipe").agg(
                jogos=("id_partida", "count"), vitorias=("vitoria", "sum"), gols=("gols_pro", "sum"),
                amarelos=("amarelos", "sum"), expulsoes=("expulsoes", "sum"),
            )
            agg["nome"] = [self.catalogo.nome_curto(e) for e in agg.index]
            top_v = [{"team": r.nome, "wins": int(r.vitorias)} for r in agg.sort_values("vitorias", ascending=False).head(5).itertuples()]
            elegiveis = agg[agg["jogos"] >= MIN_JOGOS_RANKING].copy()
            elegiveis["media_gols"] = elegiveis["gols"] / elegiveis["jogos"]
            elegiveis["media_cartoes"] = (elegiveis["amarelos"] + elegiveis["expulsoes"]) / elegiveis["jogos"]
            top_g = [{"team": r.nome, "goals_average": round(float(r.media_gols), 2)}
                     for r in elegiveis.sort_values("media_gols", ascending=False).head(5).itertuples()]
            top_c = [{"team": r.nome, "cards": round(float(r.media_cartoes), 2)}
                     for r in elegiveis.sort_values("media_cartoes", ascending=False).head(5).itertuples()]

        return {
            "result_distribution": distribuicao, "results_by_season": resultados_temp, "goals_by_season": gols_temp,
            "cards_by_season": cartoes_temp, "attendance_by_season": publico_temp, "top_winners": top_v,
            "top_goals": top_g, "top_cards": top_c, "rankings_available": oficial is None,
        }

    # ------------------------------------------------------------------ #
    # Tabela de partidas
    # ------------------------------------------------------------------ #
    def partidas(self, temporada="all", equipe="all", mando="all", pagina: int = 1, tamanho: int = 5) -> dict[str, Any]:
        if tamanho < 1 or tamanho > TAMANHO_MAXIMO_PAGINA:
            raise ErroApi(400, "parametro_invalido", f"page_size deve estar entre 1 e {TAMANHO_MAXIMO_PAGINA}.")
        if pagina < 1:
            raise ErroApi(400, "parametro_invalido", "page deve ser maior ou igual a 1.")
        d = self.recorte(*self.validar_filtros(temporada, equipe, mando)).sort_values(["data_partida", "id_partida"], ascending=False)
        total = len(d)
        paginas = max(1, -(-total // tamanho))
        pagina = min(pagina, paginas)
        recorte = d.iloc[(pagina - 1) * tamanho: pagina * tamanho]
        linhas = [
            {
                "id": str(int(r.id_partida)),
                "date": str(r.data_partida)[:10],
                "season": str(int(r.temporada)),
                "home_team": self.catalogo.nome_curto(r.home_team),
                "away_team": self.catalogo.nome_curto(r.away_team),
                "score": f"{int(r.home_team_score)} x {int(r.away_team_score)}",
                "yellow_cards": int(r.total_amarelos),
                "red_cards": int(r.total_expulsoes),
                "stadium": str(r.stadium),
                "attendance": None if pd.isna(r.publico) else int(r.publico),
            }
            for r in recorte.itertuples()
        ]
        return {"matches": linhas, "total": total, "page": pagina, "pages": paginas}

    # ------------------------------------------------------------------ #
    # Equipes
    # ------------------------------------------------------------------ #
    def resumo_equipe(self, identificador: str) -> dict[str, Any]:
        oficial = self.catalogo.resolver(identificador)
        l = self.longa[self.longa["equipe"] == oficial].sort_values("data_partida")
        jogos = len(l)

        def bloco(g: pd.DataFrame) -> dict[str, Any]:
            n = len(g)
            return {
                "matches": n,
                "wins": int(g["vitoria"].sum()), "draws": int(g["empate"].sum()), "losses": int(g["derrota"].sum()),
                "goals_for": int(g["gols_pro"].sum()), "goals_against": int(g["gols_contra"].sum()),
                "points": int(g["pontos"].sum()),
                "points_rate": round(float(g["pontos"].sum()) / (3 * n), 4) if n else None,
                "goals_for_average": round(float(g["gols_pro"].mean()), 2) if n else None,
                "goals_against_average": round(float(g["gols_contra"].mean()), 2) if n else None,
                "yellow_cards_average": round(float(g["amarelos"].mean()), 2) if n else None,
                "red_cards_average": round(float(g["expulsoes"].mean()), 2) if n else None,
            }

        por_temporada = [{"season": str(int(t)), **bloco(g)} for t, g in l.groupby("temporada")]
        publico = self.df[self.df["home_team"] == oficial]["publico"].dropna()
        return {
            "team": self.catalogo.info(oficial),
            "overall": bloco(l),
            "home": bloco(l[l["mando"] == "mandante"]),
            "away": bloco(l[l["mando"] == "visitante"]),
            "by_season": por_temporada,
            "last_five": ["V" if v else "E" if e else "D" for v, e in zip(l["vitoria"].tail(5), l["empate"].tail(5))],
            "home_attendance_average": int(round(publico.mean())) if len(publico) else None,
            "matches_total": jogos,
        }

    def comparar(self, equipe_a: str, equipe_b: str) -> dict[str, Any]:
        a, b = self.catalogo.resolver(equipe_a), self.catalogo.resolver(equipe_b)
        if a == b:
            raise ErroApi(422, "equipes_iguais", "Escolha duas equipes diferentes para comparar.")
        d = self.df
        confrontos = d[((d["home_team"] == a) & (d["away_team"] == b)) | ((d["home_team"] == b) & (d["away_team"] == a))]
        vit_a = vit_b = emp = 0
        for r in confrontos.itertuples():
            ga, gb = (r.home_team_score, r.away_team_score) if r.home_team == a else (r.away_team_score, r.home_team_score)
            vit_a += ga > gb
            vit_b += ga < gb
            emp += ga == gb
        return {
            "team_a": self.resumo_equipe(equipe_a),
            "team_b": self.resumo_equipe(equipe_b),
            "head_to_head": {
                "matches": int(len(confrontos)), "team_a_wins": int(vit_a), "draws": int(emp), "team_b_wins": int(vit_b),
                "last_matches": [
                    {"date": str(r.data_partida)[:10], "home_team": self.catalogo.nome_curto(r.home_team),
                     "away_team": self.catalogo.nome_curto(r.away_team), "score": f"{int(r.home_team_score)} x {int(r.away_team_score)}"}
                    for r in confrontos.sort_values("data_partida", ascending=False).head(5).itertuples()
                ],
            },
        }
