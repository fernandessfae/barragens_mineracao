import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange

def grafico_barra(dados: pd.DataFrame, coluna: str,
                  qt_barra: int, titulo: str) -> None:
    """Função para geração dos gráficos de barras de acordo com a coluna
       desejada, utilizando a contagem de cada valor da coluna.
       
       :param dados: Dados a serem utilizados para geração do gráfico
       :type dados: pd.DataFrame
       :param coluna: Nome da coluna para contagem dos valores dela
       :tyoe coluna: str
       :param qt_barra: Quantidade de barras a serem exibidas no gráfico
       :type qt_barra: str
       :param titulo: Nome do título do gráfico de barra
       :type titulo: str
    """
    plt.figure(figsize=(15, 5))
    if qt_barra >= 10:
        dados.value_counts(coluna)[:qt_barra].sort_values().plot(
            kind='barh', color=plt.cm.Set1(arange(qt_barra-1, -1, -1)))
        plt.xticks(fontsize=20, rotation=0)
    else:
        dados.value_counts(coluna)[:qt_barra].plot(
            kind='bar', color=plt.cm.Set2(arange(qt_barra)))
        plt.xticks(rotation=0, fontsize=20)
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.xlabel(coluna, fontdict={'fontsize': 20})
    plt.ylabel('Contagem', fontdict={'fontsize': 20})
    plt.yticks(fontsize=20)
    plt.show();
    return None


def grafico_setor(dados: pd.DataFrame, coluna: str, titulo: str) -> None:
    """Função para geração dos gráficos de setor, também conhecida como
       gráfico de pizza, de acordo com a coluna desejada, utilizando a
       contagem de cada valor da coluna.
       
       :param dados: Dados a serem utilizados para geração do gráfico
       :type dados: pd.DataFrame
       :param coluna: Nome da coluna para contagem dos valores dela
       :tyoe coluna: str
       :param titulo: Nome do título do gráfico de setor
       :type titulo: str
    """
    dados_setor: pd.DataFrame = dados.value_counts(coluna).reset_index()
    plt.figure(figsize=(10, 5))
    plt.title(titulo, fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.pie(dados_setor[0], labels=dados_setor[coluna],
            colors=plt.cm.Set1(arange(len(dados_setor[0]))), autopct="%0.2f%%",
            textprops={'fontsize': 20})
    plt.show();
    return None


dados_mineracao: pd.DataFrame = pd.read_csv(
    'barragens.csv', sep=';', encoding='latin-1')

#dados_mineracao['nome_coluna'].isnull().sum()
#dados_mineracao.value_counts('nome_coluna')

grafico_barra(dados_mineracao, 'Empreendedor',
              10, '10 empresas com maior quantidade de barragens contruídas.')

grafico_barra(dados_mineracao,'UF',
              10, '10 estados com maior quantidade de barragens contruídas.')

grafico_barra(dados_mineracao,'Categoria de Risco - CRI',
              4, 'Quantidade de barragens em relação a CRI')

grafico_barra(dados_mineracao,'Dano Potencial Associado - DPA',
              4, 'Quantidade de barragens em relação ao DPA')

grafico_setor(dados_mineracao,
              'Necessita de PAEBM',
              'As barragens estão inclusas no PAEBM?')

grafico_setor(dados_mineracao,
              'Inserido na PNSB',
              'As barragens estão inclusas na PNSB?')

grafico_barra(dados_mineracao,'Nível de Emergência',
              4, 'Quantidade de barragens em relação ao nível de emergência')

grafico_barra(dados_mineracao, 'Minério principal presente no reservatório',
              10, '10 Principais minérios presentes nas barragens de mineração')
