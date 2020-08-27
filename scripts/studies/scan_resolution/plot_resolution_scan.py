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
'''
outputs=templates.plot_mod.get_output_files(batch_data,'rund')

fig,ax=plt.subplots(1)
for run_number,output in enumerate(outputs):
    if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number]: #this is the 2D case
        ax.axhline(np.log10(output['PFC_power']['total']),color='red',label='2D case')
    elif output is not None:
        ax.scatter(np.log10(batch_data.parameters__perturbation_resolutions_R[run_number]),output['PFC_power']['total'],color='b',marker='x',linestyle='-')

ax.set_xlabel("Perturbation grid spacing (log) [m]")
ax.set_ylabel("Normalised PFC power flux")
ax.legend()
plt.show()
'''

outputs=templates.plot_mod.get_divergence_files(batch_data)
fig,ax=plt.subplots(1)
def plot_divergence(output,fig,ax): 
    if output:   
        ax.cla()
        field_data_RZ,field_data_XY=output
        field_data_RZ.plot(key='divB',fill=False,ax=ax,fig=fig)
    else:
        ax.cla()
animation=FuncAnimation(fig,plot_divergence,frames=outputs,fargs=[fig,ax],repeat=True,interval=1)
plt.show()
#animation.save('divergence_animation.gif',writer='pillow')


#cycle through poincare maps
outputs=templates.plot_mod.get_output_files(batch_data,'poinc')
axisymm=None
for run_number,output in enumerate(outputs):
    equilibrium=Equilibrium(ID='',data_format='GEQDSK',filename=batch_data.args_batch['RMP_study__filepath_equilibrium'][run_number],GEQDSKFIX1=True,GEQDSKFIX2=True)
    fig,ax=plt.subplots(1)
    if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number] and output is not None: #this is the 2D case    
        axisymm=output
    elif output is not None:
        output.plot(ax=ax,fig=fig)
    if axisymm:
        axisymm.plot(LCFS=equilibrium,limiters=equilibrium,colmap=settings.cmap_w,ax=ax,fig=fig) #XXX reduce alpha for this in future
    plt.show()

#################################
 
##################################################################
 
###################################################################################################