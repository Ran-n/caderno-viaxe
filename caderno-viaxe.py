#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	27/06/2019 12:43:03
#------------------------------------------------------------------------------------------------
import json
from functools import partial
import utils as u
import gettext
from pathlib import Path
import time
#------------------------------------------------------------------------------------------------
__codes = {'serie': 's',
			'peli': 'p',
			'docu': 'd',
			'video': 'v',
			'libro': 'l'}

__cmedia = 'media/'
__cnotas = 'media/notas/'
__cseries = __cnotas+__codes['serie']+'/'
__cpelis = __cnotas+__codes['peli']+'/'
__cdocus = __cnotas+__codes['docu']+'/'
__cvideos = __cnotas+__codes['video']+'/'
__clibros = __cnotas+__codes['libro']+'/'

#__fnotas = __cmedia + 'notas'
__findice = __cmedia + 'indice'

__sis = ('si', 'yes', 's', 'y')
#------------------------------------------------------------------------------------------------
def engadir(indice, nome = None):
	existe = False
	media = {'nome': None,
			'tipo': None}

	print('\n-----------------------')
	print(_('*> Engadindo:'))
	print('-----------------------')
	if nome is None:
		nome = input(_(' > Nome: '))
	else:
		print(_(' > Nome: '), nome)

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
				u.crear_carp(__cseries+nome)
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
		indice[len(indice)] = media

	print('-----------------------')

	# devolvemos estes valores engadidos se é que se queren
	return media['nome'], media['tipo']
#------------------------------------------------------------------------------------------------
# función que se encarga de coller e retornar os valores a meter no ficheiro de valoración
def valoracion():
	datos = {'resumo': None,
			'opinions': None,
			'nota': None}

	datos['resumo'] = input(_('\nResumo: '))

	#**

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
				fich = __cseries + nome +'/'+ cap
				# miramos se xa existe o ficheiro
				if Path(fich+'.json').is_file():
					# se quere sobreescribir a critica
					if input(_('*> Xa existe, sobreescribir? (s/n): ')).lower() in __sis:
						u.gardar_json(fich, valoracion())
						break
					else:
						u.gardar_json(fich+'_' + str(time.time()), valoracion())
						break
				# se non existe non hai proble
				else:
					u.gardar_json(fich, valoracion())
					break

			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		u.gardar_json(__cpelis + nome, valoracion())

	elif tipo == __codes['docu']:
		u.gardar_json(__cdocus + nome, valoracion())

	elif tipo == __codes['video']:
		u.gardar_json(__cvideos + nome, valoracion())

	elif tipo == __codes['libro']:
		u.gardar_json(__clibros + nome, valoracion())

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
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
		if input(_('*> Non existe, engadir? (s/n): ')).lower() in __sis:
			nome, tipo = engadir(indice, nome)
			valorar_aux(nome, tipo)

#------------------------------------------------------------------------------------------------
def mostrar(indice):
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in indice.values():
		print(_('\nNome: '), ele['nome'])
		print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
def cargas_ini():
	u.crear_carp(__cseries)
	u.crear_carp(__cpelis)
	u.crear_carp(__cdocus)
	u.crear_carp(__cvideos)
	u.crear_carp(__clibros)

	#notas = u.cargar_json(__fnotas)
	indice = u.cargar_json(__findice)

	#return notas, indice
	return indice
#------------------------------------------------------------------------------------------------
def pechar():
	print('\n-----------------------')
	print(_('*> Gardando...'))
	#u.gardar_json(__fnotas, notas)
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
		print(_('0. - Pechar o programa, sen gardar'))
		print(_('0  - Pechar o programa, gardando'))
		print(_('1  - Engadir contido audiovisual'))
		print(_('2  - Valorar contido'))
		print(_('3  - Mostrar contidos'))

		op = input(_('Opción: '))
		print('-----------------------')

		if op in __ops:
			break
		else:
			print(_('Selecciona unha das posibles.\n'))
	return op
#------------------------------------------------------------------------------------------------
if __name__=="__main__":
	_ = gettext.gettext
	#en = gettext.translation('caderno-viaxe', localedir='locales', languages=['en'])
	#en.install()
	#_ = en.gettext

	# se non existe creamos o sistema de carpetas
	#notas, indice = cargas_ini()
	indice = cargas_ini()


	__ops = {'0.': exit,
			'0': pechar,
			'1': partial(engadir, indice),
			'2': partial(valorar, indice),
			'3': partial(mostrar, indice)}

	while True:
		__ops[menu()]()
		input()

	#print('Notas')
	#print(json.dumps(notas, indent=1, sort_keys=True))
	#print('Índice')
	#print(json.dumps(indice, indent=1, sort_keys=True))
#------------------------------------------------------------------------------------------------
