"""Captura screenshots reais da aplicação em execução (front-end + API) e verifica erros no console.

Pré-requisitos: API e front-end rodando (veja o README) e o Playwright instalado:

    pip install -r requirements-dev.txt
    python -m playwright install chromium
    python scripts/capturar_screenshots.py --front http://127.0.0.1:5173

As imagens vão para ``reports/screenshots/``. O script falha se a interface não exibir os dados
esperados ou se o navegador registrar erros no console; nada é montado artificialmente.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright

RAIZ = Path(__file__).resolve().parents[1]


def capturar(front: str, saida: Path) -> list[str]:
    saida.mkdir(parents=True, exist_ok=True)
    erros: list[str] = []
    gerados: list[str] = []

    def salvar(pagina: Page, nome: str, tela_cheia: bool = True) -> None:
        pagina.wait_for_timeout(400)  # termina animações de gráficos
        pagina.screenshot(path=str(saida / nome), full_page=tela_cheia)
        gerados.append(nome)
        print(f"[OK] {nome}")

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        contexto = navegador.new_context(viewport={"width": 1366, "height": 900}, device_scale_factor=1.5, locale="pt-BR")
        pagina = contexto.new_page()
        pagina.on("console", lambda m: erros.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        pagina.on("pageerror", lambda e: erros.append(f"pageerror: {e}"))
        # Requisições canceladas de propósito (filtro trocado antes da resposta) não são falhas.
        pagina.on("requestfailed", lambda r: None if "ABORTED" in (r.failure or "") else erros.append(f"requestfailed: {r.url}"))

        # 1. Início
        pagina.goto(front)
        expect(pagina.get_by_text("Partidas analisadas")).to_be_visible()
        expect(pagina.get_by_text("1.520", exact=True)).to_be_visible()
        expect(pagina.locator(".model-status")).to_contain_text("ONLINE")
        salvar(pagina, "01_inicio.png")

        # 2. Seleção das equipes
        pagina.get_by_role("button", name="Previsão", exact=True).first.click()
        pagina.get_by_label("Time mandante").select_option("flamengo")
        pagina.get_by_label("Time visitante").select_option("palmeiras")
        expect(pagina.get_by_role("button", name="Calcular previsão")).to_be_enabled()
        salvar(pagina, "02_selecao_equipes.png", tela_cheia=False)

        # 3. Previsão, probabilidades e comparação histórica
        pagina.get_by_role("button", name="Calcular previsão").click()
        expect(pagina.get_by_label("Probabilidades da previsão")).to_be_visible()
        expect(pagina.get_by_text("Confronto direto na base")).to_be_visible()
        salvar(pagina, "03_previsao_probabilidades.png", tela_cheia=False)
        pagina.get_by_text("Indicadores históricos usados pelo modelo").scroll_into_view_if_needed()
        salvar(pagina, "04_previsao_comparacao_historica.png")

        # 4. Estatísticas: geral e filtrada
        pagina.get_by_role("button", name="Estatísticas", exact=True).first.click()
        expect(pagina.get_by_label("Indicadores do recorte selecionado")).to_be_visible()
        salvar(pagina, "05_estatisticas_geral.png")
        pagina.locator("#season-filter").select_option("2023")
        pagina.locator("#team-filter").select_option("flamengo")
        expect(pagina.get_by_label("Indicadores do recorte selecionado")).to_contain_text("38")
        salvar(pagina, "06_estatisticas_filtrada.png")

        # 5. Sobre o modelo
        pagina.get_by_role("button", name="Sobre o modelo", exact=True).first.click()
        expect(pagina.get_by_role("heading", name="Matriz de confusão (teste)")).to_be_visible()
        salvar(pagina, "07_sobre_o_modelo.png")

        # 6. Celular (390 px)
        movel = navegador.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="pt-BR", is_mobile=True)
        cel = movel.new_page()
        cel.on("console", lambda m: erros.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        cel.on("pageerror", lambda e: erros.append(f"pageerror: {e}"))
        cel.goto(front)
        cel.get_by_role("button", name="Fazer previsão").first.click()
        cel.get_by_label("Time mandante").select_option("corinthians")
        cel.get_by_label("Time visitante").select_option("santos")
        cel.get_by_role("button", name="Calcular previsão").click()
        expect(cel.get_by_label("Probabilidades da previsão")).to_be_visible()
        largura_pagina = cel.evaluate("document.documentElement.scrollWidth")
        if largura_pagina > 391:
            erros.append(f"rolagem horizontal no celular: scrollWidth={largura_pagina}")
        salvar(cel, "08_celular_previsao.png")
        movel.close()
        navegador.close()

    return erros if erros else []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--front", default="http://127.0.0.1:5173", help="URL do front-end em execução")
    ap.add_argument("--saida", default=str(RAIZ / "reports" / "screenshots"), help="pasta de saída")
    args = ap.parse_args()
    erros = capturar(args.front.rstrip("/"), Path(args.saida))
    if erros:
        print("\nERROS NO NAVEGADOR:", *erros, sep="\n - ")
        return 1
    print("\nCapturas concluídas sem erros no console.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
