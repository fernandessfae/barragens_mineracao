import unittest
import os
import sys
import pandas as pd

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

from pre_processamento_cri import PipelineCRI

class TestPipelineCRI(unittest.TestCase):

    def setUp(self):
        self.csv_file_path: str = '/home/aristotelesfernandes/vscode/data_science/barragens_mineracao/data/barragens.csv'
        self.df = None

    def test_is_valid_csv_file(self):
        self.assertTrue(PipelineCRI._is_valid_csv_file(self.csv_file_path))
        self.assertFalse(PipelineCRI._is_valid_csv_file('invalid_file.txt'))
    
    def test_load_csv(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        self.assertIsInstance(pipeline.df, pd.DataFrame)
        self.assertFalse(pipeline.df.empty)
    
    def test_column_in_dataframe(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        expected_columns = ['Tipo de fundação', 'Vazão de projeto',
                            'Percolação', 'Deformações e recalque']
        for col in expected_columns:
            self.assertTrue(pipeline._column_in_dataframe(col))

    def test_drop_na_values(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        initial_row_count = len(pipeline.df)
        pipeline.drop_na_values('all', True, 'Vazão de projeto', 'Percolação')
        self.assertLessEqual(len(pipeline.df), initial_row_count)
    
    def test_convert_column_date_dam_str_to_integer_age(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.convert_column_date_dam_str_to_integer_age('Desde')
        self.assertTrue(
            pd.api.types.is_integer_dtype(pipeline.df['Desde']))
    
    def test_rename_column(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.rename_columns({'Desde': 'Idade'})
        self.assertIn('Idade', pipeline.df.columns)
        self.assertNotIn('Desde', pipeline.df.columns)
    
    def test_convert_dam_age_column_into_label_encoding(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.convert_column_date_dam_str_to_integer_age('Desde')
        pipeline.rename_columns({'Desde': 'Idade'})
        pipeline.convert_dam_age_column_into_label_encoding('Idade')
        self.assertTrue(
            pd.api.types.is_integer_dtype(pipeline.df['Idade']))

    def test_convert_dam_height_column_into_label_encoding(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.convert_dam_height_column_into_label_encoding(
            'Altura máxima do projeto licenciado (m)')
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Altura máxima do projeto licenciado (m)']))
    
    def test_apply_ternary_label_encoding_to_column(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.apply_ternary_label_encoding_to_column(
            'Comprimento da crista do projeto (m)')
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Comprimento da crista do projeto (m)']))
    
    def test_convert_values_column_into_label_encoding(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.convert_values_column_into_label_encoding(
            'Tipo de fundação',
            {'Rocha sã': 1,
             'Rocha alterada / Saprolito': 4,
             'Solo residual / Aluvião' : 5,
             'Aluvião arenoso espesso / Solo orgânico / Rejeito / Desconhecido': 5,
             '-': 5})
        self.assertTrue(
            pd.api.types.is_integer_dtype(pipeline.df['Tipo de fundação']))
    
    def test_create_new_column_add_another_columns_sum(self):
        pipeline = PipelineCRI(self.csv_file_path)
        pipeline.df = pipeline.load_csv()
        pipeline.drop_na_values(
            'all', True, 'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)',
            'Tipo de barragem quanto ao material de construção',
            'Tipo de fundação', 'Vazão de projeto')
        pipeline.convert_dam_height_column_into_label_encoding(
            'Altura máxima do projeto licenciado (m)')
        pipeline.apply_ternary_label_encoding_to_column(
            'Comprimento da crista do projeto (m)')
        pipeline.create_new_column_add_another_columns_sum(
            'Soma Altura e Comprimento',
            'Altura máxima do projeto licenciado (m)',
            'Comprimento da crista do projeto (m)')
        self.assertIn('Soma Altura e Comprimento', pipeline.df.columns)
        self.assertTrue(
            pd.api.types.is_integer_dtype(
                pipeline.df['Soma Altura e Comprimento']))
    
    def test_run_full_cri_pipeline(self):
        pipeline = PipelineCRI(self.csv_file_path)
        df_processed = pipeline.run_full_cri_pipeline(self.csv_file_path)

        self.assertIsInstance(df_processed, pd.DataFrame)
        self.assertFalse(df_processed.empty)

        final_columns = ['CT', 'EC', 'PS']
        for col in final_columns:
            self.assertIn(
                col, df_processed.columns, 
                f"The agregation column '{col}' is not created in pipeline.")
        
        self.assertIn('Idade', df_processed.columns)
        self.assertTrue(
            pd.api.types.is_integer_dtype(df_processed['Idade']), 
            "The column 'Idade' must be integer type after processing.")
        
        for col in final_columns:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(df_processed[col]),
                f"The agregation column '{col}' should be numeric type.")
        
        self.assertIn('Categoria de Risco - CRI', df_processed.columns)

if __name__ == '__main__':
    unittest.main(verbosity=2)