import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange


def pre_processamento_dpa(nome_arquivo: str) -> pd.DataFrame:
    """Função para fazer o pre-processamento de dados da dano potencial
       associado (DPA) para modelagem de machine learning.
       :param nome_arquivo: nome do arquivo a ser carregado pelo pandas
       :type nome_arquivo: str
    """
    
    # Carregamento dos dados necessários para classificação (DPA)
    dados_dpa: pd.DataFrame = pd.read_csv(
        nome_arquivo.lower(),
        sep=';',
        encoding='latin-1',
        decimal=',',
        thousands='.',
        usecols=
        [
            'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico',
            'Dano Potencial Associado - DPA'
        ])

    #dados_dpa['nome_coluna'].isnull().sum()
    #dados_dpa.value_counts('nome_coluna')

    # Tratamento dos dados
    dados_dpa.dropna(how='all',
                     subset=[
                         'Volume de projeto licenciado do Reservatório (m³)',
                         'Existência de população a jusante',
                         'Impacto ambiental',
                         'Impacto sócio-econômico'],
                     inplace=True)

    # Convertendo as variáveis do DPA para label encoder
    dados_dpa.loc[dados_dpa[
        'Volume de projeto licenciado do Reservatório (m³)'] <= 5000000, \
            'Volume de projeto licenciado do Reservatório (m³)'] = 1
    dados_dpa.loc[(dados_dpa[
        'Volume de projeto licenciado do Reservatório (m³)'] > 5000000) & \
        (dados_dpa['Volume de projeto licenciado do Reservatório (m³)'] \
        <= 75000000), 'Volume de projeto licenciado do Reservatório (m³)'] = 2
    dados_dpa.loc[(dados_dpa[
        'Volume de projeto licenciado do Reservatório (m³)'] > 75000000) & \
            (dados_dpa['Volume de projeto licenciado do Reservatório (m³)'] \
            <= 200000000),
            'Volume de projeto licenciado do Reservatório (m³)'] = 3
    dados_dpa.loc[
        dados_dpa['Volume de projeto licenciado do Reservatório (m³)'] > \
        200000000, 'Volume de projeto licenciado do Reservatório (m³)'] = 4

    dados_dpa.replace(
        {
         'Existência de população a jusante':
         {'Inexistente (Não existem pessoas permanentes/residentes ou ' +
          'temporárias/transitando na área afetada a jusante da barragem)': 0,
          'Pouco Frequente (Não existem pessoas ocupando permanentemente a ' +
          'área afetada a jusante da barragem, mas existe estrada vicinal ' +
          'de uso local)': 4,
          'Frequente (Não existem pessoas ocupando permanentemente a área ' +
          'afetada a jusante da barragem, mas existe rodovia municipal ou ' +
          'estadual ou federal ou outro local e/ou empreendimento de ' +
          'permanência eventual de pessoas que poderão ser atingidas)': 8,
          'Existente (Existem pessoas ocupando permanentemente a área afetada'+
          ' a jusante da barragem, portanto, vidas humanas poderão ser ' +
          'atingidas)': 12,
          'Indefinido': 12
         },
         'Impacto ambiental':
         {'Insignificante (Área afetada a jusante da barragem encontra-se ' +
          'totalmente descaracterizada de suas condições naturais e a ' +
          'estrutura armazena apenas resíduos Classe II B - Inertes, segundo '
          'a NBR 10004/2004 da ABNT)': 3,
          'Pouco Significativo (Área afetada a jusante da barragem não ' +
          'apresenta área de interesse ambiental relevante ou áreas ' +
          'protegidas em legislação específica (excluidas APPs) e armazena ' +
          'apenas resíduos Classe II B - Inertes, segundo a NBR 10004/2004 ' +
          'da ABNT)': 3,
          'Significativo (Área afetada a jusante da barragem apresenta área ' +
          'de interesse ambiental relevante ou áreas protegidas em ' +
          'legislação específica (excluidas APPs)) e armazena apenas ' +
          'resíduos Classe II B - Inertes, segundo a NBR 10004/2004 ' +
          'da ABNT)': 3,
          'Muito Significativo (Barragem armazena rejeitos ou resíduos ' +
          'sólidos classificados na Classe II A - Não Inertes, segundo a NBR '+
          '10004/2004)': 5,
          'Muito Significativo Agravado (Barragem armazena rejeitos ou resíduos sólidos classificados na Classe I - Perigosos segundo a NBR 10004/2004)': 5
         },
         'Impacto sócio-econômico':
         {'Inexistente (Não existem quaisquer instalações na área afetada a ' +
          'jusante da barragem)': 0,
          'BAIXO (Existe pequena concentração de instalações residenciais, ' +
          'agrícolas, industriais ou de infraestrutura de relevância ' +
          'sócio-econômico-cultural na área afetada a jusante da barragem)': 4,
          'MÉDIO (Existe moderada concentração de instalações residenciais, ' +
          'agrícolas, industriais ou de infraestrutura de relevância ' +
          'sócio-econômico-cultural na área afetada a jusante da barragem)': 8,
          'ALTO (Existe alta concentração de instalações residenciais, ' +
          'agrícolas, industriais ou de infraestrutura de relevância ' +
          'sócio-econômico-cultural na área afetada a jusante da barragem)': 8,
          'Indefinido': 8
         },
         'Dano Potencial Associado - DPA':
         {'Não se aplica': 0,
          'Baixa': 1,
          'Média': 2,
          'Alta': 3
         }
        }, inplace=True)
        
    # Criação da coluna somatório DPA
    dados_dpa['DPA'] = dados_dpa['Volume de projeto licenciado do ' +
    'Reservatório (m³)'] + dados_dpa['Existência de população a jusante'] \
    + dados_dpa['Impacto ambiental'] + dados_dpa['Impacto sócio-econômico']
    return dados_dpa


if __name__ == '__main__':
    teste: pd.DataFrame = pre_processamento_dpa('barragens.csv')
    
    #Visualização da contagem de classes do DPA
    plt.figure(figsize=(15, 5))
    nome_colunas: list = ['Não se aplica', 'Baixa', 'Média', 'Alta']
    plt.bar(nome_colunas,
            teste.value_counts('Dano Potencial Associado - DPA'),
            color=plt.cm.Set2(arange(len(nome_colunas))))
    plt.title('Contagem das classes do Dano Potencial Associado (DPA)',
              fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(axis='y')
    plt.show();
