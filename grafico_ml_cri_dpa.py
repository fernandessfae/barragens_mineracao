import matplotlib.pyplot as plt
from numpy import arange
from typing import List

def grafico_acuracia_ml(nome_modelos: List[str],
                        acuracia_modelos: List[int],
                        titulo: str) -> None:
    """Função para geração de gráfico que compara a acurácia entre 
       os modelos de machine learning.
       param nome_modelos: Nome dos modelos de machine learning selecionados
       type nome_modelos: List[str]
       param acuracia_modelos: Pontuação dos modelo de machine learning
       selecionados
       type acuracia_modelos: List[int]
       param titulo: Nome do título do gráfico
       type titulo: str
    """
    plt.figure(figsize=(15, 5))
    plt.bar(nome_modelos,
            acuracia_modelos,
            color=plt.cm.Set3(arange(len(nome_modelos))))
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel('Precisão (%)')
    plt.grid(axis='y')
    plt.show();
    return None


nome_modelos_ml: List[str] = ['Naive Bays', 'Decision Tree',
                              'KNN', 'SVM', 'Random Forest']

acuracia_modelos_cri: List[int] = [71, 77, 77, 80, 81]
acuracia_modelos_dpa: List[int] = [37, 82, 74, 80, 82]

grafico_acuracia_ml(nome_modelos_ml,
                    acuracia_modelos_cri,
                    'Comparação da acurácia entre os modelos de ml (CRI)')
grafico_acuracia_ml(nome_modelos_ml,
                    acuracia_modelos_dpa,
                    'Comparação da precisão entre os modelos de ml (DPA)')