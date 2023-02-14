#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gurobipy import *
from gurobipy import tuplelist
import csv

import numpy as np
import EPP_PSL
import EPP_PSL
import EPP
import os




#	LEE INSTANCIA
# #-----------------------------------------------------------------
#	WINDOWS
folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\instancias_final\\instancias_EPP\\'
#carpeta = "soluciones/final/"
#	LINUX
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado/ExperimentacionGurobi/instancias_nuevas/caso_real/'
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado/ExperimentacionGurobi/instancias/'


for filename in os.listdir(folder):
   if filename.endswith('.csv'):
      print('----------------------------------------'+ filename +'----------------------------------------' )
      materias = []
      temas = []
      subtemas = []
      actividades = []
      obligatorias = []
      habilitamiento1 = {}
      habilitamiento2 = {}
      duracion = {}
      valor = {}
      estres = []
      with open(folder+filename, 'rt') as f:
         reader = csv.reader(f)
         for row in reader:
            materias.append(row[0])
            temas.append(row[1])
            subtemas.append(row[2])
            actividades.append(row[3])
            duracion[(row[3],row[2],row[1],row[0])]=float(row[4])
            valor[(row[3],row[2],row[1],row[0])]=float(row[5])
            estres.append(float(row[6]))
            if(row[7]!="0"):
               habilitamiento1[row[3]]=row[7]
            if(row[8]!="0"):
               habilitamiento2[row[3]]=row[8]
            if(row[9] == "1"):
               obligatorias.append((row[3],row[2],row[1],row[0]))
      arcs=[]
      
      for i in range(0,88):
         if ((actividades[i],subtemas[i],temas[i],materias[i]) in duracion):
            arcs.append((actividades[i],subtemas[i],temas[i],materias[i]))

      arcs = tuplelist(arcs)

		#	CREA ARCHIVO SALIDA
		# #-----------------------------------------------------------------
      CI_test=[0.95,0.99,1.03]
      ev = 's'
      k = int(filename.split('_')[3])
      """
      f1= open(folder+'soluciones/'+filename.replace('.csv','.txt'),"w+")
      ppeCISec_sol=EPP.ppeCISec(k,actividades,np.unique(subtemas),np.unique(temas),np.unique(materias),obligatorias,habilitamiento1, habilitamiento2, duracion,valor,arcs)
      if ppeCISec_sol is not None:
         for v in ppeCISec_sol:
            f1.write(v+'\n')
      f1.close()
      """
      #"""		
      for CI in CI_test:
         f2= open(folder+'soluciones/'+filename.split('.')[0]+'_'+str(k)+'_'+str(CI)+'_'+ev+'_'+'EPP-SL'+'.txt',"w+")
         ppeCISec_sol=EPP_PSL.ppeCISec(k,actividades,np.unique(subtemas),np.unique(temas),np.unique(materias),obligatorias,habilitamiento1, habilitamiento2, duracion,valor,estres,CI,arcs)
         if ppeCISec_sol is not None:
            for v in ppeCISec_sol:
               f2.write(v+'\n')
               #print(v)
         f2.close()
      #"""
