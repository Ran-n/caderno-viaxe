#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	25/06/2019 16:33:56
#------------------------------------------------------------------------------------------------
import json
from pathlib import Path
from functools import partial
#------------------------------------------------------------------------------------------------
__fnotas = 'media/notas.json'
__findice = 'media/indice.json'
#------------------------------------------------------------------------------------------------
# función encargada de cargar ficheiros tipo json
def cargar_json(fich):
	if Path(fich).is_file():
		return json.loads(open(fich).read())
	else:
		open(fich, 'w').write('{}')
		return json.loads(open(fich).read())
#------------------------------------------------------------------------------------------------
def gardar_json(fich, contido):
	open(fich, 'w').write(json.dumps(contido, indent=1, sort_keys=False))
#------------------------------------------------------------------------------------------------
def engadir(indice):
	media = {'nome': None,
			'tipo': None}

	print('\n-----------------------')
	print('*> Engadindo:')
	print('-----------------------')
	print(' > Nome', end=': ')
	media['nome'] = input()
	print(' > Tipo', end=': ')
	media['tipo'] = input()
	print('-----------------------')

	indice[len(indice)] = media
#------------------------------------------------------------------------------------------------
def valorar(indice, notas):
	print('\n-----------------------')
	print(' > Nome do contido', end=': ')
	nome = input()

	# primeiro miramos se esta no índice, senon creamolo
	for ele in indice.values():
		if ele['nome'] == nome:
			print('esta')
			break
		else:
			print('hai que crealo')

	print('-----------------------')
#------------------------------------------------------------------------------------------------
def menu():
	while True:
		print('\n1 - Engadir contido audiovisual')
		print('2 - Valorar contido')

		print('Opción', end=': ')
		op = input()

		if op in __ops:
			break
		else:
			print('Selecciona unha das posibles.\n')
	return op
#------------------------------------------------------------------------------------------------
if __name__=="__main__":
	notas = cargar_json(__fnotas)
	indice = cargar_json(__findice)
	__ops = {'1': partial(engadir, indice),
			'2': partial(valorar, indice, notas)}

	__ops[menu()]()

	#print('Notas')
	#print(json.dumps(notas, indent=1, sort_keys=True))
	#print('Índice')
	#print(json.dumps(indice, indent=1, sort_keys=True))

	gardar_json(__fnotas, notas)
	gardar_json(__findice, indice)
#------------------------------------------------------------------------------------------------