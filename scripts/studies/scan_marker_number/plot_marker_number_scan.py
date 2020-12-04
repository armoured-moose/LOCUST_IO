#plot_marker_number_scan.py
 
"""
Samuel Ward
17/08/20
----
look at effects of changing number of markers
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

import scan_marker_number_launch as batch_data

outputs=templates.plot_mod.get_output_files(batch_data,'fpl')

fig = plt.figure()
ax1 = fig.add_subplot(222)
ax2 = fig.add_subplot(221)
ax3 = fig.add_subplot(212)

Pinj=33.e6
for counter,(output,col_val) in enumerate(zip(outputs,np.linspace(0,1,len(batch_data.args_batch['LOCUST_run__dir_output'])))):
    if output: 

        output['E']/=1000. #convert to keV
        i=np.where(output['status_flag']=='PFC_intercept_3D')[0]
        number_markers=len(output['weight'])
        PFC_power=1.e6*output['f']*np.sum((output['V_R'][i]**2+output['V_phi'][i]**2+output['V_Z'][i]**2)*output['FG'][i])*0.5*constants.mass_deuteron
        ax3.scatter(np.log2(number_markers),100*PFC_power/Pinj,color=settings.cmap_default(col_val),label=number_markers)
        print(f'number_markers={number_markers},FG={output["FG"][0]},f={output["f"]}')
        output['weight']/=output['weight']*number_markers #normalise weights according to number markers
        output.plot(fig=fig,ax=ax1,axes=['R'],fill=False,label=number_markers,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)
        output.plot(fig=fig,ax=ax2,axes=['E'],fill=False,label=output.ID,colmap=settings.cmap_default,colmap_val=col_val,number_bins=200,weight=True)

#ax3.legend()
ax1.set_xlabel('R [m]')
ax2.set_xlabel('marker energy [keV]')
ax3.set_xlabel('$\mathrm{log}_{2}(n_{\mathrm{markers}})$ ')
ax1.set_ylabel('marker loss fraction')
ax2.set_ylabel('marker loss fraction')
ax3.set_ylabel('% loss power')
for ax in [ax1,ax2,ax3]: ax.set_title('')

plt.show()

#################################
 
##################################################################
 
###################################################################################################