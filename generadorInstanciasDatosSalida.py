#	Version 1 - Juan Pablo - Doctorado PISIS 21/08/2019
#
#	Archivo de entrada de a forma
#	<#> Tipo de arbol, simetrico o asimetrico
#	<#> Cuantas materias
#	<#> Cuantos temas
#	<#> Cuantos subtemas
#	<#> Cuantas actividades
#	<#> Probabilidad de act. obligatoria
#	<#> Probabilidad de 1 act. habilitante
#	<#> Probabilidad de 2 act. habilitantes
#
#
#	La seleccion de un valor y duracion de cada actividad se hizo de la siguiente forma:
#							v = 100/cant.actividades +5 o -3
#							d = 100/cant.actividades +5 o -3
#	
#	Si es o no obligatoria una actividad se hace segun la instancia:
#							Se asigna si, random.random()<= instancia[4]  Ejemplo.- instancia[4] = .2
#	Si tiene o no 1 actividad habilitante:
#							Se asigna si, random.random()<= instancia[5]  Ejemplo.- instancia[5] = .2
#	Si tiene o no 2 actividades habilitantes:
#							Se asiga si, random.random()<= instancia[4]  Ejemplo.- instancia[6] = .2
#-----------------------------------------------------------------------------------------------------
import random
import csv
import os
from tkinter import S

path1 = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\instancias_final\\soluciones\\solucionesEPP\\'
path2 = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\instancias_final\\'

def subject(act):
   t = topic(act)
   if(t%2 == 0):
      return int(t/2)
   else:
      return int(t/2) + 1

def topic(act):
   s = subtopic(act)
   if(s%2 == 0):
      return int(s/2)
   else:
      return int(s/2) + 1

def subtopic(act):
   if(act%11 == 0):
      return int(act/11)
   else:
      return int(act/11) + 1
      

def duration(filename,act):
   with open(path2+filename, 'rt') as f:
      reader = csv.reader(f)
      for row in reader:
         if(act == row[3]):
            return(int(row[4]))

def value(filename,act):
   with open(path2+filename, 'rt') as f:
      reader = csv.reader(f)
      for row in reader:
         if(act == row[3]):
            return(int(row[5]))

def stress(filename,act):
   with open(path2+filename, 'rt') as f:
      reader = csv.reader(f)
      for row in reader:
         if(act == row[3]):
            return(row[6])

#  act_sub_tem_mat_1.0
def create_instance():
   for filename in os.listdir(path1):
      filename_instace = filename[0:5]+'.csv'
      file = open(path1+filename, "r")
      row = []
      instancia = []
      for f in file:
         if(f.endswith('_1.0\n')):
            r = f.split('_')
            row.append((r[0],r[1],r[2],r[3]))
      for a in range(1,89):
         for r in row:
            if(a == int(r[0])):
               d = duration(filename_instace,r[0])
               v = value(filename_instace,r[0])
               s = stress(filename_instace,r[0])
               instancia.append([int(r[3]),int(r[2]),int(r[1]),int(r[0]),d,v,s,0,0,1])
               break
         if(len(instancia)< a):
            m = subject(a)
            t = topic(a)
            s = subtopic(a)
            d = duration(filename_instace,str(a))
            v = value(filename_instace,str(a))
            st = stress(filename_instace,str(a))
            instancia.append([m,t,s,a,d,v,st,0,0,0])
      print(instancia)
      with open(path2+'instancias_EPP\\'+ filename.replace('.txt','.csv'), 'w', newline='') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerows(instancia)
      csvFile.close()

create_instance()
