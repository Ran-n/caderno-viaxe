#! /usr/bin/python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------
#+ Autor:	Ran#
#+ Creado:	25/06/2019 14:27:50
#+ Editado:	05/08/2019 00:01:03
#------------------------------------------------------------------------------------------------
import utils as u
from khronos import khronos as kh
from base36 import base36 as b36
# ------
import json
from functools import partial
import gettext
from pathlib import Path
from unidecode import unidecode
import os
import shutil
#------------------------------------------------------------------------------------------------
# función principal que engade un contido co seu código ao ficheiro e índice
def engadir(nome = None):
	existe = False
	media = {'nome': None,
			'tipo': None,
			'nota': None,
			'autor': None,
			'editorial': None,
			'data_saida': None,
			'lonxitude': None,
			'xenero': None,
			'idioma': None,
			'data_ini': None,
			'data_fin': None}

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
	for ele in __indice.values():
		if ele['nome'].lower() == nome.lower():
			existe = True
			break

	if existe:
		print(_('*> Xa existe compi'))
	else:
		media['nome'] = nome
		# para ver que pon un tipo que exista
		while True:
			tipo = input(_(' > Tipo (1 serie, 2 peli, 3 docu, 4 video, 5 libro, 6 música, 7 artigo): '))

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
				u.crear_carp(__carpetas['libro']+nome)
				break
			elif tipo == '6':
				media['tipo'] = __codes['musica']
				break
			elif tipo == '7':
				media['artigo'] = __codes['artigo']
				break
			else:
				media['tipo'] = 'imposible'

	# nota
	while True:
		nota = input(_(' > Nota (0-100): '))
		if nota.isdigit() and int(nota) >= 0 and int(nota) <= 100:
			media['nota'] = nota
			break

	# autor
	media['autor'] = input(_(' > Autor ou creador: '))

	# editorial
	if tipo == __codes['libro']:
		media['editorial'] = input(_(' > Editorial: '))
	else:
		media['editorial'] = 'NA'


	# dato de saida
	media['data_saida'] = input(_(' > Data de saída: '))

	# lonxitude
	while True:
		valor = input(_(' > Duración (só o número): '))
		if valor.replace(',','').replace('.','').isdigit():
			if media['tipo'] in (__codes['artigo'], __codes['libro']):
				media['lonxitude'] = valor + ' páxinas'
			else:
				media['lonxitude'] = valor + ' minutos'
			break

	# xenero
	if media['tipo'] in (__codes['musica']):
		xenero_base = 'musica'
	elif media['tipo'] in (__codes['libro'], __codes['artigo']):
		xenero_base = 'literatura'
	else:
		xenero_base = 'audiovisual'

	while True:
		xenero = unidecode(input(_(' > Xénero: ')))
		if xenero == '?':
			u.pJson(__codsXeneros[xenero_base])

		elif xenero in __codsXeneros[xenero_base]:
			media['xenero'] = xenero
			break

	# idioma
	while True:
		idioma = input(_(' > Idioma: '))
		if idioma == '?':
			u.pJson([ele for ele in __codsIdiomas.keys()])
		elif idioma in __codsIdiomas:
			media['idioma'] = idioma
			break

	# data de inicio
	dini = input(_(' > Poñer data inicio? (s/n): '))
	if u.snValido(dini) == (True, True):
		media['data_ini'] = kh.getAgora()
	else:
		media['data_ini'] = None

	# data de fin
	dfin = input(_(' > Poñer data finalización? (s/n): '))
	if u.snValido(dfin) == (True, True):
		media['data_fin'] = kh.getAgora()
	else:
		media['data_fin'] = None

	# engadimos o contido audiovisual á colección xeral
	#FALTA: Mirar que a chave que se lle pon non exista xa se se eliminou
	# en lugar de poñer un simple número usaremos o tempo no que foi creado en base32
	__indice[b36.code(kh.getAgora())] = media

	print('-----------------------')

	# devolvemos estes valores engadidos se é que se queren
	return media['nome'], media['tipo']
#------------------------------------------------------------------------------------------------
# función auxiliar que se encarga de coller e retornar os valores a meter no ficheiro de valoración
def valoracion(tipo, xenero_base):
	datos = {'resumo': None,
			'opinions': None,
			'nota': None,
			'data_saida': None,
			'lonxitude': None,
			'idioma': None,
			'data_ini': None,
			'data_fin': None,
			'notas_extra': None}

	# resumo
	datos['resumo'] = input(_('\nResumo: '))

	# opinions
	datos['opinions'] = input(_('\nOpinións: '))

	# nota
	while True:
		nota = input(_('\nNota (0-100): '))
		if nota.isdigit() and int(nota) >= 0 and int(nota) <= 100:
			datos['nota'] = nota
			break

	# dato de saida
	datos['data_saida'] = input(_('\nData de saída: '))

	# lonxitude
	while True:
		valor = input(_('\nDuración (só o número): '))
		if valor.replace(',','').replace('.','').isdigit():
			if xenero_base == 'literatura':
				datos['lonxitude'] = valor + ' páxinas'
			else:
				datos['lonxitude'] = valor + ' minutos'
			break

	# idioma
	while True:
		idioma = input(_('\nIdioma: '))
		if idioma == '?':
			u.pJson([ele for ele in __codsIdiomas.keys()])
		elif idioma in __codsIdiomas:
			datos['idioma'] = idioma
			break

	# data de inicio
	dini = input(_('\nPoñer data inicio? (s/n): '))
	if u.snValido(dini) == (True, True):
		datos['data_ini'] = kh.getAgora()
	else:
		datos['data_ini'] = None

	# data de fin
	dfin = input(_('\nPoñer data finalización? (s/n): '))
	if u.snValido(dfin) == (True, True):
		datos['data_fin'] = kh.getAgora()
	else:
		datos['data_fin'] = None

	# notas extra
	datos['notas_extra'] = input(_('\nNotas extra: '))

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
						u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
						break
					else:
						u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
						break
				# se non existe non hai proble
				else:
					u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
					break

			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		fich = __carpetas['peli'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))


	elif tipo == __codes['docu']:
		fich = __carpetas['docu'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))

	elif tipo == __codes['video']:
		fich = __carpetas['video'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "audiovisual"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "audiovisual"))

	elif tipo == __codes['libro']:
		fich = __carpetas['libro'] + nome

		# miramos que nos diga un epi válido
		while True:
			cap = input(_(' > Que capítulo? (1): ')).lower()
			if cap.isdigit():
				fich = __carpetas['libro'] + nome +'/'+ cap
				# miramos se xa existe o ficheiro
				if Path(fich+'.json').is_file():
					# se quere sobreescribir a critica
					if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
						u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))
						break
					else:
						u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "literatura"))
						break
				# se non existe non hai proble
				else:
					u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))
					break

			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['artigo']:
		fich = __carpetas['artigo'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "literatura"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "literatura"))

	elif tipo == __codes['musica']:
		fich = __carpetas['musica'] + nome
		# miramos se xa existe o ficheiro
		if Path(fich+'.json').is_file():
			if u.snValido(input(_('*> Xa existe, sobreescribir? (s/n): ')).lower()) == (True, True):
				u.gardar_json(fich+'.json', valoracion(tipo, "musica"))
			else:
				u.gardar_json(fich+'_'+str(b36.code(kh.getAgora()))+'.json', valoracion(tipo, "musica"))
		else:
			u.gardar_json(fich+'.json', valoracion(tipo, "musica"))

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
# función encargada da valoración dos contidos
def valorar():
	# variable que determina se crear ou non un material audiovisual no indice
	crear = True
	print('\n-----------------------')
	nome = unidecode(input(_(' > Título do contido: ')).lower())
	# primeiro miramos se esta no índice, senon crearemolo
	for ele in __indice.values():
		# se está no índice
		if unidecode(ele['nome']) == unidecode(nome):
			# pasamos o proceso á función auxiliar
			valorar_aux(ele['nome'], ele['tipo'])
			crear = False
			print('-----------------------')
			break

	# se non está no indice crearemolo
	if crear:
		if u.snValido(input(_('*> Non existe, engadir? (s/n): ')).lower()) == (True, True):
			# haino que poñer así porque devolvemos dous valores e senón peta poñeendoo directamente
			nome, tipo = engadir(nome)
			valorar_aux(nome, tipo)
#------------------------------------------------------------------------------------------------
# función principal que se encarga de mostrar os contidos dentro do ficheiro de indice
def mostrar():
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in __indice.values():
		print(_('\nNome: '), ele['nome'])
		print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
# dado un texto clave saca as coincidencias
def buscar():
	print('\n-----------------------')
	texto = unidecode(input(_(' > Texto a buscar nos títulos: ')).lower())
	print('\n-----------------------')
	print(_('*> Contidos:'))
	print('-----------------------', end='')

	for ele in __indice.values():
		if texto in unidecode(ele['nome']):
			print(_('\nNome: '), ele['nome'])
			print(_('Tipo: '), u.trad_codes(ele['tipo'], __codes))

	print('-----------------------')
#------------------------------------------------------------------------------------------------
def edicion_aux(contido, xenero_base):
	print('-----------------------')
	for ele in contido:
		print(ele,': ', contido[ele])
		if u.snValido(input(_('Cambiar? (s/n): '))) == (True, True):
			while True:
				if ele == 'nota':
					meter = input(ele+': ')
					if meter.isdigit() and int(meter) >= 0 and int(meter) <= 100:
						contido[ele] = meter
						break
				elif ele == 'lonxitude':
					meter = input(ele+': ')
					if meter.replace(',','').replace('.','').isdigit():
						if contido[ele].endswith('minutos'):
							contido[ele] = meter + ' minutos'
						else:
							contido[ele] = meter + ' páxinas'
						break
				elif ele == 'idioma':
					meter = input(ele+': ')
					if meter == '?':
						u.pJson([ele for ele in __codsIdiomas.keys()])
					elif meter in __codsIdiomas:
						contido['idioma'] = meter
						break
				elif ele == 'data_ini':
					meter = kh.getAgora()
					input(ele+': '+meter)
					contido['data_ini'] = meter
					break

				elif ele == 'data_fin':
					meter = kh.getAgora()
					input(ele+': '+meter)
					contido['data_fin'] = meter
					break

				else:
					meter = input(ele+': ')
					contido[ele] = meter
					break
		print('-----------------------')

	return contido
#------------------------------------------------------------------------------------------------
# función auxiliar para a edición dun valor
def editar_aux(nome, tipo):
	# miramos o tipo de contido do que se trata
	if tipo == __codes['serie']:
		# miramos que nos diga un epi válido
		while True:
			cap = input(_(' > Que capítulo? (1x01): ')).lower()
			# so pasamos se o epi ten unha forma váliad
			if u.epi_valido(cap):
				# collemos todos os arquivos da serie que teñan de nome o copitulo dito
				arquivos = [elto for elto in os.listdir(__carpetas['serie']+nome) if cap in elto]
				# se é menor ca un significa que non existe e temos que crealo ou pasar
				if len(arquivos) < 1:
					if u.snValido(input(_('Non está valorado, valorámolo? (s/n): '))) == (True, True):
						valorar_aux(nome, tipo)
					else:
						break
				# se é igual a un podemos crear normal
				elif len(arquivos) == 1:
					ficheiro = __carpetas['serie'] + nome +'/'+ cap+'.json'
					u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))
					break
					# se é maior ca un debemos pedirlle que decida cal quere modificar
				elif len(arquivos) > 1:
					cont = 1
					for elto in arquivos:
						print(cont, ' - ', elto)
						cont += 1
					while True:
						escolla = input(_('*> Escolle o que queres modificar'))
						if escolla.isdigit() and escolla > '0' and escolla <= str(len(arquivos)):
							ficheiro = __carpetas['serie'] + arquivos[escolla] +'/'+ cap+'.json'
							u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))
			else:
				print(_('*> Capítulo inválido.\n'))

	elif tipo == __codes['peli']:
		ficheiro = __carpetas['peli'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['docu']:
		ficheiro = __carpetas['docu'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['video']:
		ficheiro = __carpetas['video'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'audiovisual'))

	elif tipo == __codes['libro']:
		ficheiro = __carpetas['libro'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'literatura'))

	elif tipo == __codes['artigo']:
		ficheiro = __carpetas['artigo'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'literatura'))

	elif tipo == __codes['musica']:
		ficheiro = __carpetas['musica'] + nome+'.json'
		u.gardar_json(ficheiro, edicion_aux(u.cargar_json(ficheiro), 'musica'))

	# debería ser imposible que non coincida con ningún código
	else:
		print(_('Imposible'))
#------------------------------------------------------------------------------------------------
def editar_indice(key, entrada_caderno):
	print('-----------------------')
	nome_vello = entrada_caderno['nome']

	for ele in entrada_caderno:
		print(' > '+ele,': ', entrada_caderno[ele])
		if u.snValido(input(_(' > Cambiar? (s/n): '))) == (True, True):
			while True:
				if ele == 'tipo':
					tipo_vello = entrada_caderno[ele]
					while True:
						meter = input(' > '+ele+' (serie(s), peli(p), docu(d), video(v), libro(l), música(m), artigo(a)): ')
						if meter in __codes.values():
							entrada_caderno[ele] = meter
							break

					# se lle cambiamos o tipo debemos cambiar a carpeta de lugar tamén
					if tipo_vello != meter:
						# devolve o nome que recibe a carpeta
						carpeta_nova = [ele for ele in __codes if __codes[ele] == meter][0]
						carpeta_vella = [ele for ele in __codes if __codes[ele] == tipo_vello][0]
						# miramos se cambiou o nome para remoalo adecuadamente
						if nome_vello == entrada_caderno['nome']:
							fich__ = __carpetas[carpeta_vella]+nome_vello
							# primeiro miramos se hai xiquera algo que mover
							if u.existe_fich(fich__+'.json'):
								shutil.move(fich__+'.json', __carpetas[carpeta_nova])
							elif u.existe_carp(fich__):
								shutil.move(fich__, __carpetas[carpeta_nova])
						else:
							fich__ = __carpetas[carpeta_vella]+nome_vello
							# primeiro miramos se hai xiquera algo que mover
							if u.existe_fich(fich__+'.json'):
								shutil.move(fich__+'.json', __carpetas[carpeta_nova]+entrada_caderno['nome']+'.json')
							elif u.existe_carp(fich__):
								shutil.move(fich__, __carpetas[carpeta_nova]+entrada_caderno['nome'])
						break
				elif ele == 'nota':
					meter = input(' > '+ele+': ')
					if meter.isdigit() and int(meter) >= 0 and int(meter) <= 100:
						entrada_caderno[ele] = meter
						break
				elif ele == 'lonxitude':
					meter = input(' > '+ele+': ')
					if meter.replace(',','').replace('.','').isdigit():
						if entrada_caderno[ele].endswith('minutos'):
							entrada_caderno[ele] = meter + ' minutos'
						else:
							entrada_caderno[ele] = meter + ' páxinas'
						break
				elif ele == 'xenero':
					meter = input(' > '+ele+': ')
					# quitamoslle os posibles acentos
					meter = unidecode(meter)
					if meter == '?':
						u.pJson(__codsXeneros[xenero_base])
					elif meter in __codsXeneros[xenero_base]:
						entrada_caderno['xenero'] = meter
						break
				elif ele == 'idioma':
					meter = input(' > '+ele+': ')
					if meter == '?':
						u.pJson([ele for ele in __codsIdiomas.keys()])
					elif meter in __codsIdiomas:
						entrada_caderno['idioma'] = meter
						break
				elif ele == 'data_ini':
					meter = kh.getAgora()
					input(' > '+ele+': '+meter)
					entrada_caderno['data_ini'] = meter
					break

				elif ele == 'data_fin':
					meter = kh.getAgora()
					input(' > '+ele+': '+meter)
					entrada_caderno['data_fin'] = meter
					break

				else:
					meter = input(' > '+ele+': ')
					entrada_caderno[ele] = meter
					break
		print('-----------------------')

	__indice[key] = entrada_caderno

#------------------------------------------------------------------------------------------------
# función que mostra un contido para editalo
def editar():
	print('\n-----------------------')
	nome = unidecode(input(_(' > Título do contido: ')).lower())
	while True:
		op__ = input(_(' > Editar o caderno(c) ou unha opinión(o): '))
		if op__ in ('c', 'o'):
			break

	for key, ele in __indice.items():
		# se está no índice
		if unidecode(ele['nome']) == unidecode(nome):
			# pasamos o proceso á función auxiliar
			if op__ == 'o':
				editar_aux(ele['nome'], ele['tipo'])
			elif op__ == 'c':
				editar_indice(key, ele)
			print('-----------------------')
			break
	print('\n-----------------------')
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o preciso para comezar o programa
def iniciar():
	# crea todo o sistema de ficheiros
	[u.crear_carp(valor) for valor in __carpetas.values()]
	# carga e devolve o ficheiro de índice
	return u.cargar_json(__findice), u.cargar_json(__fcodsIdiomas), u.cargar_json(__fcodsXeneros)
#------------------------------------------------------------------------------------------------
def gardar():
	print('\n-----------------------')
	print(_('*> Gardando...'))
	u.gardar_json(__findice, __indice)
	#isto para cando se poda modificar dende o programa
	u.gardar_json(__fcodsIdiomas, __codsIdiomas)
	u.gardar_json(__fcodsXeneros, __codsXeneros)
	print(_('*> Gardado'))
	print('-----------------------')
#------------------------------------------------------------------------------------------------
# función que se encarga de facer todo o pertinente para pechar o programa gardandoo
def pechar():
	gardar()
	print(_('*> Talogo'))
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
		print(_('4 - Buscar por titulo'))
		print(_('5 - Editar contido'))
		print(_('6 - Gardar'))

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
	# nome do ficheiro e variable onde se gardarán todos os xeneros coas súas claves
	__fcodsXeneros = '../media/codesXeneros'
	__codsXeneros = {}

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
	__findice = __cbase + 'caderno.json'

	## Asignacións ----------------------
	# se non existe creamos o sistema de carpetas completo
	# metemos en memoria os contidos do ficheiro índice
	__indice, __codsIdiomas, __codsXeneros = iniciar()

	#a# non creo unha función de manual e automático porque só esta pensado para manual
	# diccionario con todas as opcións posibles
	__ops = {'0.': exit,
			'0': pechar,
			'1': engadir,
			'2': valorar,
			'3': mostrar,
			'4': buscar,
			'5': editar,
			'6': gardar
			}

	while True:
		__ops[menu()]()
		input(_('Intro para continuar'))
#------------------------------------------------------------------------------------------------
