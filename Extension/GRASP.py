#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import math
import numpy as np
from operator import attrgetter

def valor_obj(solucion,I):
   vo = [[0] for i in range(len(I.students))] 
   for e in range(len(I.students)):
      for s in solucion[e]: 
         if(vo[e] == [0]):
            vo[e] = (s[0].d * (1 + (I.students[e].stress[s[1]]*math.log(s[1] + 1 ,10))) * math.pow(s[1] + 1 ,math.log(I.students[e].CI,2)))
         else:
            vo[e] = vo[e] + (s[0].d * (1 + (I.students[e].stress[s[1]]*math.log(s[1] + 1 ,10))) * math.pow(s[1] + 1 ,math.log(I.students[e].CI,2)))
   return(vo)

def calificaciones(solucion,I):
   subs = sorted(list(set(int(a.s) for a in I.activities)))
   cal = [[0 for i in range(len(subs))]  for j in range(len(I.students))]
   for e in range(len(I.students)):
      for s in solucion[e]:
         cal[e][int(s[0].s)-1] = cal[e][int(s[0].s)-1] + s[0].v
   
   return cal

def addMandatory(actividades, estudiantes):
   sol = []
   for e in range(len(estudiantes)):
      sol.append([])
      st = 0
      ct = 0
      for a in actividades:
         if(a.o == '1'):
            st = ct
            ct = st + a.d
            sol[e].append([a,st,ct])

   return(sol)

def addAct(solution,activitie, estudiantes):
   for e in range(len(estudiantes)):
      for a in activitie:
         if(a.o == '1'):
            st = ct
            ct = st + a.d
            solution[e].append([a,st,ct])
         
            
def validate_sol(solucion,I):
   
   #  ACT OBLIGATORIAS
   for e in range(len(I.students)):
      a = []
      for s in solucion[e]:
         a.append(s[0].a)
      #if([int(m) for m in I.mandatory] not in a):
      if(not set([int(i) for i in I.mandatory]).issubset(a)):
         return False

   
   #  CALIFICACION MINIMA
   """
   cal = calificaciones(solucion,I)
   subs = sorted(list(set(int(a.s) for a in I.activities)))
   for e in range(len(I.students)):
      for sub in subs:
         if(cal[e][sub-1] < I.kmin):
            return False
  """
   #  REQUERIMIENTOS DE PRESCEDENCIA
   for e in range(len(I.students)):
      for s in solucion[e]:
         r1 = int(requirment1(I,int(s[0].a)-1))
         if( r1 != 0):
            if(inSol(solucion[e],r1)):
               for s2 in solucion[e]:
                  if(s2[0].a == r1):
                     if(s2.ct > s.st):
                        return False
            else:
               return False

   for e in range(len(I.students)):
      for s in solucion[e]:
         r2 = int(requirment2(I,int(s[0].a)-1))
         if( r2 != 0):
            if(inSol(solucion[e],r2)):
               for s2 in solucion[e]:
                  if(s2[0].a == r2):
                     if(s2.ct > s.st):
                        return False
            else:
               return False
   
   return(True)

def inSol(solucion,i):
   a = []
   for s in solucion:
      a.append(s[0].a)
   if(i not in a):
      return False
   
   return True

def requirment1(I,i):
   return(I.activities[i].h1)

def requirment2(I,i):
   return(I.activities[i].h2)


def construct(I):
   #  AGREGAMOS LAS ACTIVIDADES OBLIGATORIAS
   solucion = addMandatory(I.activities, I.students )
   # -----------------	RANKEA ACTIVIDADES (DURACION/VALOR) + ESTRES Y LAS ORDENA ASCENDETE --------------
   max_d = max(I.activities, key=attrgetter('d'))     #  MAXIMA DURACION
   max_v = max(I.activities, key=attrgetter('v'))     #  MAXIMO VALOR
   #valor = [((I.activities[i].d /max_d.d)/(I.activities[i].v/max_v.v)) for i in range(len(I.activities))]
   ordenada = sorted(I.activities, key = lambda x: ((x.d /max_d.d)/(x.v/max_v.v)))     #  ORDENAMOS TODAS LAS ACTIVIDADES DISPONIBLES
   
   #  REMOVEMOS LAS ACTIVIDADES QUE YA SE AGREGARON
   for act in solucion[0]:
      for o in ordenada:
         if(act[0].a == o.a):
            ordenada.remove(o)

   #print(validate_sol(solucion,I))
   # -----------------------------------------------------------------------------------------------------
   
   while(not validate_sol(solucion, I)):		               #	MIENTRAS NO SEA FACTIBLE	
      if(len(ordenada) >= I.RCL):									#	LA LISTA ORDENADA DE ACT ES MAYOR QUE LOS RCL. NECESARIOS
         candidatos = ordenada[:I.RCL]							   #	LISTA RESTRINGIDA DE CANDIDATOS
         quien = random.randint(0,I.RCL-1)						   #	SELECCIONA RANDOM UN CANDIDATO
      else:
         candidatos = ordenada                              # LOS CANDIDATOS SON LOS RESTANTES DE LA LISTA ORDENADA
         if(len(ordenada)>1):
            quien = random.randint(0,len(ordenada)-1)
         else:
            quien = 0

      new_act = candidatos[quien]	                              #	ACTIVIDAD A REMOVER DE LA LISTA DE CANDIDATOS
      
      cal = calificaciones(solucion, I)	#	REGRESA CALIFICACION POR SUBTEMA
      for e in range(len(I.students)):
         if(cal[e][new_act.s-1] < I.kmin):                                  #  SI EL SUBTEMA AUN NO ALCANZA LA KMIN
            lista_aux = []
            lista_pres = []
            lista_aux.append(new_act)
      
         while(len(lista_aux)>0):
            a = lista_aux.pop()
            lista_pres.append(a)
            req1 = requirment1(I,a.a)	                  #	BUSCAMOS SI TIENE 1 REQUERIMIENTO
            if(req1 != 0):
               lista_aux.append(req1)
               req2 = requirment2(I,a.a)	               #	BUSCAMOS SI TIENE 2 REQUERIMIENTOS
               if(req2 != 0):
                  lista_aux.append(req2)
      
         while(len(lista_pres)>0):
            a = lista_pres.pop(-1)
            if(a+1 not in solucion):
               solucion.append(a+1)
            if(a in ordenada):
               ordenada.remove(a)                           #	REMUEVE ACTIVIDAD DE LA LISTA ORDENADA DE ACTIVIDADES RANQUEADAS
      """            
      else:
         ordenada.remove(act)	                              #	REMUEVE ACTIVIDAD DE LA LISTA ORDENADA DE ACTIVIDADES RANQUEADAS
      """
   return(solucion)

"""
def local_search(solucion):
   sol_mejor = solucion.copy()
   restantes = datos[3].copy()					               #	ACTIVIDADES RESTANTES QUE NO PERTENECEN A LA SOLUCION
   restantes = [int(item) for item in restantes]
   for s in solucion:                                          #  CREA UNA LISTA CON ACT QUE NO ESTAN EN LA SOLUCION
      if(s in restantes):
         restantes.remove(s)
   
            
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

def main(I):
   for i in range(I.it):
      sol = construct(I)								                                 #	CONSTRUYE UNA SOLUCION
      if(i < 1):
         sol_mejor = sol.copy()
      #sol_ls = local_search(sol,I)				                                    #	BUSQUEDA LOCAL CON LA SOLUCION GENERADA
      #if(valor_obj(sol_ls) <= valor_obj(sol_mejor)):								#	REEMPLAZA LA MEJOR SOLUCION SI CUMPLE
      #   sol_mejor = sol_ls.copy()
      #print("ITERACION: " +str(i)+ " GRASP VO: " + str(valor_obj(sol_mejor)))       # IMPRIME ITERACION
   return(sol_mejor)