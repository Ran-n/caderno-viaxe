#! /usr/bin/python3
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	02/08/2019 15:11:57
#+ Editado:	02/08/2019 15:11:57
## do ficheiro caderno-viaxe.py
#------------------------------------------------------------------------------------------------
import os
import subprocess
import sys
#------------------------------------------------------------------------------------------------
# cambiamos ao subdirectorio
os.chdir('src')
valores = sys.argv[1:]
valores.insert(0,'caderno-viaxe.py')
valores.insert(0,'python3')
# facemos a chamada á función
subprocess.call(valores)
#------------------------------------------------------------------------------------------------
