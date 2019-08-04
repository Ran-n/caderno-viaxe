#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	03/08/2019 13:12:40
#------------------------------------------------------------------------------------------------
import utils as u
from khronos import khronos as kh
from base36 import base36 as b36
# ------
import json
from functools import partial
import gettext
from pathlib import Path
from unidecode import unidecode
import os
#------------------------------------------------------------------------------------------------
# función principal que engade un contido co seu código ao ficheiro e índice
def engadir(nome = None):
	existe = False
	media = {'nome': None,
			'tipo': None}

	print('\n-----------------------')
	print(_('*> Engadindo:'))
	print('-----------------------')
	# se xa nos dan o nome non fai falla sacar o de que nos diga o nome
	# un exemplo sería en valorar, que o nome
	if nome is None:
		nome = input(_(' > Nome: '))
	else:
		print(_(' > Nome: '), nome)

	# miramos se o que queremos meter xa existe sabendo que so pode haber un nome
	for ele in __indice.values():
		if ele['nome'].lower() == nome.lower():
			existe = True
			break

	if existe:
		print(_('*> Xa existe compi'))
	else:
		media['nome'] = nome
		# para ver que pon un tipo que exista
		while True:
			tipo = input(_(' > Tipo (1 serie, 2 peli, 3 docu, 4 video, 5 libro, 6 música, 7 artido): '))

			# segundo o tipo poñemos o seu código
			if tipo == '1':
				media['tipo'] = __codes['serie']
				u.crear_carp(__carpetas['serie']+nome)
				break
			elif tipo == '2':
				media['tipo'] = __codes['peli']
				break
			elif tipo == '3':
				media['tipo'] = __codes['docu']
				break
			elif tipo == '4':
				media['tipo'] = __codes['video']
				break
			elif tipo == '5':
				media['tipo'] = __codes['libro']
				break
			elif tipo == '6':
				media['tipo'] = __codes['musica']
				break
			elif tipo == '5':
				media['artigo'] = __codes['artigo']
				break
			else:
				media['tipo'] = 'imposible'

		# engadimos o contido audiovisual á colección xeral
		#FALTA: Mirar que a chave que se lle pon non exista xa se se eliminou
		# en lugar de poñer un simple número usaremos o tempo no que foi creado en base32
		__indice[b36.code(kh.getAgora())] = media

	print('-----------------------')

	# devolvemos estes valores engadidos se é que se queren
	return media['nome'], media['tipo']
#------------------------------------------------------------------------------------------------
# función auxiliar que se encarga de coller e retornar os valores a meter no ficheiro de valoración
def valoracion(tipo, xenero_base):
	datos = {'resumo': None,
			'opinions': None,
			'nota': None,
			'autor': None,
			'editorial': None,
			'data_saida': None,
			'lonxitude': None,
			'xenero': None,
			'idioma': None,
			'data_ini': None,
			'data_fin': None,
			'notas_extra': None}

	# resumo
	datos['resumo'] = input(_('\nResumo: '))

	# opinions
	datos['opinions'] = input(_('\nOpinións: '))

	# nota
	while True:
		nota = input(_('\nNota (0-100): '))
		if nota.isdigit() and nota >= '0' and nota <= '100':
			datos['nota'] = nota
			break

	# autor
	datos['autor'] = input(_('\nAutor ou creador: '))

	# editorial
	if tipo == __codes['libro']:
		datos['editorial'] = input(_('\nEditorial: '))
	else:
		datos['editorial'] = 'NA'


	# dato de saida
	datos['data_saida'] = input(_('\nData de saída: '))

	# lonxitude
	datos['lonxitude'] = input(_('\nDuración (só o número): '))
	if xenero_base == 'literatura':
		datos['lonxitude'] = datos['lonxitude'] + ' páxinas'
	else:
		datos['lonxitude'] = datos['lonxitude'] + ' minutos'

	# xenero
	while True:
		xenero = unidecode(input(_('\nXénero: ')))
		if xenero == '?':
			u.pJson(__codsXeneros[xenero_base])
		elif xenero in __codsXeneros[xenero_base]:
			datos['xenero'] = xenero
			break

	# idioma
	while True:
		idioma = input(_('\nIdioma: '))
		if idioma == '?':
			u.pJson([ele for ele in __codsIdiomas.keys()])
		elif idioma in __codsIdiomas:
			datos['idioma'] = idioma
			break

	# data de inicio
	dini = input(_('\nPoñer data inicio? (s/n): '))
	if u.snValido(dini) == (True, True):
		datos['data_ini'] = kh.getAgora()
	else:
		datos['data_ini'] = None

	# data de fin
	dfin = input(_('\nPoñer data finalización? (s/n): '))
	if u.snValido(dfin) == (True, True):
		datos['data_fin'] = kh.getAgora()
	else:
		datos['data_fin'] = None

	# notas extra
	datos['notas_extra'] = input(_('\nNotas extra: '))

	return datos
#------------------------------------------------------------------------------------------------
# función auxiliar que se encarga do proceso unha vez sabemos nome e tipo do contido
def valorar_aux(nome, tipo):
	# miramos o tipo de contido do que se trata
	if tipo == __codes['serie']:
		# miramos que nos diga un epi válido
		while True:
			cap = input(_(' > Que capítulo? (1x01): ')).lower()
			if u.epi_valido(cap):
				fich = __carpetas['serie'] + nome +'/'+ cap
				# miramos se xa existe o ficheiro
				if Path(fich+'.json').is_file():
					# se quere sobreescribir a critica
					if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
						u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
						break
					else:
						u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
						break
				# se non existe non hai proble
				else:
					u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
					break

			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		fich = __carpetas['peli'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))


	elif tipo == __codes['docu']:
		fich = __carpetas['docu'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))

	elif tipo == __codes['video']:
		fich = __carpetas['video'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))

	elif tipo == __codes['libro']:
		fich = __carpetas['libro'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "literatura"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))

	elif tipo == __codes['artigo']:
		fich = __carpetas['artigo'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "literatura"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))

	elif tipo == __codes['musica']:
		fich = __carpetas['musica'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "musica"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "musica"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "musica"))

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
# función encargada da valoración dos contidos
def valorar():
	# variable que determina se crear ou non un material audiovisual no indice
	crear = True
	print('\n-----------------------')
	nome = unidecode(input(_(' > Título do contido: ')).lower())
	# primeiro miramos se esta no índice, senon crearemolo
	for ele in __indice.values():
		# se está no índice
		if unidecode(ele['nome']) == unidecode(nome):
			# pasamos o proceso á función auxiliar
			valorar_aux(ele['nome'], ele['tipo'])
			crear = False
			print('-----------------------')
			break

	# se non está no indice crearemolo
	if crear:
		if u.snValido(input(_('*> Non existe, engadir? (s/n): ')).lower()) == (True, True):
			valorar_aux(engadir(nome))
#------------------------------------------------------------------------------------------------
# función principal que se encarga de mostrar os contidos dentro do ficheiro de indice
def mostrar():
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in __indice.values():
		print(_('\nNome: '), ele['nome'])
		print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
# dado un texto clave saca as coincidencias
def buscar():
	print('\n-----------------------')
	texto = unidecode(input(_(' > Texto a buscar nos títulos: ')).lower())
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in __indice.values():
		if texto in unidecode(ele['nome']):
			print(_('\nNome: '), ele['nome'])
			print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
def edicion_aux(contido, xenero_base):
	print('-----------------------')
	for ele in contido:
		print(ele,': ', contido[ele])
		if u.snValido(input(_('Cambiar? (s/n): '))) == (True, True):
			while True:
				meter = input(ele+': ')
				if ele == 'nota':
					if meter.isdigit() and meter >= '0' and meter <= '100':
						contido[ele] = meter
						break
				elif ele == 'lonxitude':
					if meter.isdigit():
						if contido[ele].endswith('minutos'):
							contido[ele] = meter + ' minutos'
						else:
							contido[ele] = meter + ' páxinas'
						break
				elif ele == 'xenero':
					# quitamoslle os posibles acentos
					meter = unidecode(meter)
					if meter == '?':
						u.pJson(__codsXeneros[xenero_base])
					elif meter in __codsXeneros[xenero_base]:
						contido['xenero'] = meter
						break
				elif ele == 'idioma':
					if meter == '?':
						u.pJson([ele for ele in __codsIdiomas.keys()])
					elif meter in __codsIdiomas:
						contido['idioma'] = meter
						break
				elif ele == 'data_ini':
					contido['data_ini'] = kh.getAgora()
					break

				elif ele == 'data_fin':
					contido['data_fin'] = kh.getAgora()
					break

				else:
					contido[ele] = meter
					break
		print('-----------------------')

	return contido
#------------------------------------------------------------------------------------------------
# función auxiliar para a edición dun valor
def editar_aux(nome, tipo):
	# miramos o tipo de contido do que se trata
	if tipo == __codes['serie']:
		# miramos que nos diga un epi válido
		while True:
			cap = input(_(' > Que capítulo? (1x01): ')).lower()
			# so pasamos se o epi ten unha forma váliad
			if u.epi_valido(cap):
				# collemos todos os arquivos da serie que teñan de nome o copitulo dito
				arquivos = [elto for elto in os.listdir(__carpetas['serie']+nome) if cap in elto]
				# se é menor ca un significa que non existe e temos que crealo ou pasar
				if len(arquivos) < 1:
					if u.snValido(input(_('Non está valorado, valorámolo? (s/n): '))) == (True, True):
						valorar_aux(nome, tipo)
					else:
						break
				# se é igual a un podemos crear normal
				elif len(arquivos) == 1:
					ficheiro = __carpetas['serie'] + nome +'/'+ cap+'.json'
					u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))
					break
					# se é maior ca un debemos pedirlle que decida cal quere modificar
				elif len(arquivos) > 1:
					cont = 1
					for elto in arquivos:
						print(cont, ' - ', elto)
						cont += 1
					while True:
						escolla = input(_('*> Escolle o que queres modificar'))
						if escolla.isdigit() and escolla > '0' and escolla <= str(len(arquivos)):
							ficheiro = __carpetas['serie'] + arquivos[escolla] +'/'+ cap+'.json'
							u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))
			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		ficheiro = __carpetas['peli'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['docu']:
		ficheiro = __carpetas['docu'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['video']:
		ficheiro = __carpetas['video'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['libro']:
		ficheiro = __carpetas['libro'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'literatura'))

	elif tipo == __codes['artigo']:
		ficheiro = __carpetas['artigo'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'literatura'))

	elif tipo == __codes['musica']:
		ficheiro = __carpetas['musica'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'musica'))

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
# función que mostra un contido para editalo
def editar():
	print('\n-----------------------')
	nome = unidecode(input(_(' > Título do contido: ')).lower())
	for ele in __indice.values():
		# se está no índice
		if unidecode(ele['nome']) == unidecode(nome):
			# pasamos o proceso á función auxiliar
			editar_aux(ele['nome'], ele['tipo'])
			print('-----------------------')
			break
	print('\n-----------------------')
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o preciso para comezar o programa
def iniciar():
	# crea todo o sistema de ficheiros
	[u.crear_carp(valor) for valor in __carpetas.values()]
	# carga e devolve o ficheiro de índice
	return u.cargar_json(__findice), u.cargar_json(__fcodsIdiomas), u.cargar_json(__fcodsXeneros)
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o pertinente para pechar o programa gardandoo
def pechar():
	print('\n-----------------------')
	print(_('*> Gardando...'))
	u.gardar_json(__findice, __indice)
	#isto para cando se poda modificar dende o programa
	u.gardar_json(__fcodsIdiomas, __codsIdiomas)
	u.gardar_json(__fcodsXeneros, __codsXeneros)
	print(_('*> Talogo'))
	print('-----------------------')
	exit()
#------------------------------------------------------------------------------------------------
def menu():
	while True:
		print('\n-----------------------')
		print(_('*> Elixe a opción:'))
		print('-----------------------')
		print(_('0 - Pechar o programa (0. para sair sen gardar)'))
		print(_('1 - Engadir contido audiovisual ao índice'))
		print(_('2 - Valorar contido'))
		print(_('3 - Mostrar contidos'))
		print(_('4 - Buscar por titulo'))
		print(_('5 - Editar contido'))

		op = input(_('Opción: '))
		print('-----------------------')

		if op in __ops:
			break
		else:
			print(_('Selecciona unha das posibles.\n'))
	return op
#------------------------------------------------------------------------------------------------
if __name__=="__main__":
	## Declaracións ----------------------
	_ = gettext.gettext
	#en = gettext.translation('caderno-viaxe', localedir='locales', languages=['en'])
	#en.install()
	#_ = en.gettext

	# valores que mete o ficheiro de configuración
	'''	__config garda:
	ruta
	lang'''
	__config = u.read_config()

	# diccionario con códigos para cada tipo de elemento
	__codes = {'serie': 's',
				'peli': 'p',
				'docu': 'd',
				'video': 'v',
				'libro': 'l',
				'musica': 'm',
				'artigo': 'a'
			}

	# nome do ficheiro e variable onde se gardarán todos os idiomas coas súas claves
	__fcodsIdiomas = '../media/codesIdiomas'
	__codsIdiomas = {}
	# nome do ficheiro e variable onde se gardarán todos os xeneros coas súas claves
	__fcodsXeneros = '../media/codesXeneros'
	__codsXeneros = {}

	# rutas do sistema de carpetas, unha xeral e unha para cada tipo de elemento
	__cbase = __config['ruta']+ '/' +__config['nom_base'] + '/'
	__cnotas = __cbase + __config['nom_anotacions'] + '/'
	__carpetas = {
				'serie': __cnotas + __codes['serie'] + '/',
				'peli': __cnotas + __codes['peli'] + '/',
				'docu': __cnotas + __codes['docu'] + '/',
				'video': __cnotas + __codes['video'] + '/',
				'libro': __cnotas + __codes['libro'] + '/',
				'musica': __cnotas + __codes['musica'] + '/',
				'artigo': __cnotas + __codes['artigo'] + '/'
				}

	# ficheiro co índice de tódas as críticas
	__findice = __cbase + 'indice.json'

	## Asignacións ----------------------
	# se non existe creamos o sistema de carpetas completo
	# metemos en memoria os contidos do ficheiro índice
	__indice, __codsIdiomas, __codsXeneros = iniciar()

	#a# non creo unha función de manual e automático porque só esta pensado para manual
	# diccionario con todas as opcións posibles
	__ops = {'0.': exit,
			'0': pechar,
			'1': engadir,
			'2': valorar,
			'3': mostrar,
			'4': buscar,
			'5': editar
			}

	while True:
		__ops[menu()]()
		input(_('Intro para continuar'))
#------------------------------------------------------------------------------------------------
