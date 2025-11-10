import unittest
import os
import sys

dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_root)

from pre_processamento_streamlit import PreProcessamento

class TestPreProcessamento(unittest.TestCase):
    
    INVALID_INPUT = "Entrada Invalida ou Desconhecida"

    def test_init_stores_input_value(self):
        input_value = "Rocha sã"
        prep = PreProcessamento(input_value)
        self.assertEqual(prep.input_value, input_value)

    def test_idade_barragem(self):
        test_cases = [
            ('Maior do que 50 ou menor igual a 5', 4),
            ('Maior do que 5 e menor igual a 10', 3),
            ('Maior do que 10 e menor igual a 30', 2),
            ('Maior do que 30 e menor igual a 50', 1),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.idade_barragem(), expected)

    def test_altura_barragem(self):
        test_cases = [
            ('Menor igual a 15', 0),
            ('Maior do que 15 e menor do que 30', 1),
            ('Maior igual a 30 e menor igual a 60', 2),
            ('Maior do que 60', 3),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.altura_barragem(), expected)
                
    def test_comprimento_barragem(self):
        
        test_cases = [
            ('Menor igual a 200', 2),
            ('Maior do que 200', 3),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.comprimento_barragem(), expected)
                
    def test_material_construcao_barragem(self):
        test_cases = [
            ('Concreto convencional', 1),
            ('Terra', 3),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.material_construcao_barragem(), expected)

    def test_tipo_fundacao_barragem(self):
        long_input = 'Aluvião arenoso espesso/Solo ' \
        'orgânico/Rejeito/Desconhecido'
        test_cases = [
            ('Rocha sã', 1),
            ('Rocha alterada/Saprolito', 2),
            ('Solo residual/Aluvião', 3),
            (long_input, 4),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.tipo_fundacao_barragem(), expected)

    def test_vazao_barragem(self):
        long_input = 'TR inferior a 500 anos ou ' \
        'Desconhecida/Estudo não confiável'
        
        test_cases = [
            ('CMP (Cheia Máxima Provável) ou Decamilenar', 3),
            ('Milenar', 5),
            ('TR = 500 anos', 8),
            (long_input, 10),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.vazao_barragem(), expected)

    def test_conf_estrutura_extravasora_barragem(self):
        input_0_a = 'Estruturas civis bem mantidas e em operação ' \
        'normal/barragem sem necessidade de estruturas extravasoras'
        input_7 = 'Estruturas com problemas identificados e medidas ' \
        'corretivas em implantação'
        input_10 = 'Estruturas com problemas identificados e sem ' \
        'implantação das medidas corretivas necessárias'
        
        test_cases = [
            (input_0_a, 0),
            ('Não se aplica a esse tipo de barragem', 0),
            (input_7, 7),
            (input_10, 10),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(
                    prep.conf_estrutura_extravasora_barragem(), expected)

    def test_percolacao_barragem(self):
        input_0_a = 'Percolação totalmente controlada pelo sistema de drenagem'
        input_3 = 'Umidade ou surgência nas áreas de jusante, paramentos, ' \
        'taludes e ombreiras estáveis e monitorados'
        input_5 = 'Umidade ou surgência nas áreas de jusante, paramentos, ' \
        'taludes ou ombreiras sem implantação das medidas corretivas necessárias'
        input_8 = 'Surgência nas áreas de jusante com carreamento de ' \
        'material ou com vazão crescente ou infiltração do material contido,' \
        ' com potencial de comprometimento da segurança da estrutura'

        test_cases = [
            (input_0_a, 0),
            ('Não se aplica a esse tipo de barragem', 0),
            (input_3, 3),
            (input_5, 5),
            (input_8, 8),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.percolacao_barragem(), expected)

    def test_deformacao_recalque_barragem(self):
        input_0_a = 'Não existem deformações e recalques com potencial de ' \
        'comprometimento da segurança da estrutura'
        input_1 = 'Existência de trincas e abatimentos com medidas ' \
        'corretivas em implantação'
        input_5 = 'Existência de trincas e abatimentos sem implantação das ' \
        'medidas corretivas necessárias'
        input_8 = 'Existência de trincas, abatimentos ou escorregamentos, ' \
        'com potencial de comprometimento da segurança da estrutura'

        test_cases = [
            (input_0_a, 0),
            ('Não se aplica a esse tipo de barragem', 0),
            (input_1, 1),
            (input_5, 5),
            (input_8, 8),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.deformacao_recalque_barragem(), expected)
                
    def test_deterioracao_taludes_barragem(self):
        input_0_b = 'Não existe deterioração de taludes e paramentos'
        input_1 = 'Falhas na proteção dos taludes e paramentos, ' \
        'presença de vegetação arbustiva'
        input_5 = 'Erosões superficiais, ferragem exposta, presença de ' \
        'vegetação arbórea, sem implantação das medidas corretivas necessárias'
        input_7 = 'Depressões acentuadas nos taludes, escorregamentos, ' \
        'sulcos profundos de erosão, com potencial de comprometimento da ' \
        'segurança da estrutura'

        test_cases = [
            ('Não se aplica a esse tipo de barragem', 0),
            (input_0_b, 0),
            (input_1, 1),
            (input_5, 5),
            (input_7, 7),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(
                    prep.deterioracao_taludes_barragem(), expected)

    def test_documentacao_projeto_barragem(self):
        input_0_b = 'Projeto executivo e "como construído"'
        
        test_cases = [
            ('Não se aplica a esse tipo de barragem', 0),
            (input_0_b, 0),
            ('Projeto executivo ou "como construído"', 2),
            ('Projeto básico', 4),
            ('Projeto conceitual', 6),
            ('Não há documentação de projeto', 8),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(
                    prep.documentacao_projeto_barragem(), expected)
                
    def test_est_org_ql_tec_barragem(self):
        input_0_b = 'Possui unidade administrativa com profissional técnico ' \
        'qualificado responsável pela segurança da barragem'
        input_4 = 'Possui profissional técnico qualificado ' \
        '(próprio ou contratado) responsável pela segurança da barragem'
        input_8 = 'Não possui unidade administrativa e responsável técnico ' \
        'qualificado pela segurança da barragem'
        
        test_cases = [
            ('Não se aplica a esse tipo de barragem', 0),
            (input_0_b, 0),
            (input_4, 4),
            (input_8, 8),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.est_org_ql_tec_barragem(), expected)

    def test_pro_ins_seg_mon_barragem(self):
        input_0_b = 'Possui manuais de procedimentos para inspeção, ' \
        'monitoramento e operação'
        input_3 = 'Possui apenas manual de procedimentos de inspeção'
        input_5 = 'Possui e não aplica manuais de procedimentos de inspeção ' \
        'e monitoramento'
        input_6 = 'Não possui manuais ou procedimentos formais para ' \
        'monitoramento e inspeções'
        
        test_cases = [
            ('Não se aplica a esse tipo de barragem', 0),
            (input_0_b, 0),
            (input_3, 3),
            (input_5, 5),
            (input_6, 6),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.pro_ins_seg_mon_barragem(), expected)
                
    def test_rel_ins_seg_barragem(self):
        input_0_b = 'Emite regularmente relatórios de inspeção e ' \
        'monitoramento com base na instrumentação e de Análise de Segurança'
        
        test_cases = [
            ('Não se aplica a esse tipo de barragem', 0),
            (input_0_b, 0),
            ('Emite os relatorios sem perioricidade', 3),
            ('Não emite regularmente relatórios de inspeção e monitoramento '
            'e de Análise de Segurança', 5),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.rel_ins_seg_barragem(), expected)

    def test_volume_reservatorio_barragem(self):
        test_cases = [
            ('Pequeno (<= 5 milhões m³)', 1),
            ('Médio (> 5 e <= 75 milhões m³)', 2),
            ('Grande (> 75 e <= 200 milhões m³)', 3),
            ('Muito Grande (> 200 milhões m³)', 5),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.volume_reservatorio_barragem(), expected)
                
    def test_exs_pop_jus_barragem(self):
        input_0 = 'Inexistente (Não existem pessoas permanentes/residentes ' \
        'ou temporárias/transitando na área afetada a jusante da barragem)'
        input_4 = 'Pouco Frequente (Não existem pessoas ocupando ' \
        'permanentemente a área afetada a jusante da barragem, mas existe ' \
        'estrada vicinal de uso local)'
        input_8 = 'Frequente (Não existem pessoas ocupando permanentemente ' \
        'a área afetada a jusante da barragem, mas existe rodovia municipal ' \
        'ou estadual ou federal ou outro local e/ou empreendimento de ' \
        'permanência eventual de pessoas que poderão ser atingidas)'
        input_12 = 'Existente (Existem pessoas ocupando permanentemente a ' \
        'área afetada a jusante da barragem, portanto, vidas humanas ' \
        'poderão ser atingidas)'

        test_cases = [
            (input_0, 0),
            (input_4, 4),
            (input_8, 8),
            (input_12, 12),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.exs_pop_jus_barragem(), expected)

    def test_impacto_ambiental_barragem(self):
        input_3 = 'Significativo (Área afetada a jusante da barragem ' \
        'apresenta área de interesse ambiental relevante ou áreas ' \
        'protegidas em legislação específica (excluidas APPs)) e armazena ' \
        'apenas resíduos Classe II B - Inertes, segundo a NBR 10004/2004 ' \
        'da ABNT)'
        input_5 = 'Muito Significativo (Barragem armazena rejeitos ou ' \
        'resíduos sólidos classificados na Classe II A - Não Inertes, ' \
        'segundo a NBR 10004/2004)'

        test_cases = [
            (input_3, 3),
            (input_5, 5),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(prep.impacto_ambiental_barragem(), expected)

    def test_impacto_socio_economico_barragem(self):
        input_0 = 'Inexistente (Não existem quaisquer instalações na área ' \
        'afetada a jusante da barragem)'
        input_4 = 'BAIXO (Existe pequena concentração de instalações ' \
        'residenciais, agrícolas, industriais ou de infraestrutura de ' \
        'relevância sócio-econômico-cultural na área afetada a ' \
        'jusante da barragem)'
        input_8 = 'ALTO (Existe alta concentração de instalações ' \
        'residenciais, agrícolas, industriais ou de infraestrutura de ' \
        'relevância sócio-econômico-cultural na área afetada a ' \
        'jusante da barragem)'

        test_cases = [
            (input_0, 0),
            (input_4, 4),
            (input_8, 8),
            (self.INVALID_INPUT, None)
        ]

        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                prep = PreProcessamento(input_val)
                self.assertEqual(
                    prep.impacto_socio_economico_barragem(), expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)