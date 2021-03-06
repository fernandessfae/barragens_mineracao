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
    st.title("Previs??o da classifica????o da barragem de minera????o")
    
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
    material_barragem = st.selectbox('Escolha o material de constru????o da ' +
                                     'barragem',
                                     ['Concreto convencional', 'Terra'])
    fundacao_barragem = st.selectbox('Selecione o tipo de funda????o da barragem',
                                     ['Rocha s??',
                                      'Rocha alterada/Saprolito',
                                      'Solo residual/Aluvi??o',
                                      'Aluvi??o arenoso espesso/Solo org??nico/'+
                                      'Rejeito/Desconhecido'
                                     ])
    vazao_barragem = st.selectbox('Escolha o tipo de vaz??o da barragem',
                                  ['CMP (Cheia M??xima Prov??vel) ' +
                                   'ou Decamilenar',
                                   'Milenar',
                                   'TR = 500 anos',
                                   'TR inferior a 500 anos ou Desconhecida/' + 
                                   'Estudo n??o confi??vel'
                                  ])
    conf_est_ext_barragem = st.selectbox('Selecione o tipo da confiabilidade '
                                         'da estrutura extravasora',
                                        ['N??o se aplica a esse tipo ' +
                                         'de barragem',
                                         'Estruturas civis bem mantidas e '
                                         'em opera????o normal/barragem sem ' +
                                         'necessidade de estruturas ' +
                                         'extravasoras',
                                         'Estruturas com problemas ' +
                                         'identificados e medidas ' +
                                         'corretivas em implanta????o',
                                         'Estruturas com problemas ' +
                                         'identificados e sem ' +
                                         'implanta????o das medidas ' +
                                         'corretivas necess??rias'
                                        ])
    percolacao_barragem = st.selectbox('Selecione a percola????o da barragem',
                                       ['N??o se aplica a esse tipo ' +
                                        'de barragem',
                                        'Percola????o totalmente controlada ' +
                                        'pelo sistema de drenagem',
                                        'Umidade ou surg??ncia nas ??reas de ' +
                                        'jusante, paramentos, taludes e ' +
                                        'ombreiras est??veis e monitorados',
                                        'Umidade ou surg??ncia nas ??reas de ' +
                                        'jusante, paramentos, taludes ou ' +
                                        'ombreiras sem implanta????o das ' +
                                        'medidas corretivas necess??rias',
                                        'Surg??ncia nas ??reas de jusante com ' +
                                        'carreamento de material ou com ' +
                                        'vaz??o crescente ou infiltra????o do ' +
                                        'material contido, com potencial de ' +
                                        'comprometimento da seguran??a ' +
                                        'da estrutura'
                                       ])
    deformacao_recalque_barragem = st.selectbox('Selecione a deforma????o e ' +
                                                'recalque da barragem',
                                                ['N??o existem deforma????es e ' +
                                                 'recalques com potencial ' +
                                                 'de comprometimento da ' +
                                                 'seguran??a da estrutura',
                                                 'Exist??ncia de trincas e ' +
                                                 'abatimentos com medidas ' +
                                                 'corretivas em implanta????o',
                                                 'Exist??ncia de trincas e ' +
                                                 'abatimentos sem ' +
                                                 'implanta????o das medidas ' +
                                                 'corretivas necess??rias',
                                                 'Exist??ncia de trincas, ' +
                                                 'abatimentos ou ' +
                                                 'escorregamentos, com ' +
                                                 'potencial de ' +
                                                 'comprometimento da ' +
                                                 'seguran??a da estrutura'
                                                ])
    deterioracao_taludes_barragem = st.selectbox('Selecione a deteriora????o ' +
                                                 'do talude na barragem',
                                                 ['N??o se aplica a esse tipo' +
                                                  ' de barragem',
                                                  'N??o existe deteriora????o ' +
                                                  'de taludes e paramentos',
                                                  'Falhas na prote????o dos ' +
                                                  'taludes e paramentos, ' +
                                                  'presen??a de vegeta????o ' +
                                                  'arbustiva',
                                                  'Eros??es superficiais, ' +
                                                  'ferragem exposta, ' +
                                                  'presen??a de vegeta????o ' +
                                                  'arb??rea, sem implanta????o ' +
                                                  'das medidas corretivas ' +
                                                  'necess??rias',
                                                  'Depress??es acentuadas ' +
                                                  'nos taludes, ' +
                                                  'escorregamentos, sulcos ' +
                                                  'profundos de eros??o, com ' +
                                                  'potencial de ' +
                                                  'comprometimento da ' +
                                                  'seguran??a da estrutura'
                                                 ])
    documentacao_projeto_barragem = st.selectbox('Selecione a documenta????o ' +
                                                 'da barragem',
                                                 ['N??o se aplica a esse ' +
                                                  'tipo de barragem',
                                                  'Projeto executivo e ' +
                                                  '"como constru??do"',
                                                  'Projeto executivo ou ' +
                                                  '"como constru??do"',
                                                  'Projeto b??sico',
                                                  'Projeto conceitual',
                                                  'N??o h?? documenta????o ' +
                                                  'de projeto'
                                                 ])
    est_org_ql_tec_barragem = st.selectbox('Selecione a estrutura ' +
                                           'organizacional e qualifica????o ' +
                                           't??cnica dos profissionais da ' +
                                           'equipe na barragem',
                                           ['N??o se aplica a esse tipo de ' +
                                            'barragem',
                                            'Possui unidade administrativa ' +
                                            'com profissional t??cnico ' +
                                            'qualificado respons??vel pela ' +
                                            'seguran??a da barragem',
                                            'Possui profissional t??cnico ' + 
                                            'qualificado (pr??prio ou ' +
                                            'contratado) respons??vel pela ' +
                                            'seguran??a da barragem',
                                            'N??o possui unidade ' +
                                            'administrativa e respons??vel ' +
                                            't??cnico qualificado pela ' +
                                            'seguran??a da barragem'
                                           ])
    pro_ins_seg_mon_barragem = st.selectbox('Selecione o procedimento de ' +
                                            'inspe????es de seguran??a e ' +
                                            'monitoramento da barragem',
                                            ['N??o se aplica a esse tipo de ' +
                                             'barragem',
                                             'Possui manuais de procedimentos'+
                                             ' para inspe????o, monitoramento e'+
                                             ' opera????o',
                                             'Possui apenas manual de ' +
                                             'procedimentos de inspe????o',
                                             'Possui e n??o aplica manuais de' +
                                             ' procedimentos de inspe????o e ' +
                                             'monitoramento',
                                             'N??o possui manuais ou ' +
                                             'procedimentos formais para ' +
                                             'monitoramento e inspe????es'
                                            ])
    rel_ins_seg_barragem = st.selectbox('Selecione o frequ??ncia de envio de ' +
                                        'relat??rios de inspe????o de seguran??a' +
                                        ' da barragem',
                                        ['N??o se aplica a esse tipo ' +
                                         'de barragem',
                                         'Emite regularmente relat??rios de ' + 
                                         'inspe????o e monitoramento com base ' +
                                         'na instrumenta????o e de An??lise de ' +
                                         'Seguran??a',
                                         'Emite os relatorios sem ' +
                                         'perioricidade',
                                         'N??o emite regularmente relat??rios ' +
                                         'de inspe????o e monitoramento e de ' +
                                         'An??lise de Seguran??a'
                                        ])
    volume_barragem = st.selectbox('Selecione o volume total do ' +
                                   'reservat??rio da barragem',
                                   ['Pequeno (<= 5 milh??es m??)',
                                    'M??dio (> 5 e <= 75 milh??es m??)',
                                    'Grande (> 75 e <= 200 milh??es m??)',
                                    'Muito Grande (> 200 milh??es m??)'
                                   ])
    exs_pop_jus_barragem = st.selectbox('Selecione o potencial para a perda ' +
                                        'de vidas humanas a jusante da ' +
                                        'barragem',
                                        ['Inexistente (N??o existem pessoas ' +
                                         'permanentes/residentes ou ' +
                                         'tempor??rias/transitando na ??rea ' +
                                         'afetada a jusante da barragem)',
                                         'Pouco Frequente (N??o existem ' +
                                         'pessoas ocupando permanentemente ' +
                                         'a ??rea afetada a jusante da ' +
                                         'barragem, mas existe estrada ' +
                                         'vicinal de uso local)',
                                         'Frequente (N??o existem pessoas ' +
                                         'ocupando permanentemente a ??rea ' +
                                         'afetada a jusante da barragem, ' +
                                         'mas existe rodovia municipal ou ' +
                                         'estadual ou federal ou outro ' + 
                                         'local e/ou empreendimento de ' +
                                         'perman??ncia eventual de pessoas ' +
                                         'que poder??o ser atingidas)',
                                         'Existente (Existem pessoas ' + 
                                         'ocupando permanentemente a ??rea ' + 
                                         'afetada a jusante da barragem, ' + 
                                         'portanto, vidas humanas poder??o ' + 
                                         'ser atingidas)'
                                        ])
    impacto_ambiental_barragem = st.selectbox('Selecione o impacto ambiental' +
                                              ' a jusante da barragem',
                                              ['Significativo (??rea afetada ' +
                                               'a jusante da barragem ' +
                                               'apresenta ??rea de interesse ' +
                                               'ambiental relevante ou ??reas' +
                                               ' protegidas em legisla????o ' +
                                               'espec??fica (excluidas APPs))' +
                                               ' e armazena apenas res??duos ' +
                                               'Classe II B - Inertes, ' +
                                               'segundo a NBR 10004/2004 ' +
                                               'da ABNT)',
                                               'Muito Significativo ' +
                                               '(Barragem armazena rejeitos ' +
                                               'ou res??duos s??lidos ' +
                                               'classificados na Classe II ' +
                                               'A - N??o Inertes, segundo a ' +
                                               'NBR 10004/2004)'
                                              ])
    impacto_socio_economico_barragem = st.selectbox('Selecione o impacto ' +
                                                    'socioecon??mico a ' +
                                                    'jusante da barragem',
                                                    ['Inexistente (N??o ' +
                                                     'existem quaisquer ' + 
                                                    'instala????es na ??rea ' +
                                                    'afetada a jusante da ' +
                                                    'barragem)',
                                                    'BAIXO (Existe pequena ' +
                                                    'concentra????o de ' +
                                                    'instala????es ' +
                                                    'residenciais, ' +
                                                    'agr??colas, industriais ' +
                                                    'ou de infraestrutura ' +
                                                    'de relev??ncia s??cio-eco' +
                                                    'n??mico-cultural na ' +
                                                    '??rea afetada a jusante ' +
                                                    'da barragem)',
                                                    'ALTO (Existe alta ' +
                                                    'concentra????o de ' +
                                                    'instala????es ' +
                                                    'residenciais, ' +
                                                    'agr??colas, industriais ' +
                                                    'ou de infraestrutura ' +
                                                    'de relev??ncia s??cio-eco' +
                                                    'n??mico-cultural na ' +
                                                    '??rea afetada a jusante ' +
                                                    'da barragem)'
                                                    ])
    resultado_cri = ""
    resultado_dpa = ""
    
    if st.button('Previs??o'):
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
            resultado_cri = 'n??o aplic??vel'
        elif resultado_cri == 1:
            resultado_cri = 'baixo'
        elif resultado_cri == 2:
            resultado_cri = 'm??dio'
        elif resultado_cri == 3:
            resultado_cri = 'alto'
        
        if resultado_dpa == 0:
            resultado_dpa = 'n??o aplic??vel'
        elif resultado_dpa == 1:
            resultado_dpa = 'baixo'
        elif resultado_dpa == 2:
            resultado_dpa = 'm??dio'
        elif resultado_dpa == 3:
            resultado_dpa = 'alto'
    
    st.success('A barragem de rejeito de min??rio tem a categoria de risco '
               'iminente classificado(a) como {}, enquanto o dano potencial '
               'associado ?? classificado(a) '
               'como {}.'.format(resultado_cri.upper(), resultado_dpa.upper()))
    
    
# Carregando os modelos para fazer a previs??o dos dados
entrada_pickle_cri = open('classificador_ml_cri.pkl', 'rb')
classificador_cri = pickle.load(entrada_pickle_cri)

entrada_pickle_dpa = open('classificador_ml_dpa.pkl', 'rb')
classificador_dpa = pickle.load(entrada_pickle_dpa)

if __name__ == '__main__':
    main()