class PreProcessamento:
    def __init__(self, input_value: str):
        self.input_value = input_value
    
    def idade_barragem(self) -> int:

        values_idade_barragem: dict[str, int] = {
            'Maior do que 50 ou menor igual a 5': 4,
            'Maior do que 5 e menor igual a 10': 3,
            'Maior do que 10 e menor igual a 30': 2,
            'Maior do que 30 e menor igual a 50': 1}
        
        return values_idade_barragem.get(self.input_value, None)
    
    def altura_barragem(self) -> int:

        values_altura_barragem: dict[str, int] = {
            'Menor igual a 15': 0,
            'Maior do que 15 e menor do que 30': 1,
            'Maior igual a 30 e menor igual a 60': 2,
            'Maior do que 60': 3}
        
        return values_altura_barragem.get(self.input_value, None)
    
    def comprimento_barragem(self) -> int:

        values_comprimento_barragem: dict[str, int] = {
            'Menor igual a 200': 2,
            'Maior do que 200': 3}
        
        return values_comprimento_barragem.get(self.input_value, None)
        
    def material_construcao_barragem(self) -> int:

        values_material_construcao_barragem: dict[str, int] = {
            'Concreto convencional': 1,
            'Terra': 3}
        
        return values_material_construcao_barragem.get(self.input_value, None)
    
    def tipo_fundacao_barragem(self) -> int:

        values_tipo_fundacao_barragem: dict[str, int] = {
            'Rocha sã': 1,
            'Rocha alterada/Saprolito': 2,
            'Solo residual/Aluvião': 3,
            'Aluvião arenoso espesso/Solo orgânico/Rejeito/Desconhecido': 4}
        
        return values_tipo_fundacao_barragem.get(self.input_value, None)
        
    def vazao_barragem(self) -> int:

        values_vazao_barragem: dict[str, int] = {
            'CMP (Cheia Máxima Provável) ou Decamilenar': 3,
            'Milenar': 5,
            'TR = 500 anos': 8,
            'TR inferior a 500 anos ou Desconhecida/Estudo não confiável': 10}
        
        return values_vazao_barragem.get(self.input_value, None)
    
    def conf_estrutura_extravasora_barragem(self) -> int:
        
        values_conf_estrutura_extravasora_barragem: dict[str, int] = {
            'Estruturas civis bem mantidas e em operação normal/barragem '
            'sem necessidade de estruturas extravasoras': 0,
            'Não se aplica a esse tipo de barragem': 0,
            'Estruturas com problemas identificados e medidas corretivas '
            'em implantação': 7,
            'Estruturas com problemas identificados e sem implantação das '
            'medidas corretivas necessárias': 10}
        
        return values_conf_estrutura_extravasora_barragem.get(
            self.input_value, None)
        
    def percolacao_barragem(self) -> int:

        values_percolacao_barragem: dict[str, int] = {
            'Percolação totalmente controlada pelo sistema de drenagem': 0,
            'Não se aplica a esse tipo de barragem': 0,
            'Umidade ou surgência nas áreas de jusante, paramentos, taludes '
            'e ombreiras estáveis e monitorados': 3,
            'Umidade ou surgência nas áreas de jusante, paramentos, taludes '
            'ou ombreiras sem implantação das medidas corretivas '
            'necessárias': 5,
            'Surgência nas áreas de jusante com carreamento de material ou '
            'com vazão crescente ou infiltração do material contido, com '
            'potencial de comprometimento da segurança da estrutura': 8}
        
        return values_percolacao_barragem.get(self.input_value, None)
        
    def deformacao_recalque_barragem(self) -> int:

        values_deformacao_recalque_barragem: dict[str, int] = {
            'Não existem deformações e recalques com potencial de '
            'comprometimento da segurança da estrutura': 0,
            'Não se aplica a esse tipo de barragem': 0,
            'Existência de trincas e abatimentos com medidas corretivas '
            'em implantação': 1,
            'Existência de trincas e abatimentos sem implantação das '
            'medidas corretivas necessárias': 5,
            'Existência de trincas, abatimentos ou escorregamentos, com '
            'potencial de comprometimento da segurança da estrutura': 8}
        
        return values_deformacao_recalque_barragem.get(self.input_value, None)
        
    def deterioracao_taludes_barragem(self) -> int:

        values_deterioracao_taludes_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Não existe deterioração de taludes e paramentos': 0,
            'Falhas na proteção dos taludes e paramentos, presença de '
            'vegetação arbustiva': 1,
            'Erosões superficiais, ferragem exposta, presença de vegetação '
            'arbórea, sem implantação das medidas corretivas necessárias': 5,
            'Depressões acentuadas nos taludes, escorregamentos, sulcos '
            'profundos de erosão, com potencial de comprometimento da '
            'segurança da estrutura': 7}
        
        return values_deterioracao_taludes_barragem.get(self.input_value, None)
        
    def documentacao_projeto_barragem(self) -> int:

        values_documentacao_projeto_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Projeto executivo e "como construído"': 0,
            'Projeto executivo ou "como construído"': 2,
            'Projeto básico': 4,
            'Projeto conceitual': 6,
            'Não há documentação de projeto': 8}
        
        return values_documentacao_projeto_barragem.get(self.input_value, None)
        
    def est_org_ql_tec_barragem(self) -> int:

        values_est_org_ql_tec_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Possui unidade administrativa com profissional técnico '
            'qualificado responsável pela segurança da barragem': 0,
            'Possui profissional técnico qualificado (próprio ou '
            'contratado) responsável pela segurança da barragem': 4,
            'Não possui unidade administrativa e responsável técnico '
            'qualificado pela segurança da barragem': 8}
        
        return values_est_org_ql_tec_barragem.get(self.input_value, None)
        
    def est_org_ql_tec_barragem(self) -> int:

        values_est_org_ql_tec_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Possui unidade administrativa com profissional técnico '
            'qualificado responsável pela segurança da barragem': 0,
            'Possui profissional técnico qualificado (próprio ou '
            'contratado) responsável pela segurança da barragem': 4,
            'Não possui unidade administrativa e responsável técnico '
            'qualificado pela segurança da barragem': 8}
        
        return values_est_org_ql_tec_barragem.get(self.input_value, None)
    
    def est_org_ql_tec_barragem(self) -> int:

        values_est_org_ql_tec_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Possui unidade administrativa com profissional técnico '
            'qualificado responsável pela segurança da barragem': 0,
            'Possui profissional técnico qualificado (próprio ou '
            'contratado) responsável pela segurança da barragem': 4,
            'Não possui unidade administrativa e responsável técnico '
            'qualificado pela segurança da barragem': 8}
        
        return values_est_org_ql_tec_barragem.get(self.input_value, None)
    
    def pro_ins_seg_mon_barragem(self) -> int:

        values_pro_ins_seg_mon_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Possui manuais de procedimentos para inspeção, monitoramento '
            'e operação': 0,
            'Possui apenas manual de procedimentos de inspeção': 3,
            'Possui e não aplica manuais de procedimentos de inspeção '
            'e monitoramento': 5,
            'Não possui manuais ou procedimentos formais para monitoramento '
            'e inspeções': 6}
        
        return values_pro_ins_seg_mon_barragem.get(self.input_value, None)
        
    def rel_ins_seg_barragem(self) -> int:

        values_rel_ins_seg_barragem: dict[str, int] = {
            'Não se aplica a esse tipo de barragem': 0,
            'Emite regularmente relatórios de inspeção e monitoramento com '
            'base na instrumentação e de Análise de Segurança': 0,
            'Emite os relatorios sem perioricidade': 3,
            'Não emite regularmente relatórios de inspeção e monitoramento '
            'e de Análise de Segurança': 5}
        
        return values_rel_ins_seg_barragem.get(self.input_value, None)
        
    def volume_reservatorio_barragem(self) -> int:

        values_volume_reservatorio_barragem: dict[str, int] = {
            'Pequeno (<= 5 milhões m³)': 1,
            'Médio (> 5 e <= 75 milhões m³)': 2,
            'Grande (> 75 e <= 200 milhões m³)': 3,
            'Muito Grande (> 200 milhões m³)': 5}
        
        return values_volume_reservatorio_barragem.get(self.input_value, None)
        
    def exs_pop_jus_barragem(self) -> int:

        values_exs_pop_jus_barragem: dict[str, int] = {
            'Inexistente (Não existem pessoas permanentes/residentes ou '
            'temporárias/transitando na área afetada a jusante da barragem)': 0,
            'Pouco Frequente (Não existem pessoas ocupando permanentemente '
            'a área afetada a jusante da barragem, mas existe estrada vicinal '
            'de uso local)': 4,
            'Frequente (Não existem pessoas ocupando permanentemente a área '
            'afetada a jusante da barragem, mas existe rodovia municipal ou '
            'estadual ou federal ou outro local e/ou empreendimento de '
            'permanência eventual de pessoas que poderão ser atingidas)': 8,
            'Existente (Existem pessoas ocupando permanentemente a área '
            'afetada a jusante da barragem, portanto, vidas humanas poderão '
            'ser atingidas)': 12}
        
        return values_exs_pop_jus_barragem.get(self.input_value, None)
        
    def impacto_ambiental_barragem(self) -> int:

        values_impacto_ambiental_barragem: dict[str, int] = {
            'Significativo (Área afetada a jusante da barragem apresenta '
            'área de interesse ambiental relevante ou áreas protegidas em '
            'legislação específica (excluidas APPs)) e armazena apenas '
            'resíduos Classe II B - Inertes, segundo a NBR 10004/2004 '
            'da ABNT)': 3,
            'Muito Significativo (Barragem armazena rejeitos ou resíduos '
            'sólidos classificados na Classe II A - Não Inertes, segundo a '
            'NBR 10004/2004)': 5}
        
        return values_impacto_ambiental_barragem.get(self.input_value, None)
        
    def impacto_socio_economico_barragem(self) -> int:

        values_impacto_socio_economico_barragem: dict[str, int] = {
            'Inexistente (Não existem quaisquer instalações na área afetada '
            'a jusante da barragem)': 0,
            'BAIXO (Existe pequena concentração de instalações residenciais, '
            'agrícolas, industriais ou de infraestrutura de relevância '
            'sócio-econômico-cultural na área afetada a '
            'jusante da barragem)': 4,
            'MÉDIO (Existe moderada concentração de instalações residenciais, '
            'agrícolas, industriais ou de infraestrutura de relevância '
            'sócio-econômico-cultural na área afetada a '
            'jusante da barragem)': 8,
            'ALTO (Existe alta concentração de instalações residenciais, '
            'agrícolas, industriais ou de infraestrutura de relevância '
            'sócio-econômico-cultural na área afetada a jusante '
            'da barragem)': 8,
            'Indefinido': 8}
        
        return values_impacto_socio_economico_barragem.get(
            self.input_value, None)