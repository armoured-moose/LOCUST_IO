#plot_loss_grid.py
 
"""
Samuel Ward
28/05/20
----
script for plotting 2D leak rate grid
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

outputs=templates.plot_mod.get_output_files(batch_data,'rund')

for plasma_state_counter,(Pr,tftE) in enumerate(zip(batch_data.parameters__kinetic_profs_Pr,batch_data.parameters__kinetic_profs_tF_tE)):

    loss_grid_size=len(batch_data.parameters__phases_upper)*len(batch_data.parameters__phases_lower)
    plasma_state_slice=slice(plasma_state_counter*loss_grid_size,(plasma_state_counter+1)*loss_grid_size)
    PFC_power=np.array([output['PFC_power']['total'] if (output is not None and output['run_status']=='completed') else -10. for output in outputs[plasma_state_slice]]).reshape(len(batch_data.parameters__phases_upper),len(batch_data.parameters__phases_lower))

    dLPHASE,dUPHASE=batch_data.parameters__phases_lower[1]-batch_data.parameters__phases_lower[0],batch_data.parameters__phases_upper[1]-batch_data.parameters__phases_upper[0]
    LPHASE,UPHASE=np.append(batch_data.parameters__phases_lower,batch_data.parameters__phases_lower[-1]+dLPHASE),np.append(batch_data.parameters__phases_upper,batch_data.parameters__phases_upper[-1]+dUPHASE)

    fig,ax=plt.subplots(1)
    ax.set_facecolor(settings.cmap_default(np.min(PFC_power)))
    mesh=ax.pcolormesh(LPHASE-dLPHASE/2.,UPHASE-dUPHASE/2.,np.log10(PFC_power),cmap=settings.cmap_default,edgecolor='none',antialiased=True)
    ax.set_xticks(batch_data.parameters__phases_lower)
    ax.set_yticks(batch_data.parameters__phases_upper)
    ax.set_xlim([np.min(batch_data.parameters__phases_lower),np.max(batch_data.parameters__phases_lower)])
    ax.set_ylim([np.max(batch_data.parameters__phases_upper),np.min(batch_data.parameters__phases_upper)])
    ax.set_xlabel('Lower $\mathrm{d}\Phi$')
    ax.set_ylabel('Upper $\mathrm{d}\Phi$')
    fig.colorbar(mesh,ax=ax,orientation='horizontal')
    plt.show()

#################################
 
##################################################################
 
###################################################################################################