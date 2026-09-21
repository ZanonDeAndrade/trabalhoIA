"""Evidências reproduzíveis para o relatório, sem alterar a seleção do modelo.

Uso: python src/documentation_evidence.py
Gera reports/evidencias/metricas_execucao.json e previsoes_exemplo.json.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from src.data_split import carregar_e_dividir_dados
from src.modeling import construir_modelos, avaliar_modelo


def resumir(r):
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v)
            for k, v in vars(r).items()}


def executar_evidencias():
    """Reproduz o protocolo congelado e exporta métricas e exemplos cronológicos."""
    p = carregar_e_dividir_dados()
    print('INÍCIO | Execução real do protocolo temporal')
    print(f'Treino: {len(p.X_train)} | Validação: {len(p.X_val)} | Teste: {len(p.X_test)}')
    print('Treino 2020–2021 → validação 2022 → teste 2023')
    modelos = construir_modelos(p.features_numericas, p.features_categoricas)
    validacao, treino = [], []
    for nome, pipe in modelos.items():
        pipe.fit(p.X_train, p.y_train)
        treino.append(resumir(avaliar_modelo(pipe, p.X_train, p.y_train, nome, 'Treino (2020–2021)')))
        r = avaliar_modelo(pipe, p.X_val, p.y_val, nome, 'Validação (2022)')
        validacao.append(resumir(r))
        print(f'{nome}: Macro F1 validação = {r.f1_macro:.3f}')
    escolhido = max((r for r in validacao if 'Baseline' not in r['nome_modelo']), key=lambda r:r['f1_macro'])['nome_modelo']
    print(f'Seleção somente pela validação: {escolhido}')
    final = modelos[escolhido]
    final.fit(p.X_train_val, p.y_train_val)
    teste = resumir(avaliar_modelo(final, p.X_test, p.y_test, escolhido, 'Teste (2023)'))
    treino_final = resumir(avaliar_modelo(final, p.X_train_val, p.y_train_val, escolhido, 'Treino final (2020–2022)'))
    baselines = {}
    for nome, estrategia in [('majoritaria','most_frequent'),('frequencias','prior')]:
        dummy = DummyClassifier(strategy=estrategia).fit(p.X_train_val,p.y_train_val)
        baselines[nome] = resumir(avaliar_modelo(dummy,p.X_test,p.y_test,nome,'Teste (2023)'))

    # Exemplos: oito primeiras partidas elegíveis de 2023, sem escolher por acerto.
    x = p.X_test.head(8)
    prob, pred = final.predict_proba(x), final.predict(x)
    rotulos = {0:'Mandante',1:'Empate',2:'Visitante'}
    exemplos = []
    for i, (_, partida) in enumerate(p.df_test.head(8).iterrows()):
        exemplos.append({'id_partida':int(partida.id_partida),'data':str(partida.data_partida),
            'mandante':partida.home_team,'visitante':partida.away_team,
            'p_mandante':float(prob[i,0]),'p_empate':float(prob[i,1]),'p_visitante':float(prob[i,2]),
            'previsto':rotulos[int(pred[i])],'real':rotulos[int(partida.resultado_codigo)],
            'placar':f'{partida.home_team_score} × {partida.away_team_score}',
            'acertou':bool(pred[i]==partida.resultado_codigo)})
    prep = final.named_steps['prep']
    medianas_ok = bool(np.allclose(prep.named_transformers_['num'].named_steps['imputer'].statistics_,
                                    p.X_train_val[p.features_numericas].median().to_numpy()))
    coef = pd.Series(np.mean(np.abs(final.named_steps['clf'].coef_),axis=0),
                     index=prep.get_feature_names_out()).sort_values(ascending=False)
    dados = {'executado_em':datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec='seconds'),
             'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,
             'sha256_csv_original':hashlib.sha256((ROOT/'partidas_20_23.csv').read_bytes()).hexdigest(),
             'particoes':{'treino':len(p.X_train),'validacao':len(p.X_val),'teste':len(p.X_test),'treino_final':len(p.X_train_val)},
             'ausencias_mando':{'treino':int(p.X_train.isna().any(axis=1).sum()),'validacao':int(p.X_val.isna().any(axis=1).sum()),'teste':int(p.X_test.isna().any(axis=1).sum())},
             'medianas_apenas_treino_final':medianas_ok,'modelo_selecionado':escolhido,
             'treino':treino,'validacao':validacao,'treino_final':treino_final,'teste':teste,'baselines_teste':baselines,
             'coeficientes_top15':coef.head(15).to_dict(),'exemplos':exemplos}
    pasta = ROOT/'reports/evidencias'
    pasta.mkdir(parents=True,exist_ok=True)
    (pasta/'metricas_execucao.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2),encoding='utf-8')
    (pasta/'previsoes_exemplo.json').write_text(json.dumps(exemplos,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'CONCLUÍDO | {escolhido} | acurácia teste {teste["acuracia"]:.2%} | Macro F1 {teste["f1_macro"]:.3f}')
    print(f'Medianas calculadas apenas em treino + validação: {medianas_ok}')
    print('Evidências salvas em reports/evidencias/')
    return dados


if __name__ == '__main__':
    executar_evidencias()
