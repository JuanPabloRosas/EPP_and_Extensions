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

folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\'
#	Lee archivo de entrada
file = open(folder+"entradaGeneradorInstancias.txt", "r")
instancia = []
for f in file:
	instancia.append(float(f.rstrip()))

#	Funcion para asignacion de cuantas materias, temas, subtemas, actividades, etc. segun archivo de entrada
def ciclos(instancia):
    for a in range(0,88):
        sec=[]
        temp =[]
        act = int(instancia[a][3])
        sec.append(act) 
        r1 = int(instancia[act-1][7])
        if(r1!= 0):
            sec.append(r1)
            temp.append(r1)
        r2 = int(instancia[act-1][8])
        if(r2 != 0):
            sec.append(r2)
            temp.append(r2)
        while(len(temp)>0):
            act = int(instancia[temp.pop(0)-1][3])
            print(temp) 
            r1 = int(instancia[act-1][7])
            r2 = int(instancia[act-1][8])
            if(r1!= 0):
                if(r1 in sec):
                    return False
                else:
                    sec.append(r1)
                    temp.append(r1)
            
            if(r2 != 0):
                if(r2 in sec):
                    return False
                else:
                    sec.append(r2)
                    temp.append(r2)
        
    return True
            
def cuantasMaterias():
	if(instancia[1] == 1):		# Si es 1, Random entre 2 y 3
		materias = 2
	elif(instancia[1] == 2):		# Si es 2, Random entre 4 y 5
		materias = 5
	else:
		materias = 7
	return(materias)
def cuantosTemas():
	if(instancia[2] == 1):
		temas = 2
	elif(instancia[2] == 2):
		temas = 4
	else:
		temas = 6
	return(temas)
def cuantosSubtemas():
	if(instancia[3] == 1):
		subtemas = 2
	elif(instancia[3] == 2):
		subtemas = 5
	else:
		subtemas = 7
	return(subtemas)
def cuantasActividades():
	if(instancia[4] == 1):
		actividades = 6
	elif(instancia[4] == 2):
		actividades = 9
	else:
		actividades = 11
	return(actividades)
def instancia_simetrica():
	instancia_salida1=[]
	cal_sub = 0
	for m in range(1,materias+1):
		for t in range(1,temas+1):
			for s in range(1,subtemas+1):
				for a in range(1,actividades+1):
					#	La duracion y el valor es +-round(100/actividades) segun 100/cant. de actividades
					if(random.random() >=.5):	#	Incrementa el valor
						d = round(100/actividades) + random.randint(0,6)
						v = round(100/actividades) + random.randint(0,6)
						c = random.random()
						e = random.random()
					else:						#	Decrementa el valor
						d = round(100/actividades) - random.randint(0,6)
						v = round(100/actividades) #- random.randint(0,6)
						c = random.random()
						e = random.random()
					#	Asignacion de actividades obligatorias segun una probabilidad
					if(random.random()<= act_obligatorias):
						o = 1
					else:
						o = 0
					#	Asignacion de 1 actividad habilitante segun una probabilidad
					if(random.random()<=act_1habilitante):
						r1 = random.randrange(1,actividades*subtemas*temas*materias)
						while(r1 == a):
							r1 = random.randrange(1,actividades*subtemas*temas*materias)			# Requisito 1
						#	Asignacion de 2 actividades habilitantes segun una probabilidad
						if(random.random()<= act_2habilitante):
							r2 = random.randrange(1,actividades*subtemas*temas*materias)
							while(r2 == a or r2 == r1):
								r2 = random.randrange(1,actividades*subtemas*temas*materias)
						else:
							r2 = 0
					else:
						r1 = 0
						r2 = 0							

					i_t = (t+(temas*m))-temas 															# Numero de tema
					i_s1 = (s+(subtemas*((t+(temas*m))-temas)))-subtemas 								# Numero de subtema1
					i_a = (a+actividades*((s+(subtemas*((t+(temas*m))-temas)))-subtemas))-actividades 	# Numero de actividad
					
					#				ESTRES ALTO AL FINAL
					if(i_a > (((actividades*subtemas*temas*materias)/3)*2)):
						while(e<0.4 or e >0.5):
							e = random.random()
					
					#				ESTRES BAJO AL INICIO
					if(i_a <= (((actividades*subtemas*temas*materias)/3)*2)):
						while(e>0.2):
							e = random.random()
               
               
               #				ESTRES ALTO AL INICIO
					#if(i_a <= (((actividades*subtemas*temas*materias)/3))):
					#	while(e<0.4 or e >0.5):
					#		e = random.random()
					
					#				ESTRES BAJO AL FINAL
					#if(i_a > (((actividades*subtemas*temas*materias)/3))):
					#	while(e>0.2):
					#		e = random.random()

					#	Asignacion de un numero de materia, tema, subtema, actividad en forma de secuencia
					#	no se repite un mismo numero
					instancia_salida1.append([m,i_t,i_s1,i_a,d,v,e,r1,r2,o])
					cal_sub = cal_sub + v
				cal_sub = 0
	
	return(instancia_salida1)

#	Declaracion de variables
materias = cuantasMaterias()
act_obligatorias = float(instancia[5])
act_1habilitante = float(instancia[6])
act_2habilitante = float(instancia[7])
act_3habilitante = float(instancia[8])
act_4habilitante = float(instancia[9])
act_5habilitante = float(instancia[10])
act_mas_de_un_subt = float(instancia[11])

#	------------------------------------------------------------------------------------
cont = 1			#	CUANTAS INSTANCIAS GENERA
while(cont < 6):
   #	Creacion de la instancia de salida
   instancia_salida = [[]]
   temas = cuantosTemas()
   subtemas = cuantosSubtemas()
   actividades = cuantasActividades()
   instancia_salida = instancia_simetrica()   

   if(ciclos(instancia_salida)):
      with open(folder+'instancias_final\\f_'+str(cont)+'_2.csv', 'w', newline='') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerows(instancia_salida)
      csvFile.close()
      cont = cont + 1