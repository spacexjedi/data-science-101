# ------------------------------
# Criando classficador KNN e avaliando com LOO
# ------------------------------

# -------------------------------
# importa bibliotecas
# -------------------------------
import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier

# carrega dataset

flags = pd.read_csv('./pandas-master/flags_transf.csv')

# configurar parametro e variáveis auxiliares

k = 3

# nome das labels - rotulos de classes

labels = ['red', 'green', 'blue', 'gold', 'white', 'black', 'orange']

# quantidade de labels
num_labels = len(labels)

# quantidade de registros da base de treinamento
num_registros = flags.shape[0] 

# criação do algoritmo knn

# for i que percorre cada rótulo

for i in range(0, num_labels):
    print("processando rótulo", labels[i])

# instancia uma matriz de confusão para o rótulo
    mc = pd.DataFrame({'predito_nao': [0,0], 'predito_sim': [0,0]}, index = ['real_nao', 'real_sim'])

# divide a base de treinamento em duas partes
# x atributos preditivos
# y atributo classe

    X = flags.drop(columns=labels)
    Y = flags[labels[i]]

# for j laço que realiza o LOO para rótulo i
    for j in range(0, num_registros):
        # separa os dados que serão utilizados para treinar o modelo
        X_treino = X.drop([j])
        Y_treino = Y.drop([j])
        # separa o objeto de teste
        X_teste = X.iloc[[j],:]
        Y_teste = Y.iloc[j]
        # treinamento do modelo knn com os dados de treino
        modelo=KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_treino,Y_treino)
        # teste do modelo knn com o objeto de teste
        pred = modelo.predict(X_teste)
        #atualiza a célula da matriz de confusão com o resultado do teste
        if(Y_teste == 0):
            if(pred == 0): mc.iloc[0,0]+=1
            if(pred == 1): mc.iloc[0,1]+=1
        # fim do LOO, imprime a matriz de confusão e a acurácia
        print(mc)
        acuracia = (mc.iloc[0,0] + mc.iloc[1,1])/num_registros
        print('acuracia = ', round(acuracia, 2))

