from EPP_scheduling_POO_instance import Instancia
import matplotlib.pyplot as plt
import pandas as pd

class Solucion:
   def __init__(self, act, subt, duration, value, h, st, ct, r):
      self.act = act
      self.subt = subt
      self.duration = duration
      self.value = value
      self.h = h
      self.st = st
      self.ct = ct
      self.r = r
      
   
def add_to_sol(solution):
   seq = []
   I = Instancia()
   for s in solution:
      for h in I.estudiantes:
         for a in I.actividades():
            if(s[0].startswith('_x['+ a.a + ',' + a.s + ',' + str(h) )):
               act = a.a
               sub = a.s
               duration = a.d
               value = a.v
               student = str(h)
               st = '0'
               ct = '0'
               resource = a.r
               for s1 in solution:
                  if(s1[0].startswith('_st['+ a.a + ',' + a.s + ',' + str(h))):
                     st = str(s1[1])
               for s2 in solution:
                  if(s2[0].startswith('_ct['+ a.a + ',' + a.s + ',' + str(h))):
                     ct = str(s2[1])
               seq.append(Solucion(act,sub,duration,value,student,st,ct,resource))
   return seq
      
   
def print_sol(seq):
   for s in seq:
      print('[ a:' + s.act + ' , s:' + s.subt + ' , h:' + s.h + ' , st:' + s.st + ' , ct:' + s.ct + ' ]' )


def check_factibility(sol):
   I = Instancia()
   
   flag = True
   log_error = []
   
   act=[]
   for h in I.estudiantes:
      act.append([])
      for a in sol:
         if(int(a.h) == h):   
            act[h-1].append(a.act)
               
   #  No actividades repetidas en la secuencia de un mismo estudiante
   for h in I.estudiantes:
      if(len(act[h-1]) != len(set(act[h-1]))):
         log_error.append('Hay actividades duplicadas en la ruta del estudiante:' + str(h))
         flag = False
   #  --------------------------------------------------------------------------------------------
   #  No superposicion
   for h in I.estudiantes:
      for a in sol:
         for a2 in sol:
            if((a.act != a2.act) ):
               if((a.h == str(h)) and (a2.h == str(h))):
                  if(a.st == a2.st):
                     log_error.append('La actividad:' + a.act + ' del estudiante '+  str(h) + ' tiene el mismo start time de la actividad ' + a2.act)
                     flag = False
   #  --------------------------------------------------------------------------------------------
   
   #  Respeta los due dates
   for h in I.estudiantes:
      for a in sol:
         for d in I.dueDate:
            if(a.act == d[0]):
               if(float(a.ct) > int(d[1])):
                  log_error.append('La actividad:' + a.act + ' del estudiante '+  str(h) + ' se programo despues de su due date ' + str(d[1]) )
                  flag = False
   
   
   #  --------------------------------------------------------------------------------------------
   #  Asigna los recursos correctos
   for a in sol:
      for a2 in sol:
         if((a.r != '0') and (a2.r != '0') and (a.r == a2.r) and (a.st == a2.st) and (a.h != a2.h)):
            if((float(a.st) <= float(a2.st)) and (float(a.ct) >= float(a2.st))):
               log_error.append('La actividad: ' + a.act + ' del estudiante: '+ a.h + ' con el recurso: '+  a.r + ' se superpone con la actividad: ' + a2.act + ' del estudiante: ' + a2.h + ' con el recurso: '+  a2.r )
               flag = False
            
   #  --------------------------------------------------------------------------------------------
   #  Cumple los score kmin y kmax
   for h in I.estudiantes:
      scores = [0]*len(I.subtemas())
      for a in sol:
         for sub in I.subtemas() :
            if((a.h == str(h)) and (a.subt == sub)):
               scores[int(sub)-1] = scores[int(sub)-1] + int(a.value)
   for s in scores:
      if(s < I.kmin):
         log_error.append('El score:' + str(s) + ' del estudiante '+  str(h) + ' es menor que el kmin ' + str(I.kmin) )
         flag = False
      if(s > I.kmax):
         log_error.append('El score:' + str(s) + ' del estudiante '+  str(h) + ' es mayor que el kmax ' + str(I.kmax) )
         flag = False
   #  --------------------------------------------------------------------------------------------
   #  Actividades en equipo
   for eq in I.teams:
      for h in I.estudiantes:
         for h2 in I.estudiantes:
            if((h != h2) and ( h in I.teams[eq] and h2 in I.teams[eq])):
               for a in sol:
                  if(a.act in I.team_activitie):
                     for a2 in sol:
                        if(a.act == a2.act):
                           if(a.h == str(h) and a2.h == str(h2)):
                              if(a.st != a2.st):
                                 log_error.append('La actividad:' + a.act + ' del estudiante '+  str(h) + ' no esta alineada con el estudiante ' + str(h2) )
                                 flag = False
   #  --------------------------------------------------------------------------------------------
   #  Actividades obligatorias 
   for h in I.estudiantes:
      for o in I.obligatorias():
         if(o not in act[h-1]):
            log_error.append('La actividad obligatoria: ' + o + ' del estudiante: '+ str(h) + ' no se asigno')
            flag = False
   #  --------------------------------------------------------------------------------------------
   
   
   return flag, log_error


def plot_schedule(seq):
   fig, gnt = plt.subplots()

   # Setting Y-axis limits
   gnt.set_ylim(0, 500)

   # Setting X-axis limits
   gnt.set_xlim(0, 6)

   # Setting labels for x-axis and y-axis
   gnt.set_xlabel('Duration')
   gnt.set_ylabel('Student')

   # Setting ticks on y-axis
   gnt.set_yticks([15, 25, 35])
   # Labelling tickes of y-axis
   gnt.set_yticklabels(['1', '2', '3'])

   # Setting graph attribute
   gnt.grid(True)

   # Declaring a bar in schedule
   gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange'))

   # Declaring multiple bars in at same level and same width
   gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                     facecolors ='tab:blue')

   gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                           facecolors =('tab:red'))

   plt.savefig("gantt1.png")
