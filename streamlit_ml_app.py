import streamlit as st
from pre_processamento_streamlit import PreProcessamento
import pickle


def previsao_barragem_cri(idade: str, altura: str, comprimento: str,
                          material: str, fundacao: str, vazao: str,
                          conf: str, percolacao: str, def_rec: str,
                          det_tal: str, doc: str, est_org_ql_tec: str,
                          pro_ins_seg_mon: str, rel_ins_seg: str) -> int:
    idade_ = PreProcessamento(idade).idade_barragem()
    altura_ = PreProcessamento(altura).altura_barragem()
    comprimento_ = PreProcessamento(comprimento).comprimento_barragem()
    material_ = PreProcessamento(material).material_construcao_barragem()
    fundacao_ = PreProcessamento(fundacao).tipo_fundacao_barragem()
    vazao_ = PreProcessamento(vazao).vazao_barragem()
    conf_ = PreProcessamento(conf).conf_estrutura_extravasora_barragem()
    percolacao_ = PreProcessamento(percolacao).percolacao_barragem()
    def_rec_ = PreProcessamento(def_rec).deformacao_recalque_barragem()
    det_tal_ = PreProcessamento(det_tal).deterioracao_taludes_barragem()
    doc_ = PreProcessamento(doc).documentacao_projeto_barragem()
    est_org_ql_tec_ = PreProcessamento(
        est_org_ql_tec).est_org_ql_tec_barragem()
    pro_ins_seg_mon_ = PreProcessamento(
        pro_ins_seg_mon).pro_ins_seg_mon_barragem()
    rel_ins_seg_ = PreProcessamento(rel_ins_seg).rel_ins_seg_barragem()
    ct = idade_ + altura_ + comprimento_ + material_ + \
        fundacao_ + vazao_ + conf_
    ec = conf_ + percolacao_ + def_rec_ + det_tal_
    ps = doc_ + est_org_ql_tec_ + pro_ins_seg_mon_ + rel_ins_seg_
    previsao = classificador_cri.predict([[idade_, altura_, comprimento_,
                                           material_, fundacao_, vazao_,
                                           conf_, percolacao_, def_rec_,
                                           det_tal_, doc_, est_org_ql_tec_,
                                           pro_ins_seg_mon_, rel_ins_seg_, ct,
                                           ec, ps
                                         ]])
    return previsao


def previsao_barragem_dpa(volume: str, exs_pop_jus: str,
                          imp_amb: str, imp_socio_eco: str) -> int:
    volume_ = PreProcessamento(volume).volume_reservatorio_barragem()
    exs_pop_jus_ = PreProcessamento(exs_pop_jus).exs_pop_jus_barragem()
    imp_amb_ = PreProcessamento(imp_amb).impacto_ambiental_barragem()
    imp_socio_eco_ = PreProcessamento(
        imp_socio_eco).impacto_socio_economico_barragem()
    dpa = volume_ + exs_pop_jus_ + imp_amb_ + imp_socio_eco_
    previsao = classificador_dpa.predict([[volume_, exs_pop_jus_,
                                           imp_amb_, imp_socio_eco_,
                                           dpa]])
    return previsao


def main():
    st.title("Previsão da classificação da barragem de mineração")
    
    html_temp = """
    <div style ="background-color:blue;padding:13px;margin-bottom:10px">
    <h1 style ="color:black;text-align:center;">
    Categoria Risco Iminente (CRI) e Dano Potencial Associado (DPA) </h1>
    </div>
    """
    
    st.markdown(html_temp, unsafe_allow_html = True)
    
    idade_barragem = st.selectbox('Escolha a idade de funcionamento da ' +
                                'barragem (anos)',
                                ['Maior do que 50 ou menor igual a 5',
                                 'Maior do que 5 e menor igual a 10',
                                 'Maior do que 10 e menor igual a 30',
                                 'Maior do que 30 e menor igual a 50'
                                ])
    altura_barragem = st.selectbox('Escolha a altura da barragem (metros)',
                                   ['Menor igual a 15',
                                    'Maior do que 15 e menor do que 30',
                                    'Maior igual a 30 e menor igual a 60',
                                    'Maior do que 60'
                                   ])
    comprimento_barragem = st.selectbox('Escolha o comprimento da barragem ' +
                                        '(metros)',
                                        ['Menor igual a 200',
                                         'Maior do que 200'
                                        ])
    material_barragem = st.selectbox('Escolha o material de construção da ' +
                                     'barragem',
                                     ['Concreto convencional', 'Terra'])
    fundacao_barragem = st.selectbox('Selecione o tipo de fundação da barragem',
                                     ['Rocha sã',
                                      'Rocha alterada/Saprolito',
                                      'Solo residual/Aluvião',
                                      'Aluvião arenoso espesso/Solo orgânico/'+
                                      'Rejeito/Desconhecido'
                                     ])
    vazao_barragem = st.selectbox('Escolha o tipo de vazão da barragem',
                                  ['CMP (Cheia Máxima Provável) ' +
                                   'ou Decamilenar',
                                   'Milenar',
                                   'TR = 500 anos',
                                   'TR inferior a 500 anos ou Desconhecida/' + 
                                   'Estudo não confiável'
                                  ])
    conf_est_ext_barragem = st.selectbox('Selecione o tipo da confiabilidade '
                                         'da estrutura extravasora',
                                        ['Não se aplica a esse tipo ' +
                                         'de barragem',
                                         'Estruturas civis bem mantidas e '
                                         'em operação normal/barragem sem ' +
                                         'necessidade de estruturas ' +
                                         'extravasoras',
                                         'Estruturas com problemas ' +
                                         'identificados e medidas ' +
                                         'corretivas em implantação',
                                         'Estruturas com problemas ' +
                                         'identificados e sem ' +
                                         'implantação das medidas ' +
                                         'corretivas necessárias'
                                        ])
    percolacao_barragem = st.selectbox('Selecione a percolação da barragem',
                                       ['Não se aplica a esse tipo ' +
                                        'de barragem',
                                        'Percolação totalmente controlada ' +
                                        'pelo sistema de drenagem',
                                        'Umidade ou surgência nas áreas de ' +
                                        'jusante, paramentos, taludes e ' +
                                        'ombreiras estáveis e monitorados',
                                        'Umidade ou surgência nas áreas de ' +
                                        'jusante, paramentos, taludes ou ' +
                                        'ombreiras sem implantação das ' +
                                        'medidas corretivas necessárias',
                                        'Surgência nas áreas de jusante com ' +
                                        'carreamento de material ou com ' +
                                        'vazão crescente ou infiltração do ' +
                                        'material contido, com potencial de ' +
                                        'comprometimento da segurança ' +
                                        'da estrutura'
                                       ])
    deformacao_recalque_barragem = st.selectbox('Selecione a deformação e ' +
                                                'recalque da barragem',
                                                ['Não existem deformações e ' +
                                                 'recalques com potencial ' +
                                                 'de comprometimento da ' +
                                                 'segurança da estrutura',
                                                 'Existência de trincas e ' +
                                                 'abatimentos com medidas ' +
                                                 'corretivas em implantação',
                                                 'Existência de trincas e ' +
                                                 'abatimentos sem ' +
                                                 'implantação das medidas ' +
                                                 'corretivas necessárias',
                                                 'Existência de trincas, ' +
                                                 'abatimentos ou ' +
                                                 'escorregamentos, com ' +
                                                 'potencial de ' +
                                                 'comprometimento da ' +
                                                 'segurança da estrutura'
                                                ])
    deterioracao_taludes_barragem = st.selectbox('Selecione a deterioração ' +
                                                 'do talude na barragem',
                                                 ['Não se aplica a esse tipo' +
                                                  ' de barragem',
                                                  'Não existe deterioração ' +
                                                  'de taludes e paramentos',
                                                  'Falhas na proteção dos ' +
                                                  'taludes e paramentos, ' +
                                                  'presença de vegetação ' +
                                                  'arbustiva',
                                                  'Erosões superficiais, ' +
                                                  'ferragem exposta, ' +
                                                  'presença de vegetação ' +
                                                  'arbórea, sem implantação ' +
                                                  'das medidas corretivas ' +
                                                  'necessárias',
                                                  'Depressões acentuadas ' +
                                                  'nos taludes, ' +
                                                  'escorregamentos, sulcos ' +
                                                  'profundos de erosão, com ' +
                                                  'potencial de ' +
                                                  'comprometimento da ' +
                                                  'segurança da estrutura'
                                                 ])
    documentacao_projeto_barragem = st.selectbox('Selecione a documentação ' +
                                                 'da barragem',
                                                 ['Não se aplica a esse ' +
                                                  'tipo de barragem',
                                                  'Projeto executivo e ' +
                                                  '"como construído"',
                                                  'Projeto executivo ou ' +
                                                  '"como construído"',
                                                  'Projeto básico',
                                                  'Projeto conceitual',
                                                  'Não há documentação ' +
                                                  'de projeto'
                                                 ])
    est_org_ql_tec_barragem = st.selectbox('Selecione a estrutura ' +
                                           'organizacional e qualificação ' +
                                           'técnica dos profissionais da ' +
                                           'equipe na barragem',
                                           ['Não se aplica a esse tipo de ' +
                                            'barragem',
                                            'Possui unidade administrativa ' +
                                            'com profissional técnico ' +
                                            'qualificado responsável pela ' +
                                            'segurança da barragem',
                                            'Possui profissional técnico ' + 
                                            'qualificado (próprio ou ' +
                                            'contratado) responsável pela ' +
                                            'segurança da barragem',
                                            'Não possui unidade ' +
                                            'administrativa e responsável ' +
                                            'técnico qualificado pela ' +
                                            'segurança da barragem'
                                           ])
    pro_ins_seg_mon_barragem = st.selectbox('Selecione o procedimento de ' +
                                            'inspeções de segurança e ' +
                                            'monitoramento da barragem',
                                            ['Não se aplica a esse tipo de ' +
                                             'barragem',
                                             'Possui manuais de procedimentos'+
                                             ' para inspeção, monitoramento e'+
                                             ' operação',
                                             'Possui apenas manual de ' +
                                             'procedimentos de inspeção',
                                             'Possui e não aplica manuais de' +
                                             ' procedimentos de inspeção e ' +
                                             'monitoramento',
                                             'Não possui manuais ou ' +
                                             'procedimentos formais para ' +
                                             'monitoramento e inspeções'
                                            ])
    rel_ins_seg_barragem = st.selectbox('Selecione o frequência de envio de ' +
                                        'relatórios de inspeção de segurança' +
                                        ' da barragem',
                                        ['Não se aplica a esse tipo ' +
                                         'de barragem',
                                         'Emite regularmente relatórios de ' + 
                                         'inspeção e monitoramento com base ' +
                                         'na instrumentação e de Análise de ' +
                                         'Segurança',
                                         'Emite os relatorios sem ' +
                                         'perioricidade',
                                         'Não emite regularmente relatórios ' +
                                         'de inspeção e monitoramento e de ' +
                                         'Análise de Segurança'
                                        ])
    volume_barragem = st.selectbox('Selecione o volume total do ' +
                                   'reservatório da barragem',
                                   ['Pequeno (<= 5 milhões m³)',
                                    'Médio (> 5 e <= 75 milhões m³)',
                                    'Grande (> 75 e <= 200 milhões m³)',
                                    'Muito Grande (> 200 milhões m³)'
                                   ])
    exs_pop_jus_barragem = st.selectbox('Selecione o potencial para a perda ' +
                                        'de vidas humanas a jusante da ' +
                                        'barragem',
                                        ['Inexistente (Não existem pessoas ' +
                                         'permanentes/residentes ou ' +
                                         'temporárias/transitando na área ' +
                                         'afetada a jusante da barragem)',
                                         'Pouco Frequente (Não existem ' +
                                         'pessoas ocupando permanentemente ' +
                                         'a área afetada a jusante da ' +
                                         'barragem, mas existe estrada ' +
                                         'vicinal de uso local)',
                                         'Frequente (Não existem pessoas ' +
                                         'ocupando permanentemente a área ' +
                                         'afetada a jusante da barragem, ' +
                                         'mas existe rodovia municipal ou ' +
                                         'estadual ou federal ou outro ' + 
                                         'local e/ou empreendimento de ' +
                                         'permanência eventual de pessoas ' +
                                         'que poderão ser atingidas)',
                                         'Existente (Existem pessoas ' + 
                                         'ocupando permanentemente a área ' + 
                                         'afetada a jusante da barragem, ' + 
                                         'portanto, vidas humanas poderão ' + 
                                         'ser atingidas)'
                                        ])
    impacto_ambiental_barragem = st.selectbox('Selecione o impacto ambiental' +
                                              ' a jusante da barragem',
                                              ['Significativo (Área afetada ' +
                                               'a jusante da barragem ' +
                                               'apresenta área de interesse ' +
                                               'ambiental relevante ou áreas' +
                                               ' protegidas em legislação ' +
                                               'específica (excluidas APPs))' +
                                               ' e armazena apenas resíduos ' +
                                               'Classe II B - Inertes, ' +
                                               'segundo a NBR 10004/2004 ' +
                                               'da ABNT)',
                                               'Muito Significativo ' +
                                               '(Barragem armazena rejeitos ' +
                                               'ou resíduos sólidos ' +
                                               'classificados na Classe II ' +
                                               'A - Não Inertes, segundo a ' +
                                               'NBR 10004/2004)'
                                              ])
    impacto_socio_economico_barragem = st.selectbox('Selecione o impacto ' +
                                                    'socioeconômico a ' +
                                                    'jusante da barragem',
                                                    ['Inexistente (Não ' +
                                                     'existem quaisquer ' + 
                                                    'instalações na área ' +
                                                    'afetada a jusante da ' +
                                                    'barragem)',
                                                    'BAIXO (Existe pequena ' +
                                                    'concentração de ' +
                                                    'instalações ' +
                                                    'residenciais, ' +
                                                    'agrícolas, industriais ' +
                                                    'ou de infraestrutura ' +
                                                    'de relevância sócio-eco' +
                                                    'nômico-cultural na ' +
                                                    'área afetada a jusante ' +
                                                    'da barragem)',
                                                    'ALTO (Existe alta ' +
                                                    'concentração de ' +
                                                    'instalações ' +
                                                    'residenciais, ' +
                                                    'agrícolas, industriais ' +
                                                    'ou de infraestrutura ' +
                                                    'de relevância sócio-eco' +
                                                    'nômico-cultural na ' +
                                                    'área afetada a jusante ' +
                                                    'da barragem)'
                                                    ])
    resultado_cri = ""
    resultado_dpa = ""
    
    if st.button('Previsão'):
        resultado_cri = previsao_barragem_cri(idade_barragem,
                                              altura_barragem,
                                              comprimento_barragem,
                                              material_barragem,
                                              fundacao_barragem,
                                              vazao_barragem,
                                              conf_est_ext_barragem,
                                              percolacao_barragem,
                                              deformacao_recalque_barragem,
                                              deterioracao_taludes_barragem,
                                              documentacao_projeto_barragem,
                                              est_org_ql_tec_barragem,
                                              pro_ins_seg_mon_barragem,
                                              rel_ins_seg_barragem)
        resultado_dpa = previsao_barragem_dpa(volume_barragem,
                                              exs_pop_jus_barragem,
                                              impacto_ambiental_barragem,
                                              impacto_socio_economico_barragem)
        if resultado_cri == 0:
            resultado_cri = 'não aplicável'
        elif resultado_cri == 1:
            resultado_cri = 'baixo'
        elif resultado_cri == 2:
            resultado_cri = 'médio'
        elif resultado_cri == 3:
            resultado_cri = 'alto'
        
        if resultado_dpa == 0:
            resultado_dpa = 'não aplicável'
        elif resultado_dpa == 1:
            resultado_dpa = 'baixo'
        elif resultado_dpa == 2:
            resultado_dpa = 'médio'
        elif resultado_dpa == 3:
            resultado_dpa = 'alto'
    
    st.success('A barragem de rejeito de minério tem a categoria de risco '
               'iminente classificado(a) como {}, enquanto o dano potencial '
               'associado é classificado(a) '
               'como {}.'.format(resultado_cri.upper(), resultado_dpa.upper()))
    
    
# Carregando os modelos para fazer a previsão dos dados
entrada_pickle_cri = open('classificador_ml_cri.pkl', 'rb')
classificador_cri = pickle.load(entrada_pickle_cri)

entrada_pickle_dpa = open('classificador_ml_dpa.pkl', 'rb')
classificador_dpa = pickle.load(entrada_pickle_dpa)

if __name__ == '__main__':
    main()