from fileinput import filename
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

#folder = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\Paper\\instancias_nuevas\\soluciones\\caso_grupo\\'
folder = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\soluciones\\SolucionesCasoReal\\'
#--------------- HEADER NAMES PARA EL CSV DE ACTIVIDADES ---------------------------------
nombres = ['STRESS','INSTANCE','REQUIREMENT','KMIN','IQ','EVALUATE','MODEL'] 
lista = []
for i in range(1,89):
   lista.append('ACT'+str(i))
nombres = nombres + lista
#----------------------- RESULTADOS -----------------------------------------------

"""
LEE LA SOLUCION ENCONTRADA Y EXTRAE LOS DATOS DE MAKESPAN, RUNTIME Y GAP. LOS DEVUELVE EN UNA LISTA LLAMADA -DATOS-.
"""
def lee_solucion(filename):
   name = filename.split('\\')
   name = name[len(name)-1].replace('.txt','').split('_')
   name.insert(1,0)
   name.insert(2,0)
   datos = []
   with open(filename,'r') as f:
      rows = f.readlines()
   
   cuantas_act = 0
   datos.append(name[0])	# Posicion del estres
   datos.append(name[1])	# Num. de instancia
   datos.append(name[2])	# Habilitamiento
   datos.append(name[3])	# Kmin
   datos.append(name[4])	# IQ
   datos.append(name[5])	# materia, tema, subtema
   datos.append(name[6])   # modelo
      
   for r in rows:
      if "Valor Objetivo:" in r:       # MAKESPAN
         datos.append(float(r.replace("Valor Objetivo:","").replace("\n","")))
      if "Runtime:" in r:
         datos.append(float(r.replace("Runtime:","").replace("\n","")))
      if "Gap:" in r:
         datos.append(float(r.replace("Gap:","").replace("\n","")))
      if "_1.0\n" in r:
         cuantas_act = cuantas_act + 1
      if "score" in r:
         datos.append(float(r[r.rfind('_')+1:]))

   #	CUANTAS ACT HAY EN LA SOLUCION   
   if(name[6] =='EPP'):
      datos.append(0)
      datos.append(0)
      datos.append(0)
      datos.append(0)
      datos.append(0)
      datos.append(0)
      datos.append(cuantas_act)
   else:
      datos.append(cuantas_act)
   
   return datos

"""
EXTRAE LA SECUENCIA DE LA SOLUCIÓN Y DEVUELVE 3 ARCHIVOS -ACTIVIDADES-,-POSICIONES-,-SOLUCION-:
1.- CONTIENE LAS ACTIVIDADES QUE CONFORMAN LA SOLUCION.
2.- CONTIENE LAS POSICIONES QUE SE OCUPARON EN LA SOLUCION
3.- LA SOLUCION TAL CUAL CONFORMADO POR COLUMNAS CON (MATERIA, TEMA, SUBTEMA, ACTIVIDAD, POSICION)
"""
def extrae_solucion(filename):
   solucion = []
   actividades = []
   posiciones = []
   with open(filename,'r') as f:
      rows = f.readlines()
   sol = []
   for r in rows:
      if "_1.0\n" in r:
         sol = r.split('_')
         if(('EPP.txt' in filename)):
            actividades.append(sol[0])
            posiciones.append('0')
            solucion.append('(' + sol[0] + '_' + sol[1] + '_' + sol[2] + '_' + sol[3] + ')')
         else:
            actividades.append(sol[0])
            posiciones.append(sol[4])
            solucion.append('(' + sol[0] + '_' + sol[1] + '_' + sol[2] + '_' + sol[3]+ '_' + sol[4] + ')')
   return (solucion, actividades, posiciones)
   
""" 
LLENA LOS ARCHIVOS DE SALIDA CON LOS DATOS DE LAS SOLUCIONES 
"""
def extrae():
   d= open(folder + "datosCasoRealEPP_SL.csv","w+")
   s= open(folder + "solucionesCasoRealEPP_SL.csv","w+")
   a = open(folder + "actividadesCasoRealEPP_SL.csv","w+")
   p = open(folder + "posicionesCasoRealEPP_SL.csv","w+")
   for filename in os.listdir(folder):
      print('FILENAME:  ' + filename)
      if(filename.endswith('.txt')):
         lista = []
         print('----------------------------------------')
         lista = lee_solucion(folder + filename)
         sol,act,pos = extrae_solucion(folder + filename)
         for l in lista:
            d.write(str(l) + ',')
         d.write('Stress' + '\n')
			
         name = filename.replace('.txt','').split('_')
         name.insert(1,'0')
         name.insert(2,'0')
         s.write(name[0]+ ',' + name[1] + ',' + name[2] + ',' + name[3] + ',' + name[4] + ',' + name[5] + ',' + name[6])
         a.write(name[0]+ ',' + name[1] + ',' + name[2] + ',' + name[3] + ',' + name[4] + ',' + name[5] + ',' + name[6])
         p.write(name[0]+ ',' + name[1] + ',' + name[2] + ',' + name[3] + ',' + name[4] + ',' + name[5] + ',' + name[6])

         for i in sol:
            s.write(',' + i)
         s.write('\n')   
         
         act = act + ['0']*(88-len(act))  #  Llena actividades en la solucion
         for j in act:
            a.write(',' + j)
         a.write('\n')
         
         pos = pos + ['0']*(88-len(pos))
         for k in pos:
            p.write(',' + k)
         p.write('\n')
					
   d.close()
   s.close()
   a.close()
   p.close()

# -------------------- COMPARACION DE MODELOS -------------------------------------
""" 
SIMILITUD DE JACCARD:
(A nterseccion B)/(A union B), COMPARA CUANTOS ELEMENTOS DEL CONJUNTO 1 Y 2 SON SIMILARES, PERO NO CONSIDERA LA POSICION
"""
def jaccard_similarity(list1, list2):
   """Define Jaccard Similarity function for two sets"""
   intersection = list(set(list1).intersection(list2))
   union = list(set().union(list1,list2))
   return float(len(intersection)) / (len(union)-1)

"""
COMPARACION UNO A UNO D ELOS ELEMENTOS DE LA SOLUCION CONSIDERANDO LA POSICION
"""
def possition_similarity(list1, list2):
   intersection = list(set(list1).intersection(list2))
   cont = 0
   for i in range(0,88):
      if((list1[i] !=0) & (list2[i] !=0) & (list1[i] == list2[i])):
         cont = cont + 1
   #union = ( sum((x>0) for x in list1) + sum((x>0) for x in list2) ) - len(intersection)
   union = list(set().union(list1,list2))
   return cont/(len(union)-1)

"""
COMPARA LAS ACTIVIDADES QUE CONFORMAN UNA SOLUCION (JACCARD).
COMPARA LAS ACTIVIDADES Y LAS POSICIONES QUE CONFORMAN UNA SOLUCION (POSSITION).
GUARDA LOS PLOTS DE LAS COMPARACIONES EN UNA CARPETA LLAMDA -PLOTS- DENTRO DE LAS SOLUCIONES.
"""
def compara(folder):
   for k in range(70,101,5):
      for iq in [0.95,0.99,1.03]:
         for ev in ['s','t','m']:
            for model in ['EPP-SL','EPP-PSL']:
               actividades = pd.read_csv(folder +'posiciones.csv', names = nombres)
               actividades = actividades[(actividades.KMIN == k) & (actividades.REQUIREMENT == 0) & (actividades.IQ == iq) & (actividades.EVALUATE == ev) & (actividades.MODEL ==model)]
               print(len(actividades.index))
               dif_act = []
               dif_pos = []
               actividades = actividades.iloc[:,7:]
               print(actividades)
               datos = []
               for index, row in actividades.iterrows():
                  datos.append(list(row))
                  
               print(len(datos))
               for d1 in range(0,len(datos)):
                  dif_act.append([])
                  dif_pos.append([])
                  for d2 in range(0,len(datos)):
                     dif_act[d1].append(possition_similarity(datos[d1],datos[d2]))
                     dif_pos[d1].append(jaccard_similarity(datos[d1],datos[d2]))
                                 
               dif_act = pd.DataFrame(dif_act)   #, columns=['STRESS','REQUIRMENT','INSTANCE','IQ','EVALUATE','MODEL','TOTAL'])
               dif_pos = pd.DataFrame(dif_pos)   #, columns=['STRESS','REQUIRMENT','INSTANCE','IQ','EVALUATE','MODEL','TOTAL'])

               
               ax = sns.heatmap(dif_act, cmap="rocket", vmin=0, vmax=1)
               ax.set_title(str(k) + '-' + str(iq), fontsize=16)
               #plt.show()
               plt.savefig(folder + '\\plots_comp\\dif_act_' + str(k) + '_' + str(iq) + '_' + str(ev) + '_' + str(model) + '.png',dpi=100, bbox_inches = 'tight')
               ax = sns.heatmap(dif_pos, cmap="rocket", vmin=0, vmax=1)
               ax.set_title(str(k) + '-' + str(iq), fontsize=16)
               plt.savefig(folder + '\\plots_comp\\dif_pos_' + str(k) + '_' + str(iq) + '_' + str(ev) + '_' + str(model) + '.png',dpi=100, bbox_inches = 'tight')
               plt.close('all')
               dif_act.to_csv(folder+'dif_act.csv')
               dif_pos.to_csv(folder+'dif_pos.csv')

#---------------------- DATO CUADRICULA --------------------------------------------
def extrae_solucion_cuadricula(filename):
	solucion = []
	with open(folder + filename,'r') as f:
		rows = f.readlines()
	if len(rows) > 0:
		sol = []
		for r in rows:
			if "_1.0" in r:
				sol = r.split('_')
				solucion.append((sol[0],sol[1],sol[2],sol[3],sol[4]))
		return solucion

"""
BUSCA EL DATO -TIPO- EN EL ARCHIVO DE LA SOLUCION.
PUEDE SER EL VALOR; LA DURACION O EL ESTRES DE UNA ACTIVIDAD.
"""
def busca(filename, actividad, tipo):
   flag = False
   cont = 0
   comp = ''
   with open(filename,'r') as f:
      rows = f.readlines()
   for r in rows:
      if(flag):
         cont = cont + 1
         if(cont == int(str(actividad))):
               comp = r
            
      if tipo in r:
         flag = True
   return comp.replace('\n','')

def datos_cuadricula(file):
   d= open(folder + "cuadricula.csv","w+")
   name = file.split('_')
   
   for k in range(70,101,5):
      posiciones = list(range(1,89))
      filename =  name[0] + '_' + name[1] + '_' + name[2] + '_' +str(k) + '_' +  name[4] + '_' + name[5] + '_' + name[6]
      estres = name[0]
      inst = name[1]
      req = name[2]
      kmin = str(k)
      CI = name[4]
      ev = name[5]
      modelo = name[6].replace('.txt','')
      soluciones = []
      print('----------------------------------------')
      soluciones.append(extrae_solucion_cuadricula(filename))
      for sol in soluciones:
         if(sol != -1):
            for act in sol:
               if(len(act)>0):
                  valor = busca(folder + filename , act[0],'VALOR')
                  duracion = busca(folder + filename , act[0],'DURACION') 
                  estres_v = busca(folder + filename , act[0], 'ESTRES')
                  a = str(act[4])
                  posiciones.remove(int(a))
                  d.write(estres+ ',' + req + ',' + inst + ',' + kmin + ',' + CI + ',' + ev + ',' + modelo + ',' + str(act[0])
                           + ',' + str(act[1])  + "," + str(act[2]) + ',' + str(act[3]) 
                           + ',' + act[4] + "," + duracion + ',' + valor + ','+ estres_v + '\n')
      #  POR CADA POSICION QUE NO SE ASIGNO ACTIVIDAD
      for p in posiciones:
         print(p)
         d.write(estres+ ',' + req + ',' + inst + ',' + kmin + ',' + CI + ',' + ev + ',' + modelo + ',0,0,0,0,'+str(p)+',0,0,0\n')
   d.close()


"""
PLOT
"""
def cuadricula(file):
   file = file.split('_')
   filename = file[0] + '_' + file[1] + '_' + file[2] + '_' + file[4] + '_' + file[5] + '_' + file[6].replace('.txt','')
   
   nombres= ['STRESS','REQUIRMENT','INSTANCE','KMIN','IQ','EVALUATE','MODEL','ACT','SUBT','TEM','MAT','POSITION','DURATION','VALUE','STRESS_V']
   df = pd.read_csv(folder +'cuadricula.csv', names = nombres)
   df_d = df[['POSITION','KMIN','DURATION']]
   df_d = df_d.groupby(['POSITION','KMIN']).mean()
   df_d = df_d.unstack(level=0)
   df_d = df_d.fillna(0)
   print(df_d)
   
   ax= sns.heatmap(df_d , cmap="inferno", vmin= 0, vmax=20, linewidth=0.01, rasterized=True,  cbar_kws={'label': 'Duration'}, linecolor = '#525250',annot=False, annot_kws={"size": 7})
   ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
   ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
   xticks_labels = list(range(1,89,8))
   ax=plt.xticks(np.arange(1,89,8) -.5, labels=xticks_labels, fontsize=12)
   #plt.ytick(fontsize=12)
   #title = 'Learning path'.upper()
   plt.xlabel('Position', fontsize=12)
   plt.ylabel('Minimum Score', fontsize=12)
   ax=plt.subplots_adjust(left=0.1, bottom=0.320, right=1, top=0.65, wspace=0, hspace=0)
   #plt.show()
   name = folder + 'plots\\'+ filename + '_d.png'
   plt.savefig(name, dpi=100, bbox_inches = 'tight')
   plt.close()
   
   df_v = df[['POSITION','KMIN','VALUE']]
   df_v = df_v.groupby(['POSITION','KMIN']).mean()
   df_v = df_v.unstack(level=0)
   df_v = df_v.fillna(0)
   print(df_v)
   
   ax= sns.heatmap(df_v , cmap="inferno", vmin= 0, vmax=20, linewidth=0.01, rasterized=True,  cbar_kws={'label': 'Value'}, linecolor = '#525250',annot=False, annot_kws={"size": 7})
   ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
   ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
   xticks_labels = list(range(1,89,8))
   ax=plt.xticks(np.arange(1,89,8) -.5, labels=xticks_labels, fontsize=12)
   #plt.ytick(fontsize=12)
   #title = 'Learning path'.upper()
   plt.xlabel('Position', fontsize=12)
   plt.ylabel('Minimum Score', fontsize=12)
   ax=plt.subplots_adjust(left=0.1, bottom=0.320, right=1, top=0.65, wspace=0, hspace=0)
   #plt.show()
   name = folder + 'plots\\'+ filename + '_v.png'
   plt.savefig(name, dpi=100, bbox_inches = 'tight')
   plt.close()
   
   df_s = df[['POSITION','KMIN','STRESS_V']]
   df_s = df_s.groupby(['POSITION','KMIN']).mean()
   df_s = df_s.unstack(level=0)
   df_s = df_s.fillna(0)
   print(df_s)
   
   ax= sns.heatmap(df_s , cmap="inferno", vmin= 0, vmax=.5, linewidth=0.01, rasterized=True,  cbar_kws={'label': 'Stress'}, linecolor = '#525250',annot=False, annot_kws={"size": 7})
   ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)
   ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=12)
   xticks_labels = list(range(1,89,8))
   ax=plt.xticks(np.arange(1,89,8) -.5, labels=xticks_labels, fontsize=12)
   #plt.ytick(fontsize=12)
   #title = 'Learning path'.upper()
   plt.xlabel('Position', fontsize=12)
   plt.ylabel('Minimum Score', fontsize=12)
   ax=plt.subplots_adjust(left=0.1, bottom=0.320, right=1, top=0.65, wspace=0, hspace=0)
   #plt.show()
   name = folder + 'plots\\'+ filename + '_s.png'
   plt.savefig(name, dpi=100, bbox_inches = 'tight')
   plt.close()

#------------------------------------------------------------------------------------

"""
REVISA FACTIBILIDAD DE LA SOLUCION ENCONTRADA
"""
def factibilidad():
   #  NO REPETIR POSICIONES O ACTIVIDADES
   lista_fact = {}
   for filename in os.listdir(folder):
      if(filename.endswith('.txt')):
         
         actividades =[0]*88
         posiciones = [0]*88
         with open(folder + filename,'r') as f:
            rows = f.readlines()
         for r in rows:
            if(filename.endswith('EPP.txt')):
               if((r.endswith('_1.0\n'))):
                  if((int(r.split('_')[0]) in actividades)):
                     lista_fact[filename]=False
                     break
                  else:
                     actividades[int(r.split('_')[0])-1] = int(r.split('_')[0])
            else:
               if((r.endswith('_1.0\n'))):
                  if((int(r.split('_')[0]) in actividades) or (int(r.split('_')[4]) in posiciones)):
                     lista_fact[filename]=False
                     break
                  else:
                     actividades[int(r.split('_')[0])-1] = int(r.split('_')[0])
                     posiciones[int(r.split('_')[4])-1] = int(r.split('_')[4])
         lista_fact[filename]=True
   #  TODOS LOS SUBTEMAS ALCANZAN EL KMAX
   #  NO HAY CICLOS EN LAS ACTIVIDADES DE PRECEDENCIA
   return lista_fact

#"""
#  REVISA FACTIBILIDAD DE LAS SOLUCIONES
resultados = factibilidad()
for r in resultados:
   if(resultados[r] == False):
      print(r + '  ' + str(resultados[r]))
print('--------------------------  HECHO!!!!  --------------------------')
sleep(5) 
#"""
extrae()                                          #  CREA ARCHIVO DE DATOS, SOLUCIONES, ACTIVIDADES Y POSICIONES DE LAS ACTIVIDADES
#compara(folder)                                   #  CREA EL ARCHIVO DE DIFERENCIAS ENTRE LAS SOLUCIONES POR KMIN   
#  CUADRICULA
"""
for s in ['f','i']:
   for i in range(1,6):
      for r in range(0,3):
         for iq in [0.95,0.99,1.03]:
            for ev in ['s','t','m']:
               for model in ['EPP-SL','EPP-PSL']:
                  datos_cuadricula(s + '_'+ str(i) + '_' + str(r) + '_'+ str(70) + '_' + str(iq) + '_' + ev + '_' + model + '.txt')    #  CREA DATOS PARA LAS CUADRICULAS
                  cuadricula(s + '_'+ str(i) + '_' + str(r) + '_'+ str(70) + '_' + str(iq) + '_' + ev + '_' + model + '.txt')          #  PLOT DE LA CUADRICULA 
"""

