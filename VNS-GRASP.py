#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd 
import os
import csv
import random
import numpy as np
import time
import math
#  WINDOWS
folder = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\Paper\\instancias\\'
#  LINUX
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado_Linux/Experimentacion/'

nAct_total = 88
vecindarios = 3
kmin = 70
datos = []
ev = 's'

#----------------------------

def read_instance(filename):
   print('_____________________________ '+filename+' ____________________________________________________')
   materias = []
   temas = []
   subtemas = []
   actividades = []
   duracion = []
   valor = []
   estres = []
   habilitamiento1 = []
   habilitamiento2 = []
   obligatorias = []
   with open(folder+filename, 'rt') as f:
      reader = csv.reader(f)
      for row in reader:
         if(len(row)>0):
            if(row[0] != ''):
               materias.append(row[0])
               temas.append(row[1])
               subtemas.append(row[2])
               actividades.append(row[3])
               duracion.append(float(row[4]))
               valor.append(float(row[5]))
               estres.append(float(row[6]))
               habilitamiento1.append((row[3],row[7]))
               habilitamiento2.append((row[3],row[8]))
               if(row[9] == "1"):
                  obligatorias.append(row[3])
   return(list([materias,temas,subtemas,actividades,duracion,valor,estres,habilitamiento1,habilitamiento2,obligatorias]))

def valor_obj(solucion):
   vo = 0
   for actividad in solucion:
      if(actividad != 0):
         indice = int(actividad)-1
         d = int(datos[4][indice])
         e = float(datos[6][indice])
         p = solucion.index(actividad) + 1
         #  EPP-SL
         vo = vo + (d * (1 + e) * math.pow(p,math.log(CI,2)))
      #  EPP-SL
      #vo = vo + (d * (1 + (e*math.log(p,10))) * math.pow(p,math.log(CI,2)))
      #  EPP
      #vo = vo + d
   return(vo)

def validate_sol(sol,ev):
   cal_s = [0] * len(np.unique(datos[2]))									#		CUMPLE CON LA CALIFICACION MINIMA Y MAXIMA
   cal_t = [0] * len(np.unique(datos[1]))
   cal_m = [0] * len(np.unique(datos[0]))
   #   REVISA ACT OBLIGATORIAS
   if(not all(int(item) in sol for item in datos[9])):
      return(False)
   
   #--------------------------------------------------------------------------------------------
   if(ev == 's'):   
      cal_s = calificaciones(sol, np.unique(datos[2]))
         
      for c in cal_s:
         if(c < k):
            return False 						#	ES UNA SOLUCION NO FACTIBLE
   #--------------------------------------------------------------------------------------------
   cuantos_s_x_t = len(np.unique(datos[2])) / len(np.unique(datos[1]))		#	CUANTOS SUBTEMAS HAY POR TEMA
   if ev == 't':
      cal_s = calificaciones(sol, np.unique(datos[2]))
      cont_s = 0
      tem = 0
      
      for s in cal_s:
         cal_t[tem] = cal_t[tem] + s 				 #	 SUMA LA CALIFICACION DE CADA SUBTEMA
         cont_s = cont_s + 1
         if(cont_s >= cuantos_s_x_t): 
            cont_s = 0
            tem = tem + 1
      for i in range(0,len(np.unique(datos[1]))):
         cal_t[i] = cal_t[i]/cuantos_s_x_t 				 #	 PROMEDIOS POR TEMA
            
      for c in cal_t:
         if(c < k):
            return False 						#	ES UNA SOLUCION NO FACTIBLE
         
   #--------------------------------------------------------------------------------------------
   cuantos_t_x_m = len(np.unique(datos[1])) / len(np.unique(datos[0]))	#	CUANTOS TEMAS HAY POR MATERIA
   if(ev == 'm'):
      cal_s = calificaciones(sol, np.unique(datos[2]))
      cont_s = 0
      tem = 0
      for s in cal_s:
         cal_t[tem] = cal_t[tem] + s 				 #	 SUMA LA CALIFICACION DE CADA SUBTEMA
         cont_s = cont_s + 1
         if(cont_s >= cuantos_s_x_t): 
            cont_s = 0
            tem = tem + 1
         
      for i in range(0,len(np.unique(datos[1]))):
         cal_t[i] = cal_t[i]/cuantos_s_x_t 		 #   PROMEDIOS POR TEMA
         cont_t = 0
      
      mat = 0
      for t in cal_t:
         cal_m[mat] = cal_m[mat] + t 				  #  SUMA LA CALIFICACION DE CADA SUBTEMA
         cont_t = cont_t + 1
         if(cont_t >= cuantos_t_x_m): 
            cont_t = 0
            mat = mat + 1

      for i in range(0,len(mat)): 
         cal_m[i] = cal_m[i]/cuantos_t_x_m 				 #	 PROMEDIOS POR MATERIA
      
      for c in cal_m:
         if(c < k): 
            return(False) 						#	ES UNA SOLUCION NO FACTIBLE
         
	#--------------------------------------------------------------------------------------------
	#	CUMPLE CON LOS REQUERIMIENTOS DE PRESCEDENCIA
   for x,y in datos[7]:
      if(x in sol):
         if(y != 0):
            if(not y in sol):
               return(False)
            else:
               i1 = sol.index(x)
               i2 = sol.index(y)
               if(i1 < i2):
                  return(False)

   for x,y in datos[8]:
      if(x in sol):
         if( y != 0):
            if(not y in sol):
               return(False)
            else:
               i1 = sol.index(x)
               i2 = sol.index(y)
               if(i1 < i2):
                  return(False)


   return(True)

def calificaciones(sol,sub):
	cal = [0] * len(sub)

	for act in sol:
		indice = int(act)-1
		s = int(datos[2][indice])
		v = int(datos[5][indice])
		cal[s-1] = cal[s-1] + v 				 #	 SUMA LA CALIFICACION DE CADA ACTIVIDAD

	return cal

def requirment(act,cual):
	if(cual == 1):
		return(datos[7][act][1])
	else:	
		return(datos[8][act][1])

def addMandatory():
   sol = []
   for m in datos[9]:
      sol.append(int(m))
   
   return(sol)

def construct():
   #solucion = []
   solucion = addMandatory()
   req1 = ''
   req2 = ''
   # -----------------	RANKEA ACTIVIDADES (DURACION/VALOR) + ESTRES Y LAS ORDENA ASCENDETE --------------
   max_d = max(datos[4])
   max_v = max(datos[5])
   valor = [((datos[4][i]/max_d)/(datos[5][i]/max_v))+datos[6][i] for i in range(len(datos[4]))] 
   ordenada = list(np.argsort(np.array(valor)))    #  LISTA DE INDICES DE ACTIVIDADES
   for x in solucion:
      ordenada.remove(x-1)
   # -----------------------------------------------------------------------------------------------------
   
   while(not validate_sol(solucion,ev)):		               #	MIENTRAS NO SEA FACTIBLE	
      if(len(ordenada) >= cand):									   #	LA LISTA ORDENADA DE ACT ES MAYOR QUE LOS CAND. NECESARIOS
         candidatos = ordenada[:cand]							   #	LISTA RESTRINGIDA DE CANDIDATOS
         quien = random.randint(0,cand-1)						   #	SELECCIONA RANDOM UN CANDIDATO
      else:
         candidatos = ordenada                              # LOS CANDIDATOS SON LOS RESTANTES DE LA LISTA ORDENADA
         if(len(ordenada)>1):
            quien = random.randint(0,len(ordenada)-1)
         else:
            quien = 0

      act = candidatos[quien]	                              #	ACTIVIDAD A REMOVER DE LA LISTA DE CANDIDATOS
      s = int(datos[2][act])                                #  SUBTEMA DE LA ACTIVIDAD
      cal = calificaciones(solucion, np.unique(datos[2]))	#	REGRESA CALIFICACION POR SUBTEMA
      if(cal[s-1] < k):                                  #  SI EL SUBTEMA AUN NO ALCANZA LA KMIN
         lista_aux = []
         lista_pres = []
         lista_aux.append(act)
      
         while(len(lista_aux)>0):
            a = int(lista_aux.pop())
            lista_pres.append(a)
            req1 = int(requirment(a,1))	                  #	BUSCAMOS SI TIENE 1 REQUERIMIENTO
            if(req1 != 0):
               lista_aux.append(req1-1)
               req2 = int(requirment(a,2))	               #	BUSCAMOS SI TIENE 2 REQUERIMIENTOS
               if(req2 != 0):
                  lista_aux.append(req2-1)
         
         while(len(lista_pres)>0):
            a = int(lista_pres.pop(-1))
            if(a+1 not in solucion):
               solucion.append(a+1)
            if(a in ordenada):
               ordenada.remove(a)                           #	REMUEVE ACTIVIDAD DE LA LISTA ORDENADA DE ACTIVIDADES RANQUEADAS
               
      else:
         ordenada.remove(act)	                              #	REMUEVE ACTIVIDAD DE LA LISTA ORDENADA DE ACTIVIDADES RANQUEADAS
         
   return(solucion)

def local_search(solucion):
   sol_mejor = solucion.copy()
   restantes = datos[3].copy()					               #	ACTIVIDADES RESTANTES QUE NO PERTENECEN A LA SOLUCION
   restantes = [int(item) for item in restantes]
   for s in solucion:                                          #  CREA UNA LISTA CON ACT QUE NO ESTAN EN LA SOLUCION
      if(s in restantes):
         restantes.remove(s)
   
   """         
   for i in range(len(solucion)):						#	INTERCAMBIA CADA ACTIVIDAD i DE LA SOLUCION POR OTRA J DE LAS RESTANTES
      for j in range(len(restantes)):
         aux = solucion[i]
         solucion[i] = restantes[j]                #  LOS CAMBIA SIEMPRE DE IZQ A DERECHA EN ORDEN
         restantes[j] = aux
         if(validate_sol(solucion,'s') and (valor_obj(solucion) <= valor_obj(sol_mejor))):
            #sol_mejor = solucion.copy()					#	REASIGNA LA PRIMER MEJOR SOLUCION
            return(solucion)
         else:
            aux = solucion[i]						   #	DEVUELVE LA SOLUCION A SU ESTADO INICIAL
            solucion[i] = restantes[j]
            restantes[j] = aux
   """
   cont = 0
   while(True):
      cont = cont + 1
      i = random.randint(0,len(solucion)-1)						#	INTERCAMBIA CADA ACTIVIDAD i DE LA SOLUCION POR OTRA J DE LAS RESTANTES
      if((i not in datos[7]) and (i not in datos[8])):
         for j in range(len(restantes)):
            aux = solucion[i]
            solucion[i] = restantes[j]                #  LOS CAMBIA SIEMPRE DE IZQ A DERECHA EN ORDEN
            restantes[j] = aux
            if(validate_sol(solucion,'s') and (valor_obj(solucion) <= valor_obj(sol_mejor))):
               #sol_mejor = solucion.copy()					#	REASIGNA LA PRIMER MEJOR SOLUCION
               return(solucion)
            else:
               aux = solucion[i]						   #	DEVUELVE LA SOLUCION A SU ESTADO INICIAL
               solucion[i] = restantes[j]
               restantes[j] = aux
      if(cont == 1000):
         return solucion
               

#---------------------------------INICIA FUNCION PRINCIPAL-----------------------------------------------------
def grasp():
   i = 1
   while(i <= iteraciones):
      sol = construct()								                                 #	CONSTRUYE UNA SOLUCION
      sol_ls = local_search(sol)				                                    #	BUSQUEDA LOCAL CON LA SOLUCION GENERADA
      if(i == 1):
         sol_mejor = sol.copy()
      else:                                                                   #  SI LA SOLUCION ES MEJOR ACTUALIZA
         if(valor_obj(sol_ls) <= valor_obj(sol_mejor)):								#	REEMPLAZA LA MEJOR SOLUCION SI CUMPLE
            sol_mejor = sol_ls.copy()
      
      #print("ITERACION: " +str(i)+ " GRASP VO: " + str(valor_obj(sol_mejor)))       # IMPRIME ITERACION
      i = i + 1
   return(sol_mejor)
#---------------------------------TERMINA FUNCION PRINCIPAL-----------------------------------------------------

def shaking_vns(sol_,k):
	sol_agitada = sol_.copy()
	cuantos_intentos = 30
	if(k==1):
		#	INTERCAMBIA DOS ACTIVIDADES
		i1 = random.randint(0,len(sol_agitada)-1)
		i2 = random.randint(0,len(sol_agitada)-1)
		while(i1 == i2):
			i2 = random.randint(0,len(sol_agitada)-1)
		aux = sol_agitada[i1]
		sol_agitada[i1] = sol_agitada[i2]
		sol_agitada[i2] = aux
		
		cont = 0
		flag = validate_sol(sol_agitada,ev)
		#while(not validate_sol(sol_agitada,kmin,kmax,datos[10],datos[8],datos[9],sub)):
		while(not flag):
			if(cont > cuantos_intentos):
				return(sol_)
			aux = sol_agitada[i1]
			sol_agitada[i1] = sol_agitada[i2]
			sol_agitada[i2] = aux
			
			i1 = random.randint(0,len(sol_agitada)-1)
			i2 = random.randint(0,len(sol_agitada)-1)
			cont = cont + 1

			while(i1 == i2):
				i2 = random.randint(0,len(sol_agitada)-1)
			aux = sol_agitada[i1]
			sol_agitada[i1] = sol_agitada[i2]
			sol_agitada[i2] = aux
			flag = validate_sol(sol_agitada,ev)

	elif(k==2):
		#	INTERCAMBIA TRES ACTIVIDADES
		i1 = random.randint(0,len(sol_agitada)-1)
		i2 = random.randint(0,len(sol_agitada)-1)
		i3 = random.randint(0,len(sol_agitada)-1)
		while((i1 == i2) or (i1 == i3) or (i2 == i3)):
			i2 = random.randint(0,len(sol_agitada)-1)
			i3 = random.randint(0,len(sol_agitada)-1)
		aux = sol_agitada[i1]
		sol_agitada[i1] = sol_agitada[i2]
		sol_agitada[i2] = sol_agitada[i3]
		sol_agitada[i3] = aux
		
		cont = 0
		flag = validate_sol(sol_agitada,ev)
		#while(not validate_sol(sol_agitada,kmin,kmax,datos[10],datos[8],datos[9],sub)):
		while(not flag):
			if(cont > cuantos_intentos):
				return(sol_)
			aux = sol_agitada[i3]
			sol_agitada[i3] = sol_agitada[i2]
			sol_agitada[i2] = sol_agitada[i1]
			sol_agitada[i1] = aux
			cont = cont + 1
			i1 = random.randint(0,len(sol_agitada)-1)
			i2 = random.randint(0,len(sol_agitada)-1)
			i3 = random.randint(0,len(sol_agitada)-1)
			while((i1 == i2) or (i1 == i3) or (i2 == i3)):
				i2 = random.randint(0,len(sol_agitada)-1)
				i3 = random.randint(0,len(sol_agitada)-1)
			aux = sol_agitada[i1]
			sol_agitada[i1] = sol_agitada[i2]
			sol_agitada[i2] = sol_agitada[i3]
			sol_agitada[i3] = aux
			flag = validate_sol(sol_agitada,ev)
	else:
		#	INTERCAMBIA CUATRO ACTIVIDADES
		i1 = random.randint(0,len(sol_agitada)-1)
		i2 = random.randint(0,len(sol_agitada)-1)
		i3 = random.randint(0,len(sol_agitada)-1)
		i4 = random.randint(0,len(sol_agitada)-1)
		while((i1 == i2) or (i1 == i3) or (i1 == i4) or (i2 == i3) or (i2 == i4) or (i3 == i4)):
			i2 = random.randint(0,len(sol_agitada)-1)
			i3 = random.randint(0,len(sol_agitada)-1)
			i4 = random.randint(0,len(sol_agitada)-1)
		aux = sol_agitada[i1]
		sol_agitada[i1] = sol_agitada[i2]
		sol_agitada[i2] = sol_agitada[i3]
		sol_agitada[i3] = sol_agitada[i4]
		sol_agitada[i4] = aux
		
		cont = 0
		flag = validate_sol(sol_agitada,ev)
		#while(not validate_sol(sol_agitada,kmin,kmax,datos[10],datos[8],datos[9],sub)):
		while(not flag):
			if(cont > cuantos_intentos):
				return(sol_)

			aux = sol_agitada[i4]
			sol_agitada[i4] = sol_agitada[i3]
			sol_agitada[i3] = sol_agitada[i2]
			sol_agitada[i2] = sol_agitada[i1]
			sol_agitada[i1] = aux
			cont = cont + 1
			i1 = random.randint(0,len(sol_agitada)-1)
			i2 = random.randint(0,len(sol_agitada)-1)
			i3 = random.randint(0,len(sol_agitada)-1)
			i4 = random.randint(0,len(sol_agitada)-1)
			while((i1 == i2) or (i1 == i3) or (i1 == i4) or (i2 == i3) or (i2 == i4) or (i3 == i4)):
				i2 = random.randint(0,len(sol_agitada)-1)
				i3 = random.randint(0,len(sol_agitada)-1)
				i4 = random.randint(0,len(sol_agitada)-1)
			aux = sol_agitada[i1]
			sol_agitada[i1] = sol_agitada[i2]
			sol_agitada[i2] = sol_agitada[i3]
			sol_agitada[i3] = sol_agitada[i4]
			sol_agitada[i4] = aux
			flag = validate_sol(sol_agitada,ev)

	return(sol_agitada)

def local_search_vns(sol_in,k,i):
	sol_mejor = sol_in.copy()
	c = 1
	while(c < nAct_total):
		sol_vecino = shaking_vns(sol_in,k)
		if(valor_obj(sol_vecino) < valor_obj(sol_mejor)):
			sol_mejor = sol_vecino.copy()
		c = c + 1
	return(sol_mejor)

def vns():
   solucion_inicial = grasp()
   print('VO GRASP:   ' + str(valor_obj(solucion_inicial)))
   solucion_inicial = solucion_inicial + ([0] * (88-len(solucion_inicial)))
   i = 1
   mejor_sol = solucion_inicial.copy()
   while(i < iteraciones_vns):
      k = 1
      while(k <= vecindarios):
         sol_sh = shaking_vns(solucion_inicial.copy(),k)
         nueva_sol = local_search_vns(sol_sh.copy(),k,i)
         #print('VO NUEVA: ' + str(valor_obj(sol_nueva)) + 'VO MEJOR: ' + str(valor_obj(sol_best)))
         if(valor_obj(nueva_sol) <= valor_obj(mejor_sol)):
            mejor_sol = nueva_sol.copy()
         else:
            k = k + 1
      #print("ITERACION: " +str(i)+ " VNS VO: " + str(valor_obj(mejor_sol)))       # IMPRIME ITERACION
      i = i + 1
   return(mejor_sol)


f = open(folder + 'soluciones/SolucionesVNS_GRASP/VNS_GRASP.csv' , "w")
g = open(folder + 'soluciones/SolucionesVNS_GRASP/soluciones_VNS_GRASP.csv' , "w")
for CI in [0.99,0.95,1.03]:
   for cand in range(30,31,5):
      for iteraciones in range(100,101,10):
         for iteraciones_vns in range(150,151,50):
            for filename in os.listdir(folder):
               if filename.endswith(".csv"):
                  nombre = filename.split('_')
                  datos = read_instance(filename)
                  for k in range(kmin,101,5):
                     start_time = time.time()
                     sol_final = vns()
                     runtime = time.time() - start_time
                     f.write(nombre[0] + ',' + nombre[1] + ',' + nombre[2].replace('.csv','') + ',' + str(k) + ',' + str(CI) + ',' + ev + ',' + 'VNS_EPP-SL,' + str(cand) + ',' + str(iteraciones) + ',' + str(iteraciones_vns) + ',' + str(valor_obj(sol_final)) + "," + str(runtime) + "," + str(len(sol_final)) + '\n' )
                     print("CAND: "+ str(cand) + "  IT GRASP: " + str(iteraciones) + "  IT VNS: " + str(iteraciones_vns) +"  CI: " + str(CI) + "  KMIN: " + str(k) + "  RUNTIME: " + str(runtime) + "  SOL FINAL: " + str(valor_obj(sol_final)))
                     g.write(nombre[0] + ',' + nombre[1] + ',' + nombre[2].replace('.csv','') + ',' + str(k) + ',' + str(CI) + ',' + ev + ',' + 'VNS_EPP-SL,' + str(cand) + ',' + str(iteraciones) + ',' + str(sol_final+([0] * (88-len(sol_final)))).replace('[','').replace(']','') + '\n' )
                  datos = []
f.close()
g.close()
	


