'''BCI - Brain Computer Interface'''



"""
Identificar três possíveis eventos em sinais gravados com o OpenBCI. Os eventos são os seguintes:
• Mordida ou aperto de mandíbula (jaw clench);
• Piscar dos olhos (blink);
• Ritmos alpha: onda evocada no estado de meditação, aumentando as frequências que vão de 8 à 13 Hz.
• E ritmos beta: onda evocada no estado de concentração, aumentando as frequências que vão de 13 à 32 Hz.
O arquivo "Gravação_EEG_OpenBCI-GUI.mp4" contém a explicação dos períodos em que são evocados os quatro eventos.
O arquivo "OpenBCI-RAW-2020-11-02_01-35-26.txt" contém os dados gravados pelo vídeo anterior, contendo os quatro eventos.
O arquivo "OpenBCI_GUI-v5-meditation.txt" contém dados gravados no OpenBCI de um longo período de meditação, evocando intensamente os ritmos alpha.
Vocês deverão entregar um código que indique o momento em que um evento inicia e termina, além de nomear o evento ocorrido.

"""

import mne
import matplotlib.pyplot as plt 
import numpy as np 

# read file
filepath = "/data-bci/OpenBCI-RAW-2020-11-02_01-35-26.txt"

def load_files(file):
	with open(file, 'r') as f:
		data = f.readlines()
	list_data = []
	for i in range(len(data)):
		if >= 8:
			list_data.append(data[i])
	return list_data


# filter alpha and beta

# filter blink and jaw

''' blink canais 1 e 2 frequências delta e theta'''

''' jaw frequências beta e gama '''

alpha = []
beta = []
delta = []
theta = []
gamma = []
outro1 = []
outro2 = []
outro3 = []
channels = ['01', '02', '03', '04', '05', '06', '07', '08']
count = 0
md_alpha = []
md_beta = []
md_gama = []
md_gama = []
md_delta = []
md_theta = []

''' passar nas linhas '''

def read_data(data):
	temp = []
	line = data.split(',')
	for i in range(len(line)):
		temp.append(float(line[i]))
	return temp

def check_data(data):
	index = []
	temp = []
	count = 0

	for i in range(len(data)):
		idx = data[i].split(',')[0]
        if int(idx) == 255 and count == 255:
            index.extend(temp)
            temp = []
            count = 0
        elif int(idx) == 255 and count < 255:
            temp = []
            count = 0
        else:
            temp.append(read_data(data[i]))
            count += 1
    
    return index

rawdata = load_files(filepath)
data = check_data(rawdata)
size = int(len(data)/256)

# reduzir ruídos

def filter_notch(amostra):
	output = deepcopy(amostra)
	output.notch_filter(np.arange(60, 121, 60), fir_design='firwin')
	output.filter(8., 50., fir_design='firwin')
	return output


resultado = filter_notch(data)

# filtro passa baixa

def filter_passabaixa(amostra):
	output = deepcopy(amostra)
	for i in range(0,9):
		output.filter(l_freq=8., h_freq=50)
	return output

# eh a media que eu quero?
'''
Em estatística, média é definida como o valor que demonstra a concentração dos dados de uma distribuição, como o ponto de equilíbrio das frequências em um histograma.
'''

def avg(data):
	soma = 0
	for i in range(0, len(data)):
        soma = data[i] ** 2
    res = soma/len(data)
    res = res ** 1/2
    return res

# media para cada tipo de frequência

def avg_freq():
    del md_alpha[0:-1]
    del md_beta[0:-1]
    del md_theta[0:-1]
    del md_gamma[0:-1]
    
    for i in range(0, 6):
        md_theta.append(avg(theta[i]))
        md_alpha.append(avg(alpha[i]))
        md_beta.append(avg(beta[i]))
        md_gamma.append(avg(gamma[i]))
        
def large_md(data):
    maior = -1
    pos = 0
    pos_aux = pos
    for i in range(0, len(data)):
        for element in data[i]:
            if element > maior:
                maior = element
                pos = pos_aux
            pos_aux += 1
        pos_aux = 0
    return pos-1

def plot_time_frequency(raw, i, f):
    del alpha[0:-1]
    del beta[0:-1]
    del theta[0:-1]
    del gamma[0:-1]
    
    newRaw = apply_bandpass(raw)
    
    psds, freqs = pw(newRaw, 5., 50., i, f)
    print("*******Dados após psd_welch*******\n")      
    for j in range(0, 6):
        theta.append(psds[j][0:3])
        alpha.append(psds[j][3:8])
        beta.append(psds[j][8:25])
        gamma.append(psds[j][20:46])
    avg_freq()


 # comparação de q? talvez tenha que fazer um desse para cada evento

'''
A função a seguir realiza a comparação dos valores dos ritmos. Quando tem-se em alpha o maior valor medido em um eletrodo, imprime-se um comparativo dos ritmos e seus valores(em Hz) colhidos nesse eletrodo.'''

def extract_large():
    del md_ritmos[0:-1]
    md_ritmos.append(md_alpha)
    md_ritmos.append(md_beta)
    md_ritmos.append(md_gamma)
    md_ritmos.append(md_theta)
    md_ritmos.append(md_delta)
    
    idx = large_md(md_ritmos)
    maior = max(md_alpha[idx], md_beta[idx], md_theta[idx], md_gamma[idx], md_delta[idx])
    global count
    if md_alpha[idx] == maior || md_beta[idx] == maior || md_theta[idx] == maior || md_gamma[idx] || md_delta[idx]: # if igual a beta, igual a theta, igual a gama ou igual a delta
        count += 1
        print("***Comparação do maior valor em eletrodo considerando todos o ritmo Alpha:***")
        print("Eletrodo: ", ch_names[idx])
        print("Alpha (8-12)Hz: ", md_alpha[idx])
        print("Beta (12-30)Hz: ", md_beta[idx])
        print("Gamma (25-50)Hz: ", md_gamma[idx])
        print("Theta (4-7)Hz: ", md_theta[idx])
        print("*************\n")
        values = [md_alpha[idx], md_beta[idx], md_gamma[idx], md_theta[idx]]
        names = ['alpha', 'beta', 'gamma', 'theta', 'delta']
        plt.bar(names, values, color=['pink', 'blue', 'purple', 'gray', 'yellow'])
        plt.show()
        print("*************\n")
        print("***Mapeando para escala de 0 à 100: ***")
        segundo_maior = max(md_beta[idx], md_theta[idx], md_gamma[idx]) # coloca todo mundo menos o analisado
        terceiro_maior = max(md_alpha[idx], md_theta[idx], md_gamma[idx])
        quarto_maior = max(md_alpha[idx], md_beta[idx], md_gamma[idx])
        quinto_maior = max(md_alpha[idx], md_beta[idx], md_theta[idx])
        sexto_maior = max(md_alpha[idx], md_beta[idx], md_theta[idx], md_gamma[idx])
        diferenca = md_alpha[idx] - segundo_maior # compara com o analisado
        diferenca_beta = md_beta[idx] - terceiro_maior
        diferenca_theta = md_theta[idx] - quarto_maior
        diferenca_gamma = md_gamma[idx] - quinto_maior
        diferenca_delta = md_delta[idx] - sexto_maior
        escala = (100*diferenca)/md_alpha[idx] # faz a escala com o analisado
        escala_beta =
        escala_theta =
        escala_gamma =
        escala_delta =
        print("Média de alpha: ", md_alpha[idx])
        print("Segunda maior média: ", segundo_maior)
        print("Valor na escala: ", escala)

 # nas proximas muda o valor de alpha para a frequencia procurada e o segundo maior com
 # as que não estão sendo utilizadas

# bufferização

for i in range(1, 4):
    plot_time_frequency(raw, 0, i)
    extract_large()

for i in range(0, size):#size
    plot_time_frequency(raw, i, i+4)
    extract_large()

print("Qtd de vezes que alpha é maior: ", count)
print ("piscada")
print ("mordida")
print ("beta")











