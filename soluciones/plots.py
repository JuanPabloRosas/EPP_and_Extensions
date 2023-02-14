#!/usr/bin/env python
# -*- coding: utf-8 -*-

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


folder = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\soluciones\\'

def lee_grasp(file):
	return(pd.read_csv(file, names = nombres))

def box_plot(df, name, title, xlabel, ylabel, xdata, ydata):
   #sns.set(font="Times New Roman")
   #ax = sns.violinplot(x=xdata, y=ydata, hue="MODEL", data=df, palette="mako", inner="quartile", split=True,  bw=.2)
   #ax = sns.boxplot(x=xdata, y=ydata, hue="MODEL" ,data=df, palette='mako')
   ax = sns.boxplot(x=xdata, y=ydata ,data=df, palette='mako')
   
   #  FOR SIMILARITY
   #handles, _ = ax.get_legend_handles_labels()
   #ax.legend(handles, ["EPP-PSL", "EPP-SL"], title = "Method:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #plt.title('', fontsize=16)
   #plt.xlabel(xlabel, fontsize=16)
   #plt.ylabel(ylabel, fontsize=16)
   #plt.xticks(fontsize=14)
   #plt.yticks(fontsize=14)
   plt.ylim(-3, 8)
   
   #plt.setp(ax.get_legend().get_texts(), fontsize='14') # for legend text
   #plt.setp(ax.get_legend().get_title(), fontsize='16') # for legend title 
   plt.show()
   #plt.savefig(name,dpi=100, bbox_inches = 'tight')
   #plt.close('all')

#	LEE GRASP
nombres = ['STRESS','INSTANCE','REQUIREMENT','KMIN','IQ','EVALUATE','DIFF']
datos = lee_grasp(folder+'diferenciasVNS_vs_GRASP.csv')


#	--------------	MAKESPAN --------------------------------------------
P = ['STRESS','KMIN','REQUIREMENT','IQ']
for p in P: 
   name = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\makespan_'+p.lower()+'_gurobi.png'
   title = 'Makespan'
   ylabel = 'Makespan'
   if p =='IQ':
      xlabel = 'Learning Rate'
   elif p =='KMIN':
      xlabel = 'Minimum Score'
   elif p =='RCL':
      xlabel = p
   else:
      xlabel = p.capitalize()
   xdata = p
   ydata = 'DIFF'
   box_plot(datos, name, title, xlabel, ylabel, xdata, ydata)

name = 'C:/Users/pablo/Documents/PISIS/Doctorado/Paper/RepoPaper/EPPS/plots/plot.png'
box_plot(datos, name, 'Difference', 'Kmin', 'DIFF', 'KMIN', 'DIFF')

