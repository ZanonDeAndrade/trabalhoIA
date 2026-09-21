"""Alinha os textos antigos com a interpretação verificada no relatório final."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
repls={
'pois obteve o melhor equilíbrio de generalização e maior Macro F1-Score.':'pois obteve o maior Macro F1-Score na validação; a escolha não implica superioridade em todas as métricas.',
'1. **Diferenciais de Rendimento:** Variáveis calculadas como a diferença de saldo de gols e média de pontos dos últimos 5 jogos entre mandante e visitante despontaram como as mais influentes para orientar as probabilidades dos modelos.':'1. **Coeficientes:** Os 15 maiores valores da média absoluta dos coeficientes correspondem a categorias de equipes e dia da semana. O gráfico não sustenta a predominância dos diferenciais de pontos ou saldo de gols e não demonstra causalidade.',
'2. **Dificuldade Intrínseca do Empate:** O empate é notoriamente a classe mais difícil de ser discriminada no futebol moderno, pois reflete um equilíbrio dinâmico e contingências durante a partida, sendo raramente previsto com alta probabilidade a priori.':'2. **Dificuldade do Empate no Experimento:** O modelo acertou 15 dos 94 empates no teste (recall de 16,0%). O resultado limita sua capacidade de reconhecer essa classe.',
'3. **Validade e Integridade Temporal:** O pipeline executou 100% livre de vazamento de dados (*data leakage*), produzindo métricas realistas e reprodutíveis com a semente fixa `RANDOM_STATE = 42`.':'3. **Integridade Temporal e Limites:** As partições cronológicas e os históricos deslocados evitam usar a própria partida nas entradas. O teste é sequencial por jogo e pode usar partidas anteriores de 2023. As verificações não constituem garantia universal contra vazamento. Consulte relatorio_tecnico.pdf para comparação com frequências históricas e limitações.',
}
for name in ['src/modeling.py','reports/resultados_modelagem.md']:
    p=ROOT/name; s=p.read_text(encoding='utf-8')
    for a,b in repls.items(): s=s.replace(a,b)
    p.write_text(s,encoding='utf-8')
p=ROOT/'notebooks/02_modelagem_classificacao.ipynb'; n=json.loads(p.read_text(encoding='utf-8'))
for c in n['cells']:
    s=''.join(c['source'])
    if c['cell_type']=='code': s=s.replace('"20.057"','"19.117"').replace('"-18.968"','"-18.029"')
    if s.startswith('## 8. Conclusões'):
        s='''## 8. Conclusões e considerações metodológicas

1. **Protocolo temporal:** treino em 2020-2021, validação em 2022 e teste em 2023. Históricos anteriores ao jogo e transformações ajustadas no treino evitam incorporar a própria partida nas entradas. O teste pode usar partidas anteriores já encerradas em 2023.
2. **Desempenho:** Macro F1 de 0,360 e acurácia balanceada de 37,26%, superiores à referência majoritária (0,213 e 33,33%). A acurácia global de 44,48% é inferior aos 46,96% da referência. Apenas 15 de 94 empates e 23 de 98 vitórias de visitantes foram reconhecidos.
3. **Coeficientes:** os 15 maiores valores da média absoluta correspondem a categorias de equipes e dia da semana. Não se pode concluir que os diferenciais de saldo e pontos sejam os atributos de maior magnitude, nem interpretar o gráfico como efeito causal.
4. **Probabilidades:** a comparação adicional do relatório final usa frequências históricas ajustadas em treino mais validação: Log-Loss de 1,061 e Brier de 0,640, melhores que os 1,089 e 0,652 do modelo. Não há evidência de superioridade geral.

Consulte `reports/relatorio_tecnico.pdf` e o notebook `03_demonstracao_funcionamento.ipynb` para as evidências consolidadas.
'''
    c['source']=s.splitlines(keepends=True)
p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Textos atualizados.')
