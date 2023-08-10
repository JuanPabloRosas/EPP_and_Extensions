#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import time
import GRASP
import csv
from gurobipy import tuplelist

class Actividad:
   def __init__(self, num_act, sub, tem, mat, duracion, valor, obligatoria, equipo, habilitamiento1, habilitamiento2, recurso, limite_tiempo ):
      self.a = num_act
      self.s = sub
      self.t = tem
      self.m = mat
      self.d = duracion
      self.v = valor
      self.o = obligatoria
      self.eq = equipo
      self.h1 = habilitamiento1
      self.h2 = habilitamiento2
      self.r = recurso
      self.dd = limite_tiempo

class Estudiante:
   def __init__(self, stress, CI):
      self.stress = stress
      self.CI = CI     
               
class Instancia:
   def __init__(self,k_min,k_max,RCL,it,ev):
      self.teams = {1:(1,2), 2:(3,4,5)}
      self.kmin = k_min
      self.kmax = k_max
      self.RCL = RCL   
      self.it = it
      self.ev = ev
      self.activities=[]
      self.mandatory=[]
      self.dueDate=[]
      self.team_activitie=[]
      self.students = []
   
   def leeInstancia(self, filename):
      print('----------------------------------------'+ filename +'----------------------------------------' )
      with open(filename, 'rt') as f:
         reader = csv.reader(f)
         for row in reader:
            actividad = Actividad(int(row[3]),row[2],row[1],row[0],int(row[4]),int(row[5]),row[8],row[9],row[6],row[7],row[10],int(row[11]))
            self.activities.append(actividad)
            self.dueDate.append((row[3],row[11]))
            if(row[8] == '1'):
               self.mandatory.append(row[3])
            if(row[9] == '1'):
               self.team_activitie.append(row[3])
   
   def leeEstudiantes(self, filename, CI):
      estres = []
      with open(filename, 'rt') as f:
         reader = csv.reader(f)
         for row in reader:
            if(int(row[1]) == 1):
               estres.append([])
               
            estres[int(row[0])-1].append(float(row[2]))
            if(int(row[1]) == 400):
               self.students.append(Estudiante(estres[int(row[0])-1], CI))
                  
   def arcos(self):
      arcs = tuplelist()
      for a in self.activities:
         arcs.append((a.a,a.s))
      return arcs
   
   def subtemas(self):
      s = []
      for a in self.activities:
         if(a.s not in s):
            s.append(a.s)
      return s
         
   def temas(self):
      t = []
      for a in self.activities:
         if(a.t not in t):
            t.append(a.t)
      return t
   
   def materias(self):
      m = []
      for a in self.activities:
         if(a.m not in m):
            m.append(a.m)
      return m

#  WINDOWS
folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\EPP_and_Extensions\\Extension\\Instancias\\'
#  LINUX
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado_Linux/Experimentacion/'

#f = open(folder + 'soluciones/solucionesGRASP_MATEHEURISTIC/GRASP.csv' , "w")
#g = open(folder + 'soluciones/SolucionesGRASP_MATEHEURISTIC/soluciones_GRASP.csv' , "w")

for RCL in range(30,31,5):
   for iteraciones in range(100,101,10):
      for CI in [0.99,0.95,1.03]:
         for kmin in range(70,101,5):
            I = Instancia(kmin,100,RCL,iteraciones,'s')
            I.leeInstancia(folder + 'test.csv')
            I.leeEstudiantes(folder + 'estudiantes.csv', CI)

            start_time = time.time()
            sol_final = GRASP.main(I)
            runtime = time.time() - start_time
            
            #f.write(nombre[0] + ',' + nombre[1] + ',' + nombre[2].replace('.csv','') + ',' + str(k) + ',' + str(CI) + ',' + ev + ',' + 'GRASP_EPP-SL,' + str(cand) + ',' + str(iteraciones) + ',' + str(valor_obj(sol_final)) + "," + str(runtime) + "," + str(len(sol_final)) + '\n' )
            print("CAND: "+ str(RCL) + "  IT GRASP: " + str(iteraciones) +"  CI: " + str(CI) + "  KMIN: " + str(kmin) + "  RUNTIME: " + str(runtime) + "  SOL FINAL: " + str(GRASP.valor_obj(sol_final)))
            #g.write(nombre[0] + ',' + nombre[1] + ',' + nombre[2].replace('.csv','') + ',' + str(k) + ',' + str(CI) + ',' + ev + ',' + 'GRASP_EPP-SL,' + str(cand) + ',' + str(iteraciones) + ',' + str(sol_final+([0] * (88-len(sol_final)))).replace('[','').replace(']','') + '\n' )
            del I
#f.close()
#g.close()
	


