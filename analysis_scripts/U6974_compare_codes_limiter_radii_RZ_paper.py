#look at RZ, EP and EP sampled plots for TRANSP vs LOCUST vs ASCOT then animate through the limiter radii

#could also use alternate definition of : DFN_diff['dfn']=np.nan_to_num(np.log10((LOCUST_dfn_['dfn']-ASCOT_dfn_['dfn'])/np.maximum.reduce([LOCUST_dfn_['dfn'],ASCOT_dfn_['dfn']])),nan=0.,posinf=0.,neginf=0.)


import sys
import numpy as np
import context
import copy
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from classes.input_classes.equilibrium import Equilibrium
from classes.input_classes.beam_deposition import Beam_Deposition
from classes.input_classes.wall import Wall
from classes.output_classes.distribution_function import Distribution_Function
from classes.output_classes.particle_list import Final_Particle_List
import run_scripts.utils
import processing.utils
import constants
import settings


#define some colourmaps
cmap_r=settings.colour_custom([194,24,91,1])
cmap_g=settings.colour_custom([76,175,80,1])
cmap_b=settings.colour_custom([33,150,243,1])
cmap_default=settings.discrete_colmap(colmap_name='inferno_r',face_colour='white',number_bins=9) #create default colourmap
for setting_type,setting in settings.matplotlib_rc.items(): matplotlib.rc(setting_type, **setting) #enable settings

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
'''
ASCOT_files=['ascot_freia_1470026.h5','ascot_freia_1470030.h5','ascot_freia_1470033.h5','ascot_freia_1470037.h5','ascot_freia_1470041.h5','ascot_freia_1470045.h5']
ASCOT_run='ascot/run_2/' #changed ORBITMETHOD to 4, added extrapolated kinetic profiles

ASCOT_files=['ascot_freia_1470027.h5','ascot_freia_1470031.h5','ascot_freia_1470034.h5','ascot_freia_1470038.h5','ascot_freia_1470042.h5','ascot_freia_1470046.h5']
ASCOT_run='ascot/run_3/' #changed ORBITMETHOD back to 1, keep extrapolated kinetic profiles

'''
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
for radius,LOCUST_file,ASCOT_file,run_ID,colour in zip(radii,LOCUST_files,ASCOT_files,run_IDs,colours):

    #for ax_ in ax:
    #    ax_.cla()

    #toggle colourbars
    colourbars=False
    colourbar_array=[]

    LOCUST_dfn=Distribution_Function('LOCUST density (0.1s) - r = {}'.format(str(radius)),data_format='LOCUST',filename=LOCUST_run+LOCUST_file)
    TRANSP_dfn=run_scripts.utils.TRANSP_output_FI('TRANSP density (0.1s) - r = {}'.format(str(radius)),filename=shot_number+run_ID+TRANSP_files_tail_FI)
    ASCOT_dfn=Distribution_Function('ASCOT density (0.1s) - r = {}'.format(str(radius)),data_format='ASCOT',filename=ASCOT_run+ASCOT_file)

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

    #fig,ax=plt.subplots(ncols=2,sharex=True) #XXX including both ASCOT lnL and LOCUST lnL  
    fig,ax=plt.subplots(ncols=3,sharex=True) #XXX including both ASCOT lnL and LOCUST lnL  
    axes=['R','Z']

    number_bins=8
    vminmax=[5.e10,1.e12]
    lines=[]
    line_labels=[]
    for dfn,label,cmap in zip([TRANSP_dfn,ASCOT_dfn,LOCUST_dfn],['TRANSP','ASCOT','LOCUST'],[cmap_r,cmap_b,cmap_g]):
        mesh=dfn.plot(axes=axes,ax=ax[0],fig=fig,vminmax=vminmax,real_scale=True,fill=False,number_bins=number_bins,colmap=cmap,label=label)
        contours,_ = mesh.legend_elements()    
        lines.append(contours[0])
        line_labels.append(label)
    line,=ax[0].plot(equi['lcfs_r'],equi['lcfs_z'],color=settings.plot_colour_LCFS,linestyle=settings.plot_line_style_LCFS) 
    lines.append(line)
    line_labels.append('LCFS')
    line,=ax[0].plot(equi['rlim'],equi['zlim'],color=settings.plot_colour_limiters,linestyle=settings.plot_line_style_limiters) 
    lines.append(line)
    line_labels.append('true wall')
    line,=ax[0].plot(wall['rlim'],wall['zlim'],color=settings.plot_colour_limiters,linestyle='--')
    lines.append(line)
    line_labels.append('wall')
    ax[0].legend(lines,line_labels,fontsize=10)
    ax[0].set_title(r'a) Fast ion density $f$',fontsize=25,pad=20)
    ax[0].set_xlabel('R [m]',fontsize=25)  
    ax[0].set_ylabel('Z [m]',fontsize=25)  

    ASCOT_dfn_=ASCOT_dfn.transform(axes=axes)
    LOCUST_dfn_=LOCUST_dfn.transform(axes=axes)

    DFN_diff=copy.deepcopy(LOCUST_dfn)
    DFN_diff.ID='LOCUST dfn - ASCOT dfn'
    DFN_diff['dfn']=np.nan_to_num((LOCUST_dfn_['dfn']-ASCOT_dfn_['dfn'])/np.maximum.reduce([LOCUST_dfn_['dfn'],ASCOT_dfn_['dfn']]),nan=0.,posinf=0.,neginf=0.)
    
    #whilst we are here: calculate average error from all points within the LCFS
    Z_2D,R_2D=np.meshgrid(DFN_diff['Z'],DFN_diff['R'])
    R_2D,Z_2D=R_2D.flatten(),Z_2D.flatten()
    within_LCFS=processing.utils.within_LCFS(R_2D,Z_2D,equi)
    within_LCFS=within_LCFS.reshape(len(DFN_diff['R']),len(DFN_diff['Z']))
    number_points_in_plasma,mean_diff,mean_diff_abs=0,0.,0.
    for counter_R,R in enumerate(DFN_diff['R']):
        for counter_Z,Z in enumerate(DFN_diff['Z']):
            if within_LCFS[counter_R,counter_Z]:   
                number_points_in_plasma+=1
                mean_diff+=DFN_diff['dfn'][counter_R,counter_Z]
                mean_diff_abs+=np.abs(DFN_diff['dfn'][counter_R,counter_Z])
    mean_diff/=number_points_in_plasma
    mean_diff_abs/=number_points_in_plasma
    print(number_points_in_plasma)
    print(mean_diff_abs)
    print(mean_diff)

    DFN_diff['dfn']=np.nan_to_num(np.log10(np.abs(DFN_diff['dfn'])),nan=-5.)

    DFN_diff['dfn'][DFN_diff['dfn']>1.e3]=-5.
    DFN_diff_mesh=DFN_diff.plot(fig=fig,ax=ax[1],axes=axes,transform=False,real_scale=True,vminmax=[-4,0],colmap=cmap_default)
    ax[1].set_xlabel('R [m]',fontsize=25)  
    ax[1].set_ylabel('Z [m]',fontsize=25)  
    #ax[1].set_title(r'b) $\mathrm{log}_{10}(|f_{\mathrm{LOCUST}}-f_{\mathrm{ASCOT}}|\slash f_{\mathrm{LOCUST}})$',fontsize=25,pad=20) #XXX including both ASCOT lnL and LOCUST lnL
    ax[1].set_title(r'b) $\delta f$',fontsize=25,pad=20) #XXX including both ASCOT lnL and LOCUST lnL
    ax[1].plot(wall['rlim'],wall['zlim'],color=settings.plot_colour_limiters,linestyle='--',label='wall')

    for ax_ in ax:
        dr,dz=[np.abs(np.max(equi[lim])-np.min(equi[lim])) for lim in ['rlim','zlim']]  
        ax_.set_xlim([np.min(equi['rlim']-dr*0.1),np.max(equi['rlim'])+dr*0.1])
        ax_.set_ylim([np.min(equi['zlim'])-dz*0.1,np.max(equi['zlim'])+dz*0.1])
        ax_.set_xticks(np.linspace(1,2.4,8)[::2])
        ax_.set_yticks(np.linspace(-1.5,1.5,31)[::2])

    if colourbars:
        for ax_,mesh in zip([ax[1]],[DFN_diff_mesh]):
            cbar=fig.colorbar(mesh,ax=ax_,orientation='vertical',ticks=[-4,-3,-2,-1,0])
            colourbar_array.append(cbar)

    fig.set_tight_layout(True)  
    #plt.show() #XXX including both ASCOT lnL and LOCUST lnL  




#XXX including both ASCOT lnL and LOCUST lnL  
ascot_coulog=False

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


for radius,LOCUST_file,ASCOT_file,run_ID,colour in zip(radii,LOCUST_files,ASCOT_files,run_IDs,colours):

    #for ax_ in ax:
    #    ax_.cla()

    #toggle colourbars
    colourbars=True
    colourbar_array=[]

    LOCUST_dfn=Distribution_Function('LOCUST density (0.1s) - r = {}'.format(str(radius)),data_format='LOCUST',filename=LOCUST_run+LOCUST_file)
    ASCOT_dfn=Distribution_Function('ASCOT density (0.1s) - r = {}'.format(str(radius)),data_format='ASCOT',filename=ASCOT_run+ASCOT_file)
    LOCUST_dfn['E']/=1000.
    ASCOT_dfn['E']/=1000.
    ASCOT_dfn['dfn']*=beam_power/(BPCAP_ascot)
    ASCOT_dfn_=ASCOT_dfn.transform(axes=axes)
    LOCUST_dfn_=LOCUST_dfn.transform(axes=axes)
    DFN_diff=copy.deepcopy(LOCUST_dfn)
    DFN_diff.ID='LOCUST dfn - ASCOT dfn'
    DFN_diff['dfn']=np.nan_to_num((LOCUST_dfn_['dfn']-ASCOT_dfn_['dfn'])/np.maximum.reduce([LOCUST_dfn_['dfn'],ASCOT_dfn_['dfn']]),nan=0.,posinf=0.,neginf=0.)
    
    #whilst we are here: calculate average error from all points within the LCFS
    Z_2D,R_2D=np.meshgrid(DFN_diff['Z'],DFN_diff['R'])
    R_2D,Z_2D=R_2D.flatten(),Z_2D.flatten()
    within_LCFS=processing.utils.within_LCFS(R_2D,Z_2D,equi)
    within_LCFS=within_LCFS.reshape(len(DFN_diff['R']),len(DFN_diff['Z']))
    number_points_in_plasma,mean_diff,mean_diff_abs=0,0.,0.
    for counter_R,R in enumerate(DFN_diff['R']):
        for counter_Z,Z in enumerate(DFN_diff['Z']):
            if within_LCFS[counter_R,counter_Z]:   
                number_points_in_plasma+=1
                mean_diff+=DFN_diff['dfn'][counter_R,counter_Z]
                mean_diff_abs+=np.abs(DFN_diff['dfn'][counter_R,counter_Z])
    mean_diff/=number_points_in_plasma
    mean_diff_abs/=number_points_in_plasma
    print(number_points_in_plasma)
    print(mean_diff_abs)
    print(mean_diff)

    DFN_diff['dfn']=np.nan_to_num(np.log10(np.abs(DFN_diff['dfn'])),nan=-5.)
    DFN_diff['dfn'][DFN_diff['dfn']>1.e3]=-5.
    DFN_diff_mesh=DFN_diff.plot(fig=fig,ax=ax[2],axes=axes,transform=False,real_scale=True,vminmax=[-4,0],colmap=cmap_default)
    ax[2].set_xlabel('R [m]',fontsize=25)  
    ax[2].set_ylabel('Z [m]',fontsize=25)  
    #ax[2].set_title(r'c) $\mathrm{log}_{10}(|f_{\mathrm{LOCUST}}-f_{\mathrm{ASCOT}}|\slash f_{\mathrm{LOCUST}})$',fontsize=25,pad=20)
    ax[2].set_title(r'c) $\delta f\prime$',fontsize=25,pad=20) #XXX including both ASCOT lnL and LOCUST lnL
    ax[2].plot(wall['rlim'],wall['zlim'],color=settings.plot_colour_limiters,linestyle='--',label='wall')

    for ax_ in ax:
        dr,dz=[np.abs(np.max(equi[lim])-np.min(equi[lim])) for lim in ['rlim','zlim']]
        ax_.set_xlim([np.min(equi['rlim']-dr*0.1),np.max(equi['rlim'])+dr*0.1])
        ax_.set_ylim([np.min(equi['zlim'])-dz*0.1,np.max(equi['zlim'])+dz*0.1])
        ax_.set_xticks(np.linspace(1,2.4,8)[::2])
        ax_.set_yticks(np.linspace(-1.5,1.5,31)[::2])

    if colourbars:
        for ax_,mesh in zip([ax[2]],[DFN_diff_mesh]):
            cbar=fig.colorbar(mesh,ax=ax_,orientation='vertical',ticks=[-4,-3,-2,-1,0])
            colourbar_array.append(cbar)

    fig.set_tight_layout(True)  
    #plt.show() #XXX including both ASCOT lnL and LOCUST lnL  

plt.show()