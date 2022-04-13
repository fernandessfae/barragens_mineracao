import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from numpy import arange


def pre_processamento_cri(nome_arquivo: str) -> pd.DataFrame:   
    """Função para fazer o pre-processamento de dados da categoria de 
       risco (CRI) para modelagem de machine learning.
       :param nome_arquivo: nome do arquivo a ser carregado pelo pandas
       :type nome_arquivo: str
    """
    
    # Carregamento dos dados necessários para classificação (CRI)
    dados_cri: pd.DataFrame = pd.read_csv(
        nome_arquivo.lower(),
        sep=';',
        encoding='latin-1',
        decimal=',',
        thousands='.',
        usecols=
        [
            'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação',
            'Desde',
            'Vazão de projeto',
            'Confiabilidade das estruturas extravasora',
            'Percolação',
            'Deformações e recalque',
            'Deteriorização dos taludes / paramentos',
            'Documentação de projeto',
            'Estrutura organizacional e qualificação técnica dos ' +
            'profissionais na equipe de Segurança da Barragem',
            'Manuais de Procedimentos para Inspeções ' +
            'de Segurança e Monitoramento',
            'Relatórios de inspeção e monitoramento da instrumentação ' +
            'e de Análise de Segurança',
            'Categoria de Risco - CRI'
        ])

    #dados_cri['nome_coluna'].isnull().sum()
    #dados_cri.value_counts('nome_coluna')

    # Tratamento dos dados
    dados_cri.dropna(how='all',
                     subset=[
                         'Altura máxima do projeto licenciado (m)',
                         'Comprimento da crista do projeto (m)',
                         'Tipo de barragem quanto ao material de construção',
                         'Tipo de fundação',
                         'Vazão de projeto'],
                     inplace=True)

    data_atual: date = date.today()
    dados_cri['Desde'] = dados_cri['Desde'].apply(
        lambda x: int(data_atual.year) - int(str(x)[6:10]) if \
            len(x) == 10 else 70)
    dados_cri.rename(columns={'Desde':'Idade'}, inplace=True)

    # Convertendo as variáveis do CT, EC e PS para label encoder
    dados_cri.loc[
        (dados_cri['Idade'] > 50) | (dados_cri['Idade'] <= 5), 'Idade'] = 4
    dados_cri.loc[
        (dados_cri['Idade'] > 5) & (dados_cri['Idade'] <= 10), 'Idade'] = 3
    dados_cri.loc[
        (dados_cri['Idade'] > 10) & (dados_cri['Idade'] <= 30), 'Idade'] = 2
    dados_cri.loc[
        (dados_cri['Idade'] > 30) & (dados_cri['Idade'] <= 50), 'Idade'] = 1

    dados_cri.loc[dados_cri['Altura máxima do projeto licenciado (m)'] <= 15,
                  'Altura máxima do projeto licenciado (m)'] = 0
    dados_cri.loc[(dados_cri['Altura máxima do projeto licenciado (m)'] > 15)\
                  & (dados_cri['Altura máxima do projeto licenciado (m)'] < 30),
                  'Altura máxima do projeto licenciado (m)'] = 1
    dados_cri.loc[(dados_cri['Altura máxima do projeto licenciado (m)'] >= 30)\
                  & (dados_cri['Altura máxima do projeto licenciado (m)'] <= 60),
                  'Altura máxima do projeto licenciado (m)'] = 2
    dados_cri.loc[dados_cri['Altura máxima do projeto licenciado (m)'] > 60,
                  'Altura máxima do projeto licenciado (m)'] = 3

    dados_cri['Comprimento da crista do projeto (m)'] = dados_cri[
        'Comprimento da crista do projeto (m)'].apply(
            lambda comprimento: 2 if comprimento <= 200 else 3)
            
    dados_cri['Tipo de barragem quanto ao material de construção'] = dados_cri[
        'Tipo de barragem quanto ao material de construção'].apply(
            lambda material: 1 if material == 'Concreto' else 3)

    dados_cri.replace(
        {
         'Tipo de fundação': 
         {'Rocha sã': 1,
          'Rocha alterada / Saprolito': 4,
          'Solo residual / Aluvião' : 5,
          'Aluvião arenoso espesso / Solo orgânico / Rejeito / Desconhecido': 5,
          '-': 5
         },
         'Vazão de projeto': 
         {'CMP (Cheia Máxima Provável) ou Decamilenar': 3,
          'Milenar': 5,
          'TR = 500 anos': 8,
          'TR inferior a 500 anos ou Desconhecida/ Estudo não confiável': 10,
          '-': 10
         },
         'Confiabilidade das estruturas extravasora': 
         {'0 - Estruturas civis bem mantidas e em operação normal / ' +
          'barragem sem necessidade de estruturas extravasoras': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '3 - Estruturas com problemas identificados e medidas corretivas ' +
          'em implantação': 7,
          '6 - Estruturas com problemas identificados e sem implantação das ' +
          'medidas corretivas necessárias': 10,
          '10 - Estruturas com problemas identificados, com redução de ' +
          'capacidade vertente e sem medidas corretivas': 10
         },
         'Percolação':
         {'Não se aplica a esse tipo de barragem': 0,
          '0 - Percolação totalmente controlada pelo sistema de drenagem': 0,
          '3 - Umidade ou surgência nas áreas de jusante, ' +
          'paramentos, taludes e ombreiras estáveis e monitorados': 3,
          '6 - Umidade ou surgência nas áreas de jusante, paramentos, ' +
          'taludes ou ombreiras sem implantação das medidas ' +
          'corretivas necessárias': 5,
          '10 - Surgência nas áreas de jusante com carreamento de material ' +
          'ou com vazão crescente ou infiltração do material contido, ' +
          'com potencial de comprometimento da segurança da estrutura': 8
         },
         'Deformações e recalque':
         {'0 - Não existem deformações e recalques com potencial de ' +
          'comprometimento da segurança da estrutura': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '2 - Existência de trincas e abatimentos com ' +
          'medidas corretivas em implantação': 1,
          '6 - Existência de trincas e abatimentos sem implantação ' +
          'das medidas corretivas necessárias': 5,
          '10 - Existência de trincas, abatimentos ou escorregamentos, ' +
          'com potencial de comprometimento da segurança da estrutura': 8
         },
         'Deteriorização dos taludes / paramentos':
         {'Não se aplica a esse tipo de barragem': 0,
          '0 - Não existe deterioração de taludes e paramentos': 0,
          '2 - Falhas na proteção dos taludes e paramentos, ' +
          'presença de vegetação arbustiva': 1,
          '6 - Erosões superficiais, ferragem exposta, presença de vegetação '+
          'arbórea, sem implantação das medidas corretivas necessárias': 5,
          '10 - Depressões acentuadas nos taludes, escorregamentos, ' +
          'sulcos profundos de erosão, com potencial de comprometimento ' +
          'da segurança da estrutura': 7
         },
         'Documentação de projeto':
         {'Não se aplica a esse tipo de barragem': 0,
          'Projeto executivo e como construído""': 0,
          'Projeto executivo ou como construído""': 2,
          'Projeto como está""': 2,
          'Projeto básico': 4,
          'Projeto conceitual': 6,
          'Não há documentação de projeto': 8,
          '-': 8
         },
         'Estrutura organizacional e qualificação técnica dos profissionais ' +
         'na equipe de Segurança da Barragem':
         {'Não se aplica a esse tipo de barragem': 0,
          'Possui unidade administrativa com profissional técnico ' +
          'qualificado responsável pela segurança da barragem ou é barragem ' +
          'não enquadrada nos incisos I, II, III ou IV, parágrafo único do ' +
          'art. 1º da Lei nº 12.334/2010': 0,
          'Possui profissional técnico qualificado (próprio ou contratado) ' +
          'responsável pela segurança da barragem': 4,
          'Possui unidade administrativa sem profissional técnico ' +
          'qualificado responsável pela segurança da barragem': 4,
          'Não possui unidade administrativa e responsável técnico ' +
          'qualificado pela segurança da barragem': 8,
          '-': 8
         },
         'Manuais de Procedimentos para Inspeções de Segurança e Monitoramento':
         {'Não se aplica a esse tipo de barragem': 0,
          'Possui manuais de procedimentos para inspeção, monitoramento e ' +
          'operação ou é barragem não enquadrada nos incisos I, II, III ou ' +
          'IV, parágrafo único do art. 1º da Lei nº 12.334/2010': 0,
          'Possui apenas manual de procedimentos de inspeção': 3,
          'Possui apenas manual de procedimentos de monitoramento': 5,
          'Não possui manuais ou procedimentos formais para monitoramento ' +
          'e inspeções': 6,
          '-': 6
         },
         'Relatórios de inspeção e monitoramento da instrumentação e ' +
         'de Análise de Segurança':
         {'Não se aplica a esse tipo de barragem': 0,
          'Emite regularmente relatórios de inspeção e monitoramento com ' +
          'base na instrumentação e de Análise de Segurança ou é barragem ' +
          'não enquadrada nos incisos I, II, III ou IV, parágrafo único do ' +
          'art. 1º da Lei nº 12.334/2010': 0,
          'Emite regularmente APENAS relatórios de inspeção e monitoramento': 3,
          'Emite regularmente APENAS relatórios de inspeção visual': 3,
          'Emite regularmente APENAS relatórios de Análise de Segurança': 3,
          'Não emite regularmente relatórios de inspeção e monitoramento ' +
          'e de Análise de Segurança': 5,
          '-': 5
         },
         'Categoria de Risco - CRI':
         {'Não se aplica': 0,
          'Baixa': 1,
          'Média': 2,
          'Alta': 3
         }
        }, inplace=True)

    # Criação das colunas CT, EC e PS 
    dados_cri['CT'] = dados_cri['Altura máxima do projeto licenciado (m)'] +\
        dados_cri['Comprimento da crista do projeto (m)'] + dados_cri[
        'Tipo de barragem quanto ao material de construção'] + dados_cri[
        'Tipo de fundação'] + dados_cri['Vazão de projeto'] + dados_cri['Idade']
    dados_cri['EC'] = dados_cri['Confiabilidade das estruturas extravasora'] +\
        dados_cri['Percolação'] + dados_cri['Deformações e recalque'] + \
        dados_cri['Deteriorização dos taludes / paramentos']
    dados_cri['PS'] = dados_cri['Documentação de projeto'] + dados_cri[
        'Estrutura organizacional e qualificação técnica dos profissionais ' +
        'na equipe de Segurança da Barragem'] + dados_cri['Manuais de ' +
        'Procedimentos para Inspeções de Segurança e Monitoramento'] + \
        dados_cri['Relatórios de inspeção e monitoramento da ' +
        'instrumentação e de Análise de Segurança']
    return dados_cri


if __name__ == '__main__':
    teste: pd.DataFrame = pre_processamento_cri('barragens.csv')
    
    #Visualização da contagem de classes do CRI
    plt.figure(figsize=(15, 5))
    nome_colunas: list = ['Não se aplica', 'Baixa', 'Média', 'Alta']
    plt.bar(nome_colunas,
            teste.value_counts('Categoria de Risco - CRI'),
            color=plt.cm.Set2(arange(len(nome_colunas))))
    plt.title('Contagem das classes da Categoria de Risco (CRI)',
              fontdict={'fontsize': 20, 'fontweight':'bold'})
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(axis='y')
    plt.show();
