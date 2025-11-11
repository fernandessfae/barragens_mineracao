import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import numpy as np

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

from streamlit_ml_app import previsao_barragem_cri, previsao_barragem_dpa

# --- PreProcessing Mock Class ---
# Simulate a PreProcessamento class with methods returning fixed values
class MockPreProcessamento:
    def __init__(self, input_value):
        pass

    # Mock of 14 methods for CRI (returning 1 to 14)
    def idade_barragem(self): return 1
    def altura_barragem(self): return 2
    def comprimento_barragem(self): return 3
    def material_construcao_barragem(self): return 4
    def tipo_fundacao_barragem(self): return 5
    def vazao_barragem(self): return 6
    def conf_estrutura_extravasora_barragem(self): return 7
    def percolacao_barragem(self): return 8
    def deformacao_recalque_barragem(self): return 9
    def deterioracao_taludes_barragem(self): return 10
    def documentacao_projeto_barragem(self): return 11
    def est_org_ql_tec_barragem(self): return 12
    def pro_ins_seg_mon_barragem(self): return 13
    def rel_ins_seg_barragem(self): return 14
    
    # Mock of 4 methods for DPA (returning 10, 20, 30, 40)
    def volume_reservatorio_barragem(self): return 10
    def exs_pop_jus_barragem(self): return 20
    def impacto_ambiental_barragem(self): return 30
    def impacto_socio_economico_barragem(self): return 40

# Patch global para substituir o import real de PreProcessamento pela Mock
@patch('streamlit_ml_app.PreProcessamento', new=MockPreProcessamento)
class TestPrevisaoBarragem(unittest.TestCase):

    DUMMY_INPUTS_CRI = {
        'idade': 'Dummy', 'altura': 'Dummy', 'comprimento': 'Dummy',
        'material': 'Dummy', 'fundacao': 'Dummy', 'vazao': 'Dummy',
        'conf': 'Dummy', 'percolacao': 'Dummy', 'def_rec': 'Dummy',
        'det_tal': 'Dummy', 'doc': 'Dummy', 'est_org_ql_tec': 'Dummy',
        'pro_ins_seg_mon': 'Dummy', 'rel_ins_seg': 'Dummy'
    }
    
    DUMMY_INPUTS_DPA = {
        'volume': 'Dummy', 'exs_pop_jus': 'Dummy', 
        'imp_amb': 'Dummy', 'imp_socio_eco': 'Dummy'
    }

    @patch('streamlit_ml_app.classificador_cri')
    def test_previsao_barragem_cri(self, mock_classificador_cri):
        
        # 1. Configuration of the CRI Classifier Mock (does not matter the input, always returns EXPECTED_PREDICTION)
        EXPECTED_PREDICTION = 2
        mock_classificador_cri.predict.return_value = np.array(
            [[EXPECTED_PREDICTION]])

        # 2. Execute the function with dummy inputs
        result = previsao_barragem_cri(**self.DUMMY_INPUTS_CRI)

        # 3. Calculate expected values (based on returns from 1 to 14 from MockPreProcessamento)
        
        # ct = 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28
        EXPECTED_CT = 28
        
        # ec = 7 + 8 + 9 + 10 = 34
        EXPECTED_EC = 34
        
        # ps = 11 + 12 + 13 + 14 = 50
        EXPECTED_PS = 50
        
        # 4. Expected feature vector
        expected_feature_vector = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 
            EXPECTED_CT, EXPECTED_EC, EXPECTED_PS         
        ]
        
        # 5. Verify that the predict method was called ONCE with the correct vector
        mock_classificador_cri.predict.assert_called_once()
        args, _ = mock_classificador_cri.predict.call_args
        self.assertEqual(
            args[0], [expected_feature_vector], 
            "The feature vector passed to the CRI predict method is incorrect.")
        
        # 6. Verify the returned result
        self.assertEqual(
            result, EXPECTED_PREDICTION, 
            "The result returned by the function does not match the mocked prediction.")

    @patch('streamlit_ml_app.classificador_dpa')
    def test_previsao_barragem_dpa(self, mock_classificador_dpa):
        
        # 1. Configure the DPA Classifier Mock
        EXPECTED_PREDICTION = 3
        mock_classificador_dpa.predict.return_value = np.array(
            [[EXPECTED_PREDICTION]])

        # 2. Execute the function with dummy inputs
        result = previsao_barragem_dpa(**self.DUMMY_INPUTS_DPA)

        # 3. Calculate expected values (based on returns of 10, 20, 30, 40 from MockPreProcessamento)
        
        # dpa = 10 + 20 + 30 + 40 = 100
        EXPECTED_DPA = 100
        
        # 4. Expected feature vector
        expected_feature_vector = [
            10, 20, 30, 40,
            EXPECTED_DPA    
        ]
        
        # 5. Verify that the predict method was called ONCE with the correct vector
        mock_classificador_dpa.predict.assert_called_once()
        args, _ = mock_classificador_dpa.predict.call_args
        self.assertEqual(
            args[0], [expected_feature_vector],
            "The feature vector passed to the DPA predict method is incorrect.")
        
        # 6. Verify the returned result
        self.assertEqual(
            result, EXPECTED_PREDICTION,
            "The result returned by the function does not match the mocked prediction.")

if __name__ == '__main__':
    unittest.main(verbosity=2)