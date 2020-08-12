#plot_scan_rigid.py
 
"""
Samuel Ward
03/08/20
----
script for plotting rigid rotation 
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

import scan_rigid_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'rund')

for plasma_state_counter,(Pr,tftE) in enumerate(zip(batch_data.parameters__kinetic_profs_Pr,batch_data.parameters__kinetic_profs_tF_tE)):

    scan_range=len(batch_data.parameters__phases_upper)
    plasma_state_slice=slice(plasma_state_counter*scan_range,(plasma_state_counter+1)*scan_range)
    global_phase_shift=batch_data.parameters__phases_upper
    PFC_power=np.array([output['PFC_power']['total'] if (output is not None and output['run_status']=='completed') else -10. for output in outputs[plasma_state_slice]])

    relative_phases_upper_middle=batch_data.parameters__phases_upper-batch_data.parameters__phases_middle
    relative_phases_upper_lower=batch_data.parameters__phases_upper-batch_data.parameters__phases_lower

    fig,ax=plt.subplots(1)
    ax.scatter(batch_data.parameters__phases_upper,PFC_power/1.e6)
    ax.set_xlabel('Absolute rigid phase $\mathrm{d}\Phi$')
    ax.set_ylabel('PFC power flux [MW]$')
    ax.set_title(f'relative phase U:M={relative_phases_upper_middle[0]}, U:L={relative_phases_upper_lower[0]}')
    plt.show()

#################################
 
##################################################################
 
###################################################################################################