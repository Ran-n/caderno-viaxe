#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 21:37:29
#+ Editado:	27/06/2019 12:45:12
#------------------------------------------------------------------------------------------------
import json
from pathlib import Path
#------------------------------------------------------------------------------------------------
# función encargada de cargar ficheiros tipo json
def cargar_json(fich):
	fich = fich +'.json'
	if Path(fich).is_file():
		return json.loads(open(fich).read())
	else:
		open(fich, 'w').write('{}')
		return json.loads(open(fich).read())
#------------------------------------------------------------------------------------------------
# función de gardado de ficheiros tipo json
def gardar_json(fich, contido):
	open(fich+'.json', 'w').write(json.dumps(contido, indent=1, sort_keys=False, ensure_ascii=False))
#------------------------------------------------------------------------------------------------
def crear_carp(carp):
	if Path(carp).is_dir() == False:
		Path(carp).mkdir(parents=True, exist_ok=True)
#------------------------------------------------------------------------------------------------
def epi_valido(epi):
	if 'x' in epi:
		temp, epi = epi.split('x')

		if (temp.isdigit()) & (epi.isdigit()):
			return True

	return False
#------------------------------------------------------------------------------------------------
def trad_codes(code, codes):
	if code == codes['serie']:
		return 'serie'

	if code == codes['video']:
		return 'video'

	if code == codes['peli']:
		return 'peli'

	if code == codes['docu']:
		return 'docu'
#------------------------------------------------------------------------------------------------
