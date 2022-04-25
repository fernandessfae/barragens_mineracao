from pre_processamento_dpa import pre_processamento_dpa
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from yellowbrick.classifier import ConfusionMatrix

# Carregamento dos dados e separaçao entre os atributos e a classe
dados_dpa = pre_processamento_dpa('barragens.csv')
previsores = dados_dpa.iloc[:, 1:6].values
classe = dados_dpa.iloc[:, 0].values

# Holdout (Train_test_split)
previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = \
    train_test_split(previsores, classe, test_size=0.3, random_state=0)

classificador = SVC()
classificador.fit(previsores_treinamento, classe_treinamento)
previsoes = classificador.predict(previsores_teste)

precisao_modelo: float = round(accuracy_score(classe_teste, previsoes), 2)
matriz_confusao = confusion_matrix(classe_teste, previsoes)

#print(classificador.classes_)
#print(classificador.class_count_)
#print(classificador.class_prior_)

# Geração da matriz de confusão e métricas de classificação do modelo (Holdout)
mc_holdout = ConfusionMatrix(classificador,
                            encoder={0: 'Não se aplica', 1: 'Baixo',
                                     2: 'Médio', 3: 'Alto'})
mc_holdout.fit(previsores_treinamento, classe_treinamento)
mc_holdout.score(previsores_teste, classe_teste)
mc_holdout.show();

print(classification_report(classe_teste,
                            previsoes,
                            target_names=['Não se aplica', 'Baixa',
                                          'Média', 'Alta']))
