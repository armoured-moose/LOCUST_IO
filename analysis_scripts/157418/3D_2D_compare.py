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
    add minor radius vs phi plots
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
run_type='full_slow'
run_type='23ms'
eq_filename=support.dir_input_files / shot_number / 'LOCUST' / 'g157418.03000'
wall_filename=eq_filename
folder_name_vacuum='response_hi_res'
folder_name_response='response_hi_res_-90_i3dr1'


folder_2D='2D_'+run_type
folder_3D='3D_'+run_type

DFN_2D_vacuum_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_2D).glob('*.dfn'))[0]
DFN_2D_response_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_2D).glob('*.dfn'))[0]
DFN_3D_vacuum_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_3D).glob('*.dfn'))[0]
DFN_3D_response_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_3D).glob('*.dfn'))[0]
DFN_2D_vacuum_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_2D).glob('ptcl_cache.dat'))[0]
DFN_2D_response_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_2D).glob('ptcl_cache.dat'))[0]
DFN_3D_vacuum_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_3D).glob('ptcl_cache.dat'))[0]
DFN_3D_response_split_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_3D).glob('ptcl_cache.dat'))[0]
MOM_2D_vacuum_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_2D).glob('*.h5'))[0]
MOM_2D_response_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_2D).glob('*.h5'))[0]
MOM_3D_vacuum_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_vacuum / folder_3D).glob('*.h5'))[0]
MOM_3D_response_filename=list(pathlib.Path(support.dir_output_files / shot_number / 'LOCUST' / folder_name_response / folder_3D).glob('*.h5'))[0]

DFN_2D_vacuum=DFN(ID='2D with vacuum deposition',data_format='LOCUST',filename=DFN_2D_vacuum_filename)
DFN_2D_response=DFN(ID='2D with response deposition',data_format='LOCUST',filename=DFN_2D_response_filename)
DFN_3D_vacuum=DFN(ID='3D with vacuum field',data_format='LOCUST',filename=DFN_3D_vacuum_filename)
DFN_3D_response=DFN(ID='3D with response field',data_format='LOCUST',filename=DFN_3D_response_filename)

DFN_2D_vacuum_split=FPL(ID='2D -DSPLIT with vacuum deposition',data_format='LOCUST',filename=DFN_2D_vacuum_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time','PFC_intercept'])
DFN_2D_response_split=FPL(ID='2D -DSPLIT with response deposition',data_format='LOCUST',filename=DFN_2D_response_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time','PFC_intercept'])
DFN_3D_vacuum_split=FPL(ID='3D -DSPLIT with vacuum field',data_format='LOCUST',filename=DFN_3D_vacuum_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time','PFC_intercept'])
DFN_3D_response_split=FPL(ID='3D -DSPLIT with response field',data_format='LOCUST',filename=DFN_3D_response_split_filename,compression=True,coordinates=['R','Z','V_R','phi','V_tor','V_Z','status_flag','time','PFC_intercept'])

MOM_2D_vacuum=Mom(ID='2D moments',data_format='LOCUST',filename=MOM_2D_vacuum_filename)
MOM_2D_response=Mom(ID='2D moments',data_format='LOCUST',filename=MOM_2D_response_filename)
MOM_3D_vacuum=Mom(ID='3D moments',data_format='LOCUST',filename=MOM_3D_vacuum_filename)
MOM_3D_response=Mom(ID='3D moments',data_format='LOCUST',filename=MOM_3D_response_filename)

eq=EQ(ID='157418 300ms equilibrium',data_format='GEQDSK',filename=eq_filename,GEQDSKFIX=1)
wall=Wall(ID='157418 2D wall',data_format='GEQDSK',filename=wall_filename)




#calculate some missing quantities and edit the data
DFN_2D_vacuum_split['E']=.5*constants.species_mass*(DFN_2D_vacuum_split['V_R']**2+DFN_2D_vacuum_split['V_tor']**2+DFN_2D_vacuum_split['V_Z']**2)/constants.charge_e
DFN_2D_response_split['E']=.5*constants.species_mass*(DFN_2D_response_split['V_R']**2+DFN_2D_response_split['V_tor']**2+DFN_2D_response_split['V_Z']**2)/constants.charge_e
DFN_3D_vacuum_split['E']=.5*constants.species_mass*(DFN_3D_vacuum_split['V_R']**2+DFN_3D_vacuum_split['V_tor']**2+DFN_3D_vacuum_split['V_Z']**2)/constants.charge_e
DFN_3D_response_split['E']=.5*constants.species_mass*(DFN_3D_response_split['V_R']**2+DFN_3D_response_split['V_tor']**2+DFN_3D_response_split['V_Z']**2)/constants.charge_e
#DFN_2D_vacuum_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_2D_vacuum_split,eq)
#DFN_2D_response_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_2D_response_split,eq)
#DFN_3D_vacuum_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_3D_vacuum_split,eq)
#DFN_3D_response_split['V_pitch']=processing.utils.pitch_calc_2D(DFN_3D_response_split,eq)



Pdep_desired=1.
Einj=80000 #eV
for DFN in [DFN_2D_vacuum_split,DFN_2D_response_split,DFN_3D_vacuum_split,DFN_3D_response_split]:

    #XXX need to check here which status flags we need to include
    i=np.where((DFN['status_flag']<=0)&(DFN['status_flag']>=-15.))[0] #calculate the PFC power flux
    number_of_markers=len(DFN['status_flag'][i]) 
    Pdep_simulation=Einj*number_of_markers*constants.charge_e #calculate Pdep as if markers in sim represented ALL the real ions (this also corrects for rejected markers)
    Pdep_scale_factor=Pdep_desired/Pdep_simulation
    DFN['weight']=DFN['E']*constants.charge_e*Pdep_scale_factor #reason why include E here is because this weight is used later as a proxy for heat load (when looking at dfn(R))
    i=np.where((DFN['PFC_intercept']<0)) #look at all markers which were lost from plasma
    DFN['PFC_power']=np.histogram(DFN['time'][i],bins=100,weights=DFN['E'][i]*constants.charge_e*Pdep_scale_factor)[0] #place against same time base as LOCUST
    DFN['PFC_power']=np.cumsum(DFN['PFC_power']) #this replicates the LOCUST way of calculating PFC power
  


DFN_2D_vacuum=DFN_2D_vacuum.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)
DFN_2D_response=DFN_2D_response.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)
DFN_3D_vacuum=DFN_3D_vacuum.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)
DFN_3D_response=DFN_3D_response.crop(R=[1.55,1.93],Z=[-0.25,0.25],inside=False)






fig,((ax1,ax2),(ax3,ax4),(ax5,ax6))=plt.subplots(3,2)

'''
mesh_2D=DFN_2D.plot(fig=fig,ax=ax1,axes=['E','V_pitch'],vminmax=[0,30000.])
mesh_3D=DFN_3D.plot(fig=fig,ax=ax2,axes=['E','V_pitch'],vminmax=[0,30000.])
ax1.set_xlim(10000,85000)
ax1.set_ylim(-1,1)
ax2.set_xlim(10000,85000)
ax2.set_ylim(-1,1)
'''

DFN_2D_vacuum.plot(fig=fig,ax=ax1,axes=['R','Z'],real_scale=True,limiters=wall,fill=False,colmap=settings.cmap_b,number_bins=5)
DFN_3D_vacuum.plot(fig=fig,ax=ax1,axes=['R','Z'],real_scale=True,limiters=wall,fill=False,colmap=settings.cmap_k,number_bins=5)
ax1.legend(tuple([DFN_2D_vacuum.ID,DFN_3D_vacuum.ID]))
DFN_2D_response.plot(fig=fig,ax=ax2,axes=['R','Z'],real_scale=True,limiters=wall,fill=False,colmap=settings.cmap_b,number_bins=5)
DFN_3D_response.plot(fig=fig,ax=ax2,axes=['R','Z'],real_scale=True,limiters=wall,fill=False,colmap=settings.cmap_r,number_bins=5)
ax2.legend(tuple([DFN_2D_response.ID,DFN_3D_response.ID]))

#for ax,mesh in zip([ax1,ax2],[mesh_2D,mesh_3D]):
#    cbar=fig.colorbar(mesh,ax=ax,orientation='vertical')


#DFN_2D_vacuum_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_b,weight=True,number_bins=300)#,style='scatter') #heat load vs time
#DFN_2D_response_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_c,weight=True,number_bins=300)#,style='scatter') 
#DFN_3D_vacuum_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_k,weight=True,number_bins=300)#,style='scatter')
#DFN_3D_response_split.plot(fig=fig,ax=ax3,axes=['time'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_r,weight=True,number_bins=300)#,style='scatter') 
#DFN_3D_response_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept_3D'],weight=True,style='histogram',real_scale=True,number_bins=500,limiters=wall) #heat in RZ space 

DFN_2D_response_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_g,weight=True,style='histogram',number_bins=100) #heat in R space 
DFN_3D_response_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_r,weight=True,style='histogram',number_bins=100) 
DFN_2D_vacuum_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_g,weight=True,style='histogram',number_bins=100) 
DFN_3D_vacuum_split.plot(fig=fig,ax=ax3,axes=['R'],status_flags=['PFC_intercept_3D'],colmap=settings.cmap_r,weight=True,style='histogram',number_bins=100) 

#DFN_3D_response_split.plot(fig=fig,ax=ax3,axes=['R','Z'],status_flags=['PFC_intercept_3D'],colfield='E',colmap=cmap_blues,weight=True,style='scatter',real_scale=True,limiters=wall) #scatter in RZ space 
#DFN_3D_response_split.plot(fig=fig,ax=ax3,axes=['phi','Z'],status_flags=['PFC_intercept_3D'],colfield='E',colmap=settings.cmap_r,weight=True,style='scatter') #in Z phi space 

moment_to_plot='density'
MOM_2D_vacuum.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_b)
MOM_3D_vacuum.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_k)
MOM_2D_response.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_b)
MOM_3D_response.plot(key=moment_to_plot,fig=fig,ax=ax4,colmap=settings.cmap_r)
ax4.set_xlim([0.6,1.1])
#ax4.set_ylim([0.,8e11])


ax5.plot(100*DFN_2D_vacuum_split['PFC_power']/Pdep_desired,color='b') #100 to turn into percentage
ax5.plot(100*DFN_2D_response_split['PFC_power']/Pdep_desired,color='b')
ax5.plot(100*DFN_3D_vacuum_split['PFC_power']/Pdep_desired,color='k')
ax5.plot(100*DFN_3D_response_split['PFC_power']/Pdep_desired,color='r')
ax5.set_title('% PFC power/Pdep')
ax5.legend(('2D vacuum','2D response','3D vacuum','3D response'))


DFN_2D_vacuum=DFN_2D_vacuum.transform(axes=['E','V_pitch']) #plot the difference
DFN_3D_vacuum=DFN_3D_vacuum.transform(axes=['E','V_pitch'])
DFN_diff_vacuum=copy.deepcopy(DFN_3D_vacuum)
DFN_diff_vacuum['dfn']=DFN_3D_vacuum['dfn']-DFN_2D_vacuum['dfn']
DFN_diff_vacuum_mesh=DFN_diff_vacuum.plot(ax=ax6,fig=fig,axes=['E','V_pitch'],transform=False,colmap=settings.cmap_k,fill=False,number_bins=5)

DFN_2D_response=DFN_2D_response.transform(axes=['E','V_pitch']) #plot the difference
DFN_3D_response=DFN_3D_response.transform(axes=['E','V_pitch'])
DFN_diff_response=copy.deepcopy(DFN_3D_response)
DFN_diff_response['dfn']=DFN_3D_response['dfn']-DFN_2D_response['dfn']
DFN_diff_response_mesh=DFN_diff_response.plot(ax=ax6,fig=fig,axes=['E','V_pitch'],transform=False,colmap=settings.cmap_r,fill=False,number_bins=5)

#cbar=fig.colorbar(DFN_diff_vacuum_mesh,ax=ax6,orientation='vertical')
ax6.set_xlim(10000,85000)
ax6.set_ylim(-1,1)
ax6.legend(('vacuum difference','response difference'))
plt.show()
#################################
 
##################################################################
 
###################################################################################################
