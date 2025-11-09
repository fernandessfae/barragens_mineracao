import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import MagicMock, patch, call
from sklearn.base import BaseEstimator

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

from ml_cri import CRIModelEvaluator


DUMMY_DATA = pd.DataFrame({
    'CRI': [0, 1, 2, 3, 0, 1, 2, 3, 0, 1], # 10 amostras
    'F1': np.random.rand(10),
    'F2': np.random.rand(10),
    'F3': np.random.rand(10),
    'F4': np.random.rand(10)
})

class MockModel(BaseEstimator):
    """Mock Model to simulate fit/predict behavior."""
    def fit(self, X, y):
        return self
    
    def predict(self, X):
        return np.array([3] * len(X)) 

class TestCRIModelEvaluator(unittest.TestCase):

    def setUp(self):
        self.data = DUMMY_DATA.copy()
        self.evaluator = CRIModelEvaluator(self.data, target_index=0)
        self.mock_model_dt = MockModel()
        self.mock_model_lr = MockModel()
    
    def test_init_separates_xy_correctly(self):
        self.assertEqual(len(self.evaluator.X), 10)
        self.assertEqual(len(self.evaluator.X.columns), 4)
        self.assertTrue('F1' in self.evaluator.X.columns)
        self.assertEqual(len(self.evaluator.y), 10)
        self.assertFalse(self.evaluator.y.empty)

    def test_init_raises_error_on_empty_dataframe(self):
        with self.assertRaisesRegex(
            ValueError, "The provided DataFrame is empty."):
            CRIModelEvaluator(pd.DataFrame())
    
    @patch('ml_cri.print')
    def test_add_model_stores_model(self, mock_print):
        self.evaluator.add_model(self.mock_model_dt, 'DecisionTree')
        self.assertIn('DecisionTree', self.evaluator.models)
        self.assertIs(
            self.evaluator.models['DecisionTree'], self.mock_model_dt)

    @patch('ml_cri.print')
    def test_split_data_divides_correctly(self, mock_print):
        self.evaluator.split_data(test_size=0.4, random_state=42)
        
        self.assertEqual(len(self.evaluator.X_train), 6)
        self.assertEqual(len(self.evaluator.X_test), 4)
    
    def test_train_model_not_split_raises_error(self):
        self.evaluator.add_model(self.mock_model_dt, 'DT')
        self.evaluator.X_train = None 

        with self.assertRaisesRegex(
            AttributeError, "Not data split. Call 'split_data' first."):
            self.evaluator.train_model('DT')

    @patch('ml_cri.accuracy_score', return_value=0.75)
    @patch('ml_cri.confusion_matrix', return_value=np.array([[3, 1], [0, 0]]))
    @patch('ml_cri.print')
    def test_train_model_success_stores_results(
        self, mock_print, mock_cm, mock_acc):
        self.evaluator.add_model(self.mock_model_dt, 'DT')
        self.evaluator.split_data(test_size=0.4, random_state=42)

        mock_fit = MagicMock(return_value=self.mock_model_dt)
        mock_predict = MagicMock(return_value=np.array([3] * 4)) 

        self.mock_model_dt.fit = mock_fit
        self.mock_model_dt.predict = mock_predict
        
        self.evaluator.train_model('DT')
        
        self.assertIn('DT', self.evaluator.results)
        self.assertAlmostEqual(self.evaluator.results['DT']['accuracy'], 0.75)

        mock_fit.assert_called_once() 
        mock_predict.assert_called_once() 

    @patch.object(CRIModelEvaluator, 'train_model')
    def test_train_all_models_calls_all_train_model(self, mock_train_model):
        self.evaluator.add_model(MagicMock(), 'ModelA')
        self.evaluator.add_model(MagicMock(), 'ModelB')
        
        self.evaluator.train_all_models()
        
        mock_train_model.assert_has_calls([call('ModelA'), call('ModelB')])
        self.assertEqual(mock_train_model.call_count, 2)

    def _setup_trained_model_results(
            self, name: str, accuracy: float, model_instance: BaseEstimator):
        self.evaluator.split_data(test_size=0.3)
        self.evaluator.results[name] = {
            'model': model_instance,
            'predictions': self.evaluator.y_test,
            'accuracy': accuracy,
            'confusion_matrix': np.array([[1, 0], [0, 2]])
        }

    @patch('ml_cri.print')
    @patch('ml_cri.classification_report')
    @patch('ml_cri.ConfusionMatrix')
    @patch('ml_cri.plt')
    @patch('ml_cri.os.makedirs')
    def test_evaluate_model_plots_and_reports(
        self, mock_makedirs, mock_plt, MockCM, mock_cr, mock_print):
        self._setup_trained_model_results('DT', 0.99, self.mock_model_dt)
        
        # ConfusionMatrix mock setup
        mock_mc_instance = MockCM.return_value
        
        self.evaluator.evaluate_model('DT')

        mock_cr.assert_called_once()
         
        MockCM.assert_called_once()
        mock_mc_instance.fit.assert_called_once()
        mock_mc_instance.score.assert_called_once()
        
        mock_plt.close.assert_called_once()
    
    def test_compare_models_raises_error_no_results(self):
        self.evaluator.results = {}
        
        with self.assertRaisesRegex(
            ValueError, "No models trained for comparison."):
            self.evaluator.compare_models()
            
    @patch('ml_cri.print')
    def test_compare_models_finds_best(self, mock_print):

        self.evaluator.results = {
            'A': {'model': self.mock_model_dt, 'accuracy': 0.85},
            'B': {'model': self.mock_model_lr, 'accuracy': 0.92} 
        }
        
        best_name, best_model = self.evaluator.compare_models(
            metric='accuracy')
        
        self.assertEqual(best_name, 'B')
        self.assertIs(best_model, self.mock_model_lr)
    
    def test_save_best_model_raises_error_no_results(self):
        
        self.evaluator.results = {}
        
        with self.assertRaisesRegex(
            ValueError, "No models trained for serialization."):
            self.evaluator.save_best_model()

    @patch('ml_cri.open', new_callable=unittest.mock.mock_open)
    @patch.object(
        CRIModelEvaluator, 'compare_models', return_value=('DT', MagicMock()))
    @patch('ml_cri.pickle.dump')
    @patch('ml_cri.print')
    def test_save_best_model_success_calls_pickle_dump(
        self, mock_print, mock_dump, mock_compare, mock_file):
        
        self.evaluator.results = {
            'DT': {'accuracy': 0.9, 'model': mock_compare.return_value[1]}}
        
        self.evaluator.save_best_model('custom_output.pkl')
        
        mock_compare.assert_called_once_with(metric='accuracy')
        
        mock_file.assert_called_once_with('custom_output.pkl', 'wb')
        
        mock_dump.assert_called_once_with(
            mock_compare.return_value[1], mock_file())


if __name__ == '__main__':
    unittest.main(verbosity=2)