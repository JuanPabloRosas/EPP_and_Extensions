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
      
   def act(self):
      return self.a
   def subtema(self):
      return self.s
   def tema(self):
      return self.t
   def materia(self):
      return self.m
   def duracion(self):
      return self.d
   def valor(self):
      return self.v 
   def obl(self):
      return self.o
   def equipo(self):
      return self.eq
   def hab1(self):
      return self.h1
   def hab2(self):
      return self.h2
   def rec(self):
      return self.r
   def dueDate(self):
      return self.dd

class Estudiante:
   def __init__(self, stress):
      self.stress = stress
      
class Instancia:
   def __init__(self):
      #self.estudiantes = [1,2,3,4,5]
      self.teams = {1:(1,2), 2:(3,4,5)}
      self.kmin = 70
      self.kmax = 120
   
   students = []
   activities=[]
   mandatory=[]
   dueDate=[]
   team_activitie=[]
   
   def leeInstancia(self, filename):
      print('----------------------------------------'+ filename +'----------------------------------------' )
      with open(filename, 'rt') as f:
         reader = csv.reader(f)
         for row in reader:
            actividad = Actividad(row[3],row[2],row[1],row[0],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
            self.activities.append(actividad)
            self.dueDate.append((row[3],row[11]))
            if(row[6] == '1'):
               self.mandatory.append(row[3])
            if(row[7] == '1'):
               self.team_activitie.append(row[3])
      return self.activities
   
   def leeEstudiantes(self, students):
      estres = []
      with open(students, 'rt') as f:
         reader = csv.reader(f)
         for row in reader:
            if(int(row[1]) == 1):
               estres.append([])
            estres[int(row[0])-1].append(float(row[2]))
            if(int(row[1]) == 400):
               self.students.append(Estudiante(estres[int(row[0])-1]))
            
      return self.students
   
   def actividades(self):
      return self.activities
   
   def obligatorias(self):
      return self.mandatory

   def estudiantes(self):
      return self.students
   
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
         