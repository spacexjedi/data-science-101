import pandas as pd 

#cria o dataframe

dados = {'nome': ['Argentina','Brasil','França','Itália','Reino Unido'],'continente': ['América','América','Europa','Europa','Europa'],'extensao': [2780,8511,644,301,244],'corVerde': [0,1,0,1,0]}
siglas = ['AR', 'BR', 'FR', 'IT', 'UK']
paises = pd.DataFrame(dados, index=siglas)

print(paises)
# lista rotulo das linhas
idx = paises.index
print(idx)
# lista rotulo das colunas
col = paises.columns
print(col)

num_linhas = paises.shape[0]
num_colunas = paises.shape[1]
paises_tipo = type(paises)
paises_dtypes = paises.dtypes
paises_idx_dtype = paises.index.dtype

print('número de linhas: ', num_linhas)
print('número de colunas: ', num_colunas)
print('tipo (type): ',paises_tipo)
print('dtypes das colunas:\n', paises_dtypes)
print('dtype dos rótulos das linhas:', paises_idx_dtype)
