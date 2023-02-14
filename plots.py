import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


folder = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\soluciones\\'
#folder = 'C:\\Users\\pablo\Documents\\PISIS\\Doctorado\\'


def lee_grasp(file):
	return(pd.read_csv(file, names = nombres))

# EPP, EPP-PSL, EPP - SL
def line_plot(df, name, title, xlabel, ylabel, xdata, ydata):
   sns.set(font="Times New Roman")
   sns.axes_style("white")
   sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
   ax = sns.lineplot(x=xdata, y=ydata, hue="MODEL", data=df, palette='viridis')
   #ax = sns.lineplot(x=xdata, y=ydata, hue="MODEL", sort=True, hue_order=['m1','m2','m3','m4','m5'], style='MODEL', data=df)
   handles, _ = ax.get_legend_handles_labels()
   #ax.legend(handles, ["10","20","30","40","50"], title = "Iterations VNS:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #ax.legend(handles, ["100","150","200"], title = "Iterations VNS:", loc = 'center left', bbox_to_anchor = (1,0.5))
   ax.legend(handles, ['EPP-PSL','EPP-SL','EPP'], title = "Model:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #ax.legend(handles, ["EPP","EPP-PSL","EPP-SL"], title = "Model:")
   plt.title('', fontsize=16)
   plt.xlabel(xlabel, fontsize=16)
   plt.ylabel(ylabel, fontsize=16)
   plt.xticks(fontsize=14)
   plt.yticks(fontsize=14)
   #plt.ylim(0, 45)
   plt.setp(ax.get_legend().get_texts(), fontsize='14') # for legend text
   plt.setp(ax.get_legend().get_title(), fontsize='16') # for legend title 
   plt.show()
   #plt.savefig(name,dpi=100, bbox_inches = 'tight')
   plt.close('all')

def box_plot(df, name, title, xlabel, ylabel, xdata, ydata):
   sns.set(font="Times New Roman")
   #EPP: #433c64
   #EPP-PSL: #437795
   #EPP-SL: #59b3a3
   #EPP->EPP-PSL: #006a4e
   #VNS_GRASP-SL:  #d35400 
   #VNS_GRASP-PSL:  #f1c40f 
   #GRASP: #921099
   my_colors = ["#437795", "#59b3a3", "#d35400", "#f1c40f"]
   sns.set_palette(my_colors)
   #ax = sns.violinplot(x=xdata, y=ydata, hue="MODEL", data=df, palette="mako", split=True, inner="quartile", bw=.2)
   #ax = sns.boxplot(x=xdata, y=ydata, hue="MODEL" ,data=df, order=[0,1.03,.99,.95])
   #ax = sns.boxplot(x=xdata, y=ydata, hue="MODEL" ,data=df, order=['i','f'])
   ax = sns.boxplot(x=xdata, y=ydata, hue="MODEL" ,data=df, order=[1.03,.99,.95])
   
   #  FOR SIMILARITY
   handles, _ = ax.get_legend_handles_labels()
   #ax.legend(handles, ['EPP','EPP-PSL','EPP-SL'], title = "Model:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #ax.legend(handles, ['EPP-PSL','EPP-SL'], title = "Model:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #ax.legend(handles, ['EPP','EPP-PSL','EPP->EPP-PSL'], title = "Model:", loc = 'center left', bbox_to_anchor = (1,0.5))
   #ax.legend(handles, ['EPP','EPP-PSL','EPP->EPP-PSL'], ncol = 4, title = "Model:", loc="upper center", bbox_to_anchor = (0.5,1.2))
   #ax.legend(handles, ['EPP','EPP->EPP-PSL'], title = "Model:", loc = 'center left', bbox_to_anchor = (1,0.5))
   ax.legend(handles, ['EPP-PSL','EPP-SL','VNS-GRASP-SL','VNS-GRASP-PSL'], ncol = 4, title = "Model:", loc="upper center", bbox_to_anchor = (0.5,1.2))
   plt.title('', fontsize=16)
   plt.xlabel(xlabel, fontsize=16)
   plt.ylabel(ylabel, fontsize=16)
   plt.xticks(fontsize=14)
   plt.yticks(fontsize=14)
   #ax.set_xticklabels(['--','low','medium','high'])
   #ax.set_xticklabels(['begin','end'])
   ax.set_xticklabels(['low','medium','high'])
   if(ydata == 'ACTIVITIES'):
      plt.ylim(40, 100)
   elif(ydata == 'RUNTIME'):
      plt.ylim(0, 1000)
   else:
      plt.ylim(0, 1200)
   plt.setp(ax.get_legend().get_texts(), fontsize='14') # for legend text
   plt.setp(ax.get_legend().get_title(), fontsize='16') # for legend title 
   #plt.show()
   plt.savefig(name,dpi=100, bbox_inches = 'tight')
   plt.close('all')

#	LEE GRASP
nombres = ['STRESS','INSTANCE','REQUIREMENT','KMIN','IQ','EVALUATE','MODEL','MAKESPAN','RUNTIME','GAP','S1','S2','S3','S4','S5','S6','S7','S8','T1','T2','T3','T4','M1','M2','ACTIVITIES','STRESS_V']
datos = lee_grasp(folder+'acumulado.csv')
#EPP-PSL vs EPP-SL vs EPP
#datos = datos[(datos.MODEL != 'EPP-PSL_OutEPP') & (datos.MODEL != 'VNS_EPP-SL') & (datos.MODEL != 'VNS_EPP-PSL')]
#EPP-PSL vs EPP-PSL Output EPP
#datos = datos[(datos.MODEL != 'EPP-SL') & (datos.MODEL != 'VNS_EPP-SL') & (datos.MODEL != 'VNS_EPP-PSL')]
#EPP-PSL vs EPP-SL
#datos = datos[(datos.MODEL != 'VNS_EPP-SL') & (datos.MODEL != 'EPP') & (datos.MODEL != 'EPP-PSL_OutEPP')]
#VNS
datos = datos[(datos.MODEL != 'EPP') & (datos.MODEL != 'EPP-PSL_OutEPP')]

P = ['STRESS','KMIN','REQUIREMENT','IQ']
#"""
#	--------------	RUNTIME --------------------------------------------
for p in P: 
   name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\run_'+p.lower()+'_EPP-PSLvsEPP-SLvsEPP.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\run_'+p.lower()+'_EPP-PSLvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\run_'+p.lower()+'_EPPvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\run_'+p.lower()+'_EPP-PSLvsEPP-SLGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\run_'+p.lower()+'_EPPvsVNS-EPPGurobi.png'
   title = 'Runtime'
   ylabel = 'Time (sec)'
   if p =='IQ':
      xlabel = 'Learning Rate'
   elif p =='KMIN':
      xlabel = 'Minimum Score'
   elif p =='RCL':
      xlabel = p
   else:
      xlabel = p.capitalize()
   xdata = p
   ydata = 'RUNTIME'
   #line_plot(datos, name, title, xlabel, ylabel, xdata, ydata)
   box_plot(datos, name, title, xlabel, ylabel, xdata, ydata)
#"""

"""
#	--------------	MAKESPAN --------------------------------------------

for p in P: 
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\makespan_'+p.lower()+'_EPP-PSLvsEPP-SLvsEPP.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\makespan_'+p.lower()+'_EPP-PSLvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\makespan_'+p.lower()+'_EPPvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\makespan_'+p.lower()+'_EPP-PSLvsEPP-SLGurobi.png'
   name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\makespan_'+p.lower()+'_EPPvsVNS-EPPGurobi.png'
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
   ydata = 'MAKESPAN'
   #line_plot(datos, name, title, xlabel, ylabel, xdata, ydata)
   box_plot(datos, name, title, xlabel, ylabel, xdata, ydata)

"""
"""
#	--------------	ACTIVITIES --------------------------------------------
for p in P: 
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\act_'+p.lower()+'_EPP-PSLvsEPP-SLvsEPP.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\act_'+p.lower()+'_EPP-PSLvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\act_'+p.lower()+'_EPPvsOutputEPPGurobi.png'
   #name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\act_'+p.lower()+'_EPP-PSLvsEPP-SLGurobi.png'
   name = 'C:\\Users\\pablo\\Documents\\PISIS\\Doctorado\\Paper\\RepoPaper\\EPPS\\plots\\act_'+p.lower()+'_EPPvsVNS-EPPGurobi.png'
   title = 'Activities'
   ylabel = 'Activities'
   if p =='IQ':
      xlabel = 'Learning Rate'
   elif p =='KMIN':
      xlabel = 'Minimum Score'
   elif p =='RCL':
      xlabel = p
   else:
      xlabel = p.capitalize()
   xdata = p
   ydata = 'ACTIVITIES'
   #line_plot(datos, name, title, xlabel, ylabel, xdata, ydata)
   box_plot(datos, name, title, xlabel, ylabel, xdata, ydata)
"""