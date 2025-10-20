import unittest
import os
import sys

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

class TestIsDataFrame(unittest.TestCase):
    def test_is_dataframe(self):
        from analise import is_dataframe
        from pandas import DataFrame

        df = DataFrame({'A': [1, 2], 'B': [3, 4]})
        self.assertTrue(is_dataframe(df))

        not_df = [1, 2, 3]
        self.assertFalse(is_dataframe(not_df))

class TestColumnInDataFrame(unittest.TestCase):
    def test_column_in_dataframe(self):
        from analise import column_in_dataframe
        from pandas import DataFrame

        df = DataFrame({'A': [1, 2], 'B': [3, 4]})
        self.assertTrue(column_in_dataframe('A', df))
        self.assertTrue(column_in_dataframe('B', df))
        self.assertFalse(column_in_dataframe('C', df))

class TestEnsureDirectoryExists(unittest.TestCase):

    def test_ensure_directory_exists(self):
        from analise import ensure_directory_exists
        directory = 'readme_images'
        ensure_directory_exists(directory)
        self.assertTrue(os.path.exists(directory))
        os.rmdir(directory) 

if __name__ == '__main__':
    unittest.main(verbosity=2)