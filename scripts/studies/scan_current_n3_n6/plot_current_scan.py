#plot_current_scan.py
 
"""
Samuel Ward
28/05/20
----
script resolution scan
---
 
notes:         
---
"""

###################################################################################################
#Preamble
 
import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway

try:
    import numpy as np
    import pathlib
    import copy
    import matplotlib.pyplot as plt
    import os
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

if __name__=='__main__':

    try:
        import context
    except:
        raise ImportError("ERROR: context.py could not be imported!\nreturning\n")
        sys.exit(1)

try:
    from classes.input_classes.equilibrium import Equilibrium
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/input_classes/equilibrium.py could not be imported!\nreturning\n") 
    sys.exit(1)

try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import constants
except:
    raise ImportError("ERROR: LOCUST_IO/src/constants.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

try:
    cwd=pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(str(cwd.parents[1]))
    import templates.plot_mod
except:
    raise ImportError("ERROR: templates/template_mod.py could not be imported!\nreturning\n") 
    sys.exit(1)
    
################################################################## 
#Main 

import scan_current_n3_n6_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')
fig1,ax1=plt.subplots(1)
fig2,ax2=plt.subplots(1)
fig3,ax3=plt.subplots(1)
Pinj=33.e6
PFC_power=[]
for run_number,(output,current,col_val) in enumerate(zip(outputs,batch_data.parameters__currents_upper,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output'])))):
    if output: 
        output.plot(fig=fig1,ax=ax1,axes=['time'],fill=False,label=str(current/1000.),colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=False)
        output['E']/=1000. #convert to keV
        output.plot(fig=fig2,ax=ax2,axes=['E'],fill=False,label=str(current/1000.),colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=False)

    #calculate losses from particle list

    if output:
        i=np.where(output['status_flag']=='PFC_intercept_3D')[0]
        power_loss=1.e6*output['f']*np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron
        if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number]: #this is the 2D case
            ax3.axhline(power_loss/1.e6,color='red',label='2D case')
        PFC_power.append([power_loss/1.e6])
    else:
        PFC_power.append([-10.])

ax3.plot(batch_data.parameters__currents_upper,PFC_power,color='b',marker='x',linestyle='-',label='3D cases')

ax1.legend()
ax2.legend()
ax3.legend()
ax1.set_xlabel('time [s]')
ax2.set_xlabel('energy [keV]')
ax3.set_xlabel("Coil current [kAt]")
ax1.set_ylabel('losses')
ax2.set_ylabel('losses')
ax3.set_ylabel("Normalised PFC power flux")
ax1.set_title('')
ax2.set_title('')
ax3.set_title('')
plt.show()

outputs=templates.plot_mod.get_output_files(batch_data,'dfn')

fig,ax=plt.subplots(1)
for output,current,col_val in zip(outputs,batch_data.parameters__currents_upper,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output']))):
    if output: output.plot(fig=fig,ax=ax,axes=['R'],label=current,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200)
ax.legend()
plt.show()

#cycle through poincare maps
outputs=templates.plot_mod.get_output_files(batch_data,'poinc')
axisymm=None
for run_number,output in enumerate(outputs):
    equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=batch_data.args_batch['RMP_study__filepath_equilibrium'][run_number],GEQDSKFIX1=True,GEQDSKFIX2=True)
    if 'B3D_EX' in batch_data.args_batch['LOCUST_run__flags'][run_number] and output is not None: #this is the 2D case    
        fig,ax=plt.subplots(1)
        output.plot(LCFS=equilibrium,limiters=equilibrium,ax=ax,fig=fig)
        equilibrium.plot(fill=False,ax=ax,fig=fig)
        plt.show()
        
#################################
 
##################################################################
 
###################################################################################################