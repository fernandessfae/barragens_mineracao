class PreProcessamento:
    def __init__(self, valor_entrada: str):
        self.valor_entrada = valor_entrada
    
    def idade_barragem(self) -> int:
        if self.valor_entrada == 'Maior do que 50 ou menor igual a 5':
            return 4
        elif self.valor_entrada == 'Maior do que 5 e menor igual a 10':
            return 3
        elif self.valor_entrada == 'Maior do que 10 e menor igual a 30':
            return 2
        elif self.valor_entrada == 'Maior do que 30 e menor igual a 50':
            return 1
    
    def altura_barragem(self) -> int:
        if self.valor_entrada == 'Menor igual a 15':
            return 0
        elif self.valor_entrada == 'Maior do que 15 e menor do que 30':
            return 1
        elif self.valor_entrada == 'Maior igual a 30 e menor igual a 60':
            return 2
        elif self.valor_entrada == 'Maior do que 60':
            return 3
    
    def comprimento_barragem(self) -> int:
        if self.valor_entrada == 'Menor igual a 200':
            return 2
        elif self.valor_entrada == 'Maior do que 200':
            return 3
        
    def material_construcao_barragem(self) -> int:
        if self.valor_entrada == 'Concreto convencional':
            return 1
        elif self.valor_entrada == 'Terra':
            return 3
    
    def tipo_fundacao_barragem(self) -> int:
        if self.valor_entrada == 'Rocha sã':
            return 1
        elif self.valor_entrada == 'Rocha alterada/Saprolito':
            return 2
        elif self.valor_entrada == 'Solo residual/Aluvião':
            return 3
        elif self.valor_entrada == 'Aluvião arenoso espesso/Solo orgânico/' + \
        'Rejeito/Desconhecido':
            return 4
        
    def vazao_barragem(self) -> int:
        if self.valor_entrada == 'CMP (Cheia Máxima Provável) ou Decamilenar':
            return 3
        elif self.valor_entrada == 'Milenar':
            return 5
        elif self.valor_entrada == 'TR = 500 anos':
            return 8
        elif self.valor_entrada == 'TR inferior a 500 anos ou ' + \
        'Desconhecida/Estudo não confiável':
            return 10
    
    def conf_estrutura_extravasora_barragem(self) -> int:
        if self.valor_entrada == 'Estruturas civis bem mantidas e em ' + \
        'operação normal/barragem sem necessidade de estruturas extravasoras' \
            or self.valor_entrada == 'Não se aplica a esse tipo de barragem':
            return 0
        elif self.valor_entrada == 'Estruturas com problemas identificados' + \
        ' e medidas corretivas em implantação':
            return 7
        elif self.valor_entrada == 'Estruturas com problemas identificados' + \
        ' e sem implantação das medidas corretivas necessárias':
            return 10
        
    def percolacao_barragem(self) -> int:
        if self.valor_entrada == 'Percolação totalmente controlada pelo ' + \
        'sistema de drenagem' or self.valor_entrada == 'Não se aplica a ' + \
        'esse tipo de barragem':
            return 0
        elif self.valor_entrada == 'Umidade ou surgência nas áreas de ' + \
        'jusante, paramentos, taludes e ombreiras estáveis e monitorados':
            return 3
        elif self.valor_entrada == 'Umidade ou surgência nas áreas de ' + \
        'jusante, paramentos, taludes ou ombreiras sem implantação das ' + \
        'medidas corretivas necessárias':
            return 5
        elif self.valor_entrada == 'Surgência nas áreas de jusante com ' + \
        'carreamento de material ou com vazão crescente ou infiltração ' + \
        'do material contido, com potencial de comprometimento da ' + \
        'segurança da estrutura':
            return 8
        
    def deformacao_recalque_barragem(self) -> int:
        if self.valor_entrada == 'Não existem deformações e recalques com ' + \
        'potencial de comprometimento da segurança da estrutura' or \
        self.valor_entrada == 'Não se aplica a esse tipo de barragem':
            return 0
        elif self.valor_entrada == 'Existência de trincas e abatimentos ' + \
        'com medidas corretivas em implantação':
            return 1
        elif self.valor_entrada == 'Existência de trincas e abatimentos ' + \
        'sem implantação das medidas corretivas necessárias':
            return 5
        elif self.valor_entrada == 'Existência de trincas, abatimentos ' + \
        'ou escorregamentos, com potencial de comprometimento da ' + \
        'segurança da estrutura':
            return 8
        
    def deterioracao_taludes_barragem(self) -> int:
        if self.valor_entrada == 'Não se aplica a esse tipo de barragem' or \
            self.valor_entrada == 'Não existe deterioração de taludes ' + \
            'e paramentos':
            return 0
        elif self.valor_entrada == 'Falhas na proteção dos taludes e ' + \
        'paramentos, presença de vegetação arbustiva':
            return 1
        elif self.valor_entrada == 'Erosões superficiais, ferragem ' + \
        'exposta, presença de vegetação arbórea, sem implantação das ' + \
        'medidas corretivas necessárias':
            return 5
        elif self.valor_entrada == 'Depressões acentuadas nos taludes, ' + \
        'escorregamentos, sulcos profundos de erosão, com potencial de ' + \
        'comprometimento da segurança da estrutura':
            return 7
        
    def documentacao_projeto_barragem(self) -> int:
        if self.valor_entrada == 'Não se aplica a esse tipo de barragem' or \
            self.valor_entrada == 'Projeto executivo e "como construído"':
            return 0
        elif self.valor_entrada == 'Projeto executivo ou "como construído"':
            return 2
        elif self.valor_entrada == 'Projeto básico':
            return 4
        elif self.valor_entrada == 'Projeto conceitual':
            return 6
        elif self.valor_entrada == 'Não há documentação de projeto':
            return 8
    
    def est_org_ql_tec_barragem(self) -> int:
        if self.valor_entrada == 'Não se aplica a esse tipo de barragem' or \
            self.valor_entrada == 'Possui unidade administrativa com ' + \
            'profissional técnico qualificado responsável pela segurança ' + \
            'da barragem':
            return 0
        elif self.valor_entrada == 'Possui profissional técnico ' + \
        'qualificado (próprio ou contratado) responsável pela segurança ' + \
        'da barragem':
            return 4
        elif self.valor_entrada == 'Não possui unidade administrativa e ' + \
        'responsável técnico qualificado pela segurança da barragem':
            return 8
    
    def pro_ins_seg_mon_barragem(self) -> int:
        if self.valor_entrada == 'Não se aplica a esse tipo de barragem' or \
            self.valor_entrada == 'Possui manuais de procedimentos para ' + \
            'inspeção, monitoramento e operação':
            return 0
        elif self.valor_entrada == 'Possui apenas manual de procedimentos ' + \
        'de inspeção':
            return 3
        elif self.valor_entrada == 'Possui e não aplica manuais de ' + \
        'procedimentos de inspeção e monitoramento':
            return 5
        elif self.valor_entrada == 'Não possui manuais ou procedimentos ' + \
        'formais para monitoramento e inspeções':
            return 6
        
    def rel_ins_seg_barragem(self) -> int:
        if self.valor_entrada == 'Não se aplica a esse tipo de barragem' or \
            self.valor_entrada == 'Emite regularmente relatórios de ' + \
            'inspeção e monitoramento com base na instrumentação e de ' + \
            'Análise de Segurança':
            return 0
        elif self.valor_entrada == 'Emite os relatorios sem perioricidade':
            return 3
        elif self.valor_entrada == 'Não emite regularmente relatórios de ' + \
        'inspeção e monitoramento e de Análise de Segurança':
            return 5
        
    def volume_reservatorio_barragem(self) -> int:
        if self.valor_entrada == 'Pequeno (<= 5 milhões m³)':
            return 1
        elif self.valor_entrada == 'Médio (> 5 e <= 75 milhões m³)':
            return 2
        elif self.valor_entrada == 'Grande (> 75 e <= 200 milhões m³)':
            return 3
        elif self.valor_entrada == 'Muito Grande (> 200 milhões m³)':
            return 5
        
    def exs_pop_jus_barragem(self) -> int:
        if self.valor_entrada == 'Inexistente (Não existem pessoas ' + \
        'permanentes/residentes ou temporárias/transitando na área afetada' + \
        ' a jusante da barragem)':
            return 0
        elif self.valor_entrada == 'Pouco Frequente (Não existem pessoas ' + \
        'ocupando permanentemente a área afetada a jusante da barragem, ' + \
        'mas existe estrada vicinal de uso local)':
            return 4
        elif self.valor_entrada == 'Frequente (Não existem pessoas ' + \
        'ocupando permanentemente a área afetada a jusante da barragem, ' + \
        'mas existe rodovia municipal ou estadual ou federal ou outro ' + \
        'local e/ou empreendimento de permanência eventual de pessoas ' + \
        'que poderão ser atingidas)':
            return 8
        elif self.valor_entrada == 'Existente (Existem pessoas ocupando ' + \
        'permanentemente a área afetada a jusante da barragem, portanto, ' + \
        'vidas humanas poderão ser atingidas)':
            return 12
        
    def impacto_ambiental_barragem(self) -> int:
        if self.valor_entrada == 'Significativo (Área afetada a jusante ' + \
        'da barragem apresenta área de interesse ambiental relevante ou ' + \
        'áreas protegidas em legislação específica (excluidas APPs)) e ' + \
        'armazena apenas resíduos Classe II B - Inertes, segundo a NBR ' + \
        '10004/2004 da ABNT)':
            return 3
        elif self.valor_entrada == 'Muito Significativo (Barragem ' + \
        'armazena rejeitos ou resíduos sólidos classificados na Classe II ' + \
        'A - Não Inertes, segundo a NBR 10004/2004)':
            return 5
        
    def impacto_socio_economico_barragem(self) -> int:
        if self.valor_entrada == 'Inexistente (Não existem quaisquer ' + \
        'instalações na área afetada a jusante da barragem)':
            return 0
        elif self.valor_entrada == 'BAIXO (Existe pequena concentração ' + \
        'de instalações residenciais, agrícolas, industriais ou de ' + \
        'infraestrutura de relevância sócio-econômico-cultural na área ' + \
        'afetada a jusante da barragem)':
            return 4
        elif self.valor_entrada == 'ALTO (Existe alta concentração de ' + \
        'instalações residenciais, agrícolas, industriais ou de ' + \
        'infraestrutura de relevância sócio-econômico-cultural na área ' + \
        'afetada a jusante da barragem)':
            return 8