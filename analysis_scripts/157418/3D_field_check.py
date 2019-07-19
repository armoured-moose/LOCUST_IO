#check DIII-D 3D field



import context
import run_scripts.utils as rutils
import numpy as np
from classes.input_classes.equilibrium import Equilibrium
import constants
import pathlib


'''
#dump perturbation in poloidal plane 
toroidal_angle=0.
output_time=0.
R_2D,Z_2D=np.meshgrid(equi['R_1D'],equi['Z_1D'])

R=R_2D.flatten()
Z=Z_2D.flatten()

phi=np.full(len(R),toroidal_angle),
time=np.full(len(R),output_time)

rutils.dump_perturbation_point_data_input(R=R,phi=phi,Z=Z,time=time) 

#dump perturbation at single point in poloidal plane, rotating toroidally

number_of_points=1000
phi=np.linspace(0.,constants.pi*2.4,number_of_points)
R=np.full(number_of_points,2.07001)
Z=np.full(number_of_points,0.69999)
time=np.full(number_of_points,0.)

rutils.dump_perturbation_point_data_input(R=R,phi=phi,Z=Z,time=time) 


'''



from classes.input_classes.perturbation import Perturbation as perturbation
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm

colmap=matplotlib.cm.get_cmap('plasma') #set default colourmap


fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2)
number_bins=50

switch='i3dr' #XXX instead of commenting etc. could add command line argparse 
switch='i3dr-1'

harmonic='n3'
harmonic='n-3'
#harmonic='n-3_phase_90' 

pulse='157418'
code='LOCUST'
folder='3D_field_checks'

filename_eq=pathlib.Path(pulse) / code / 'g157418.03000' 
equi=Equilibrium(filename_eq,'GEQDSK',filename_eq)

per_rot=perturbation('rot','LOCUST_field_data',pathlib.Path(pulse) / folder / switch / harmonic / 'field_data.out_rot') #check our perturbation at fixed RZ point but rotating toroidally
per_plane=perturbation('plane','LOCUST_field_data',pathlib.Path(pulse) / folder / switch / harmonic / 'field_data.out_plane') #check out perturbation at fixed toroidal point and examine poloidal plane

#plane is on regular poloidal grid - infer the grid dimensions
Z_dim=int(np.where(per_plane['R']==per_plane['R'][0])[0].size)
R_dim=int((per_plane['R'].size)/Z_dim)

X=per_plane['R'].reshape(R_dim,Z_dim)
Y=per_plane['Z'].reshape(R_dim,Z_dim)
#per_plane['R_1D']=per_plane['R_2D'][:,0]
#per_plane['Z_1D']=per_plane['Z_2D'][0,:]

phi_cut_off=np.abs(per_rot['phi']-2.*3.14159).argmin() #go up to 2pi
vminmax=[0,0.006]

for ax,quantity,colour in zip([ax1,ax2,ax3],['dB_field_R','dB_field_Z','dB_field_tor'],['k','r','b']):
    Z=np.abs(per_plane[quantity].reshape(R_dim,Z_dim))
    mesh=ax.pcolormesh(X,Y,Z,cmap=colmap,vmin=np.amin(vminmax),vmax=np.amax(vminmax))
    fig.colorbar(mesh,ax=ax,orientation='vertical')
    ax.set_title(quantity)
    ax.set_aspect('equal')
    ax.plot(equi['lcfs_r'],equi['lcfs_z'],'m') #add a LCFS
    ax4.plot(per_rot['phi'][0:phi_cut_off],per_rot[quantity][0:phi_cut_off],colour) #plot the toroidal variation

ax4.set_title(harmonic[0:-1])
ax4.legend(['dB_field_R','dB_field_Z','dB_field_tor'])
plt.show()