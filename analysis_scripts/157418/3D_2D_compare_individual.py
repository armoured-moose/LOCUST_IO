#3D_2D_compare.py
 
"""
Samuel Ward
22/04/2019
----
compare results from 2D and 3D runs
---
usage:
 
todo:
    make into command-line arguement script
    add comments
    add ability to plot all 3 types of field
---
"""

import context
import glob
import copy
import support
import settings
import processing.utils
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
from matplotlib import cm
import pathlib
import constants

cmap_reds=matplotlib.cm.get_cmap('Reds_r')
cmap_blues=matplotlib.cm.get_cmap('Blues_r')

from classes.output_classes.distribution_function import Distribution_Function as DFN
from classes.output_classes.particle_list import Final_Particle_List as FPL
from classes.output_classes.moments import Moments as Mom
from classes.input_classes.equilibrium import Equilibrium as EQ
from classes.input_classes.wall import Wall as Wall
import processing.utils



shot_number='157418'

response_type='response'    
response_type='vacuum'


folder_2D='2D_23ms'  
folder_3D='3D_23ms'
folder_2D='2D_full_slow'  
folder_3D='3D_full_slow'

DFN_2D_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_2D).glob('*.dfn'))[0]
DFN_3D_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_3D).glob('*.dfn'))[0]
DFN_2D_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_2D).glob('ptcl_cache.dat'))[0]
DFN_3D_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_3D).glob('ptcl_cache.dat'))[0]
MOM_2D_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_2D).glob('*.h5'))[0]
MOM_3D_filename=list(pathlib.Path(support.dir_output_files / shot_number / response_type / folder_3D).glob('*.h5'))[0]
eq_filename='g157418.03000'
wall_filename='LOCUST_wall'

DFN_2D=DFN(ID='2D',data_format='LOCUST',filename=DFN_2D_filename)
DFN_3D=DFN(ID='3D',data_format='LOCUST',filename=DFN_3D_filename)
DFN_2D_split=FPL(ID='2D -DSPLIT',data_format='LOCUST',filename=DFN_2D_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time'])
DFN_3D_split=FPL(ID='3D -DSPLIT',data_format='LOCUST',filename=DFN_3D_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time'])
MOM_2D=Mom(ID='2D moments',data_format='LOCUST',filename=MOM_2D_filename)
MOM_3D=Mom(ID='3D moments',data_format='LOCUST',filename=MOM_3D_filename)
eq=EQ(ID='157418 300ms equilibrium',data_format='GEQDSK',filename=eq_filename,GEQDSKFIX=1)
wall=Wall(ID='157418 2D wall',data_format='GEQDSK',filename='g157418.03000')




#calculate some missing quantities and edit the data
DFN_2D_split['E']=.5*constants.species_mass*(DFN_2D_split['V_R']**2+DFN_2D_split['V_tor']**2+DFN_2D_split['V_Z']**2)/constants.charge_e
DFN_3D_split['E']=.5*constants.species_mass*(DFN_3D_split['V_R']**2+DFN_3D_split['V_tor']**2+DFN_3D_split['V_Z']**2)/constants.charge_e
#DFN_2D_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_2D_split,eq)
#DFN_3D_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_3D_split,eq)


#XXX need to check here which status flags we need to include
i=np.where((DFN_2D_split['status_flag']==-5) | (DFN_2D_split['status_flag']==-8.) | (DFN_2D_split['status_flag']==-9.) | (DFN_2D_split['status_flag']==-14.) | (DFN_2D_split['status_flag']==0.))[0] #calculate the PFC power flux
number_of_particles_2D=len(DFN_2D_split['status_flag'][i]) 
i=np.where((DFN_3D_split['status_flag']==-5) | (DFN_3D_split['status_flag']==-8.) | (DFN_3D_split['status_flag']==-9.) | (DFN_3D_split['status_flag']==-14.) | (DFN_3D_split['status_flag']==0.))[0] #calculate the PFC power flux
number_of_particles_3D=len(DFN_3D_split['status_flag'][i])
Pdep_2D_desired=1.
Pdep_3D_desired=1.
Einj_2D=80000
Einj_3D=80000
Pdep_2D_simulation=Einj_2D*number_of_particles_2D*constants.charge_e
Pdep_3D_simulation=Einj_3D*number_of_particles_3D*constants.charge_e
Pdep_scale_factor_2D=Pdep_2D_desired/Pdep_2D_simulation
Pdep_scale_factor_3D=Pdep_3D_desired/Pdep_3D_simulation

i=np.where((DFN_2D_split['status_flag']<0)&(DFN_2D_split['status_flag']>-8.))[0] #look at all markers which were lost from plasma
DFN_2D_split['PFC_power']=np.histogram(DFN_2D_split['time'][i],bins=100,weights=DFN_2D_split['E'][i]*constants.charge_e*Pdep_scale_factor_2D)[0] #place against same time base as LOCUST
DFN_2D_split['PFC_power']=np.cumsum(DFN_2D_split['PFC_power'])
i=np.where((DFN_3D_split['status_flag']<0)&(DFN_3D_split['status_flag']>-8.))[0]
DFN_3D_split['PFC_power']=np.histogram(DFN_3D_split['time'][i],bins=100,weights=DFN_3D_split['E'][i]*constants.charge_e*Pdep_scale_factor_3D)[0] #place against same time base as LOCUST
DFN_3D_split['PFC_power']=np.cumsum(DFN_3D_split['PFC_power'])

DFN_2D_split['weight']=DFN_2D_split['E']*constants.charge_e*Pdep_scale_factor_2D
DFN_3D_split['weight']=DFN_3D_split['E']*constants.charge_e*Pdep_scale_factor_3D

DFN_2D=DFN_2D.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)
DFN_3D=DFN_3D.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)





fig,((ax1,ax2),(ax3,ax4))=plt.subplots(2,2)

'''
mesh_2D=DFN_2D.plot(fig=fig,ax=ax1,axes=['E','V_pitch'],vminmax=[0,30000.])
mesh_3D=DFN_3D.plot(fig=fig,ax=ax2,axes=['E','V_pitch'],vminmax=[0,30000.])
ax1.set_xlim(10000,85000)
ax1.set_ylim(-1,1)
ax2.set_xlim(10000,85000)
ax2.set_ylim(-1,1)
'''

DFN_2D.plot(fig=fig,ax=ax1,axes=['R','Z'],real_scale=True,limiters=wall)
DFN_3D.plot(fig=fig,ax=ax2,axes=['R','Z'],real_scale=True,limiters=wall)
#for ax,mesh in zip([ax1,ax2],[mesh_2D,mesh_3D]):
#    cbar=fig.colorbar(mesh,ax=ax,orientation='vertical')


#DFN_3D_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept'],colmap=settings.cmap_k,weight=True,number_bins=300)#,style='scatter') #as a function of energy
#DFN_2D_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept'],colmap=settings.cmap_b,weight=True,number_bins=300)#,style='scatter') 
#DFN_2D_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept'],colfield='E',colmap=cmap_blues,weight=True,style='scatter',real_scale=True,limiters=wall) #scatter in RZ space 
#DFN_3D_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept'],colfield='E',colmap=cmap_reds,weight=True,style='scatter',real_scale=True,limiters=wall) 
DFN_2D_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept'],weight=True,style='histogram',real_scale=True,number_bins=500,limiters=wall) #heat in RZ space 
DFN_3D_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept'],weight=True,style='histogram',real_scale=True,number_bins=500,limiters=wall) 
#DFN_3D_split.plot(fig=fig,ax=ax3,axes=['phi','Z'],status_flags=['PFC_intercept'],colfield='E',colmap=cmap_reds,weight=True,style='scatter') 
#DFN_2D_split.plot(fig=fig,ax=ax3,axes=['phi','Z'],status_flags=['PFC_intercept'],colfield='E',colmap=cmap_blues,weight=True,style='scatter') #in Z phi space 
#DFN_2D_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept'],colmap=settings.cmap_g,weight=True,style='histogram',number_bins=100) #heat in R space 
#DFN_3D_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept'],colmap=settings.cmap_r,weight=True,style='histogram',number_bins=100) 


moment_to_plot='density'
MOM_2D.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_b)
MOM_3D.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_k)
ax4.set_xlim([0.6,1.1])
ax4.set_ylim([0.,8e11])
plt.show()

plt.plot(100*DFN_2D_split['PFC_power']/Pdep_2D_desired,color='b') #100 to turn into percentage
plt.plot(100*DFN_3D_split['PFC_power']/Pdep_3D_desired,color='k')
plt.title('% PFC power/Pdep')
plt.legend(('2D','3D'))
plt.show()

fig,((ax1))=plt.subplots(1) #plot the difference
DFN_2D=DFN_2D.transform(axes=['E','V_pitch']) 
DFN_3D=DFN_3D.transform(axes=['E','V_pitch'])
DFN_diff=copy.deepcopy(DFN_3D)
DFN_diff['dfn']=DFN_3D['dfn']-DFN_2D['dfn']
DFN_diff_mesh=DFN_diff.plot(ax=ax1,fig=fig,axes=['E','V_pitch'],transform=False)
cbar=fig.colorbar(DFN_diff_mesh,ax=ax1,orientation='vertical')
ax1.set_xlim(10000,85000)
ax1.set_ylim(-1,1)
plt.show()
#################################
 
##################################################################
 
###################################################################################################
