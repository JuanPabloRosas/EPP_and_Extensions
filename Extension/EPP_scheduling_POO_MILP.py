#		V1.0 Educational Planning Problem (PPE) like Scheduling Problem POO - Gurobi - Python
#		Autor: Juan Pablo Rosas Baldazo		29/09/22
#		
#		
#-------------------------------------------------------------------------------------------
from ast import Expr
from parser import expr
import gurobipy as gp
from gurobipy import GRB
import time
import math 
from EPP_scheduling_POO_instance import Instancia

         
def EPP_scheduling():
   start_time = time.time()	
   M =  500                     #  Big M
   #	Crea ambiente
   model = gp.Model('EPP')
   model.setParam('TimeLimit', 300)
   # #	Variables
   # -------------------------------------------------------------------------------------
	
   I = Instancia()
   
   #  Makespan por estudiante, solo acumula la duración del learning path
   """
   _mk={}
   for h in I.students:
      for a in I.actividades():
         _mk[a.s,h] = model.addVar(lb= 0, vtype = GRB.INTEGER ,name='_mk[%s,%s]' % (a.s,h))
   """
   #	La actividad act_a,s,t,m se realiza por el estudiante h      
   _x={}
   for h in range(0,len(I.students)):
      for a in I.actividades():
         for t in range(0,len(I.students[h].stress)):
            _x[a.a,a.s,h,t] = model.addVar(0.0, 1.0, vtype = GRB.BINARY ,name='_x[%s,%s,%s,%s]' % (a.a,a.s,h,t))
   
   #  Tiempo de inicio
   """
   _st = {}
   for h in range(0,len(I.students)):
      for a in I.actividades():
         _st[a.a,a.s,h] = model.addVar(lb = 0, vtype = GRB.INTEGER ,name='_st[%s,%s,%s]' % (a.a,a.s,h))
   """
   #  Tiempo de completitud
   _ct ={}
   for h in range(0,len(I.students)):
      for a in I.actividades():
         _ct[a.a,a.s,h] = model.addVar(vtype = GRB.CONTINUOUS ,name='_ct[%s,%s,%s]' % (a.a,a.s,h))

   #  Precedencia, vale 1 si la actividad alfa habilia la alfa prima
   _p={}
   for a in I.actividades():
      for a2 in I.actividades():
         for h in range(0,len(I.students)):
            _p[a.a,a2.a,h] = model.addVar(0.0, 1.0, vtype=GRB.BINARY ,name='_p_%s_%s_%s' % (a.a,a2.a,h))
   
   #  Recursos
   _r={}
   for h in range(0,len(I.students)):
      for a in I.actividades():
         for h2 in range(0,len(I.students)):
            for a2 in I.actividades():
               _r[a.a,a2.a,h,h2] = model.addVar(0.0, 1.0, vtype=GRB.BINARY ,name='_r_%s_%s_%s_%s' % (a.a,a2.a,h,h2))
   
   model.update()

	#	Restricciones
	#-------------------------------------------------------------------------------------   
   #  Score
   for h in range(0,len(I.students)):
      for sub in I.subtemas() :
         for t in range(0,len(I.students[h].stress)):
            #	Score mayor a kmin por subtema
            model.addConstr(gp.quicksum(int(a.v) * _x[a.a,a.s,h,t] for a in I.actividades() if a.s == sub) >= I.kmin,"Kmin_%s_%s" % (a.s,h))
            #	Score menor a kmax por subtema
            model.addConstr(gp.quicksum(int(a.v) * _x[a.a,a.s,h,t] for a in I.actividades() if a.s == sub) <= I.kmax,"Kmax_%s_%s" % (a.s,h))
   
	#-------------------------------------------------------------------------------------
   #	Actividades Obligatorias
   #"""
   for h in range(0,len(I.students)):
      for a in I.actividades():
         if(a.o == '1'):
            model.addConstr(gp.quicksum(_x[a.a,a.s,h,t] for t in range(0,len(I.students[h].stress))) == 1, "mandatory_%s_%s_%s_%s" % (a.a,a.s,h,t))
   #"""   
	#-------------------------------------------------------------------------------------
   for h in range(0,len(I.students)):
      for a in I.actividades():
         for t in range(0,len(I.students[h].stress)):
            """
            #  Completation time
            model.addConstr(_ct[a.a,a.s,h] == _st[a.a,a.s,h] + (int(a.d) * (1 + I.students[h].stress[t] ))  * _x[a.a,a.s,h,t], "ct_%s_%s_%s" % (a.a,a.s,h))
            """
            #model.addConstr(_ct[a.a,a.s,h] == t + (int(a.d) * (1 + I.students[h].stress[t] ))  * _x[a.a,a.s,h,t], "ct_%s_%s_%s" % (a.a,a.s,h))
            model.addConstr(_ct[a.a,a.s,h] == t + (int(a.d)) * _x[a.a,a.s,h,t], "ct_%s_%s_%s" % (a.a,a.s,h))
            #  Start time
            #model.addConstr(t <= M - int(a.d)  * _x[a.a,a.s,h,t], "st_%s_%s_%s" % (a.a,a.s,h))
            #  Due dates      
            model.addConstr(_ct[a.a,a.s,h] <= int(a.dd), "dd_%s_%s_%s" % (a.a,a.s,h))
   #-------------------------------------------------------------------------------------
   #"""
   #  Precedence
   for h in range(0,len(I.students)):
      for a in I.actividades():
         for a2 in I.actividades():
            for t in range(0,len(I.students[h].stress)):
               for t2 in range(0,len(I.students[h].stress)):
                  if(a.a!=a2.a):
                     #model.addConstr(_p[a.a,a2.a,h] >= _x[a.a,a.s,h] + _x[a2.a,a2.s,h] - 1, "pre_%s_%s" % (a.a,a2.a))
                     #model.addConstr(_p[a.a,a2.a,h] <= _x[a.a,a.s,h] , "p_a_%s" % (a.a))
                     #model.addConstr(_p[a.a,a2.a,h] <= _x[a2.a,a2.s,h] , "p_a2_%s" % (a2.a))
                     #model.addConstr(_p[a.a,a2.a,h] - _p[a2.a,a.a,h] <= 1 , "p-p2_%s_%s" % (a.a,a2.a))
                     
                     #model.addConstr(_ct[a.a,a.s,h] <= _st[a2.a,a2.s,h] + M*(3 - _p[a.a,a2.a,h] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h,t]) , "seq_%s_%s_%s" % (a.a,a2.a,h))
                     #model.addConstr(_ct[a2.a,a2.s,h] <= _st[a.a,a.s,h] + M*(2 + _p[a.a,a2.a,h] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h,t]), "seq_%s_%s_%s" % (a2.a,a.a,h))
                     model.addConstr(_ct[a.a,a.s,h] <= t2 + M * (3 - _p[a.a,a2.a,h] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h,t2]) , "seq_%s_%s_%s" % (a.a,a2.a,h))
                     model.addConstr(_ct[a2.a,a2.s,h] <= t + M * (2 + _p[a.a,a2.a,h] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h,t2]), "seq_%s_%s_%s" % (a2.a,a.a,h))
   #"""         
   #-------------------------------------------------------------------------------------
   #  Restricciones validas
   for h in range(0,len(I.students)):
      for a in I.actividades():
         model.addConstr(_ct[a.a,a.s,h] <= M, "n_ct_%s_%s_%s" % (a.a,a.s,h))
         #model.addConstr(_st[a.a,a.s,h] >= 0, "n_st_%s_%s_%s" % (a.a,a.s,h))
   #-------------------------------------------------------------------------------------
   #  Equipo
   """
   for h in range(0,len(I.students)):
      for h2 in range(0,len(I.students)):
         if(h != h2):
            for a in I.actividades():
               if(a.eq == '1'):
                  for eq in I.teams:
                        if( h in I.teams[eq] and h2 in I.teams[eq]):
                           for t in range(0,len(I.students[h].stress)):
                              #model.addConstr(_st[a.a,a.s,h] == _st[a.a,a.s,h2], "team")
                              model.addConstr(_x[a.a,a.s,h,t] == _x[a.a,a.s,h2,t], "team")
   """
   #-------------------------------------------------------------------------------------
   """
   #  Recursos
   for h in range(0,len(I.students)):
      for a in I.actividades():
         for h2 in range(0,len(I.students)):
            for a2 in I.actividades():
               for t in range(0,len(I.students[h].stress)):
                  for t2 in range(0,len(I.students[h].stress)):
                     if((int(a.r) != 0) and (int(a2.r) != 0) and (a.r==a2.r)):
                        model.addConstr(_ct[a.a,a.s,h] <= t2 + M*(3 - _r[a.a,a2.a,h,h2] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h2,t2]) , "rec_%s_%s" % (a.a,a2.a))
                        model.addConstr(_ct[a2.a,a2.s,h2] <= t + M*(2 + _r[a.a,a2.a,h,h2] - _x[a.a,a.s,h,t] - _x[a2.a,a2.s,h2,t2]), "rec_%s_%s" % (a2.a,a.a))
   """
   #-------------------------------------------------------------------------------------
   
   #  Makespan by students
   #for h in I.estudiantes:
   #   model.addConstr(_mk[a.s,h] == gp.quicksum(int(a.d) * _x[a.a,a.s,h] for a in I.actividades()))
   
	#	Funcion Objetivo
	#-------------------------------------------------------------------------------------
   # EPP-PSL
   #obj = gp.quicksum(a.d * _x[a.a,a.s,h] for a in I.actividades() for h in I.estudiantes)
   obj = gp.quicksum((int(a.d) * (1 + I.students[h].stress[t] )) * _x[a.a,a.s,h,t] for a in I.actividades() for h in range(0,len(I.students)) for t in range(0,len(I.students[h].stress)))

   #model.update()
   model.setObjective(obj, GRB.MINIMIZE)

   #	Optimiza
   #-------------------------------------------------------------------------------------
   model.write("EPP_scheduling.lp")
   model.optimize()
   solucion=[]
   if model.status == GRB.INFEASIBLE:
      print("INFEASIBLE")
      return -1

   else:
      obj = model.getObjective()
      print("------------------------------ \n")
      print("Objective value:"+ str(obj.getValue()) + " \n")
      print("Runtime:"+ str( time.time() - start_time) + " \n")
      print("Gap:"+ str(model.MIPGap) +" \n")
      print("------------------------------ \n")

      for v in model.getVars():
         if float(v.X) >= 0.5:
            solucion.append((v.Varname,str(v.X)))
      return(solucion)


if __name__ == '__main__':
   EPP_scheduling()