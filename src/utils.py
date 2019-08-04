#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	25/06/2019 21:37:29
#+ Editado:	05/08/2019 00:01:07
## caderno-viaxe.py
#------------------------------------------------------------------------------------------------
import json
from pathlib import Path
#------------------------------------------------------------------------------------------------
texto_config = '''
# selecionar carpeta raiz, . significa carpeta actual
ruta = .

# selecionar o idioma para a versión interactiva
# galego (gl), inglés (en), castelán (es)
lang=gl

#nome da carpeta base do proxecto
nom_base=opinions

#nome da carpeta onde se gardan as anotacións
nom_anotacions=anotacions
'''
#------------------------------------------------------------------------------------------------
# función encargada de cargar ficheiros tipo json coa extensión dada se se dá
def cargar_json(fich):
	if Path(fich).is_file():
		return json.loads(open(fich).read())
	else:
		open(fich, 'w').write('{}')
		return json.loads(open(fich).read())
#------------------------------------------------------------------------------------------------
# función de gardado de ficheiros tipo json coa extensión dada se se da
def gardar_json(fich, contido):
	open(fich, 'w').write(json.dumps(contido, indent=1, sort_keys=False, ensure_ascii=False))
#------------------------------------------------------------------------------------------------
# se existe, crea unha carpeta
def crear_carp(carp):
	if Path(carp).is_dir() == False:
		Path(carp).mkdir(parents=True, exist_ok=True)
#------------------------------------------------------------------------------------------------
# imprime un diccionario en modo bonito
def pJson(diccionario, sort=False):
	print(json.dumps(diccionario, indent=4, sort_keys=sort))
#------------------------------------------------------------------------------------------------
# función que se encarga de devolver verdadeiro se o episodio esta ben posto
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
		return 'película'

	if code == codes['docu']:
		return 'documental'

	if code == codes['musica']:
		return 'música'

	if code == codes['artigo']:
		return 'artigo'
		
	if code == codes['libro']:
		return 'libro'
#------------------------------------------------------------------------------------------------
# función que devolve verdadeiro ou falso dependendo de se a entrada está dentro
# das respostas positivas ou negativas válidas e verdadeiro ou falso para o tipo
# de resposta que deu nun principio si verdadeiro non falso
def snValido(resposta):
	sis = ('si', 's', 'yes', 'y')
	nons = ('non', 'no', 'n')

	if resposta in sis:
		# valido e resposta
		return True, True
	# non poñer nada conta como dicir non
	elif resposta in nons or resposta == '':
		return True, False
	else:
		return False, False
#------------------------------------------------------------------------------------------------
# función para ler o ficheiro de configuración e devolver as variables adecuadas
def read_config():
	fich = '../.config'
	# se o ficheiro xa existe
	if Path(fich).is_file():
		config = {}
		'''
		Lemos todas as liñas do ficheiro e quitamoslle os \n
		De todas as liñas só nos quedamos coas que non comezan por un comentario
		Das liñas de configuración o que facemos e separalas por igual e quedarnos
		co segundo elemento de valor e o primeiro de clave, co cal a orde dos elementos pode ser alterada.
		Poderíase facer que mirase o nome da variable pero da pereza e non ten
		sentido e mentres non a cambien non importa.
		Facemos que o da esquerda da variable sexa a clave do diccionario e o da dereita o valor.
		'''
		for x in open(fich):
			''' facemos isto porque debe ser máis eficiente ca facer senón strip
			cada vez que chamemos a x'''
			x = x.strip()
			if not x.startswith('#') and x != '':
				config[x.split('=')[0].strip()] = x.split('=')[1].strip()
		return config
	# se non existe o que facemos e crealo cos valores por defecto postos na variable e recargar a operacion
	else:
		open(fich, 'w').write(texto_config)
		return read_config()
#------------------------------------------------------------------------------------------------
