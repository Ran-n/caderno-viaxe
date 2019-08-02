#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	01/08/2019 14:07:40
#------------------------------------------------------------------------------------------------
import utils as u
from khronos import khronos as kh
from base36 import base36 as b36
# ------
import json
from functools import partial
import gettext
from pathlib import Path
#------------------------------------------------------------------------------------------------
# función principal que engade un contido co seu código ao ficheiro e índice
def engadir(indice, nome = None):
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
	for ele in indice.values():
		if ele['nome'].lower() == nome.lower():
			existe = True
			break

	if existe:
		print(_('*> Xa existe compi'))
	else:
		media['nome'] = nome
		# para ver que pon un tipo que exista
		while True:
			tipo = input(_(' > Tipo (1 serie, 2 peli, 3 docu, 4 video, 5 libro): '))

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
			else:
				media['tipo'] = 'imposible'

		# engadimos o contido audiovisual á colección xeral
		#FALTA: Mirar que a chave que se lle pon non exista xa se se eliminou
		# en lugar de poñer un simple número usaremos o tempo no que foi creado en base32
		indice[b36.code(kh.getAgora())] = media

	print('-----------------------')

	# devolvemos estes valores engadidos se é que se queren
	return media['nome'], media['tipo']
#------------------------------------------------------------------------------------------------
# función auxiliar que se encarga de coller e retornar os valores a meter no ficheiro de valoración
def valoracion():
	datos = {'resumo': None,
			'opinions': None,
			'valoracion': None,
			'nota': None}

	datos['resumo'] = input(_('\nResumo: '))
	datos['opinions'] = input(_('\nOpinions: '))
	datos['valoracion'] = input(_('\nValoración: '))
	datos['nota'] = input(_('\nNota: '))

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
						u.gardar_json(fich+'.json', valoracion())
						break
					else:
						u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion())
						break
				# se non existe non hai proble
				else:
					u.gardar_json(fich+'.json', valoracion())
					break

			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		u.gardar_json(__carpetas['peli'] + nome+'.json', valoracion())

	elif tipo == __codes['docu']:
		u.gardar_json(__carpetas['docu'] + nome+'.json', valoracion())

	elif tipo == __codes['video']:
		u.gardar_json(__carpetas['video'] + nome+'.json', valoracion())

	elif tipo == __codes['libro']:
		u.gardar_json(__carpetas['libro'] + nome+'.json', valoracion())

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
# función encargada da valoración dos contidos
def valorar(indice):
	# variable que determina se crear ou non un material audiovisual no indice
	crear = True
	print('\n-----------------------')
	nome = input(_(' > Título do contido: ')).lower()
	# primeiro miramos se esta no índice, senon crearemolo
	for ele in indice.values():
		# se está no índice
		if ele['nome'] == nome:
			# pasamos o proceso á función auxiliar
			valorar_aux(ele['nome'], ele['tipo'])
			crear = False
			print('-----------------------')
			break

	# se non está no indice crearemolo
	if crear:
		if u.snValido(input(_('*> Non existe, engadir? (s/n): ')).lower()) == (True, True):
			nome, tipo = engadir(indice, nome)
			valorar_aux(nome, tipo)
#------------------------------------------------------------------------------------------------
# función principal que se encarga de mostrar os contidos dentro do ficheiro de indice
def mostrar(indice):
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in indice.values():
		print(_('\nNome: '), ele['nome'])
		print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o preciso para comezar o programa
def iniciar():
	# crea todo o sistema de ficheiros
	[u.crear_carp(valor) for valor in __carpetas.values()]
	# carga e devolve o ficheiro de índice
	return u.cargar_json(__findice)
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o pertinente para pechar o programa gardandoo
def pechar():
	print('\n-----------------------')
	print(_('*> Gardando...'))
	u.gardar_json(__findice, indice)
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
	indice = iniciar()


	#a# non creo unha función de manual e automático porque só esta pensado para manual
	# diccionario con todas as opcións posibles
	__ops = {'0.': exit,
			'0': pechar,
			'1': partial(engadir, indice),
			'2': partial(valorar, indice),
			'3': partial(mostrar, indice)
			}

	while True:
		__ops[menu()]()
#------------------------------------------------------------------------------------------------
