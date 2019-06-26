#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	26/06/2019 16:07:25
#------------------------------------------------------------------------------------------------
import json
from functools import partial
import utils as u
import gettext
#------------------------------------------------------------------------------------------------
__cmedia = 'media/'
__cnotas = 'media/notas/'
__cseries = __cnotas+'s/'
__cpelis = __cnotas+'p/'
__cdocus = __cnotas+'d/'

__fnotas = __cmedia + 'notas.json'
__findice = __cmedia + 'indice.json'

__cod_serie = 's'
__cod_peli = 'p'
__cod_docu = 'd'
#------------------------------------------------------------------------------------------------
def engadir(indice):
	existe = False
	media = {'nome': None,
			'tipo': None}

	print('\n-----------------------')
	print(_('*> Engadindo:'))
	print('-----------------------')
	print(_(' > Nome'), end=': ')
	nome = input()

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
			print(_(' > Tipo (1 serie, 2 peli, 3 docu)'), end=': ')
			tipo = input()

			# segundo o tipo poñemos o seu código
			if tipo == '1':
				media['tipo'] = __cod_serie
				u.crear_carp(nome)
				break
			elif tipo == '2':
				media['tipo'] = __cod_peli
				break
			elif tipo == '3':
				media['tipo'] = __cod_docu
				break
			else:
				media['tipo'] = 'imposible'

		# engadimos o contido audiovisual á colección xeral
		indice[len(indice)] = media

	print('-----------------------')

	# devolvemos estes valores engadidos se é que se queren
	return media['nome'], media['tipo']
#------------------------------------------------------------------------------------------------
# función que se encarga de coller e retornar os valores a meter no ficheiro de valoración
def valorar_aux2():
	valoracion = {'resumo': None,
				'opinions': None,
				'nota': None}

	print(_('\nResumo: '))
	valoracion['resumo'] = input()

	return valoracion
#------------------------------------------------------------------------------------------------
# función auxiliar que se encarga do proceso unha vez sabemos nome e tipo do contido
def valorar_aux(nome, tipo):
	# miramos o tipo de contido do que se trata
	if tipo == __cod_serie:
		# miramos que nos diga un epi válido
		while True:
			print(_(' > Que capítulo? (1x01)'), end=': ')
			cap = input().lower()
			if u.epi_valido(cap):
				u.gardar_json(__cseries + nome +'/'+ cap+'.json', valorar_aux2())
				break
			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __cod_peli:
		u.gardar_json(__cpelis + nome +'.json', valorar_aux2())

	elif tipo == __cod_docu:
		u.gardar_json(__cdocus + nome +'.json', valorar_aux2())

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
def valorar(indice, notas):
	# variable que determina se crear ou non un material audiovisual no indice
	crear = True

	print('\n-----------------------')
	print(_(' > Título do contido'), end=': ')
	nome = input()

	# primeiro miramos se esta no índice, senon crearemolo
	for ele in indice.values():
		# se está no índice
		if ele['nome'].lower() == nome.lower():
			# pasamos o proceso á función auxiliar
			valorar_aux(ele['nome'], ele['tipo'])

			crear = False
			print('-----------------------')
			break

	# se non está no indice crearemolo
	if crear:
		print(_('*> Non existe, engadir? (s/n)'), end=': ')
		if input() == ('s' or 'y'):
			nome, tipo = engadir(indice)
			valorar_aux(nome, tipo)

#------------------------------------------------------------------------------------------------
def pechar():
	print('\n-----------------------')
	print(_('*> Gardando...'))
	u.gardar_json(__fnotas, notas)
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

		print(_('Opción'), end=': ')
		op = input()
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

	notas = u.cargar_json(__fnotas)
	indice = u.cargar_json(__findice)
	__ops = {'0.': exit,
			'0': pechar,
			'1': partial(engadir, indice),
			'2': partial(valorar, indice, notas)}

	while True:
		__ops[menu()]()

	#print('Notas')
	#print(json.dumps(notas, indent=1, sort_keys=True))
	#print('Índice')
	#print(json.dumps(indice, indent=1, sort_keys=True))
#------------------------------------------------------------------------------------------------
