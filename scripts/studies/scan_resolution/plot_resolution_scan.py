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

import scan_resolution_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'rund')

fig,ax=plt.subplots(1)
for run_number,output in enumerate(outputs):
    if 'B3D_EX' not in batch_data.args_batch['LOCUST_run__flags'][run_number]: #this is the 2D case
        ax.axhline(np.log10(output['PFC_power']['total']),color='red',label='2D case')
    elif output is not None:
        ax.scatter(np.log10(batch_data.parameters__perturbation_resolutions_R[run_number]),np.log10(output['PFC_power']['total']),color='b',marker='x',linestyle='-')

ax.set_xlabel("Perturbation grid spacing (log) [m]")
ax.set_ylabel("Normalised PFC power flux")
ax.legend()
plt.show()

#################################
 
##################################################################
 
###################################################################################################