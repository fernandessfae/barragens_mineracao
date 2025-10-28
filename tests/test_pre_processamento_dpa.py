import unittest
import os
import sys
import pandas as pd

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

from pre_processamento_dpa import PipelineDPA

class TestPipelineDPA(unittest.TestCase):

    def setUp(self):
        self.csv_file_path: str = '/home/aristotelesfernandes/vscode/data_science/barragens_mineracao/data/barragens.csv'
        self.df = None

    def test_is_valid_csv_file(self):
        self.assertTrue(PipelineDPA._is_valid_csv_file(self.csv_file_path))
        self.assertFalse(PipelineDPA._is_valid_csv_file('invalid_file.txt'))
    
    def test_load_csv(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        self.assertIsInstance(pipeline.df, pd.DataFrame)
        self.assertFalse(pipeline.df.empty)
    
    def test_column_in_dataframe(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        expected_columns = ['Tipo de fundação', 'Vazão de projeto',
                            'Percolação', 'Deformações e recalque']
        for col in expected_columns:
            self.assertTrue(pipeline._column_in_dataframe(col))

    def test_drop_na_values(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        initial_row_count = len(pipeline.df)
        pipeline.drop_na_values('all', True, 'Impacto ambiental',
                         'Impacto sócio-econômico')
        self.assertLessEqual(len(pipeline.df), initial_row_count)
    
    def test_convert_reservatory_volumn_licensed_project_column_into_label_encoding(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico')
        pipeline.convert_reservatory_volumn_licensed_project_column_into_label_encoding()
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Volume de projeto licenciado do Reservatório (m³)']))
    
    def test_convert_values_column_into_label_encoding(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico')
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
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Impacto sócio-econômico']))
    
    def test_create_new_column_add_another_columns_sum(self):
        pipeline = PipelineDPA(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Volume de projeto licenciado do Reservatório (m³)',
            'Existência de população a jusante',
            'Impacto ambiental',
            'Impacto sócio-econômico')
        pipeline.convert_reservatory_volumn_licensed_project_column_into_label_encoding()
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
            'Soma número impacto socioeconomico + reservatório',
            'Volume de projeto licenciado do Reservatório (m³)',
            'Impacto sócio-econômico')
        self.assertIn('Soma número impacto socioeconomico + reservatório',
                      pipeline.df.columns)
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Soma número impacto socioeconomico + reservatório']))
    
    def test_run_full_cri_pipeline(self):
        pipeline = PipelineDPA(self.csv_file_path)
        df_processed = pipeline.run_full_dpa_pipeline(self.csv_file_path)

        self.assertIsInstance(df_processed, pd.DataFrame)
        self.assertFalse(df_processed.empty)

        self.assertIn('DPA', df_processed.columns, 
            f"The agregation column 'DPA' is not created in pipeline.")
        
        self.assertTrue(pd.api.types.is_numeric_dtype(df_processed['DPA']),
                f"The agregation column 'DPA' should be numeric type.")
        
        self.assertIn('Dano Potencial Associado - DPA', df_processed.columns)


if __name__ == '__main__':
    unittest.main(verbosity=2)