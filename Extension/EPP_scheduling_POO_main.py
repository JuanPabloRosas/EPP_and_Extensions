#!/usr/bin/env python
# -*- coding: utf-8 -*-

import EPP_scheduling_POO_instance
import EPP_scheduling_POO_MILP
import EPP_scheduling_POO_solution
import os

#	LEE INSTANCIA
# #-----------------------------------------------------------------
#	WINDOWS
folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper2\\Instancias\\instancias\\'
#	LINUX
#folder = '/home/juanpablo/Documentos/PISIS/Doctorado/ExperimentacionGurobi/instancias/'



#	CREA ARCHIVO SALIDA
# #-----------------------------------------------------------------
kmin = 70
kmax = 100
CI=[0.95]



#for filename in os.listdir(folder):
   #if filename.endswith('.csv'):
i = EPP_scheduling_POO_instance.Instancia()
instance = i.leeInstancia(folder + 'juguete.csv')
estudiantes = i.leeEstudiantes(folder + 'estudiantes.csv')
for k in range(kmin,kmax + 1,10):	
   for iq in CI:         
         #solution_file = open(folder + filename.split('.')[0]+'_'+str(k)+'_'+str(iq)+'_'+'EPP-SL_scheduling'+'.txt',"w+")
         s = EPP_scheduling_POO_MILP
         solution = s.EPP_scheduling()
         f = EPP_scheduling_POO_solution
         seq = f.add_to_sol(solution)
         flag,errors_list = f.check_factibility(seq)
         f.print_sol(seq)
         if flag:
            f.print_sol(seq)
            f.plot_schedule(seq)
         else:
            for e in errors_list:
               print(e)
         #     DELETE VARIABLES AND OBJECTS
         #d = dir()
         #for obj in d:
         #   if not obj.startswith('__'):
         #      del globals()[obj]
del instance
      
      
      

