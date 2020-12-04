#plot_loss_grid.py
 
"""
Samuel Ward
28/05/20
----
script for plotting 2D leak rate grid
---
 
notes:
    phase shift origin moved to centre of coils as per Todd Evans convention         
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

import scan_upper_lower_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')

Pinj=33.e6
PFC_power=[]
for output in outputs:
    if output:
        i=np.where(output['status_flag']=='PFC_intercept_3D')[0]
        PFC_power.append([1.e6*output['f']*np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron])
    else:
        PFC_power.append([-10.])

PFC_power=np.array(PFC_power).reshape(len(batch_data.parameters__kinetic_profs_Pr),len(batch_data.parameters__phases_upper),len(batch_data.parameters__phases_lower))

for plasma_state_counter,(Pr,tftE) in enumerate(zip(batch_data.parameters__kinetic_profs_Pr,batch_data.parameters__kinetic_profs_tF_tE)):

    loss_grid_size=len(batch_data.parameters__phases_upper)*len(batch_data.parameters__phases_lower)
    plasma_state_slice=slice(plasma_state_counter*loss_grid_size,(plasma_state_counter+1)*loss_grid_size)

    dLPHASE,dUPHASE=batch_data.parameters__phases_lower[1]-batch_data.parameters__phases_lower[0],batch_data.parameters__phases_upper[1]-batch_data.parameters__phases_upper[0]
    LPHASE,UPHASE=np.append(batch_data.parameters__phases_lower,batch_data.parameters__phases_lower[-1]+dLPHASE),np.append(batch_data.parameters__phases_upper,batch_data.parameters__phases_upper[-1]+dUPHASE)

    fig,ax=plt.subplots(1)
    ax.set_facecolor(settings.cmap_default(np.min(PFC_power[plasma_state_counter])))
    mesh=ax.pcolormesh(LPHASE-dLPHASE/2.-30.,UPHASE-dUPHASE/2.-30.,100*PFC_power[plasma_state_counter]/Pinj,cmap=settings.cmap_default,edgecolor='none',antialiased=True,vmin=0,vmax=10)
    ax.set_xticks(batch_data.parameters__phases_lower-30.)
    ax.set_yticks(batch_data.parameters__phases_upper-30.)
    ax.set_xlim([np.min(batch_data.parameters__phases_lower)-30.,np.max(batch_data.parameters__phases_lower)-30.])
    ax.set_ylim([np.max(batch_data.parameters__phases_upper)-30.,np.min(batch_data.parameters__phases_upper)-30.])
    ax.set_xlabel('Lower $\mathrm{d}\Phi$')
    ax.set_ylabel('Upper $\mathrm{d}\Phi$')
    ax.set_title('Loss power as % of $P_{injected}=33\mathrm{MW}$')
    fig.colorbar(mesh,ax=ax,orientation='horizontal')
    plt.show()


#################################
 
##################################################################
 
###################################################################################################