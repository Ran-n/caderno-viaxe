#! /usr/bin/python3
# -*- coding: utf-8 -*-

#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	25/06/2019 16:33:56
#------------------------------------------------------------------------------------------------
import json
from functools import partial
import utils as u
import gettext
#------------------------------------------------------------------------------------------------
__fnotas = 'media/notas.json'
__findice = 'media/indice.json'

__cod_serie = 's'
__cod_peli = 'p'
__cod_docu = 'd'
#------------------------------------------------------------------------------------------------
def engadir(indice):
	media = {'nome': None,
			'tipo': None}

	print('\n-----------------------')
	print(_('*> Engadindo:'))
	print('-----------------------')
	print(_(' > Nome'), end=': ')
	media['nome'] = input()

	while True:
		print(_(' > Tipo (1 serie, 2 peli, 3 docu)'), end=': ')
		tipo = input()

		if tipo == '1':
			media['tipo'] = __cod_serie
			break
		elif tipo == '2':
			media['tipo'] = __cod_peli
			break
		elif tipo == '3':
			media['tipo'] = __cod_docu
			break
		else:
			media['tipo'] = 'imposible'
	print('-----------------------')

	indice[len(indice)] = media
#------------------------------------------------------------------------------------------------
def valorar(indice, notas):
	crear = True
	print('\n-----------------------')
	print(_(' > Título do contido'), end=': ')
	nome = input()

	# primeiro miramos se esta no índice, senon creamolo
	for ele in indice.values():
		if ele['nome'].lower() == nome.lower():
			if ele['tipo'] == __cod_serie:
				while True:
					print(_(' > Que capítulo? (1x01)'), end=': ')
					cap = input().lower()
					if u.epi_valido(cap):
						print('beeen')
						break
					else:
						print(_('*> Capítulo inválido.\n'))

			crear = False
			print('-----------------------')
			break

	if crear:
		print(_('*> Non existe, engadir? (si[s]/non[n])'), end=': ')
		if input() == 's':
			engadir(indice)

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
		print(_('0 - Pechar o programa'))
		print(_('1 - Engadir contido audiovisual'))
		print(_('2 - Valorar contido'))

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
	#_ = gettext.gettext
	en = gettext.translation('caderno-viaxe', localedir='locales', languages=['en'])
	en.install()
	_ = en.gettext

	notas = u.cargar_json(__fnotas)
	indice = u.cargar_json(__findice)
	__ops = {'0': pechar,
			'1': partial(engadir, indice),
			'2': partial(valorar, indice, notas)}
	
	while True:
		__ops[menu()]()

	#print('Notas')
	#print(json.dumps(notas, indent=1, sort_keys=True))
	#print('Índice')
	#print(json.dumps(indice, indent=1, sort_keys=True))
#------------------------------------------------------------------------------------------------