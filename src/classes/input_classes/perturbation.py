#perturbation.py
 
"""
Samuel Ward
29/07/2018
----
class to handle LOCUST perturbation input data
---
usage:
    see README.md for usage
 
notes:         
---
"""


###################################################################################################
#Preamble
 
import sys #have global imports --> makes less modular (no "from input_classes import x") but best practice to import whole input_classes module anyway

try:
    import numpy as np
    import pathlib
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

try:
    import processing.utils
except:
    raise ImportError("ERROR: LOCUST_IO/processing/utils.py could not be imported!\nreturning\n")
    sys.exit(1)  

try:
    import classes.base_input 
except:
    raise ImportError("ERROR: LOCUST_IO/classes/base_input.py could not be imported!\nreturning\n")
    sys.exit(1) 

try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/support.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import constants
except:
    raise ImportError("ERROR: LOCUST_IO/constants.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    from settings import *
except:
    raise ImportError("ERROR: LOCUST_IO/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

################################################################## Perturbation read functions
 
def read_perturbation_LOCUST(filepath,**properties):
    """
    reads perturbation stored in LOCUST format

    notes:
        assumes R is slower-varying dimension in file when inferring dimensions
    """

    print("reading LOCUST perturbation")

    with open(filepath,'r') as file:
                 
        #initialise data
        input_data={}
        input_data['R_2D']=[]
        input_data['Z_2D']=[]
        input_data['B_field_R_real']=[]
        input_data['B_field_R_imag']=[]
        input_data['B_field_Z_real']=[]
        input_data['B_field_Z_imag']=[]
        input_data['B_field_tor_real']=[]
        input_data['B_field_tor_imag']=[]

        #read lazily
        for line in file:
            split_line=line.split()
            input_data['R_2D'].append(float(split_line[0]))
            input_data['Z_2D'].append(float(split_line[1]))
            input_data['B_field_R_real'].append(float(split_line[2]))
            input_data['B_field_R_imag'].append(float(split_line[3]))
            input_data['B_field_Z_real'].append(float(split_line[4]))
            input_data['B_field_Z_imag'].append(float(split_line[5]))
            input_data['B_field_tor_real'].append(float(split_line[6]))
            input_data['B_field_tor_imag'].append(float(split_line[7]))

        input_data['R_2D']=np.asarray(input_data['R_2D'])
        input_data['Z_2D']=np.asarray(input_data['Z_2D'])
        input_data['B_field_R_real']=np.asarray(input_data['B_field_R_real'])
        input_data['B_field_R_imag']=np.asarray(input_data['B_field_R_imag'])
        input_data['B_field_Z_real']=np.asarray(input_data['B_field_Z_real'])
        input_data['B_field_Z_imag']=np.asarray(input_data['B_field_Z_imag'])
        input_data['B_field_tor_real']=np.asarray(input_data['B_field_tor_real'])
        input_data['B_field_tor_imag']=np.asarray(input_data['B_field_tor_imag'])
  
        #infer the grid dimensions and axes
        if input_data['Z_2D'][0]==input_data['Z_2D'][1]: #Z is slowly-varying
            R_dim=int(np.where(input_data['Z_2D']==input_data['Z_2D'][0])[0].size)
            Z_dim=int(np.where(input_data['R_2D']==input_data['R_2D'][0])[0].size)
            input_data['R_2D']=input_data['R_2D'].reshape(Z_dim,R_dim).T
            input_data['Z_2D']=input_data['Z_2D'].reshape(Z_dim,R_dim).T
            input_data['R_1D']=input_data['R_2D'][:,0]
            input_data['Z_1D']=input_data['Z_2D'][0,:]
            input_data['B_field_R_real']=input_data['B_field_R_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_R_imag']=input_data['B_field_R_imag'].reshape(Z_dim,R_dim).T
            input_data['B_field_Z_real']=input_data['B_field_Z_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_Z_imag']=input_data['B_field_Z_imag'].reshape(Z_dim,R_dim).T
            input_data['B_field_tor_real']=input_data['B_field_tor_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_tor_imag']=input_data['B_field_tor_imag'].reshape(Z_dim,R_dim).T
        else: #R is slowly-varying
            R_dim=int(np.where(input_data['Z_2D']==input_data['Z_2D'][0])[0].size)
            Z_dim=int(np.where(input_data['R_2D']==input_data['R_2D'][0])[0].size)
            input_data['R_2D']=input_data['R_2D'].reshape(R_dim,Z_dim)
            input_data['Z_2D']=input_data['Z_2D'].reshape(R_dim,Z_dim)
            input_data['R_1D']=input_data['R_2D'][:,0]
            input_data['Z_1D']=input_data['Z_2D'][0,:]
            input_data['B_field_R_real']=input_data['B_field_R_real'].reshape(R_dim,Z_dim)
            input_data['B_field_R_imag']=input_data['B_field_R_imag'].reshape(R_dim,Z_dim)
            input_data['B_field_Z_real']=input_data['B_field_Z_real'].reshape(R_dim,Z_dim)
            input_data['B_field_Z_imag']=input_data['B_field_Z_imag'].reshape(R_dim,Z_dim)
            input_data['B_field_tor_real']=input_data['B_field_tor_real'].reshape(R_dim,Z_dim)
            input_data['B_field_tor_imag']=input_data['B_field_tor_imag'].reshape(R_dim,Z_dim)

    input_data['B_field_R']=np.sqrt(input_data['B_field_R_real']**2+input_data['B_field_R_imag']**2)
    input_data['B_field_Z']=np.sqrt(input_data['B_field_Z_real']**2+input_data['B_field_Z_imag']**2)
    input_data['B_field_tor']=np.sqrt(input_data['B_field_tor_real']**2+input_data['B_field_tor_imag']**2)
    input_data['B_field_mag']=np.sqrt(input_data['B_field_tor']**2+input_data['B_field_R']**2+input_data['B_field_Z']**2)

    print("finished reading LOCUST perturbation")
    
    return input_data

def read_perturbation_LOCUST_field_data(filepath,**properties):
    """
    notes:
        reads from the file_data.out file produced by LOCUST BCHECK mode
    """

    print("reading LOCUST test field data")

    with open(filepath,'r') as file: #open file

        input_data={}

        lines=file.readlines()
        del(lines[0]) #delete headerline

        for quantity in ['R','phi','Z','time','B_field_R_mag','B_field_tor_mag','B_field_Z_mag','dB_field_R','dB_field_tor','dB_field_Z','divB']:
            input_data[quantity]=[]

        for line in lines:
            for counter,quantity in enumerate(['R','phi','Z','time','B_field_R_mag','B_field_tor_mag','B_field_Z_mag','dB_field_R','dB_field_tor','dB_field_Z','divB']):
            
                try:
                    input_data[quantity].append(float(line.split()[counter]))
                except:
                    input_data[quantity].append(0.0)

        for quantity in ['R','phi','Z','time','B_field_R_mag','B_field_tor_mag','B_field_Z_mag','dB_field_R','dB_field_tor','dB_field_Z','divB']:
            input_data[quantity]=np.asarray(input_data[quantity])

    print("reading LOCUST test field data")

    return input_data

def read_perturbation_ASCOT_field_data(filepath,**properties):
    """
    read perturbation field data equivalent from ASCOT input particles file

    notes:
        since the input particles file essentially contains the magnetic field at different points where ions are born, this can be used to calibrate a 3D field
    """

    with open(filepath,'w') as file: #open file

        for line in file:
            if 'Number of particles' in line:
                number_particles=int(line.split()[0])
            if 'Number of different fields' in line:
                number_fields=int(line.split()[0])
                break

        fields=[] #this will hold the names of the quantites stored in the file - in order
        counter=0
        for line in file:
            fields.append(line.split()[0])
            counter+=1
            if counter==number_fields:
                break

        blank_line=file.readline() #remove read blank line XXX check this

        raw_data={} #create data dictionaries for holding all data and final returned data
        input_data={}
        for field in fields:
            raw_data[field]=[]
        
        for line_number in range(number_particles):
            line=file.readline() #XXX check this
            for number,field in zip(line.split(),fields):
                raw_data[field].extend([float(number)])

        #rename variables to LOCUST_IO conventions
        ascot_names_1=['Rprt','phiprt' ,'zprt','BR','Bphi','Bz'] #possible ASCOT fields - full orbit
        ascot_names_2=['R','phi' ,'z','BR','Bphi','Bz'] #possible ASCOT fields - guiding centre
        locust_names['R','phi','Z','B_field_R_mag','B_field_tor_mag','B_field_Z_mag'] #corresponding LOCUST_IO fields that we want to retain
        for ascot_name_1,ascot_name_2,locust_io_name in zip(ascot_names_1,ascot_names_2,locust_io_names):
            if ascot_name_1 in raw_data.keys():
                input_data[locust_io_name]=copy.deepcopy(raw_data[ascot_name_1])
                input_data[locust_io_name]=np.asarray(input_data[locust_io_name])
            elif ascot_name_2 in raw_data.keys():
                input_data[locust_io_name]=copy.deepcopy(raw_data[ascot_name_2])
                input_data[locust_io_name]=np.asarray(input_data[locust_io_name])                
    
    return input_data

'''
def read_perturbation_IDS(shot,run,**properties):
    """
    notes:

    """ 

    try:
        import imas 
    except:
        raise ImportError("ERROR: read_perturbation_IDS could not import IMAS module!\nreturning\n")
        return
'''
'''
def read_perturbation_JOREK(filepath,**properties):
    """
    notes:
    """

    try:
        import h5py
    except:
        print("ERROR: read_perturbation_JOREK could not import h5py!\n")
        return

    input_data={} #initialise data dictionary
    file = h5py.File(filepath, 'r')

    input_data['']=np.array(file['Output Data']['Fast Ions']['Profiles (1D)']['sqrt(PSIn)']) 

    return input_data
'''

def read_perturbation_MARSF(filepath,**properties):
    """
    reads perturbation stored in MARSF format

    notes:
        assumes R is quickly-varying dimension in file when inferring dimensions
    """

    print("reading MARSF perturbation")

    with open(filepath,'r') as file:
                 
        #initialise data
        input_data={}
        input_data['R_2D']=[]
        input_data['Z_2D']=[]
        input_data['B_field_R_real']=[]
        input_data['B_field_R_imag']=[]
        input_data['B_field_Z_real']=[]
        input_data['B_field_Z_imag']=[]
        input_data['B_field_tor_real']=[]
        input_data['B_field_tor_imag']=[]

        #read lazily 
        #skip header lines
        counter=0
        number_headerlines=3
        for line in file:
            counter+=1
            if counter==number_headerlines:
                break

        for line in file:
            split_line=line.split()
            input_data['R_2D'].append(float(split_line[0]))
            input_data['Z_2D'].append(float(split_line[1]))
            input_data['B_field_R_real'].append(float(split_line[2]))
            input_data['B_field_R_imag'].append(float(split_line[3]))
            input_data['B_field_Z_real'].append(float(split_line[4]))
            input_data['B_field_Z_imag'].append(float(split_line[5]))
            input_data['B_field_tor_real'].append(float(split_line[6]))
            input_data['B_field_tor_imag'].append(float(split_line[7]))

        input_data['R_2D']=np.asarray(input_data['R_2D'])
        input_data['Z_2D']=np.asarray(input_data['Z_2D'])
        input_data['B_field_R_real']=np.asarray(input_data['B_field_R_real'])
        input_data['B_field_R_imag']=np.asarray(input_data['B_field_R_imag'])
        input_data['B_field_Z_real']=np.asarray(input_data['B_field_Z_real'])
        input_data['B_field_Z_imag']=np.asarray(input_data['B_field_Z_imag'])
        input_data['B_field_tor_real']=np.asarray(input_data['B_field_tor_real'])
        input_data['B_field_tor_imag']=np.asarray(input_data['B_field_tor_imag'])
    
        #infer the grid dimensions and axes
        if input_data['Z_2D'][0]==input_data['Z_2D'][1]: #Z is slowly-varying
            R_dim=int(np.where(input_data['Z_2D']==input_data['Z_2D'][0])[0].size)
            Z_dim=int(np.where(input_data['R_2D']==input_data['R_2D'][0])[0].size)
            input_data['R_2D']=input_data['R_2D'].reshape(Z_dim,R_dim).T
            input_data['Z_2D']=input_data['Z_2D'].reshape(Z_dim,R_dim).T
            input_data['R_1D']=input_data['R_2D'][:,0]
            input_data['Z_1D']=input_data['Z_2D'][0,:]
            input_data['B_field_R_real']=input_data['B_field_R_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_R_imag']=input_data['B_field_R_imag'].reshape(Z_dim,R_dim).T
            input_data['B_field_Z_real']=input_data['B_field_Z_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_Z_imag']=input_data['B_field_Z_imag'].reshape(Z_dim,R_dim).T
            input_data['B_field_tor_real']=input_data['B_field_tor_real'].reshape(Z_dim,R_dim).T
            input_data['B_field_tor_imag']=input_data['B_field_tor_imag'].reshape(Z_dim,R_dim).T
        else: #R is slowly-varying
            R_dim=int(np.where(input_data['Z_2D']==input_data['Z_2D'][0])[0].size)
            Z_dim=int(np.where(input_data['R_2D']==input_data['R_2D'][0])[0].size)
            input_data['R_2D']=input_data['R_2D'].reshape(R_dim,Z_dim)
            input_data['Z_2D']=input_data['Z_2D'].reshape(R_dim,Z_dim)
            input_data['R_1D']=input_data['R_2D'][0,:].flatten()
            input_data['Z_1D']=input_data['Z_2D'][:,0].flatten()
            input_data['B_field_R_real']=input_data['B_field_R_real'].reshape(R_dim,Z_dim)
            input_data['B_field_R_imag']=input_data['B_field_R_imag'].reshape(R_dim,Z_dim)
            input_data['B_field_Z_real']=input_data['B_field_Z_real'].reshape(R_dim,Z_dim)
            input_data['B_field_Z_imag']=input_data['B_field_Z_imag'].reshape(R_dim,Z_dim)
            input_data['B_field_tor_real']=input_data['B_field_tor_real'].reshape(R_dim,Z_dim)
            input_data['B_field_tor_imag']=input_data['B_field_tor_imag'].reshape(R_dim,Z_dim)

    input_data['B_field_R']=np.sqrt(input_data['B_field_R_real']**2+input_data['B_field_R_imag']**2)
    input_data['B_field_Z']=np.sqrt(input_data['B_field_Z_real']**2+input_data['B_field_Z_imag']**2)
    input_data['B_field_tor']=np.sqrt(input_data['B_field_tor_real']**2+input_data['B_field_tor_imag']**2)
    input_data['B_field_mag']=np.sqrt(input_data['B_field_tor']**2+input_data['B_field_R']**2+input_data['B_field_Z']**2)

    print("finished reading MARSF perturbation")
    
    return input_data

def read_perturbation_MARSF_bplas(filepath=pathlib.Path(''),response=True,ideal=False,phase_shift=0,bcentr=1.75660107,rmaxis=1.70210874):
    """
    read perturbation bplas files produced by MARSF for individual harmonics and coil sets 
    
    args:
       filepath - path to files in input_files/
       response - toggle whether vacuum field or with plasma response i.e. bplas_vac_upper/lower or bplas_ideal/resist_resp_upper/lower
       ideal - toggle whether resistive or ideal bplasma i.e. bplas_ideal_resp_upper/lower or bplas_resist_resp_upper/lower
       phase_shift - phase shift between upper and lower rows (applied to upper coils) [degrees]
       bcentr - vacuum toroidal magnetic field at rcentr
       rmaxis - R at magnetic axis (O-point)
    notes:
       adapted from David Ryan's scripts david.ryan@ukaea.uk
       response overrides ideal toggle setting
       assumes following default filenames within filepath directory:
          rmzm_geom
          rmzm_pest
          profeq
          bplas_vac_upper/bplas_ideal_resp_upper/bplas_resist_resp_upper
          bplas_vac_lower/bplas_ideal_resp_lower/bplas_resist_resp_lower
       e.g. of file name from MARS-F for individual harmonic=bplas_resist_resp_lower
       reading this way allows one to rotate coil sets with respect to each other
    """

    print("reading MARSF_bplas perturbation")

    class rzcoords():
 
        def __init__(self, path, nchi):
            rmzm=scipy.loadtxt(path)
            Nm0=int(rmzm[0,0]) #Num. poloidal harmonics for equilibrium quantities (not necessarily same as for perturbation quantities, but should be).
            Ns_plas=int(rmzm[0,1]) #Num. radial points in plasma
            Ns_vac=int(rmzm[0,2]) #Num. radial points in vacuum
            Ns=Ns_plas+Ns_vac
            R0EXP=rmzm[0,3]
            B0EXP=rmzm[1,3]
            s=rmzm[1:Ns+1, 0]
            RM=rmzm[Ns+1:,0]+1j*rmzm[Ns+1:,1]
            ZM=rmzm[Ns+1:,2]+1j*rmzm[Ns+1:,3]
            RM=RM.reshape((Nm0, Ns))
            RM=scipy.transpose(RM)
            ZM=ZM.reshape((Nm0, Ns))
            ZM=scipy.transpose(ZM)
            RM[:,1:]=2*RM[:,1:]
            ZM[:,1:]=2*ZM[:,1:]
            
            m=scipy.arange(0,Nm0,1)
            chi=scipy.linspace(-scipy.pi, scipy.pi,nchi)
            expmchi=scipy.exp(scipy.tensordot(m,chi,0)*1j)
            R=scipy.dot(RM[:,:Nm0],expmchi)
            Z=scipy.dot(ZM[:,:Nm0],expmchi)
            
            self.R=scipy.array(R.real) #R coordinates
            self.Z=scipy.array(Z.real) #Z coordinates
            self.Nchi=nchi
            self.Nm0=Nm0
            self.Ns_plas=Ns_plas       #number is s points in plasma
            self.Ns_vac=Ns_vac         #number of s points in vacuum
            self.Ns=Ns                 #total number of s points
            self.R0EXP=R0EXP           #normalisation length
            self.B0EXP=B0EXP           #normalisation magnetic field
            self.m=m                   #equilibrium poloidal harmonics
            self.chi=chi               #poloidal angle coordinate
            self.s=s                   #radial coordinate=sqrt(psi_pol)
 
    class jacobian():
 
        #decide what stuff is needed later, and add a self. in front of it.
        def __init__(self, rz):
            if not isinstance(rz, rzcoords):
                print("read_perturbation_MARSF_bplas.jacobian - must pass in coordinate system of type plotting_base.rzcoords")
                return

            self.Ns=rz.Ns #Used in jacobian.plot(), so pass in from rzcoords
            
            self.dRds=scipy.copy(rz.R) 
            self.dZds=scipy.copy(rz.R)
            self.dRdchi=scipy.copy(rz.R)
            self.dZdchi=scipy.copy(rz.R)
            self.jacobian=scipy.copy(rz.R)
    
            #this is for the vacuum region. these are overwritten for the plasma region
            #just having a number to denote the boundary index might be simpler in the future.
            #Vac_start variable should be all that's needed. II is way too complicated
            II_start=int(rz.Ns_plas)-1; II_end=len(rz.R[:,0])
            II2_start=int(rz.Ns_plas); II2_end=len(rz.R[:,0])
           
            s0=scipy.copy(rz.s[II_start:II_end]); R0=scipy.copy(rz.R[II_start:II_end, :])
            chi0=scipy.squeeze(scipy.copy(scipy.array(rz.chi))); Z0=scipy.copy(rz.Z[II_start:II_end, :])
           
            hs=0.5*(s0[1:]-s0[:-1]).min(); hs=min(hs,  2e-5)
            hchi=0.5*(chi0[1:]-chi0[:-1]).min(); hchi=min(hchi,  1e-4)
            s1=s0-hs; s2=s0+hs
            chi1=chi0-hchi;  chi2=chi0+hchi
           
            #compute dR/ds using R(s,chi)
            R1=scipy.zeros(scipy.shape(R0))
            R2=scipy.zeros(scipy.shape(R0))
            for i in range(rz.Nchi):
               R1[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,R0[:,i], bbox=[s1[0], s0[-1]])(s1)
               R2[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,R0[:,i], bbox=[s0[0], s2[-1]])(s2)
            self.dRds[II_start:II_end,:]=(R2-R1)/(2*hs)
    
            #compute dZ/ds using Z(s,chi) 
            Z1=scipy.zeros(scipy.shape(Z0))
            Z2=scipy.zeros(scipy.shape(Z0))
            for i in range(rz.Nchi):
               Z1[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,Z0[:,i], bbox=[s1[0], s0[-1]])(s1)
               Z2[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,Z0[:,i], bbox=[s0[0], s2[-1]])(s2)
            self.dZds[II_start:II_end,:]=(Z2-Z1)/(2*hs)
    
            # compute dR/dchi using R(s,chi) 
            R1=scipy.zeros(scipy.shape(R0))
            R2=scipy.zeros(scipy.shape(R0))
            for i in range(int(rz.Ns_vac)+1):
               R1[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,R0[i,:], bbox=[chi1[0], chi0[-1]])(chi1)
               R2[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,R0[i,:], bbox=[chi0[0], chi2[-1]])(chi2) 
               self.dRdchi[i+II_start,:]=(R2[i,:]-R1[i,:])/(2*hchi) 
       
            #compute dZ/dchi using Z(s,chi) 
            Z1=scipy.zeros(scipy.shape(Z0))
            Z2=scipy.zeros(scipy.shape(Z0))
            for i in range(int(rz.Ns_vac)+1):
               Z1[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,Z0[i,:], bbox=[chi1[0], chi0[-1]])(chi1)
               Z2[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,Z0[i,:], bbox=[chi0[0], chi2[-1]])(chi2)
            self.dZdchi[II_start:II_end,:]=(Z2-Z1)/(2*hchi)
       
            #Now do same calculations for plasma region
            II_start=0; II_end=rz.Ns_plas;
       
            s0=scipy.copy(rz.s[II_start:II_end]); R0=scipy.copy(rz.R[II_start:II_end, :])
            chi0=scipy.squeeze(scipy.copy(scipy.array(rz.chi))); Z0=scipy.copy(rz.Z[II_start:II_end, :])
       
            hs=0.5*(s0[1:]-s0[:-1]).min(); hs=min(hs,  2e-5)
            hchi=0.5*(chi0[1:]-chi0[:-1]).min(); hchi=min(hchi,  1e-4)
            s1=s0-hs; s2=s0+hs
            chi1=chi0-hchi;  chi2=chi0+hchi
       
            #compute dR/ds using R(s,chi) 
            R1=scipy.zeros(scipy.shape(R0))
            R2=scipy.zeros(scipy.shape(R0))
            for i in range(rz.Nchi):
                R1[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,R0[:,i], bbox=[s1[0], s0[-1]])(s1)
                R2[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,R0[:,i], bbox=[s0[0], s2[-1]])(s2)
            self.dRds[II_start:II_end,:]=(R2-R1)/(2*hs)
    
            #compute dZ/ds using Z(s,chi) 
            Z1=scipy.zeros(scipy.shape(Z0))
            Z2=scipy.zeros(scipy.shape(Z0))
            for i in range(rz.Nchi):
                Z1[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,Z0[:,i], bbox=[s1[0], s0[-1]])(s1)
                Z2[:,i]=scipy.interpolate.InterpolatedUnivariateSpline(s0,Z0[:,i], bbox=[s0[0], s2[-1]])(s2)
                self.dZds[:II_end,i]=(Z2[:,i]-Z1[:,i])/(2*hs)
    
            # compute dR/dchi using R(s,chi)
            R1=scipy.zeros(scipy.shape(R0))
            R2=scipy.zeros(scipy.shape(R0))
            for i in range(int(rz.Ns_plas)):
               R1[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,R0[i,:], bbox=[chi1[0], chi0[-1]])(chi1)
               R2[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,R0[i,:], bbox=[chi0[0], chi2[-1]])(chi2)
            self.dRdchi[II_start:II_end,:]=(R2-R1)/(2*hchi)
    
            #compute dZ/dchi using Z(s,chi) 
            Z1=scipy.zeros(scipy.shape(Z0))
            Z2=scipy.zeros(scipy.shape(Z0))
            for i in range(int(rz.Ns_plas)):
               Z1[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,Z0[i,:], bbox=[chi1[0], chi0[-1]])(chi1)
               Z2[i,:]=scipy.interpolate.InterpolatedUnivariateSpline(chi0,Z0[i,:], bbox=[chi0[0], chi2[-1]])(chi2)
            self.dZdchi[II_start:II_end,:]=(Z2-Z1)/(2*hchi)
    
            G11=scipy.square(self.dRds)+scipy.square(self.dZds)
            G12=scipy.multiply(self.dRds, self.dRdchi)+scipy.multiply(self.dZds, self.dZdchi)
            G22=scipy.square(self.dRdchi)+scipy.square(self.dZdchi)
            G22[0,:]=G22[1,:]
            G33=scipy.square(rz.R)
    
            #Metrics elements
            self.G11=G11
            self.G12=G12
            self.G22=G22
            self.G33=G33
    
            self.jacobian=(-self.dRdchi*self.dZds+self.dRds*self.dZdchi)*rz.R
            self.jacobian[0,:]=self.jacobian[1,:]
    
    class bplasma():
 
        def __init__(self, path, rz, jc):
        
            self.path=path
            bplasma=scipy.loadtxt(self.path)
            Nm1=int(bplasma[0,0]) #Number of perturbation poloidal harmonics (should be same as equilibrium harmonics)
            self.bm1=bplasma[Nm1+1:, 0]+1j*bplasma[Nm1+1:, 1]
            self.bm2=bplasma[Nm1+1:, 2]+1j*bplasma[Nm1+1:, 3]
            self.bm3=bplasma[Nm1+1:, 4]+1j*bplasma[Nm1+1:, 5]
        
            self.bm1=self.bm1.reshape((Nm1, rz.Ns))
            self.bm2=self.bm2.reshape((Nm1, rz.Ns))
            self.bm3=self.bm3.reshape((Nm1, rz.Ns))
        
            #bm2 and bm3 are defined at half int points. 
            #3 ways to recompute at int points, see MacReadBPLASMA.m, lines 109-124
            #For now, simplest implemented. Assume spline_B23==2.
            for i in range(len(self.bm2[:,1])):
                self.bm2[i, 1:]=self.bm2[i, :-1]
                self.bm3[i, 1:]=self.bm3[i, :-1]
        
            m=scipy.array(bplasma[1:Nm1+1,0])
        
            expmchi=scipy.exp(scipy.tensordot(m,rz.chi,0)*1j)
        
            self.b1=scipy.dot(self.bm1.T,expmchi)
            self.b2=scipy.dot(self.bm2.T,expmchi)
            self.b3=scipy.dot(self.bm3.T,expmchi)
        
            self.bn=self.b1/scipy.sqrt(jc.G22*jc.G33)
        
            self.m=m 
        
            self.Br=scipy.divide(scipy.multiply(self.b1, jc.dRds)+scipy.multiply(self.b2, jc.dRdchi), jc.jacobian)
            self.Bz=scipy.divide(scipy.multiply(self.b1, jc.dZds)+scipy.multiply(self.b2,jc.dZdchi), jc.jacobian)
            self.Bphi=scipy.divide(scipy.multiply(self.b3, rz.R), jc.jacobian)
        
            self.Br[0,:]=self.Br[1,:]
            self.Bz[0,:]=self.Bz[1,:]
            self.Bphi[0:2,:]=self.Bphi[3,:]
        
            self.AbsB=scipy.sqrt(scipy.square(scipy.absolute(self.Br))+scipy.square(scipy.absolute(self.Bz))+scipy.square(scipy.absolute(self.Bphi)))
        
            self.Nm1=Nm1
        
            self.rz=rz
            self.jc=jc
       
    #start of function
 
    import scipy
    import scipy.interpolate

    rmzm_geom_path=filepath / 'rmzm_geom'
    rmzm_pest_path=filepath / 'rmzm_pest'
    profeq_path=filepath / 'profeq'

    if response:
        if ideal: #ideal plasma response
          bplas_u_path=filepath / 'bplas_ideal_resp_upper'
          bplas_l_path=filepath / 'bplas_ideal_resp_lower'
        else: #resistive plasma response
            bplas_u_path=filepath / 'bplas_resist_resp_upper'
            bplas_l_path=filepath / 'bplas_resist_resp_lower'
    else:
        bplas_u_path=filepath / 'bplas_vac_upper'
        bplas_l_path=filepath / 'bplas_vac_lower'
 
    #make ascot input from B field
    nchi=2400
  
    R_min=0.5
    R_max=2.5
  
    Z_min=-1.5
    Z_max=1.5
  
    numR=400
    numZ=600
    
    phase_shift_rad=phase_shift*(scipy.pi/180.0)
  
    rz_geom=rzcoords(rmzm_geom_path, nchi)
    jc_geom=jacobian(rz_geom)
    bplas_u_geom=bplasma(bplas_u_path, rz_geom,jc_geom)
    bplas_l_geom=bplasma(bplas_l_path, rz_geom,jc_geom)
  
    BN=(bplas_u_geom.bn*scipy.exp(1j*phase_shift_rad)+bplas_l_geom.bn)*bcentr
    BR=(bplas_u_geom.Br*scipy.exp(1j*phase_shift_rad)+bplas_l_geom.Br)*bcentr
    BZ=(bplas_u_geom.Bz*scipy.exp(1j*phase_shift_rad)+bplas_l_geom.Bz)*bcentr
    BP=(bplas_u_geom.Bphi*scipy.exp(1j*phase_shift_rad)+bplas_l_geom.Bphi)*bcentr
  
    B=scipy.sqrt(scipy.square(scipy.absolute(BR))+scipy.square(scipy.absolute(BZ))+scipy.square(scipy.absolute(BP)))
  
    R1=rz_geom.R*rmaxis
    Z1=rz_geom.Z*rmaxis
  
    B1=B
    BR1=BR
    BZ1=BZ
    BP1=BP
  
    R_rect=scipy.linspace(R_min, R_max, numR)
    Z_rect=scipy.linspace(Z_min, Z_max, numZ)
  
    R_grid, Z_grid=scipy.meshgrid(R_rect,Z_rect)
  
    BR_rect=scipy.interpolate.griddata((R1.ravel(), Z1.ravel()), BR1.ravel(), (R_grid, Z_grid), method='linear')
    BR_rect=BR_rect.reshape((numZ,numR))
  
    BZ_rect=scipy.interpolate.griddata((R1.ravel(), Z1.ravel()), BZ1.ravel(), (R_grid, Z_grid), method='linear')
    BZ_rect=BZ_rect.reshape((numZ,numR))
  
    BP_rect=scipy.interpolate.griddata((R1.ravel(), Z1.ravel()), BP1.ravel(), (R_grid, Z_grid), method='linear')
    BP_rect=BP_rect.reshape((numZ,numR))
  
    B_rect=scipy.sqrt(scipy.absolute(BR_rect)**2+scipy.absolute(BZ_rect)**2+scipy.absolute(BP_rect)**2)
 
    input_data={}
    input_data['R_2D']=np.array(R_grid,ndmin=2).swapaxes(0,1)
    input_data['Z_2D']=np.array(Z_grid,ndmin=2).swapaxes(0,1)
    input_data['R_1D']=np.array(input_data['R_2D'][:,0],ndmin=2)
    input_data['Z_1D']=np.array(input_data['Z_2D'][0,:],ndmin=2)
    input_data['B_field_R_real']=np.array(BR_rect.real,ndmin=2).swapaxes(0,1)
    input_data['B_field_R_imag']=np.array(BR_rect.imag,ndmin=2).swapaxes(0,1)
    input_data['B_field_Z_real']=np.array(BZ_rect.real,ndmin=2).swapaxes(0,1)
    input_data['B_field_Z_imag']=np.array(BZ_rect.imag,ndmin=2).swapaxes(0,1)
    input_data['B_field_tor_real']=np.array(BP_rect.real,ndmin=2).swapaxes(0,1)
    input_data['B_field_tor_imag']=np.array(BP_rect.imag,ndmin=2).swapaxes(0,1)
    input_data['B_field_R']=np.sqrt(input_data['B_field_R_real']**2+input_data['B_field_R_imag']**2)
    input_data['B_field_Z']=np.sqrt(input_data['B_field_Z_real']**2+input_data['B_field_Z_imag']**2)
    input_data['B_field_tor']=np.sqrt(input_data['B_field_tor_real']**2+input_data['B_field_tor_imag']**2)
    input_data['B_field_mag']=np.sqrt(input_data['B_field_tor']**2+input_data['B_field_R']**2+input_data['B_field_Z']**2)

    print("finished reading MARSF_bplas perturbation")

    return input_data
    
################################################################## Perturbation write functions
 
def dump_perturbation_LOCUST(output_data,filepath,**properties):
    """
    writes perturbation to LOCUST format

    notes:
        dumps data with quickly-varying Z like usual LOCUST input
    """
 
    print("writing LOCUST perturbation")

    with open(filepath,'w') as file: #open file
        
        quantities=['R_2D','Z_2D','B_field_R_real','B_field_R_imag','B_field_Z_real','B_field_Z_imag','B_field_tor_real','B_field_tor_imag']

        for row in np.array([output_data[quantity].flatten() for quantity in quantities]).T:
            line=''
            for number in row:
                line+=processing.utils.fortran_string(number_out=number,length=18,decimals=10,exponential=True)
            line+=' \n' 
            file.write(line)

    print("finished writing LOCUST perturbation")

def dump_perturbation_point_data_LOCUST(output_data,filepath='point_data.inp',BCHECK=1,**properties):
    """
    generates the point_data.inp file for checking magnetic perturbations using LOCUST -DBCHECK

    args:
        BCHECK - coordinate format setting for LOCUST field checking (1=RPhiZ,2=XYZ)  
    notes:
        uses R_point_data, phi_point_data, Z_point_data and time_point_data arrays stored in perturbation class 
    """

    print("writing point_inp.dat test points")

    with open(filepath,'w') as file: #open file

        if BCHECK==1:
            for R,Phi,Z,time in zip(output_data['R_point_data'],output_data['phi_point_data'],output_data['Z_point_data'],output_data['time_point_data']):
                line=' '
                line+=processing.utils.fortran_string(R,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(Phi,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(Z,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(time,11,6,exponential=False)
                line+='  '
                file.write('{}\n'.format(line))

        elif BCHECK==2:
            for X,Y,Z,time in zip(output_data['X_point_data'],output_data['Y_point_data'],output_data['Z_point_data'],output_data['time_point_data']):
                line=' '
                line+=processing.utils.fortran_string(X,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(Y,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(Z,11,6,exponential=False)
                line+=' '
                line+=processing.utils.fortran_string(time,11,6,exponential=False)
                line+='  '
                file.write('{}\n'.format(line))

    print("finished writing point_inp.dat test points")

################################################################## perturbation class
 
class Perturbation(classes.base_input.LOCUST_input):
    """
    class describing magnetic field perturbation for LOCUST
 
    inherited from LOCUST_input:
        self.ID                     unique object identifier, good convention to fill these for error handling etc
        self.data                   holds all input data in dictionary object
        self.LOCUST_input_type      string which holds this class' input type, this case = 'perturbation'
    class data
        self.data_format            data format of original data e.g. LOCUST
        self.filename               name of file in input_files folder
        self.filepath               full path of file in input_files folder  
        self.shot                   shot number
        self.run                    run number
        self.properties             data to hold additional class-specific information e.g. ion species
        key, value                  key for data dictionary to specify data entry holding value
        target                      external object to copy from
        filename                    name of file to write to
        filepath                    full path to output file in input_files folder
 
    notes:
    """
 
    LOCUST_input_type='perturbation'
 
    def read_data(self,data_format=None,filename=None,shot=None,run=None,**properties):
        """
        read perturbation from file 
 
        notes:
        """
 
        if processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() - data_format required\n".format(self.ID),data_format): #must always have data_format if reading in data
            pass
 
        elif data_format=='LOCUST': #here are the blocks for various file types, they all follow the same pattern
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from LOCUST - filename required\n".format(self.ID),filename): #must check we have all info required for reading
 
                self.data_format=data_format #add to the member data
                self.filename=filename
                self.filepath=support.dir_input_files / filename
                self.properties={**properties}
                self.data=read_perturbation_LOCUST(self.filepath,**properties)

        elif data_format=='LOCUST_field_data': #here are the blocks for various file types, they all follow the same pattern
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from LOCUST_field_data - filename required\n".format(self.ID),filename): #must check we have all info required for reading
 
                self.data_format=data_format #add to the member data
                self.filename=filename
                self.filepath=support.dir_output_files / filename
                self.properties={**properties}
                self.data=read_perturbation_LOCUST_field_data(self.filepath,**properties)

        elif data_format=='ASCOT_field_data': #here are the blocks for various file types, they all follow the same pattern
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from ASCOT_field_data - filename required\n".format(self.ID),filename): #must check we have all info required for reading
 
                self.data_format=data_format #add to the member data
                self.filename=filename
                self.filepath=support.dir_output_files / filename
                self.properties={**properties}
                self.data=read_perturbation_ASCOT_field_data(self.filepath,**properties)

        elif data_format=='IDS':
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from magnetics IDS - shot and run required\n".format(self.ID),shot,run):
 
                self.data_format=data_format
                self.shot=shot
                self.run=run
                self.properties={**properties}
                self.data=read_perturbation_IDS(self.shot,self.run,**properties)

        elif data_format=='MARSF': #here are the blocks for various file types, they all follow the same pattern
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from MARSF - filename required\n".format(self.ID),filename): #must check we have all info required for reading
 
                self.data_format=data_format #add to the member data
                self.filename=filename
                self.filepath=support.dir_input_files / filename
                self.properties={**properties}
                self.data=read_perturbation_MARSF(self.filepath,**properties)

        elif data_format=='MARSF_bplas': #here are the blocks for various file types, they all follow the same pattern
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot read_data() from MARSF_bplas - filename required\n".format(self.ID),filename): #must check we have all info required for reading
 
                self.data_format=data_format #add to the member data
                self.filename=filename
                self.filepath=support.dir_input_files / filename
                self.properties={**properties}
                self.data=read_perturbation_MARSF_bplas(self.filepath,**properties)

        else:
            print("ERROR: {} cannot read_data() - please specify a compatible data_format (LOCUST/LOCUST_field_data/ASCOT_field_data/IDS/MARSF/MARSF_bplas)\n".format(self.ID))            
 
    def dump_data(self,data_format=None,filename=None,shot=None,run=None,BCHECK=1,**properties):
        """
        write perturbation to file
 
        notes: 
        """

        if not self.run_check():
            print("WARNING: run_check() returned false - insufficient data for LOCUST run (ID={})".format(self.ID))
        if processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot dump_data() - self.data and compatible data_format required\n".format(self.ID),self.data,data_format):
            pass
         
        elif data_format=='LOCUST':
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot dump_data() to LOCUST - filename required\n".format(self.ID),filename):
                filepath=support.dir_input_files / filename
                dump_perturbation_LOCUST(self.data,filepath,**properties)

        elif data_format=='point_data':
            if not processing.utils.none_check(self.ID,self.LOCUST_input_type,"ERROR: {} cannot dump_data() to point_data.inp - filename required\n".format(self.ID),filename):
                filepath=support.dir_input_files / filename
                dump_perturbation_point_data_LOCUST(self.data,filepath,BCHECK,**properties)

        else:
            print("ERROR: {} cannot dump_data() - please specify a compatible data_format (LOCUST/point_data)\n".format(self.ID))

    def plot(self,key='B_field_R_real',LCFS=False,limiters=False,number_bins=20,fill=True,vminmax=None,colmap=cmap_default,ax=False,fig=False):
        """
        plots a perturbation
        
        notes:
            
        args:
            key - selects which data in perturbation to plot
            LCFS - toggles plasma boundary on/off in 2D plots (requires equilibrium arguement)
            limiters - object which contains limiter data rlim and zlim
            number_bins - set number of bins or levels
            fill - toggle contour fill on 2D plots
            vminmax - set mesh Vmin/Vmax values
            colmap - set the colour map (use get_cmap names)
            ax - take input axes (can be used to stack plots)
            fig - take input fig (can be used to add colourbars etc)
        """

        import scipy
        import matplotlib
        from matplotlib import cm
        import matplotlib.pyplot as plt
        from mpl_toolkits import mplot3d #import 3D plotting axes
        from mpl_toolkits.mplot3d import Axes3D

        if ax is False:
            ax_flag=False #need to make extra ax_flag since ax state is overwritten before checking later
        else:
            ax_flag=True

        if fig is False:
            fig_flag=False
        else:
            fig_flag=True

        #0D data
        if self[key].ndim==0:
            print([key])
            return
        
        #>0D data is plottable
        if fig_flag is False:
            fig = plt.figure() #if user has not externally supplied figure, generate
        
        if ax_flag is False: #if user has not externally supplied axes, generate them
            ax = fig.add_subplot(111)
        ax.set_title(self.ID)

        #1D data
        if self[key].ndim==1:
            ax.plot(self[key],color=colmap(np.random.uniform()))
            ax.set_ylabel(key)

        #2D data
        elif self[key].ndim==2:

            X=self['R_1D'] #make a mesh
            Y=self['Z_1D'] 
            Y,X=np.meshgrid(Y,X) #swap since things are defined r,z 
            Z=self[key] #2D array (nR_1D,nZ_1D) of poloidal flux
 
            if vminmax:
                vmin=vminmax[0]
                vmax=vminmax[1]
            else:
                vmin=np.amin(Z)
                vmax=np.amax(Z)

            #2D plot
            if fill is True:
                mesh=ax.contourf(X,Y,Z,levels=np.linspace(vmin,vmax,num=number_bins),colors=colmap(np.linspace(0.,1.,num=number_bins)),edgecolor='none',linewidth=0,antialiased=True,vmin=vmin,vmax=vmax)
                for c in mesh.collections: #for use in contourf
                    c.set_edgecolor("face")
            else:
                mesh=ax.contour(X,Y,Z,levels=np.linspace(vmin,vmax,num=number_bins),colors=colmap(np.linspace(0.,1.,num=number_bins)),edgecolor='none',linewidth=0,antialiased=True,vmin=vmin,vmax=vmax)
                if plot_contour_labels:
                    ax.clabel(mesh,inline=1,fontsize=10)
                
            #mesh=ax.pcolormesh(X,Y,Z,colors=colmap(np.linspace(0.,1.,num=number_bins)),edgecolor='none',linewidth=0,antialiased=True,vmin=np.amin(Z),vmax=np.amax(Z))

            #3D plot
            #ax=ax.axes(projection='3d')
            #ax.view_init(elev=90, azim=None) #rotate the camera
            #ax.plot_surface(X,Y,Z,rstride=1,cstride=1,colors=colmap(np.linspace(0.,1.,num=number_bins)),edgecolor='none',linewidth=0,antialiased=True,vmin=np.amin(Z),vmax=np.amax(Z))
            
            if fig_flag is False:    
                fig.colorbar(mesh,ax=ax,orientation='horizontal')
            ax.set_aspect('equal')
            ax.set_xlim(np.min(self['R_1D']),np.max(self['R_1D']))
            ax.set_ylim(np.min(self['Z_1D']),np.max(self['Z_1D']))
            ax.set_xlabel('R [m]')
            ax.set_ylabel('Z [m]')

            if LCFS:
                ax.plot(LCFS['lcfs_r'],LCFS['lcfs_z'],plot_style_LCFS) 
            if limiters: #add boundaries if desired
                ax.plot(limiters['rlim'],limiters['zlim'],plot_style_limiters) 

            if ax_flag is True or fig_flag is True: #return the plot object
                return mesh

        if ax_flag is False and fig_flag is False:
            plt.show()


    def plot_field_stream(self,LCFS=False,limiters=False,colmap=cmap_default,ax=False,fig=False):
        """
        stream plot of magnetic field in R,Z plane

        args:
            LCFS - toggles plasma boundary on/off in 2D plots
            limiters - toggles limiters on/off in 2D plots
            colmap - set the colour map (use get_cmap names)
            ax - take input axes (can be used to stack plots)
            fig - take input fig (can be used to add colourbars etc)
        notes:
            take transpose due to streamplot index convention
        """

        import scipy
        import matplotlib
        from matplotlib import cm
        import matplotlib.pyplot as plt
        from mpl_toolkits import mplot3d #import 3D plotting axes
        from mpl_toolkits.mplot3d import Axes3D

        if ax is False:
            ax_flag=False #need to make extra ax_flag since ax state is overwritten before checking later
        else:
            ax_flag=True

        if fig is False:
            fig_flag=False
        else:
            fig_flag=True

        if fig_flag is False:
            fig = plt.figure() #if user has not externally supplied figure, generate
        
        if ax_flag is False: #if user has not externally supplied axes, generate them
            ax = fig.add_subplot(111)
            ax.set_title(self.ID)
        ax.set_aspect('equal')

        if not np.all([component in self.data.keys() for component in ['B_field_R','B_field_tor','B_field_Z']]): #calculate B field if missing
            print("plot_field_stream - found no B_field in equilibrium - calculating!")
            self.B_calc()

        B_mag=np.sqrt(self['B_field_R']**2+self['B_field_Z']**2) #calculate poloidal field magnitude
        strm = ax.streamplot(self['R_1D'],self['Z_1D'],self['B_field_R'].T,self['B_field_Z'].T, color=B_mag.T, linewidth=1, cmap=colmap)

        if LCFS:
            ax.plot(LCFS['lcfs_r'],LCFS['lcfs_z'],plot_style_LCFS) 
        if limiters: #add boundaries if desired
            ax.plot(limiters['rlim'],limiters['zlim'],plot_style_limiters) 

        if fig_flag is False:    
            fig.colorbar(strm.lines,ax=ax,orientation='horizontal')
        ax.set_xlim(np.min(self['R_1D']),np.max(self['R_1D']))
        ax.set_ylim(np.min(self['Z_1D']),np.max(self['Z_1D']))

        ax.set_xlabel('R [m]')
        ax.set_ylabel('Z [m]')

        if ax_flag is False and fig_flag is False:
            plt.show()

#################################
 
##################################################################
 
###################################################################################################