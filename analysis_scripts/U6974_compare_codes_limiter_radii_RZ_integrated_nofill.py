#look at RZ, EP and EP sampled plots for TRANSP vs LOCUST vs ASCOT then animate through the limiter radii

import sys
import numpy as np
import context
import matplotlib.pyplot as plt
from classes.input_classes.equilibrium import Equilibrium
from classes.input_classes.beam_deposition import Beam_Deposition
from classes.input_classes.wall import Wall
from classes.output_classes.distribution_function import Distribution_Function
from classes.output_classes.particle_list import Final_Particle_List
from processing import process_input
from processing import process_output
import run_scripts.utils
import constants
from matplotlib import cm
from matplotlib.colors import ListedColormap
import settings

#define some colourmaps
cmap_r=settings.colour_custom([194,24,91,1])
cmap_g=settings.colour_custom([76,175,80,1])
cmap_b=settings.colour_custom([33,150,243,1])

filename_eq='g157418.03000'
equi=Equilibrium(filename_eq,'GEQDSK',filename_eq)



wall_files='input.wall_2d_'
radii=['1.05','1.10','1.20','1.30','1.40','1.50'] #radii for limiter profiles
run_IDs=['U69','U70','U71','U72','U73','U74']
shot_number='157418'
colours=['r-','g-','b-','m-','k-','c-']
ascot_coulog=True

TRANSP_files_tail_FI='_fi_1_gc.cdf'
TRANSP_files_tail_CDF='.CDF'

ASCOT_files=['ascot_freia_1470025.h5','ascot_freia_1470029.h5','ascot_freia_1470032.h5','ascot_freia_1470036.h5','ascot_freia_1470040.h5','ascot_freia_1470044.h5']
ASCOT_run='ascot/run_1/' #this is with old kinetic profiles which are not extrapolated, ORBITMETHOD=1

ASCOT_files=['ascot_freia_1470026.h5','ascot_freia_1470030.h5','ascot_freia_1470033.h5','ascot_freia_1470037.h5','ascot_freia_1470041.h5','ascot_freia_1470045.h5']
ASCOT_run='ascot/run_2/' #changed ORBITMETHOD to 4, added extrapolated kinetic profiles

ASCOT_files=['ascot_freia_1470027.h5','ascot_freia_1470031.h5','ascot_freia_1470034.h5','ascot_freia_1470038.h5','ascot_freia_1470042.h5','ascot_freia_1470046.h5']
ASCOT_run='ascot/run_3/' #changed ORBITMETHOD back to 1, keep extrapolated kinetic profiles

ASCOT_files=['ascot_freia_1470028.h5','ascot_freia_1480719.h5','ascot_freia_1470035.h5','ascot_freia_1470039.h5','ascot_freia_1470043.h5','ascot_freia_1470047.h5']
ASCOT_run='ascot/run_4/' #ORBITMETHOD 4 and non-extrapolated kinetic profiles

LOCUST_beam_depo_tail='_ptcles.dat'
LOCUST_files=['F_04-12-2018_16-11-28.285_TOTL.dfn','F_03-12-2018_22-55-59.961_TOTL.dfn','F_03-12-2018_22-58-49.281_TOTL.dfn','F_03-12-2018_22-57-37.348_TOTL.dfn','F_04-12-2018_00-13-14.371_TOTL.dfn','F_04-12-2018_14-11-36.625_TOTL.dfn']
LOCUST_moments=['LOCUST_04-12-2018_16-11-28.285.h5','LOCUST_03-12-2018_22-55-59.961.h5','LOCUST_03-12-2018_22-58-49.281.h5','LOCUST_03-12-2018_22-57-37.348.h5','LOCUST_04-12-2018_00-13-14.371.h5','LOCUST_04-12-2018_14-11-36.625.h5']
LOCUST_run='locust/run_1/'
if ascot_coulog:
    LOCUST_files[0]='F_28-04-2020_23-59-02.590_TOTL.dfn'
    LOCUST_moments[0]='LOCUST_28-04-2020_23-59-02.590.h5'
    LOCUST_run='locust/U69_ascot_coulog/noSOLCOL/'

LOCUST_files=['F_04-12-2018_16-10-58.977_TOTL.dfn','F_04-12-2018_15-06-13.311_TOTL.dfn','F_04-12-2018_15-10-53.134_TOTL.dfn','F_04-12-2018_17-17-41.999_TOTL.dfn','F_04-12-2018_17-19-35.424_TOTL.dfn','F_05-12-2018_01-15-34.057_TOTL.dfn']
LOCUST_moments=['LOCUST_04-12-2018_16-10-58.977.h5','LOCUST_04-12-2018_15-06-13.311.h5','LOCUST_04-12-2018_15-10-53.134.h5','LOCUST_04-12-2018_17-17-41.999.h5','LOCUST_04-12-2018_17-19-35.424.h5','LOCUST_05-12-2018_01-15-34.057.h5']
LOCUST_run='locust/run_2/' #added -DSOLCOL
if ascot_coulog:
    LOCUST_files[0]='F_28-04-2020_18-10-55.938_TOTL.dfn'
    LOCUST_moments[0]='LOCUST_28-04-2020_18-10-55.938.h5'
    LOCUST_run='locust/U69_ascot_coulog/SOLCOL/'

#plot just one radius (still need to comment out desired files where necessary)
rad=0
radii=[radii[rad]]
ASCOT_files=[ASCOT_files[rad]]
run_IDs=[run_IDs[rad]]
LOCUST_files=[LOCUST_files[rad]]

#start by creating some axis objects
fig,(ax1)=plt.subplots(1,1)

for radius,LOCUST_file,ASCOT_file,run_ID,colour in zip(radii,LOCUST_files,ASCOT_files,run_IDs,colours):

    #for ax in [ax1,ax2,ax3]:
    #    ax.cla()

    #toggle colourbars
    colourbars=False
    colourbar_array=[]

    LOCUST_dfn=Distribution_Function('LOCUST density (0.1s) - r = {}'.format(str(radius)),'LOCUST',filename=LOCUST_run+LOCUST_file)
    TRANSP_dfn=run_scripts.utils.TRANSP_output_FI('TRANSP density (0.1s) - r = {}'.format(str(radius)),filename=shot_number+run_ID+TRANSP_files_tail_FI)
    ASCOT_dfn=Distribution_Function('ASCOT density (0.1s) - r = {}'.format(str(radius)),'ASCOT',filename=ASCOT_run+ASCOT_file)

    #import wall, redefine pitch for ASCOT vs current in DIII-D and normalise DFNs according to beam powers
    wall=Wall('limiter - '+radius,data_format='ASCOT_2D_input',filename=wall_files+radius)
    ASCOT_dfn['V_pitch']*=-1.

    TRANSP_CDF=run_scripts.utils.TRANSP_output(ID='{}'.format(shot_number+run_ID+TRANSP_files_tail_CDF),filename=shot_number+run_ID+TRANSP_files_tail_CDF) #need to scale some things by captured beam power
    output_time=3.1 #time at which the distribution function was written out
    BPCAP_index=np.abs(TRANSP_CDF['TIME']-output_time).argmin()
    BPCAP=TRANSP_CDF['BPCAP'][BPCAP_index]
    TRANSP_dfn['dfn']/=BPCAP

    beam_depo=Final_Particle_List(ID=run_ID,data_format='ASCOT',filename=ASCOT_run+ASCOT_file)
    beam_power=1. #1 Watt beam power
    beam_energy=80000
    k=np.where(beam_depo['status_flag']>0)[0] #scale by all markers which actually contributed to the simulation
    BPCAP_ascot=np.sum(beam_energy*constants.species_charge*beam_depo['weight'][k])
    ASCOT_dfn['dfn']*=beam_power/(BPCAP_ascot)

    #RZ

    axes=['R','Z']

    vminmax=[0.1e11,7.e11]

    #####optional crop of dfns in energy

    
    energy_min=18000
    energy_max=100000

    #TRANSP_dfn=process_output.crop(TRANSP_dfn,E=[energy_min,energy_max])
    #ASCOT_dfn=process_output.crop(ASCOT_dfn,E=[energy_min,energy_max])
    #LOCUST_dfn=process_output.crop(LOCUST_dfn,E=[energy_min,energy_max])

    #for ax in [ax4,ax5,ax6,ax7,ax8,ax9]: #show where we've cropped in energy
        #ax.axvline(energy_min,color='m')
        #ax.axvline(energy_max,color='m')

    #####

    #####optional crop of LOCUST/ASCOT dfns in R and Z
    

    R_min=0.
    R_max=2.
    Z_min=-0.51
    Z_max=0.51

    i=np.where((R_min<TRANSP_dfn['R2D'])&(TRANSP_dfn['R2D']<R_max)&(TRANSP_dfn['Z2D']>Z_min)&(TRANSP_dfn['Z2D']<Z_max))[0]
    #for quantity in ['dfn','dVOL','R2D','Z2D']: #remember space is first dimension in TRANSP array, so can do this
        #TRANSP_dfn[quantity]=TRANSP_dfn[quantity][i]
    #ASCOT_dfn=process_output.crop(ASCOT_dfn,R=[R_min,R_max],Z=[Z_min,Z_max])
    #LOCUST_dfn=process_output.crop(LOCUST_dfn,R=[R_min,R_max],Z=[Z_min,Z_max])

    #for ax in [ax1,ax2,ax3]: #show where we've cropped in R
        #ax.axvline(R_min,color='m')
        #ax.axvline(R_max,color='m')

    #####       

    number_bins=6

    TRANSP_mesh=TRANSP_dfn.plot(axes=axes,limiters=wall,LCFS=equi,ax=ax1,fig=fig,vminmax=vminmax,real_scale=True,fill=False,number_bins=number_bins,colmap=cmap_r)
    ASCOT_mesh=ASCOT_dfn.plot(axes=axes,limiters=wall,LCFS=equi,ax=ax1,fig=fig,vminmax=vminmax,real_scale=True,fill=False,number_bins=number_bins,colmap=cmap_b)
    LOCUST_mesh=LOCUST_dfn.plot(axes=axes,limiters=wall,LCFS=equi,ax=ax1,fig=fig,vminmax=vminmax,real_scale=True,fill=False,number_bins=number_bins,colmap=cmap_g)

    #add scatter point if you fancy

    r_sample_points=[1.7835,2.18]
    z_sample_points=[0.0143,0.37]

    for r_sample_point,z_sample_point in zip(r_sample_points,z_sample_points):


        #for point we have chosen, find closest dfn bin in real space
        diff_r=np.abs(TRANSP_dfn['R2D']-r_sample_point)**2 #irregular grid so need to minimise distance to every point
        diff_z=np.abs(TRANSP_dfn['Z2D']-z_sample_point)**2
        index_rz_transp=(diff_r+diff_z).argmin()
        r_transp=TRANSP_dfn['R2D'][index_rz_transp]
        z_transp=TRANSP_dfn['Z2D'][index_rz_transp]

        index_r_ascot=np.abs(ASCOT_dfn['R']-r_sample_point).argmin() #regular grids so can use this method
        index_z_ascot=np.abs(ASCOT_dfn['Z']-z_sample_point).argmin() 
        r_ascot=ASCOT_dfn['R'][index_r_ascot]
        z_ascot=ASCOT_dfn['Z'][index_z_ascot]

        index_r_locust=np.abs(LOCUST_dfn['R']-r_sample_point).argmin()
        index_z_locust=np.abs(LOCUST_dfn['Z']-z_sample_point).argmin()
        r_locust=LOCUST_dfn['R'][index_r_locust]
        z_locust=LOCUST_dfn['Z'][index_z_locust]

        #ax1.scatter(r_transp,z_transp,color='w',s=20)
        #ax1.scatter(r_ascot,z_ascot,color='w',s=20)
        #ax1.scatter(r_locust,z_locust,color='w',s=20)


    if colourbars is True:
        for ax,mesh in zip([ax1],[LOCUST_mesh]):
            cbar=fig.colorbar(mesh,ax=ax,orientation='vertical')
            colourbar_array.append(cbar)

    #set labels and plot

    for ax in [ax1]:
        #ax.set_title('limiter radius = {}'.format(radii[0]))
        ax.set_title('Fast ion density',fontsize=25)
        ax.set_xlabel('R [m]',fontsize=25)  
        ax.set_ylabel('Z [m]',fontsize=25)  
        #ax.set_xlim([np.min(equi['R_1D']),np.max(equi['R_1D'])])
        #ax.set_ylim([1.1*np.min(equi['lcfs_z']),1.1*np.max(equi['lcfs_z'])])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[0:2], ['TRANSP','ASCOT','LOCUST'],fontsize=25)
        #plt.legend(['TRANSP','ASCOT','LOCUST'])


    plt.draw()
    plt.pause(0.0001)
    #fig.clear()

plt.show()