import context
from classes.input_classes.perturbation import Perturbation as pert
import numpy as np
import matplotlib
from matplotlib import cm
colmap=matplotlib.cm.get_cmap('plasma') #set default colourmap



i3dr=1
phase=2*np.pi/2
phi=np.linspace(0,2*3.14159,100)


p=pert('','LOCUST','sample_BPLASMA_n3',mode_number=-3)
#p.plot_components(R=2.0701,Z=0.69999,phi=0,phase=phase,colmap=colmap,absolute=False,vminmax=[-0.006,0.006])
p.plot_components(R=1.7701,Z=1.3,phi=0,phase=phase,colmap=colmap,absolute=False,vminmax=[-0.006,0.006])

#phi=0.
#p['dB_field_R']=np.cos(p.mode_number*phi*i3dr-phase)*p['dB_field_R_real']-np.sin(p.mode_number*phi*i3dr-phase)*p['dB_field_R_imag']
#p.plot(key='dB_field_R',colmap=colmap)
