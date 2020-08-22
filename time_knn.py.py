# Realização dos imports das bibliotecas
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.model_selection import train_test_split
import sys
import time
import os.path


inicio_cpu = time.clock()
inicio_real = time.time()

def class_histogram(kn_neighbors, n_classes):
    '''Faz a contagem das classes dos k vizinhos mais próximos.
    Recebe o vetor com os k mais próximos.'''
    countx = 0
    # Cria um vetor c zerado com n_classes posições
    c = [0] * n_classes
    
    # Para cada vizinho entre os k mais próximos
    for i in kn_neighbors:
        # incrementar contagem
        c[i] += 1
        countx += 1
    # retorna contagem das classes dos k vizinhos mais próximos
    print('countx:', countx)
    return c

def knn(X_train, Y_train, x, k):
    '''Faz a classificação do exemplo x baseado nos k mais próximos em X_train.'''
    
    # Calcula o vetor de distâncias entre x e todos os pontos em X_train
    d = euclidean_distances(x.reshape(1, -1), X_train).reshape(-1)
    
    # Ordena o vetor d e retorna os índices da ordenação em relação ao vetor d original. Não mexe no vetor d.
    # Isto ajuda porque é necessário indexar Y_train das posições correspondentes depois da ordenação!
    idx = np.argsort(d)
    # Calcula a contagem das classes dos k vizinhos mais próximos:
    # Y_train[idx][:k] <-- obtém os rótulos dos k vizinhos mais próximos!
    hist = class_histogram(Y_train[idx][:k], len(set(Y_train)))
    # hist apenas é um vetor [c0, c1, c2, ..., c_nclasses] de forma que c0 é a quantidade de vizinhos mais
    # próximos que são da classe 0, c1 é a quantidade de vizinhos mais proximos que são da classe 1, e 
    # assim por diante.
    
    # O knn classifica x como sendo da classe com a maior quantidade de vizinhos mais próximos. Assim,
    # basta retornar a posição da classe que tem a maior quantidade de vizinhos mais próximos.
    #    ex: se np.argmax(hist) == 0, a classe 0 tem a maioria dos vizinhos mais próximos de x.
    return np.argmax(hist)

    # Carrega um dataset ``digits'' do sklearn. Esse dataset é composto de 1797 imagens de dígitos manuscritos 
# 8x8 em 16 tons de cinza. Há 64 características por imagem, uma para o valor de cada pixel.
X, Y = load_digits(return_X_y=True)

# Vamos dividir o dataset com 70% no treino e 30% no teste. X_train é o conjunto de treino com os exemplos
# e Y_train são os gabaritos de cada exemplo de X_train. X_test é o conjunto de treino com os exemplos e 
# Y_test são os gabaritos de cada exemplo de X_test se shuffle=True, "embaralha" o dataset antes de fazer
# a separação.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)

misses, hits = 0, 0
k = 3
county = 0
countz = 0
# Para cada exemplo no conjunto de teste
for i, x in enumerate(X_test):
    # Classificar o exemplo. Se o exemplo estiver correto (for igual do gabarito)
    county+=1
    if knn(X_train, Y_train, x, k) == Y_test[i]:
        hits += 1
        countz+=1
    else:
        misses += 1

# A acurácia é dada por acertos / (acertos + erros).
print ("Acurácia: %.02f%%" % (hits / float(hits + misses) * 100))

fim_cpu = time.clock()
fim_real = time.time()

tempo_real = fim_real - inicio_real

tempo_cpu = fim_cpu - inicio_cpu

print ('Tempo de CPU:', tempo_cpu)

print ('Tempo Real:', tempo_real)


print('county:', county)
print('countz:', countz)
