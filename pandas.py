import pandas as pd
import numpy as np
import os

pd.set_option('display.max_colums', 10)

endereco_programa = os.path.join( os.path.abspath('.'), 'src')
endereco_programa = os.path.dirname( os.path.abspath(__file__) )

endereco_projeto = os.path.dirname( endereco_programa )
endereco_dados = os.path.join( endereco_projeto, 'data' )

filepath_csv = os.path.join(endereco_dados, 'tb_candidatura_2018.csv')
df_candidatura = pd.read_csv(filepath_csv, sep=";")

df_candidatura.head()

#objetivo da live filtrar deputados por características

remove_columns = ['declara_bens']

keep_columns = list(set(df_candidatura.columns) - set(remove_columns))

df_dp_estadual = df_candidatura(df_candidatura['descricao_cargo'] == 'DEPUTADO ESTADUAL') &
(df_candidatura['descricao_situacao_candidatura'] == 'APTO')[keep_columns]

df_dp_estadual.shape[0] / df_candidatura[df_candidatura['descricao_cargo'] == 'DEPUTADO ESTADUAL'].shape(0)

df_dp_estadual.shape #base
df_dp_estadual['cpf'].nunique() #equivalente ao distinct

# isso é um dataframe multiindex
agrupa_estado_genero = df_dp_estadual.groupby('sigla_uf').[['cpf']].nunique # campos métricas . função

#desempilha os valores
df_estado_genero = agrupa_estado_genero.unstack()

# remove multiindex
df_estado_genero.columns = df_estado_genero.columms.droplevel()

df_estado_genero = df_estado_genero.reset_index()

#importando pratrimônio dos c**     

filepath_xlsx = os.path.join('endereco_dados', 'nomedoarquivo.xlsx')
df_patrimonio = pd.read_excel(filepath_xlsx)
df_patrimonio_candidato = (df_patrimonio.groupby(['numero_sequencial'])[['valor']].sum().reset_index())

