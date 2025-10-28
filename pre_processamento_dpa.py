import os
import pandas as pd
from typing import Optional, List


class PipelineDPA:
    
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
    
    def convert_reservatory_volumn_licensed_project_column_into_label_encoding(
            self,
            column: str='Volume de projeto licenciado do Reservatório (m³)') -> pd.DataFrame:
        if self.df is None:
            raise ValueError(
                "DataFrame is not loaded. Please load the CSV first.")
        
        if not self._column_in_dataframe(column):
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        if column != 'Volume de projeto licenciado do Reservatório (m³)':
            raise ValueError("This method is only applicable to the " \
            "'Volume de projeto licenciado do Reservatório (m³)' column.")
        
        if not pd.api.types.is_float_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' must be float type.")

        self.df.loc[self.df[column] <= 5_000_000, column] = 1
        self.df.loc[
            (self.df[column] > 5_000_000) | (self.df[column] <= 75_000_000),
            column] = 2
        self.df.loc[
            (self.df[column] > 75_000_000) & (self.df[column] <= 200_000_000),
            column] = 3
        self.df.loc[self.df[column] > 200_000_000, column] = 4

        self.df[column] = self.df[column].astype('int32')
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
    
    def run_full_dpa_pipeline(self, csv_file_path: str) -> pd.DataFrame:

        # 0 - Initial Setup

        cols_to_load = [
            'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico',
            'Dano Potencial Associado - DPA'
        ]

        cols_to_drop_na = (
            'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico',
        )

        map_existencia_populacao_jusante = {
          'Inexistente (Não existem pessoas permanentes/residentes ou ' +
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
        }
        
        map_impacto_ambiental = {
          'Insignificante (Área afetada a jusante da barragem encontra-se ' +
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
          'Muito Significativo Agravado (Barragem armazena rejeitos ou ' +
          'resíduos sólidos classificados na Classe I - Perigosos segundo a' +
          ' NBR 10004/2004)': 5
        }

        map_impacto_socio_economico = {
          'Inexistente (Não existem quaisquer instalações na área afetada a ' +
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
        }

        map_dpa = {
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

        print("Pipeline: Initiated encoding columns (Label Encoding).")

        self.convert_reservatory_volumn_licensed_project_column_into_label_encoding()
        self.convert_values_column_into_label_encoding(
            'Existência de população a jusante',
            map_existencia_populacao_jusante)
        self.convert_values_column_into_label_encoding(
            'Impacto ambiental', map_impacto_ambiental)
        self.convert_values_column_into_label_encoding(
            'Impacto sócio-econômico',
            map_impacto_socio_economico)
        self.convert_values_column_into_label_encoding(
            'Dano Potencial Associado - DPA', map_dpa)
        
        # 4 - Create agregated column DPA
        
        print("Pipeline: Creating agregated column DPA.")
        
        self.create_new_column_add_another_columns_sum(
            'DPA', 'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico')
        
        print("Pre-processing DPA pipeline done.")
        return self.df

if __name__ == "__main__":
    from analise import generate_bar_graphic

    file_path = "data/barragens.csv"
    pipeline = PipelineDPA(file_path)
    pipeline.load_csv(
        [
            'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico',
            'Dano Potencial Associado - DPA'
        ])
    
    df = pipeline.df
    print(df.head())
    print()
    print(df.isnull().sum())
    print()
    pipeline.drop_na_values(
        'all', True, 'Volume de projeto licenciado do Reservatório (m³)',
        'Existência de população a jusante', 'Impacto ambiental',
        'Impacto sócio-econômico')
    print(df.isnull().sum())
    pipeline.convert_reservatory_volumn_licensed_project_column_into_label_encoding()
    pipeline.convert_values_column_into_label_encoding(
            'Existência de população a jusante',
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
        })
    pipeline.convert_values_column_into_label_encoding(
          'Impacto ambiental',
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
          'Muito Significativo Agravado (Barragem armazena rejeitos ou ' +
          'resíduos sólidos classificados na Classe I - Perigosos segundo a' +
          ' NBR 10004/2004)': 5
        })
    pipeline.convert_values_column_into_label_encoding(
        'Impacto sócio-econômico',
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
        })
    pipeline.create_new_column_add_another_columns_sum(
        'DPA', 'Volume de projeto licenciado do Reservatório (m³)',
        'Existência de população a jusante', 'Impacto ambiental',
        'Impacto sócio-econômico')
    print(df.tail())
    generate_bar_graphic(
        df, 'Dano Potencial Associado - DPA', 4,
        'Quantidade de barragens em relação ao Dano Potencial Associado - DPA',
        'contagem_classes_dpa', 'imagens_ml')