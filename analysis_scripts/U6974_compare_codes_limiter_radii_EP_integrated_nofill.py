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
import matplotlib
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

TRANSP_files_tail_FI='_fi_1_gc.cdf'
TRANSP_files_tail_CDF='.CDF'

#NEW

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

#LOCUST_files=['F_04-12-2018_16-10-58.977_TOTL.dfn','F_04-12-2018_15-06-13.311_TOTL.dfn','F_04-12-2018_15-10-53.134_TOTL.dfn','F_04-12-2018_17-17-41.999_TOTL.dfn','F_04-12-2018_17-19-35.424_TOTL.dfn','F_05-12-2018_01-15-34.057_TOTL.dfn']
#LOCUST_moments=['LOCUST_04-12-2018_16-10-58.977.h5','LOCUST_04-12-2018_15-06-13.311.h5','LOCUST_04-12-2018_15-10-53.134.h5','LOCUST_04-12-2018_17-17-41.999.h5','LOCUST_04-12-2018_17-19-35.424.h5','LOCUST_05-12-2018_01-15-34.057.h5']
#LOCUST_run='locust/run_2/' #added -DSOLCOL


#plot just one radius (still need to comment out desired files where necessary)
rad=0
radii=[radii[rad]]
ASCOT_files=[ASCOT_files[rad]]
run_IDs=[run_IDs[rad]]
LOCUST_files=[LOCUST_files[rad]]

#start by creating some axis objects
fig,((ax4,ax5,ax6),(ax10,ax11,ax12))=plt.subplots(2,3)


#sample point for second EP plot
r_sample_points=[1.797,2.0,2.1,1.3,1.5]
z_sample_points=[0.396,0.396,0.396,0.,0.]

#r_sample_points=[2.0511]
#z_sample_points=[0.1]

r_sample_points=[1.7835]
z_sample_points=[0.0143]

for r_sample_point,z_sample_point in zip(r_sample_points,z_sample_points):

    for ax in [ax10,ax11,ax12]:
        ax.cla()

    for radius,LOCUST_file,ASCOT_file,run_ID,colour in zip(radii,LOCUST_files,ASCOT_files,run_IDs,colours):

        #for ax in [ax4,ax5,ax6,ax10,ax11,ax12]:
        #    ax.cla()

        #toggle colourbars
        colourbars=False
        colourbar_array=[]

        LOCUST_dfn=Distribution_Function('LOCUST density (0.1s) - r = {}'.format(str(radius)),data_format='LOCUST',filename=LOCUST_run+LOCUST_file)
        TRANSP_dfn=run_scripts.utils.TRANSP_output_FI('TRANSP density (0.1s) - r = {}'.format(str(radius)),filename=shot_number+run_ID+TRANSP_files_tail_FI)
        ASCOT_dfn=Distribution_Function('ASCOT density (0.1s) - r = {}'.format(str(radius)),data_format='ASCOT',filename=ASCOT_run+ASCOT_file)

        LOCUST_dfn['E']/=1000 #so the axes are in KeV (does not affect integration since uses dE quantity)
        TRANSP_dfn['E']/=1000
        ASCOT_dfn['E']/=1000

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



        #EP

        axes=['E','V_pitch']

        vminmax=[0.,0.8e8]

        TRANSP_mesh=TRANSP_dfn.plot(axes=axes,ax=ax4,fig=fig,vminmax=vminmax)
        ASCOT_mesh=ASCOT_dfn.plot(axes=axes,ax=ax5,fig=fig,vminmax=vminmax)
        LOCUST_mesh=LOCUST_dfn.plot(axes=axes,ax=ax6,fig=fig,vminmax=vminmax)

        if colourbars is True:
            for ax,mesh in zip([ax4,ax5,ax6],[TRANSP_mesh,ASCOT_mesh,LOCUST_mesh]):
                cbar=fig.colorbar(mesh,ax=ax,orientation='vertical')
                colourbar_array.append(cbar)

        #EP

        axes=['E','V_pitch']

        vminmax=[1.e7,6.e7]
        number_bins=5

        TRANSP_mesh=TRANSP_dfn.plot(axes=axes,ax=ax12,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_r)
        ASCOT_mesh=ASCOT_dfn.plot(axes=axes,ax=ax12,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_b)
        LOCUST_mesh=LOCUST_dfn.plot(axes=axes,ax=ax12,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_g)

        if colourbars is True:
            for ax,mesh in zip([ax12],[LOCUST_mesh]):
                cbar=fig.colorbar(mesh,ax=ax,orientation='vertical')
                colourbar_array.append(cbar)

             
        #E

        axes=['E']

        #either plotting at a single point
        
        '''
        TRANSP_plot=TRANSP_dfn.dfn_integrate(space=False,energy=False) #crop and plot the TRANSP dfn
        dVOL=2.*constants.pi*LOCUST_dfn['R'][index_r_locust]*LOCUST_dfn['dR']*LOCUST_dfn['dZ'] #TRANSP volume elements dVOL are different sizes to ASCOT/LOCUST so need to do some scaling
        TRANSP_plot['dfn']=TRANSP_plot['dfn'][index_rz_transp,:]*dVOL #integrate over cell of interest and scale according to LOCUST volume elements
        ASCOT_dfn=process_output.crop(ASCOT_dfn,R=[r_sample_point],Z=[z_sample_point]) #crop and plot the ASCOT dfn
        LOCUST_dfn=process_output.crop(LOCUST_dfn,R=[r_sample_point],Z=[z_sample_point]) #crop and plot the LOCUST dfn
        '''

        #or plotting over all current space
        #'''
        TRANSP_plot=TRANSP_dfn.dfn_integrate(energy=False) #crop and plot the TRANSP dfn    
        #'''

        vminmax=[0,np.amax(1.1*TRANSP_plot['dfn'])]

        ax10.plot(TRANSP_plot['E'],TRANSP_plot['dfn'],color=cmap_r(0))
        ASCOT_dfn.plot(axes=axes,ax=ax10,fig=fig,colmap=cmap_b)
        LOCUST_dfn.plot(axes=axes,ax=ax10,fig=fig,colmap=cmap_g)

        ax10.set_xlabel('E [keV]')
        ax10.set_ylabel('[#/eV]')
        ax10.set_ylim(vminmax)

        #ax10.set_ylim([0,np.max(TRANSP_plot['dfn'])])
        #ax10.set_ylim([0,np.max([np.max(dfn) for dfn in [TRANSP_plot['dfn'],ASCOT_dfn['dfn'],LOCUST_dfn['dfn']]])]) #find current max across arrays





        #pitch
        axes=['V_pitch']

        #either plotting at a single point
        
        '''
        TRANSP_plot=TRANSP_dfn.dfn_integrate(space=False,pitch=False) #crop and plot the TRANSP dfn
        dVOL=2.*constants.pi*LOCUST_dfn['R'][index_r_locust]*LOCUST_dfn['dR']*LOCUST_dfn['dZ'] #TRANSP volume elements dVOL are different sizes to ASCOT/LOCUST so need to do some scaling
        TRANSP_plot['dfn']=TRANSP_plot['dfn'][index_rz_transp,:]*dVOL #integrate over cell of interest and scale according to LOCUST volume elements
        ASCOT_dfn=process_output.crop(ASCOT_dfn,R=[r_sample_point],Z=[z_sample_point]) #crop and plot the ASCOT dfn
        LOCUST_dfn=process_output.crop(LOCUST_dfn,R=[r_sample_point],Z=[z_sample_point]) #crop and plot the LOCUST dfn
        '''

        #or plotting over all current space
        #'''
        TRANSP_plot=TRANSP_dfn.dfn_integrate(pitch=False) #crop and plot the TRANSP dfn    
        #'''

        vminmax=[0,np.amax(1.1*TRANSP_plot['dfn'])]

        ax11.plot(TRANSP_plot['V_pitch'],TRANSP_plot['dfn'],color=cmap_r(0))
        ASCOT_dfn.plot(axes=axes,ax=ax11,fig=fig,colmap=cmap_b)
        LOCUST_dfn.plot(axes=axes,ax=ax11,fig=fig,colmap=cmap_g)

        #ax11.set_title('')
        ax11.set_xlabel('V$_{\|\|}$/V')
        ax11.set_ylabel('[#/dPitch]')
        ax11.set_ylim(vminmax)
        #ax11.set_ylim([0,np.max(TRANSP_plot['dfn'])])
        #ax11.set_ylim([0,np.max([np.max(dfn) for dfn in [TRANSP_plot['dfn'],ASCOT_dfn['dfn'],LOCUST_dfn['dfn']]])]) #find current max across arrays



             
        #set labels and plot

        for ax in [ax4,ax5,ax6]:
            ax.set_ylabel('')
            ax.set_xlabel('E [keV]')
            ax.set_xlim([0,100])
            ax.set_ylim([-0.8,0.8])
        ax4.set_ylabel('V$_{\|\|}$/V')
        ax12.set_xlabel('E [keV]')
        ax12.set_ylabel('V$_{\|\|}$/V')

        for ax in [ax10,ax11,ax12]:
            ax.set_title('')

        ax10.legend(tuple(['TRANSP','ASCOT','LOCUST']))
        ax11.legend(tuple(['TRANSP','ASCOT','LOCUST']))
        
        plt.show()
        plt.pause(0.0001)
        #fig.clear()








        #EP

        fig,ax=plt.subplots(1)

        axes=['E','V_pitch']

        vminmax=[1.e7,6.e7]
        number_bins=5

        TRANSP_mesh=TRANSP_dfn.plot(axes=axes,ax=ax,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_r)
        ASCOT_mesh=ASCOT_dfn.plot(axes=axes,ax=ax,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_b)
        LOCUST_mesh=LOCUST_dfn.plot(axes=axes,ax=ax,fig=fig,vminmax=vminmax,fill=False,number_bins=number_bins,colmap=cmap_g)
        ax.legend(['TRANSP','ASCOT','LOCUST'],fontsize=25)
        ax.set_title('Fast ion density',fontsize=25)
        ax.set_xlabel('E [keV]',fontsize=25)
        ax.set_ylabel('$V_{||}\slash V$',fontsize=25)

        plt.show()
