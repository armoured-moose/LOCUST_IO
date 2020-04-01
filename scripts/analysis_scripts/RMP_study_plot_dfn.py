#RMP_study_plot_dfn.py
 
"""
Samuel Ward
24/02/20
----
script for plotting dfn data produced by the RMP_study_run and RMP_study_launch_static scripts
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
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    import sys
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
    from classes.output_classes.distribution_function import Distribution_Function as dfn
except:
    raise ImportError("ERROR: LOCUST_IO/src/classes/output_classes/distribution_function.py could not be imported!\nreturning\n")
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

################################################################## 
#Main 

sys.path.append("..")
try:
    import batch_scripts.RMP_study_launch_static
except:
    pass

axes=['R','Z']
xmin=0
xmax=0
ymin=0
ymax=0

def get_2D_dfn():
    for counter,dir_output in enumerate(batch_scripts.RMP_study_launch_static.args_batch['LOCUST_run__dir_output']): #within each GPU folder the path to each output is the same
        dir_output=pathlib.Path(dir_output.strip("\'"))
        dir_output_filepaths=list(dir_output.glob('*.dfn')) #get all filenames for runs corresponding to this choice of parameters    
        if dir_output_filepaths:
            for dir_output_filepath in dir_output_filepaths:
                if batch_scripts.RMP_study_launch_static.parameters__phases_upper[counter] < 0: #this is the 2D file
                    return dfn(ID='',data_format='LOCUST',filename=dir_output_filepath,phase_upper=batch_scripts.RMP_study_launch_static.parameters__phases_upper[counter])
def get_3D_dfn():
    for counter,dir_output in enumerate(batch_scripts.RMP_study_launch_static.args_batch['LOCUST_run__dir_output']): #within each GPU folder the path to each output is the same
        dir_output=pathlib.Path(dir_output.strip("\'"))
        dir_output_filepaths=list(dir_output.glob('*.dfn')) #get all filenames for runs corresponding to this choice of parameters    
        if dir_output_filepaths:
            for dir_output_filepath in dir_output_filepaths:
                if batch_scripts.RMP_study_launch_static.parameters__phases_upper[counter] > 0: #this is the 2D file
                    yield dfn(ID='',data_format='LOCUST',filename=dir_output_filepath,phase_upper=batch_scripts.RMP_study_launch_static.parameters__phases_upper[counter])

def draw_frame(output_data,ax,fig):    
    ax.collections=[]
    ax.cla() #do this for colorbar axis too
    output_data=output_data.transform(axes=axes) #plot the difference
    output_data['dfn']=dfn_2D['dfn']-output_data['dfn']
    output_data.plot(axes=axes,transform=False,fig=fig,ax=ax)
    ax.set_xlim()
    ax.set_ylim()
    ax.set_title(f'upper coil phase = {output_data.properties["phase_upper"]}')

fig,ax=plt.subplots(1)
frames=get_3D_dfn()
animation=FuncAnimation(fig,draw_frame,frames=frames,fargs=[ax,fig],repeat=True) #cycle through phases and make animation
plt.show()
animation.save(f"{batch_scripts.RMP_study_launch_static.args_batch['RMP_study__name'][0]}.gif",writer='pillow')

#################################
 
##################################################################
 
###################################################################################################