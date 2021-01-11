#plot_resolution_scan.py
 
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
    from matplotlib.animation import FuncAnimation
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

import scan_resolution_launch as batch_data

#cycle through poincare maps
outputs=templates.plot_mod.get_output_files(batch_data,'poinc')
for run_number,output in enumerate(outputs):
    equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=batch_data.args_batch['RMP_study__filepath_equilibrium'][run_number],GEQDSKFIX1=True,GEQDSKFIX2=True)
    fig,ax=plt.subplots(1)
    if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number] and output is not None: #this is the 2D case    
        equilibrium.plot()
    elif output is not None:
        output.plot(ax=ax,fig=fig,LCFS=equilibrium,limiters=equilibrium,real_scale=True)
        ax.set_xlim([4.5,6.0])
        ax.set_ylim([-4.0,-1.3])
    plt.show()

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')
fig,ax=plt.subplots(1)
Pinj=33.e6
Einj=1.e6
for run_number,output in enumerate(outputs):
    if output is not None:
        i=np.where(output['status_flag']=='PFC_intercept_3D')[0]
        PFC_power=100.*1.e6*output['f']*np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron/Pinj
        #weight_factor=Pinj/np.sum(output['weight']*Einj*constants.charge_e)
        #print(1.e6*output['f']*np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron)
        #print(np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron)
        #print(batch_data.parameters__perturbation_resolutions_R[run_number])
        if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number]: #this is the 2D case
            ax.axhline(PFC_power,color='red',label='axisymmetric field',linewidth=2)
        else:
            ax.scatter(np.log10(batch_data.parameters__perturbation_resolutions_R[run_number]),PFC_power,color='black',marker='x',linestyle='solid',alpha=1,linewidth=2)
ax.set_xlabel("Perturbation grid spacing [m] [log$_{10}$]")
ax.set_ylabel("% loss power")
ax.legend()
plt.show()

outputs=templates.plot_mod.get_divergence_files(batch_data)
fig,ax=plt.subplots(1)
for run_number,output in enumerate(outputs):
    if output is not None:
        field_data_RZ,field_data_XY=output
        divB=np.log10(np.sum(np.abs(field_data_RZ['divB']))/len(field_data_RZ['divB'].flatten()))
        if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number]: #this is the 2D case
            ax.axhline(divB,color='red',label='2D case')
        else:
            ax.scatter(np.log10(batch_data.parameters__perturbation_resolutions_R[run_number]),divB,color='black',marker='x',linestyle='solid',alpha=1,linewidth=2)
            #ax.scatter(np.log10(batch_data.parameters__perturbation_resolutions_R[run_number]),divB,color='black',marker='x',linestyle='-',alpha=1,linewidth=2)

ax.set_xlabel(r"Perturbation grid spacing [m] [log$_{10}$]")
ax.set_ylabel(r"Mean $\nabla B$ [log$_{10}$]")
plt.show()

'''
outputs=templates.plot_mod.get_divergence_files(batch_data)
fig,ax=plt.subplots(1)
def plot_divergence(output,fig,ax): 
    try:
        if output:   
            ax.cla()
            field_data_RZ,field_data_XY=output
            field_data_RZ.plot(key='divB',fill=False,ax=ax,fig=fig)
        else:
            ax.cla()
    except:
        pass
animation=FuncAnimation(fig,plot_divergence,frames=outputs,fargs=[fig,ax],repeat=True,interval=1)
plt.show()
animation.save('divergence_animation.gif',writer='pillow')
'''

#################################
 
##################################################################
 
###################################################################################################