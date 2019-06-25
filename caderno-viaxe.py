#!/usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	25/06/2019 14:57:51
#------------------------------------------------------------------------------------------------
import json
from pathlib import Path
#from functools import partial
#------------------------------------------------------------------------------------------------
# función encargada de cargar ficheiros tipo json
def cargar_json(fich):
	if Path(fich).is_file():
		return json.loads(open(fich).read())
	else:
		open(fich, 'w').write('{}')
		return json.loads(open(fich).read())
#------------------------------------------------------------------------------------------------
def engadir():
	print('engadindo')
#------------------------------------------------------------------------------------------------
def menu():
	#__ops = {'1': partial(engadir, )}
	__ops = {'1': engadir}

	while True:
		print('1 - Engadir Serie/Peli/Docu')

		print('Opción', end=': ')
		op = input()

		if op in __ops:
			break
		else:
			print('Selecciona unha das posibles.\n')
	__ops[op]()
#------------------------------------------------------------------------------------------------
if __name__=="__main__":
	__fnotas = 'media/notas.json'
	__findice = 'media/indice.json'

	notas = cargar_json(__fnotas)
	indice = cargar_json(__findice)

	menu()

	print(json.dumps(notas, indent=1, sort_keys=True))
	print(json.dumps(indice, indent=1, sort_keys=True))
#------------------------------------------------------------------------------------------------