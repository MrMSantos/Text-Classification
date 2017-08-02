#LN 16/17 Projecto2
#78403 Luis Neto
#78445 Manuel Santos

import os
import glob
from decimal import Decimal

pontuation = ['.', ':', ',', ';', '!', '?', '(', ')', '[', ']', '*', '/', '«', '»', '<', '>', '“', '”', '_', '-', '\'', '\"']
final_pont = ['.', '!', '?', '...']
endofline =	['\n', '\r']
affix = '_norm.txt'
autores = ['AlmadaNegreiros', 'CamiloCasteloBranco', 'EcaDeQueiros', 'JoseRodriguesSantos', 'JoseSaramago', 'LuisaMarquesSilva']
testes = ['500Palavras', '1000Palavras']
ngramas_autores = {'AlmadaNegreiros': {}, 'CamiloCasteloBranco': {}, 'EcaDeQueiros': {}, 'JoseRodriguesSantos': {}, 'JoseSaramago': {}, 'LuisaMarquesSilva': {}}

def normalization(filename):
	name = filename[:-4]
	with open(name + affix, 'w') as f2:
		with open(filename, 'r') as f1:
			for line in f1:
				char=0
				while char<len(line)-1:
					if line[char] in pontuation  and line[char+1]==line[char] and  line[char+2]==line[char]:
						f2.write(line[char]+line[char+1]+line[char+2]+' ')
						char=char+3

					elif line[char] in pontuation  and line[char+1]==line[char]:
						f2.write(line[char]+line[char+1]+' ')
						char=char+2
					
					elif line[char]!=' ' and line[char] not in pontuation and line[char+1] in pontuation and line[char+2]!=' ' and line[char+2] not in pontuation and line[char+2] not in endofline:
						f2.write(line[char]+line[char+1])
						char=char+2
					elif (line[char]!=' ' and line[char+1] in pontuation) or (line[char+1]!=' ' and line[char+1] not in endofline and line[char] in pontuation):
						f2.write(line[char]+' ')
						char=char+1
					else:
						f2.write(line[char])
						char=char+1
				f2.write(line[len(line)-1])
	os.remove(filename)

#Criação de unigrama num dicionário
def unigrams():
	unigramas = {}
	for filename in glob.glob('*.txt'):
		with open(filename, 'r') as f1:
			for line in f1:
				vec_line = line.split()
				for word in vec_line:
					if word in unigramas:
						unigramas[word] = unigramas[word] + 1
					else:
						unigramas[word] = 1
	return unigramas

#Criação de bigrama num dicionário
def bigrams():
	bigramas = {}
	i = 0
	for filename in glob.glob('*.txt'):
		with open(filename, 'r') as f1:
			for line in f1:
				vec_line = line.split()
				while(i < len(vec_line) - 2):
					if vec_line[i] in bigramas:
						if vec_line[i + 1] in bigramas[vec_line[i]]:
							bigramas[vec_line[i]][vec_line[i + 1]] = bigramas[vec_line[i]][vec_line[i + 1]] + 1
						else:
							bigramas[vec_line[i]][vec_line[i + 1]] = 1
					else:
						bigramas[vec_line[i]] = {}
						bigramas[vec_line[i]][vec_line[i + 1]] = 1
					i = i + 1
				i = 0
	return bigramas

def laplace(texto, unigram, bigram):
	i = 0
	result = 1.0
	C = len(unigram)
	with open(texto, 'r') as f1:
		for line in f1:
			vec_line = line.split()
			while(i < len(vec_line) - 2):
				if vec_line[i] in bigram and vec_line[i + 1] in bigram[vec_line[i]]:
					count1 = bigram[vec_line[i]][vec_line[i + 1]]
				else:
					count1 = 0
				if vec_line[i] in unigram:
					count2 = unigram[vec_line[i]]
				else:
					count2 = 0
				result_aux = (float(count1 + 1.0) / float(count2 + C))
				result = Decimal(result) * Decimal(result_aux)
				i = i + 1
				count1 = 0
				count2 = 0
				result_aux = 0
			i = 0
	return result

def pontuacao_texto(texto):
	n_pontFinal = 0
	total_palavras = 0
	with open(texto, 'r') as f1:
		for line in f1:
			vec_line = line.split()
			for word in vec_line:
				if word in final_pont:
					n_pontFinal += 1
				total_palavras += 1
	return Decimal(total_palavras/n_pontFinal)

def palavras_ngrama(ngrama):
	result = 0
	for word in ngrama:
		result += ngrama[word]
	return result

def pontuacao_ngrama(ngrama):
	result = 0
	for word in ngrama:
		if word in final_pont:
			result += ngrama[word]
	return result

def distance_unigram(lista, texto):
	pont = 0
	i = 0
	with open(texto, 'r') as f1:
		for line in f1:
			vec_line = line.split()
			for word in vec_line:
				while(word != lista[i]):
					if i == 500:
						break;
					i += 1
				pont += i
				i = 0
	return pont

def calcula_maior(dicionario):
	return max(dicionario, key = dicionario.get)

def calcula_menor(dicionario):
	return min(dicionario, key = dicionario.get)

#Altera path para a pasta treino
home = os.getcwd()
dir_treino = home + '/treino'
os.chdir(dir_treino)

#Ciclo que normaliza e calcula unigramas e bigramas de cada autor
for nome_autor in autores:
	autores_path = dir_treino + '/' + nome_autor
	os.chdir(autores_path)
	for filename in glob.glob('*.txt'):
		normalization(filename)

	unigrama_final = unigrams()
	bigrama_final = bigrams()

	with open('unigramas.txt', 'w') as f1:
		for valor in unigrama_final:
			f1.write(valor + ' ' + str(unigrama_final[valor]) + "\n")

	with open('bigramas.txt', 'w') as f1:
		for unigrama in bigrama_final:
			for valor in bigrama_final[unigrama]:
				f1.write(unigrama + ' ' + valor + ' ' + str(bigrama_final[unigrama][valor]) + "\n")

	with open('unigramas_alisamento.txt', 'w') as f1:
		for valor in unigrama_final:
			f1.write(valor + ' ' + str(unigrama_final[valor] + 1) + "\n")

	with open('bigramas_alisamento.txt', 'w') as f1:
		for unigrama in bigrama_final:
			for valor in bigrama_final[unigrama]:
				f1.write(unigrama + ' ' + valor + ' ' + str(bigrama_final[unigrama][valor] + 1) + "\n")


	ngramas_autores[nome_autor] = {}
	ngramas_autores[nome_autor]['unigrama'] = unigrama_final
	ngramas_autores[nome_autor]['bigrama'] = bigrama_final

print('-- Textos de treino normalizados --\n')
print('-- Unigramas e bigramas calculados --\n')

#Altera path para a pasta teste
dir_teste = home + '/teste'
os.chdir(dir_teste)

#Ciclo que normaliza os textos de teste
for tipo_teste in testes:
	teste_path = dir_teste + '/' + tipo_teste
	os.chdir(teste_path)
	for filename in glob.glob('*.txt'):
			normalization(filename)

print('-- Textos de teste normalizados --\n')

print('-- Teste Laplace com Bigramas -- \n')

#Aplicaçao do teste com alisamento laplace para unigramas e bigramas
result_Laplace = {}

for tipo_teste in testes:

	print(tipo_teste)
	teste_path = dir_teste + '/' + tipo_teste
	os.chdir(teste_path)
	for filename in glob.glob('*.txt'):

		print(filename)
		for autor in ngramas_autores:

			result = laplace(filename, ngramas_autores[autor]['unigrama'], ngramas_autores[autor]['bigrama'])
			result_Laplace[autor] = result
			print(autor + ' ' + str(result))

		print('Texto atribuido a ' + calcula_maior(result_Laplace) + '\n')

print('-- Teste do numero de palavras por frase --\n')

#Aplicaçao do teste que calcula numero de palavras por frase
result_texto = {}

for tipo_teste in testes:

	print(tipo_teste)
	teste_path = dir_teste + '/' + tipo_teste
	os.chdir(teste_path)

	for filename in glob.glob('*.txt'):

		print(filename)
		n_pontTeste = Decimal(pontuacao_texto(filename))
		for autor in ngramas_autores:

			palavras_total = palavras_ngrama(ngramas_autores[autor]['unigrama'])
			n_pontAutor = pontuacao_ngrama(ngramas_autores[autor]['unigrama'])
			ratio_autor = (float(palavras_total) / float(n_pontAutor))
			result = Decimal(ratio_autor) - Decimal(n_pontTeste)
			result_texto[autor] = abs(result)
			print(autor + ' ' + str(abs(result)))

		print('Texto atribuido a ' + calcula_menor(result_texto) + '\n')

print('-- Teste da pontucação de unigramas --\n')

#Aplicaçao do teste que atribui pontuaçao de acordo com a frequencia de unigramas
result2_texto = {}
lista_ordenada = []

for tipo_teste in testes:

	print(tipo_teste)
	teste_path = dir_teste + '/' + tipo_teste
	os.chdir(teste_path)

	for filename in glob.glob('*.txt'):

		print(filename)
		for autor in ngramas_autores:

			lista_ordenada = sorted(ngramas_autores[autor]['unigrama'], key=ngramas_autores[autor]['unigrama'].__getitem__, reverse=True)
			distance_pont = distance_unigram(lista_ordenada, filename)
			result2_texto[autor] = distance_pont
			print(autor + ' ' + str(distance_pont))

		print('Texto atribuido a ' + calcula_menor(result2_texto) + '\n')
	print()