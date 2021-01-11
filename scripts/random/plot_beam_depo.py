import context
import numpy as np
import settings
from classes.input_classes.beam_deposition import Beam_Deposition as bd 
import matplotlib.pyplot as plt

def read_beam_depo_IDS(shot,run,source,**properties):
    """
    reads birth profile from a distribution_sources IDS and returns as a dictionary
 
    notes:
        retains coordinate names from IMAS entries - must overwrite these manually
        reads in an arbitrary number of coordinates and injectors for each source        
        assumes that all sources have the same coordinate structure
        assumes markers hold only one time slice, at ...markers[0]
    """
    print("reading beam deposition from IDS")
    try:
        import imas 
    except:
        raise ImportError("ERROR: read_beam_depo_IDS could not import IMAS module!\nreturning\n")
        return
    input_IDS=imas.ids(int(shot),int(run)) #initialise new blank IDS
    if 'username' not in properties: properties['username']=settings.username
    if 'imasdb' not in properties: properties['imasdb']=settings.imasdb
    if 'imas_version' not in properties: properties['imas_version']=settings.imas_version
    input_IDS.open_env(properties['username'],properties['imasdb'],properties['imas_version'])
    input_IDS.distribution_sources.get() #open the file and get all the data from it
    input_data = {} #initialise blank dictionary to hold the data
    input_data['weight']=[]
    for identifier in input_IDS.distribution_sources.source[0].markers[0].coordinate_identifier: #generate keys for input_data by looking at the coordinates of the particle markers
        input_data[identifier.name.replace('\x00','').strip()]=[] #need to remove the unicode bits
    for source in [input_IDS.distribution_sources.source[source]]: #cycle through all possible sources    
        if len(source.markers)>0:
            if len(source.markers[0].positions)>0:
                for coordinate_index in range(len(source.markers[0].positions[0,:])): #loop over the possible coordinate types e.g. r, phi, z
                    coordinate_name=source.markers[0].coordinate_identifier[coordinate_index].name.replace('\x00','').strip()
                    for marker in source.markers[0].positions[:,coordinate_index]: #this range should/must be the same for all values of coordinate_index
                        input_data[coordinate_name].extend([marker])    
            if len(source.markers[0].weights)>0: #if markers have defined weights
                input_data['weight'].extend(source.markers[0].weights)
    for key in input_data: #convert to numpy arrays
        input_data[key]=np.asarray(input_data[key])
    #check for common field names to convert to LOCUST_IO variable names
    #possible field names for different codes
    nemo_names=['Energy','Rhotor','V_PHI','Pitch angle'] 
    bbnbi_names=['z','vx','vy','vz','energy','pitch']
    #matching LOCUST_IO fields that we want to have instead
    locust_io_names=[
    ['E','rho_tor','V_phi','V_pitch'],
    ['Z','V_X','V_Y','V_Z','E','V_pitch']
    ]
    for code_counter,code_names in enumerate([nemo_names,bbnbi_names]):
        for code_name,locust_io_name in zip(code_names,locust_io_names[code_counter]):
            if code_name in input_data.keys():
                input_data[locust_io_name]=input_data.pop(code_name)
    input_IDS.close()
    print("finished reading beam deposition from IDS")
    return input_data


HNB1=bd('') #open some blank beam depositions
HNB2=bd('')
HNB1.data=read_beam_depo_IDS(66,66,0)
HNB2.data=read_beam_depo_IDS(66,66,1)


import matplotlib as mpl
import matplotlib
mpl.rcParams.update(mpl.rcParamsDefault)

matplotlib_rc={} #matplotlib RC settings
matplotlib_rc['font'] = {
                        'family'     : 'Bitstream Vera Sans', 
                        'serif'      : 'DejaVu Serif', 
                        'sans-serif' : 'Arial', 
                        'weight'     : 'normal',
                        'size'       :  20
                        }
matplotlib_rc['lines'] = {
                        'linewidth' : 2.,
                        'linestyle' : 'solid'
                        }
matplotlib_rc['axes'] = {    
                        'labelsize' : 30,
                        'titlesize' : 30
                        }
matplotlib_rc['figure'] = {    
                        'titlesize' : 30,
                        'figsize' : [10.,8.]
                        }
matplotlib_rc['legend'] = {
                        'loc' : 'best'    
                        }
for setting_type,setting in matplotlib_rc.items(): matplotlib.rc(setting_type, **setting) #enable settings


cmap_blue_nice=settings.colour_custom([25,118,210,1])
cmap_green_nice=settings.colour_custom([76,175,80,1])
cmap_red_nice=settings.colour_custom([244,67,54,1])

fig,ax=plt.subplots(1,2)

HNB1.plot(axes=['R'],fig=fig,ax=ax[0],colmap=cmap_green_nice,number_bins=200)
HNB2.plot(axes=['R'],fig=fig,ax=ax[0],colmap=cmap_blue_nice,number_bins=200)

HNB1.plot(axes=['Z'],fig=fig,ax=ax[1],colmap=cmap_green_nice,number_bins=200,label='off-axis')
HNB2.plot(axes=['Z'],fig=fig,ax=ax[1],colmap=cmap_blue_nice,number_bins=200,label='on-axis')

ax[0].set_ylabel('NBI deposition [ions s$^{-1}$]',fontsize=35)
ax[0].set_xlabel('R [m]')
ax[1].set_xlabel('Z [m]')
ax[1].legend()

fig.set_tight_layout(True)
plt.show()

