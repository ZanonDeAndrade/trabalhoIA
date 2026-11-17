"""Compatibilidade: gera as evidências do relatório reaproveitando o pipeline de treino.

Uso: python src/documentation_evidence.py

O experimento completo (treino, validação, teste, modelo salvo, métricas e figuras) é executado
uma única vez por ``src/modeling.py``; este módulo apenas o chama e devolve o dicionário de
resultados, que também é gravado em ``reports/evidencias/metricas_execucao.json``.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.modeling import executar_experimento_completo


def executar_evidencias() -> dict[str, Any]:
    """Reexecuta o protocolo temporal e regrava modelo, métricas, figuras e exemplos."""
    print("INÍCIO | Execução real do protocolo temporal (treino 2020–21, validação 2022, teste 2023)")
    resultados = executar_experimento_completo(salvar=True)
    teste = resultados["final"]["teste"]
    print(f"CONCLUÍDO | {resultados['modelo_selecionado']} | acurácia teste {teste['acuracia']:.2%} | Macro F1 {teste['f1_macro']:.3f}")
    return resultados


if __name__ == "__main__":
    executar_evidencias()
