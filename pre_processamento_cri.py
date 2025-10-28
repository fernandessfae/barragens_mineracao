import os
import pandas as pd
from typing import List, Optional
from datetime import date

class PipelineCRI:
    
    def __init__(self, file_path: str):
        self.csv_file_path = file_path
        self.df = None
    
    @staticmethod
    def _is_valid_csv_file(file_path: str) -> bool:
        return os.path.isfile(file_path) and file_path.endswith('.csv')
    
    def load_csv(self, cols_to_use: Optional[List[str]] = None):
        if not self._is_valid_csv_file(self.csv_file_path):
            raise FileNotFoundError(
                f"File {self.csv_file_path} not found or is not a CSV file.")

        self.df = pd.read_csv(
            self.csv_file_path, sep=';', encoding='latin-1',
            decimal=',', thousands='.', usecols=cols_to_use)
        return self.df

    def _column_in_dataframe(self, column: str) -> bool:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")

        if column not in self.df.columns:
            return False
        return True
        
    def drop_na_values(
            self, how: str, inplace: bool = True, *args) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if how not in ['any', 'all']:
            raise ValueError("Parameter 'how' must be either 'any' or 'all'.")
        
        selected_columns: list[str] = []

        for column in args:
            if not self._column_in_dataframe(column):
                raise ValueError(f"Column '{column}' not found in DataFrame.")
            selected_columns.append(column)

        self.df.dropna(how=how, subset=selected_columns, inplace=inplace)
        return self.df
    
    def convert_column_date_dam_str_to_integer_age(
            self, column: str) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        current_year = date.today().year

        # If the dam has unknown date, assign age 70
        self.df[column] = self.df[column].apply(
            lambda x: int(current_year) - int(str(x)[6:10]) if \
            len(x) == 10 else 70)
        return self.df
        
    def rename_columns(self, columns_mapping: dict) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")

        for col in columns_mapping.keys():
            if not self._column_in_dataframe(col):
                raise ValueError(f"Column '{col}' not found in DataFrame.")
        
        for new_name in columns_mapping.values():
            if new_name in self.df.columns:
                raise ValueError(f"New column name '{new_name}' "
                                 "already exists in DataFrame.")

        self.df.rename(columns=columns_mapping, inplace=True)
        return self.df
    
    def convert_dam_age_column_into_label_encoding(
            self, column: str='Idade') -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        if column != 'Idade':
            raise ValueError(
                "This method is only applicable to the 'Idade' column.")
        
        if not pd.api.types.is_integer_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' must be of integer type.")

        self.df.loc[
            (self.df[column] > 50) | (self.df[column] <= 5), column] = 4
        self.df.loc[
            (self.df[column] > 5) & (self.df[column] <= 10), column] = 3
        self.df.loc[
            (self.df[column] > 10) & (self.df[column] <= 30), column] = 2
        self.df.loc[
            (self.df[column] > 30) & (self.df[column] <= 50), column] = 1
        return self.df
    
    def convert_dam_height_column_into_label_encoding(
            self, column: str='Altura máxima do projeto licenciado (m)') -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        if column != 'Altura máxima do projeto licenciado (m)':
            raise ValueError("This method is only applicable to the " \
            "'Altura máxima do projeto licenciado (m)' column.")
        
        if not pd.api.types.is_float_dtype(self.df[column]):
            raise ValueError(
                f"Column '{column}' must be of float or int type.")

        self.df.loc[
            (self.df[column] <= 15), column] = 0
        self.df.loc[
            (self.df[column] > 15) & (self.df[column] <= 30), column] = 1
        self.df.loc[
            (self.df[column] >= 30) & (self.df[column] <= 60), column] = 2
        self.df.loc[(self.df[column] > 60), column] = 3

        self.df[column] = self.df[column].astype('int32')
        return self.df
    
    def apply_ternary_label_encoding_to_column(
            self, column: str) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")

        lambda_function: [str, callable] = {
            'Comprimento da crista do projeto (m)': 
            lambda length: 2 if length <= 200 else 3,
            'Tipo de barragem quanto ao material de construção':
            lambda material: 1 if material == 'Concreto' else 3}
        
        try:
            self.df[column] = self.df[column].apply(lambda_function[column])
        except KeyError:
            raise ValueError("Ternary label encoding is not " \
            f"defined for column '{column}'.")
        
        return self.df
    
    def convert_values_column_into_label_encoding(
            self, column: str, mapping: dict) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")

        self.df[column] = self.df[column].map(mapping)
        return self.df
    
    def create_new_column_add_another_columns_sum(
            self, new_column: str, *args: str) -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if self._column_in_dataframe(new_column):
            raise ValueError(
                f"New column name '{new_column}' already exists in DataFrame.")
        
        for column in args:
            if not self._column_in_dataframe(column):
                raise ValueError(f"Column '{column}' not found in DataFrame.")

        self.df[new_column] = self.df[list(args)].sum(axis=1)
        return self.df
    
    def run_full_cri_pipeline(self, csv_file_path: str) -> pd.DataFrame:

        # 0 - Initial Setup

        cols_to_load = [
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
        ]

        cols_to_drop_na = (
            'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação',
            'Vazão de projeto'
        )

        map_tipo_fundacao = {
            'Rocha sã': 1,
            'Rocha alterada / Saprolito': 4,
            'Solo residual / Aluvião': 5,
            'Aluvião arenoso espesso / Solo orgânico / Rejeito ' +
            '/ Desconhecido': 5,
            '-': 5
        }
        
        map_vazao_projeto = {
            'CMP (Cheia Máxima Provável) ou Decamilenar': 3,
            'Milenar': 5,
            'TR = 500 anos': 8,
            'TR inferior a 500 anos ou Desconhecida/ Estudo não confiável': 10,
            '-': 10
        }

        map_confiabilidade_estruturas_extravasoras = {
          '0 - Estruturas civis bem mantidas e em operação normal / ' +
          'barragem sem necessidade de estruturas extravasoras': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '3 - Estruturas com problemas identificados e medidas corretivas ' +
          'em implantação': 7,
          '6 - Estruturas com problemas identificados e sem implantação das ' +
          'medidas corretivas necessárias': 10,
          '10 - Estruturas com problemas identificados, com redução de ' +
          'capacidade vertente e sem medidas corretivas': 10
        }

        map_percolacao = {
          'Não se aplica a esse tipo de barragem': 0,
          '0 - Percolação totalmente controlada pelo sistema de drenagem': 0,
          '3 - Umidade ou surgência nas áreas de jusante, ' +
          'paramentos, taludes e ombreiras estáveis e monitorados': 3,
          '6 - Umidade ou surgência nas áreas de jusante, paramentos, ' +
          'taludes ou ombreiras sem implantação das medidas ' +
          'corretivas necessárias': 5,
          '10 - Surgência nas áreas de jusante com carreamento de material ' +
          'ou com vazão crescente ou infiltração do material contido, ' +
          'com potencial de comprometimento da segurança da estrutura': 8
        }

        map_deformacoes_e_recalque = {
          '0 - Não existem deformações e recalques com potencial de ' +
          'comprometimento da segurança da estrutura': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '2 - Existência de trincas e abatimentos com ' +
          'medidas corretivas em implantação': 1,
          '6 - Existência de trincas e abatimentos sem implantação ' +
          'das medidas corretivas necessárias': 5,
          '10 - Existência de trincas, abatimentos ou escorregamentos, ' +
          'com potencial de comprometimento da segurança da estrutura': 8
        }

        map_deterioracao_taludes_parametros = {
          'Não se aplica a esse tipo de barragem': 0,
          '0 - Não existe deterioração de taludes e paramentos': 0,
          '2 - Falhas na proteção dos taludes e paramentos, ' +
          'presença de vegetação arbustiva': 1,
          '6 - Erosões superficiais, ferragem exposta, presença de vegetação '+
          'arbórea, sem implantação das medidas corretivas necessárias': 5,
          '10 - Depressões acentuadas nos taludes, escorregamentos, ' +
          'sulcos profundos de erosão, com potencial de comprometimento ' +
          'da segurança da estrutura': 7
        }

        map_documentacao_projeto = {
          'Não se aplica a esse tipo de barragem': 0,
          'Projeto executivo e como construído""': 0,
          'Projeto executivo ou como construído""': 2,
          'Projeto como está""': 2,
          'Projeto básico': 4,
          'Projeto conceitual': 6,
          'Não há documentação de projeto': 8,
          '-': 8
        }

        map_estrutura_administrativa_pessoal_barragens = {
          'Não se aplica a esse tipo de barragem': 0,
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
        }

        map_manuais_procedimentos_inspecao_monitoramento_barragem = {
          'Não se aplica a esse tipo de barragem': 0,
          'Possui manuais de procedimentos para inspeção, monitoramento e ' +
          'operação ou é barragem não enquadrada nos incisos I, II, III ou ' +
          'IV, parágrafo único do art. 1º da Lei nº 12.334/2010': 0,
          'Possui apenas manual de procedimentos de inspeção': 3,
          'Possui apenas manual de procedimentos de monitoramento': 5,
          'Não possui manuais ou procedimentos formais para monitoramento ' +
          'e inspeções': 6,
          '-': 6
        }

        map_relatorio_inspecao_monitoramento_barragem = {
          'Não se aplica a esse tipo de barragem': 0,
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
        }

        map_categoria_risco_cri= { 
          'Não se aplica': 0,
          'Baixa': 1,
          'Média': 2,
          'Alta': 3
        }

        # 1 - Load CSV

        self.csv_file_path = csv_file_path
        self.load_csv(cols_to_load)
        
        print(f"Pipeline: DF loaded with {self.df.shape[0]} rows.")

        # 2 - Drop NaNs in critical columns

        print("Pipeline: Dropping NaNs in critical columns.")
        self.drop_na_values('all', True, *cols_to_drop_na)

        # 3 - Feature Engineering and Label Encoding

        print("Pipeline: Processing 'Desde' column (Idade).")
        self.convert_column_date_dam_str_to_integer_age('Desde')
        self.rename_columns({'Desde': 'Idade'})
        self.convert_dam_age_column_into_label_encoding('Idade')

        print("Pipeline: Initiated encoding columns (Label Encoding).")

        self.convert_dam_height_column_into_label_encoding(
            'Altura máxima do projeto licenciado (m)')
        
        self.apply_ternary_label_encoding_to_column(
            'Comprimento da crista do projeto (m)')
        self.apply_ternary_label_encoding_to_column(
            'Tipo de barragem quanto ao material de construção')
        
        self.convert_values_column_into_label_encoding(
            'Tipo de fundação', map_tipo_fundacao)
        self.convert_values_column_into_label_encoding(
            'Vazão de projeto', map_vazao_projeto)
        self.convert_values_column_into_label_encoding(
            'Confiabilidade das estruturas extravasora',
            map_confiabilidade_estruturas_extravasoras)
        self.convert_values_column_into_label_encoding(
            'Percolação', map_percolacao)
        self.convert_values_column_into_label_encoding(
            'Deformações e recalque', map_deformacoes_e_recalque)
        self.convert_values_column_into_label_encoding(
            'Deteriorização dos taludes / paramentos',
            map_deterioracao_taludes_parametros)
        self.convert_values_column_into_label_encoding(
            'Documentação de projeto', map_documentacao_projeto)
        self.convert_values_column_into_label_encoding(
            'Estrutura organizacional e qualificação técnica dos ' +
            'profissionais na equipe de Segurança da Barragem',
            map_estrutura_administrativa_pessoal_barragens)
        self.convert_values_column_into_label_encoding(
            'Manuais de Procedimentos para Inspeções ' +
            'de Segurança e Monitoramento',
            map_manuais_procedimentos_inspecao_monitoramento_barragem)
        self.convert_values_column_into_label_encoding(
            'Relatórios de inspeção e monitoramento da instrumentação ' +
            'e de Análise de Segurança',
            map_relatorio_inspecao_monitoramento_barragem)
        self.convert_values_column_into_label_encoding(
            'Categoria de Risco - CRI', map_categoria_risco_cri)
        
        # 4 - Create agregated columns CT, EC, PS
        
        print("Pipeline: Creating agregated columns (CT, EC, PS).")
        
        self.create_new_column_add_another_columns_sum(
            'CT', 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto', 'Idade')
            
        self.create_new_column_add_another_columns_sum(
            'EC', 'Confiabilidade das estruturas extravasora', 'Percolação',
            'Deformações e recalque', 'Deteriorização dos taludes / paramentos')
            
        self.create_new_column_add_another_columns_sum(
            'PS', 'Documentação de projeto',
            'Estrutura organizacional e qualificação técnica dos profissionais ' +
            'na equipe de Segurança da Barragem',
            'Manuais de Procedimentos para Inspeções de Segurança e Monitoramento',
            'Relatórios de inspeção e monitoramento da instrumentação e de Análise de Segurança')
        
        print("Pre-processing CRI pipeline done.")
        return self.df


if __name__ == "__main__":
    from analise import generate_bar_graphic

    file_path = "data/barragens.csv"
    pipeline = PipelineCRI(file_path)
    pipeline.load_csv(
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
    
    df = pipeline.df
    print(df.head())
    print()
    print(df.isnull().sum())
    print()
    pipeline.drop_na_values(
        'all', True,
        'Altura máxima do projeto licenciado (m)',
        'Comprimento da crista do projeto (m)',
        'Tipo de barragem quanto ao material de construção',
        'Tipo de fundação',
        'Vazão de projeto')
    print(df.isnull().sum())
    pipeline.convert_column_date_dam_str_to_integer_age('Desde')
    pipeline.rename_columns({'Desde': 'Idade'})
    pipeline.convert_dam_age_column_into_label_encoding('Idade')
    pipeline.convert_dam_height_column_into_label_encoding(
        'Altura máxima do projeto licenciado (m)')
    pipeline.apply_ternary_label_encoding_to_column(
        'Comprimento da crista do projeto (m)')
    pipeline.apply_ternary_label_encoding_to_column(
        'Tipo de barragem quanto ao material de construção')
    pipeline.convert_values_column_into_label_encoding(
        'Tipo de fundação',
        {
        'Rocha sã': 1,
        'Rocha alterada / Saprolito': 4,
        'Solo residual / Aluvião': 5,
        'Aluvião arenoso espesso / Solo orgânico / Rejeito / Desconhecido': 5,
        '-': 5
        })
    pipeline.convert_values_column_into_label_encoding('Vazão de projeto',
        {'CMP (Cheia Máxima Provável) ou Decamilenar': 3,
          'Milenar': 5,
          'TR = 500 anos': 8,
          'TR inferior a 500 anos ou Desconhecida/ Estudo não confiável': 10,
          '-': 10
        })
    pipeline.convert_values_column_into_label_encoding(
        'Confiabilidade das estruturas extravasora',
        {'0 - Estruturas civis bem mantidas e em operação normal / ' +
          'barragem sem necessidade de estruturas extravasoras': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '3 - Estruturas com problemas identificados e medidas corretivas ' +
          'em implantação': 7,
          '6 - Estruturas com problemas identificados e sem implantação das ' +
          'medidas corretivas necessárias': 10,
          '10 - Estruturas com problemas identificados, com redução de ' +
          'capacidade vertente e sem medidas corretivas': 10
        })
    pipeline.convert_values_column_into_label_encoding(
        'Percolação',
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
         })
    pipeline.convert_values_column_into_label_encoding(
        'Deformações e recalque',
        {'0 - Não existem deformações e recalques com potencial de ' +
          'comprometimento da segurança da estrutura': 0,
          'Não se aplica a esse tipo de barragem': 0,
          '2 - Existência de trincas e abatimentos com ' +
          'medidas corretivas em implantação': 1,
          '6 - Existência de trincas e abatimentos sem implantação ' +
          'das medidas corretivas necessárias': 5,
          '10 - Existência de trincas, abatimentos ou escorregamentos, ' +
          'com potencial de comprometimento da segurança da estrutura': 8
        })
    pipeline.convert_values_column_into_label_encoding(
        'Deteriorização dos taludes / paramentos',
        {'Não se aplica a esse tipo de barragem': 0,
          '0 - Não existe deterioração de taludes e paramentos': 0,
          '2 - Falhas na proteção dos taludes e paramentos, ' +
          'presença de vegetação arbustiva': 1,
          '6 - Erosões superficiais, ferragem exposta, presença de vegetação '+
          'arbórea, sem implantação das medidas corretivas necessárias': 5,
          '10 - Depressões acentuadas nos taludes, escorregamentos, ' +
          'sulcos profundos de erosão, com potencial de comprometimento ' +
          'da segurança da estrutura': 7
        })
    pipeline.convert_values_column_into_label_encoding(
        'Documentação de projeto',
        {'Não se aplica a esse tipo de barragem': 0,
          'Projeto executivo e como construído""': 0,
          'Projeto executivo ou como construído""': 2,
          'Projeto como está""': 2,
          'Projeto básico': 4,
          'Projeto conceitual': 6,
          'Não há documentação de projeto': 8,
          '-': 8
        })
    pipeline.convert_values_column_into_label_encoding(
        'Estrutura organizacional e qualificação técnica dos profissionais ' +
        'na equipe de Segurança da Barragem',
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
        })
    pipeline.convert_values_column_into_label_encoding(
        'Manuais de Procedimentos para Inspeções de Segurança e Monitoramento',
        {'Não se aplica a esse tipo de barragem': 0,
          'Possui manuais de procedimentos para inspeção, monitoramento e ' +
          'operação ou é barragem não enquadrada nos incisos I, II, III ou ' +
          'IV, parágrafo único do art. 1º da Lei nº 12.334/2010': 0,
          'Possui apenas manual de procedimentos de inspeção': 3,
          'Possui apenas manual de procedimentos de monitoramento': 5,
          'Não possui manuais ou procedimentos formais para monitoramento ' +
          'e inspeções': 6,
          '-': 6
        })
    pipeline.convert_values_column_into_label_encoding(
        'Relatórios de inspeção e monitoramento da instrumentação e ' +
        'de Análise de Segurança',
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
        })
    pipeline.create_new_column_add_another_columns_sum(
        'CT', 'Altura máxima do projeto licenciado (m)',
        'Comprimento da crista do projeto (m)',
        'Tipo de barragem quanto ao material de construção',
        'Tipo de fundação', 'Vazão de projeto', 'Idade')
    pipeline.create_new_column_add_another_columns_sum(
        'EC', 'Confiabilidade das estruturas extravasora', 'Percolação',
        'Deformações e recalque', 'Deteriorização dos taludes / paramentos')
    pipeline.create_new_column_add_another_columns_sum(
        'PS', 'Documentação de projeto',
        'Estrutura organizacional e qualificação técnica dos profissionais ' +
        'na equipe de Segurança da Barragem',
        'Manuais de ' +
        'Procedimentos para Inspeções de Segurança e Monitoramento',
        'Relatórios de inspeção e monitoramento da ' +
        'instrumentação e de Análise de Segurança')
    print()
    print(df.head())
    print(df.tail())
    generate_bar_graphic(
        df, 'Categoria de Risco - CRI', 4,
        'Quantidade de barragens em relação à Categoria de Risco - CRI',
        'contagem_classes_cri', 'imagens_ml')