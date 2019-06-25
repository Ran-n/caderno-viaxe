#!/usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	25/06/2019 14:57:51
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
def engadir(indice, cant):
	media = {'nome': None,
			'tipo': None}

	print('Nome', end=': ')
	media['nome'] = input()
	print('Tipo', end=': ')
	media['tipo'] = input()

	indice[cant] = media

#------------------------------------------------------------------------------------------------
def menu():
	while True:
		print('1 - Engadir Serie/Peli/Docu')

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
	cant = len(indice)
	__ops = {'1': partial(engadir, indice, cant)}

	__ops[menu()]()

	print('Notas')
	print(json.dumps(notas, indent=1, sort_keys=True))
	print('Índice')
	print(json.dumps(indice, indent=1, sort_keys=True))

	gardar_json(__fnotas, notas)
	gardar_json(__findice, indice)
#------------------------------------------------------------------------------------------------