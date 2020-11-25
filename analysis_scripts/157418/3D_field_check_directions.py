#3D_field_check_direction.py
 
"""
Samuel Ward
22/06/2019
----
check direction of 3D DIII-D field using new perturbation.plot_components and perturbation.evaluate functions
---
usage:
 
---
"""

import context
from classes.input_classes.perturbation import Perturbation as pert
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
colmap=matplotlib.cm.get_cmap('plasma') #set default colourmap
import numpy as np


i3dr=+1
phase=np.pi/2
n=-3
phi=np.linspace(0,2*3.14159,100)
R=2.0701
Z=0.69999

p=pert('','LOCUST','sample_BPLASMA_n3',mode_number=n)
p.plot_components(R=R,Z=Z,phi=0,phase=phase,i3dr=i3dr,colmap=colmap,absolute=False,vminmax=[0,0.006])

#print([dB for dB in p.evaluate(R=,phi=,Z=)]) #compare vs example field

exit()

#Mike's code
#'''
r_index=np.argmin(np.abs(p['R_1D']-R))
z_index=np.argmin(np.abs(p['Z_1D']-Z))
br=p['dB_field_R_real']
br2=p['dB_field_R_imag']
bz=p['dB_field_Z_real']
bz2=p['dB_field_Z_imag']
bt=p['dB_field_tor_real']
bt2=p['dB_field_tor_imag']

amp_br=(br**2+br2**2)**0.5
amp_bz=(bz**2+bz2**2)**0.5
amp_bt=(bt**2+bt2**2)**0.5
phas_br=np.arctan2(br,br2)
phas_bz=np.arctan2(bz,bz2)
phas_bt=np.arctan2(bt,bt2)

ntor=3
dshift=0#np.pi/2.    

print(phas_br[r_index,z_index])
print(phas_bz[r_index,z_index])
print(phas_bt[r_index,z_index])

loc_br=amp_br[r_index,z_index]*np.sin(phas_br[r_index,z_index]+phi*ntor+dshift)
loc_bz=amp_bz[r_index,z_index]*np.sin(phas_bz[r_index,z_index]+phi*ntor+dshift)
loc_btor=amp_bt[r_index,z_index]*np.sin(phas_bt[r_index,z_index]+phi*ntor+dshift)

plt.plot(phi,loc_br,'k-')
plt.plot(phi,loc_bz,'r-')
plt.plot(phi,loc_btor,'b-')
plt.show()
#'''
