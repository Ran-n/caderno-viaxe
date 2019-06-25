#! /usr/bin/python3
#+ Autor:	Ran#
# -*- coding: utf-8 -*-
#+ Creado:	25/06/2019 21:37:29
#+ Editado:	25/06/2019 21:37:29
#------------------------------------------------------------------------------------------------
import json
from pathlib import Path
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
def epi_valido(epi):
	if 'x' not in epi:
		return False

	temp, epi = epi.split('x')
	if (temp.isdigit()) & (int(temp)>0) & (epi.isdigit()):
		return True
	else:
		return False
#------------------------------------------------------------------------------------------------