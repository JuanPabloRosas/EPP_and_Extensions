#		V1.0 Problema de Planificacion Educativa (PPE) - Gurobi - Python
#		Autor: Juan Pablo Rosas Baldazo		02/09/19
#
#		Considera el coeficiente intelectual del estudiante para afectar
#		la duracion de las actividades
#		
#-------------------------------------------------------------------------------------------

from gurobipy import *
import time

def habilitan(a,act,hab1,hab2):
   lista = []
   for h1 in hab1:
      if(a == h1):
         lista.append(hab1[h1])
   for h2 in hab2:
      if(act == h2):
         lista.append(hab2[h2])
      
   return lista

def ppeCISec(kmin,actividades,subtemas,temas,materias,obligatorias,habilitamiento1,habilitamiento2,duracion,valor,arcs):
   start_time = time.time()

   model = Model('Planning modelo original')

   #	Variables
   #-------------------------------------------------------------------------------------
   kmax = 120
   #	Actividades
   x={}
   for a,s,t,m in arcs:
      x[a,s,t,m] = model.addVar(0.0,1.0,obj=1.0, vtype=GRB.BINARY ,name='%s_%s_%s_%s' % (a,s,t,m))

   #	Subtemas
   y={}
   for a,s,t,m in arcs:
      y[s,t,m] = model.addVar(lb = 0, ub= kmax , vtype=GRB.INTEGER ,name='score_s_%s_%s_%s' % (s,t,m))

   model.update()

   #	Restricciones
   #-------------------------------------------------------------------------------------
   #	Actividades Obligatorias   
   for a,s,t,m in arcs:
      for o in obligatorias:
         if(a == o):
            model.addConstr(quicksum(x[o,s,t,m]) == 1, "mandatory_%s" % (o))
   
   
   #for o,s,t,m in obligatorias:
   #   model.addConstr(quicksum(x[o,s,t,m]) == 1, "mandatory_%s" % (o))

   #	Score mayor a kmin por subtema
   for s in subtemas:
      model.addConstr(quicksum(valor[a,s2,t,m] * x[a,s2,t,m] for a,s2,t,m in arcs.select('*', s ,'*','*')) >= kmin,"Kmin_%s_%s_%s_%s" % (a,s,t,m))

   #	Score menor a kmax por subtema
   for s in subtemas:
      model.addConstr(quicksum(valor[a,s2,t,m] * x[a,s2,t,m] for a,s2,t,m in arcs.select('*', s ,'*','*')) <= kmax,"Kmax_%s_%s_%s_%s" % (a,s,t,m))

   # #	Habilitamiento i requiere i2	
   for a in actividades:
      hab = habilitan(a,actividades,habilitamiento1,habilitamiento2)
      for a2,s,t,m in arcs.select(a,'*','*','*'):
         model.addConstr((quicksum(x[a3,s2,t2,m2] 
         for h in hab for a3,s2,t2,m2 in arcs.select(h,'*','*','*')))
         >= len(hab)*x[a2,s,t,m],"Habilitamiento_%s_%s" % (a,a2))
   """
   #	Restriccion de habilitamiento
   for i,i2 in habilitamiento:
   model.addConstr((quicksum(x[i3,j]
      for i3,j in arcs.select(i,'*')) <= (quicksum(x[i4,j2]
      for i4,j2 in arcs.select(i2,'*')))),"Habilitamiento")
   """

   #	Acumula el score de los subtemas
   for a,s,t,m in arcs:
      model.addConstr(y[s,t,m] == quicksum(valor[a,s,t,m]*x[a,s2,t2,m2] for a,s2,t2,m2 in arcs.select('*',s,t,m)))


   #	Funcion Objetivo
   #-------------------------------------------------------------------------------------
   obj = quicksum(duracion[a,s,t,m] * x[a,s,t,m] for a,s,t,m in arcs)
   model.setObjective(obj, GRB.MINIMIZE)


   #	Optimiza
   #-------------------------------------------------------------------------------------
   model.optimize()
   solucion=[]
   if model.status == GRB.INFEASIBLE:
      model.computeIIS()
   else:
      obj = model.getObjective()
      #model.setParam("LogFile",filename+".txt")
      print("------------------------------ \n")
      print("Valor objetivo: \n")
      print(obj.getValue())
      solucion.append("Valor Objetivo:"+str(obj.getValue()))

      print("------------------------------ \n")
      print("Runtime: \n")
      runtime = time.time() - start_time
      print(runtime)
      solucion.append("Runtime:"+str(runtime))

      print("------------------------------ \n")
      print("Gap: \n")
      print(model.MIPGap)
      solucion.append("Gap:"+str(model.MIPGap))

      print("------------------------------ \n")
      print("Solucion: \n")
      for v in model.getVars():
         if v.X != 0:
            s =  round(float(v.X),1)
            print(v.Varname,s)
            if(s > 0):
               solucion.append(v.Varname + '_' + str(s))
      print("------------------------------ \n")
      solucion.append("DURACION")
      for (a,s,t,m)in duracion:
         solucion.append(str(duracion[(a,s,t,m)]))
      solucion.append("VALOR")
      for (a,s,t,m) in valor:
         solucion.append(str(valor[(a,s,t,m)]))

      return(solucion)

if __name__ == '__main__':
    ppeCI()