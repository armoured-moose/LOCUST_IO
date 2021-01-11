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

PFC_power=np.array(PFC_power).reshape(len(batch_data.configs_beam_1),len(batch_data.parameters__kinetic_profs_Pr),len(batch_data.parameters__phases_upper),len(batch_data.parameters__phases_lower))

fig,ax=plt.subplots(len(batch_data.parameters__kinetic_profs_Pr),len(batch_data.configs_beam_1))
counter=0 #counter over different scenarios
for beam_config_counter,(config_beam_1,config_beam_2) in enumerate(zip(batch_data.configs_beam_1,batch_data.configs_beam_2)):
    for plasma_state_counter,(Pr,tftE) in enumerate(zip(batch_data.parameters__kinetic_profs_Pr,batch_data.parameters__kinetic_profs_tF_tE)):
        dLPHASE,dUPHASE=batch_data.parameters__phases_lower[1]-batch_data.parameters__phases_lower[0],batch_data.parameters__phases_upper[1]-batch_data.parameters__phases_upper[0]
        LPHASE,UPHASE=np.append(batch_data.parameters__phases_lower,batch_data.parameters__phases_lower[-1]+dLPHASE),np.append(batch_data.parameters__phases_upper,batch_data.parameters__phases_upper[-1]+dUPHASE)
        mesh=ax[plasma_state_counter,beam_config_counter].pcolormesh(LPHASE-dLPHASE/2.-30.,UPHASE-dUPHASE/2.-30.,100*PFC_power[beam_config_counter,plasma_state_counter]/Pinj,cmap=settings.discrete_colmap(colmap_name='inferno',face_colour='black',number_bins=11),edgecolor='none',antialiased=True,vmin=0,vmax=10)
        ax[plasma_state_counter,beam_config_counter].set_xticks(batch_data.parameters__phases_lower-30.)
        ax[plasma_state_counter,beam_config_counter].set_yticks(batch_data.parameters__phases_upper-30.)
        ax[plasma_state_counter,beam_config_counter].set_xlim([np.min(batch_data.parameters__phases_lower)-30.,np.max(batch_data.parameters__phases_lower)-30.])
        ax[plasma_state_counter,beam_config_counter].set_ylim([np.min(batch_data.parameters__phases_upper)-30.,np.max(batch_data.parameters__phases_upper)-30.])
        ax[plasma_state_counter,beam_config_counter].set_xlabel('$\Delta\Phi_{\mathrm{L}}$')
        ax[plasma_state_counter,beam_config_counter].set_ylabel('$\Delta\Phi_{\mathrm{U}}$')
        ax[plasma_state_counter,beam_config_counter].text(x=0.05,y=0.1,s=r'Pr={}, $\tau_{{\Phi}}/\tau_{{\mathrm{{E}}}}={}, \mathrm{{NBI}}_{{1}},\mathrm{{NBI}}_{{2}}$=[{},{}]'.format(Pr,tftE,config_beam_1,config_beam_2),fontsize=15,horizontalalignment='left',transform=ax[plasma_state_counter,beam_config_counter].transAxes,color=settings.cmap_w(0.))
        counter+=1

fig.suptitle('Total NBI power loss (%)',fontsize=35)
fig.colorbar(mesh,ax=ax.ravel().tolist())
#fig.set_tight_layout(True)  
plt.show()

#################################
 
##################################################################
 
###################################################################################################