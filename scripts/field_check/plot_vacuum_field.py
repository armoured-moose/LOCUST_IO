# produce vacuum field data for ITER w/o RW response
# for benchmarking withprobe_g
# MARS-F vacuum data are stored in: ../Data_VAC
# note that vacuum data assumes 1 kAt n=3 or n=6 coil current in each row w/o In/Ic factor
# consider one optimal coil phasing from EvansNF13 paper:
# DeltaPhiU=86, DeltaPhiM=0, DeltaPhiL=34 using Eq. (1) in the paper
# compare field along phi-angle at R=6.2273m, Z=0.0571m
# compare both the n=3 main harmonic and the n=6 sideband field

import numpy as np 
import matplotlib.pyplot as plt
import scipy.io
import copy

# convert to MARS-F definition of coil phasing:
n_ASCOT = 3
phic_ASCOT = np.array([30,26.7,30])
PHI_ASCOT=np.array([86,0,34])
PHI_SHIFT=180
k = 1
PHI_MARS = n_ASCOT*(phic_ASCOT-PHI_ASCOT)-PHI_SHIFT+360*k
PHI_MARS = PHI_MARS - PHI_MARS[1]
PHI_MARS[0] += 360
PHI_MARS[2] += 360
# ==> PHI_MARS=[111.9 0 267.9]

PHI_MARS = n_ASCOT*(PHI_ASCOT) #XXX use this transformation in mars_read and should get vacuum fields!!!

# get vacuum field from each row of coils at (R,Z)
# FIO_EVAL_FIELD_CPLX/fio_test.x ==> data0 below
# assume 1kAt currentt per row w/o RW, w/o In/Ic factor
# I have checked these and they check out
#'''
data0_n3_V = np.array([
#Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
[0.57865387E-05,  0.36730866E-16, -0.10698996E-15,  0.10890207E-04,  0.14486468E-04,  0.10227762E-15],  #U
[0.71598882E-04,  0.11469550E-15, -0.24859318E-17,  0.52280031E-04,  0.20087279E-04,  0.20979606E-15],  #M
[0.15210121E-04,  0.70365481E-16, -0.31805307E-15,  0.19037078E-04, -0.24623779E-04, -0.10433730E-16]   #L
])
data0_n6_V = np.array([
#Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
[0.37564248E-05, -0.65616162E-18,  0.11678465E-16,  0.62478631E-05,  0.63687428E-05,  0.43718308E-17],  #U
[0.49043808E-04, -0.15219669E-16, -0.27875665E-17,  0.42481952E-04,  0.10532992E-04,  0.72137744E-17],  #M
[0.11458338E-04, -0.28802074E-17, -0.14583073E-16,  0.14619530E-04, -0.13670587E-04, -0.66732591E-17]   #L
])

'''
data0_n3_V = np.array([ #XXX added - resistive wall vacuum vield
#Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
[0.12810790E-05, -0.34079052E-05,  0.46962186E-05,  0.58689276E-05,  0.10512555E-04, -0.55204622E-05],#U at phi=0
[0.48380158E-04, -0.26771538E-04,  0.20989276E-04,  0.32207506E-04,  0.17421626E-04, -0.52254748E-05],#M at phi=0
[0.76322180E-05, -0.72488468E-05,  0.75555054E-05,  0.11624651E-04, -0.20202125E-04,  0.71962314E-05] #L at phi=0
])  
data0_n6_V = np.array([ #XXX added - resistive wall vacuum vield
#Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
[0.34947201E-05, -0.40959355E-06,  0.21548156E-05,  0.55912858E-05,  0.56505042E-05, -0.25898652E-05], #U at phi=0
[0.43889773E-04, -0.13147478E-04,  0.14049653E-04,  0.36642226E-04,  0.56740161E-05, -0.12990575E-04], #M at phi=0
[0.88517553E-05, -0.71245661E-05,  0.49056987E-05,  0.12563813E-04, -0.14074332E-04,  0.96032629E-06]  #L at phi=0
])
#''
data0_n3_V = np.array([ #XXX added - resistive wall vacuum vield
[0.34079052E-05, 0.12810790E-05, -0.58689276E-05,  0.46962186E-05,  0.55204622E-05,  0.10512555E-04], #U at phi=30.
[0.34690849E-04, 0.43056938E-04, -0.28119247E-04,  0.26214139E-04,  0.81429485E-05,  0.16263795E-04], #M at phi=26.7
[0.72488468E-05, 0.76322180E-05, -0.11624651E-04,  0.75555054E-05, -0.71962314E-05, -0.20202125E-04] #L at phi=30.0
])
data0_n6_V = np.array([ #XXX added - resistive wall vacuum vield
[-0.34947201E-05, 0.40959355E-06, -0.21548156E-05, -0.55912858E-05, -0.56505042E-05,  0.25898652E-05], #U at phi=30
[-0.36841494E-04, 0.27237339E-04, -0.25631160E-04, -0.29716816E-04, -0.93817231E-06,  0.14144587E-04], #M at phi=26.7
[-0.88517553E-05, 0.71245661E-05, -0.49056987E-05, -0.12563813E-04,  0.14074332E-04, -0.96032629E-06] #L at phi=30
])
'''

# In/Ic factors for n=3 and n=6 fields
fac_InIc = np.array([
#n   fU      fM      fL
 [3,   0.6645,  0.4968,  0.6840],
 [6,   0.4772,  0.4243,  0.4773]
])

'''
fac_InIc = np.array([ #XXX added to single out a row
#n   fU      fM      fL
 [3,   0.6645,  0*0.4968,  0*0.6840],
 [6,   0.4772,  0*0.4243,  0*0.4773]
])
'''

# linear superposition of U+M+L with proper In/Ic factor and proper coil phasing
# and store results in data1 below
# n=3 main harmonic
fac = fac_InIc[0,1:]
BR  = data0_n3_V[:,0]+1j*data0_n3_V[:,1]
BP  = data0_n3_V[:,2]+1j*data0_n3_V[:,3]
BZ  = data0_n3_V[:,4]+1j*data0_n3_V[:,5]
PHI = -PHI_MARS #- for nice field        -- this is for a wave form ~cos(n[phi+dPhi]) in the MARSF system (dPhi keeps its sign due to current definition but phi_coil is opposite since in MARS system) 
BRn3 = np.sum(fac*BR*np.exp(1j*PHI/180*np.pi))
BPn3 = np.sum(fac*BP*np.exp(1j*PHI/180*np.pi))
BZn3 = np.sum(fac*BZ*np.exp(1j*PHI/180*np.pi))
res3  = [BRn3.real,BRn3.imag,BPn3.real,BPn3.imag,BZn3.real,BZn3.imag]

# n=6 main harmonic
fac = fac_InIc[1,1:] 
PHI = -9*phic_ASCOT + PHI_MARS #-+ for nice field
BR  = data0_n6_V[:,0]+1j*data0_n6_V[:,1]
BP  = data0_n6_V[:,2]+1j*data0_n6_V[:,3]
BZ  = data0_n6_V[:,4]+1j*data0_n6_V[:,5]

BRn6 = np.sum(fac*BR*np.exp(1j*PHI/180*np.pi))
BPn6 = np.sum(fac*BP*np.exp(1j*PHI/180*np.pi))
BZn6 = np.sum(fac*BZ*np.exp(1j*PHI/180*np.pi))
res6  = [BRn6.real,BRn6.imag,BPn6.real,BPn6.imag,BZn6.real,BZn6.imag]

#combined U+M+L vacuum field
data1 = [
#n  Re(dBR)      Im(dBR)      Re(dBphi)    Im(dBphi)    Re(dBZ)      Im(dBZ)
 [3,  3.3755e-05,  -6.8291e-06,   6.2983e-06,   2.2796e-05,   7.0061e-06,   2.5763e-05],
 [6, -1.4112e-05,   1.7207e-05,  -1.4289e-05,  -1.3138e-05,   7.1262e-06,   2.9876e-06]
]

data1 = [ #XXX added
#n    Re(dBR)      Im(dBR)      Re(dBphi)    Im(dBphi)    Re(dBZ)      Im(dBZ)
 [3]+res3,
 [6]+res6
]

# get B-field along phi
# assuming 90 kAt coil current
# note that the phi-angle below should correspond to the absolute phi-angle as defined in ITER
phi  = np.linspace(0,360,361) 
phi0 = 0. 
Cphi = np.exp((phi+phi0)*n_ASCOT*1j*np.pi/180)*1e+4*90 
rBRn3  = (BRn3*Cphi).real
rBPn3  = (BPn3*Cphi).real
rBZn3  = (BZn3*Cphi).real

Cphi = np.exp((phi+phi0)*6*1j*np.pi/180)*1e+4*90 
rBRn6  = (BRn6*Cphi).real
rBPn6  = (BPn6*Cphi).real
rBZn6  = (BZn6*Cphi).real

#plot vacuum field from MARS-F
SS   = 'r-'

fig,axes=plt.subplots(8)
axes[0].plot(phi,rBRn3,SS)
axes[0].set_xlabel('$\phi$ [degrees]')
axes[0].set_ylabel('$n=3 {\delta}B_R$ [Gauss]')

axes[1].plot(phi,rBPn3,SS)
axes[1].set_xlabel('$\phi$ [degrees]')
axes[1].set_ylabel('$n=3 {\delta}B_{\phi}$ [Gauss]')

axes[2].plot(phi,rBZn3,SS)
axes[2].set_xlabel('\phi [degrees]')
axes[2].set_ylabel('$n=3 {\delta}B_Z$ [Gauss]')

axes[3].plot(phi,rBRn6,SS)
axes[3].set_xlabel('\phi [degrees]')
axes[3].set_ylabel('$n=6 {\delta}B_R$ [Gauss]')

axes[4].plot(phi,rBPn6,SS)
axes[4].set_xlabel('\phi [degrees]')
axes[4].set_ylabel('$n=6 {\delta}B_{\phi}$ [Gauss]')

axes[5].plot(phi,rBZn6,SS)
axes[5].set_xlabel('$\phi$ [degrees]')
axes[5].set_ylabel('$n=6 {\delta}B_Z$ [Gauss]')

dBR=rBRn3+rBRn6 #XXX added
dBphi=rBPn3+rBPn6 #XXX added
dBZ=rBZn3+rBZn6 #XXX added
axes[6].plot(phi,np.sqrt((dBR)**2+(dBphi)**2+(dBZ)**2),SS,label='MARS-F eval') #XXX added
dBR=rBRn6 #XXX added
dBphi=rBPn6 #XXX added
dBZ=rBZn6 #XXX added
#axes[6].plot(phi,np.sqrt((dBR)**2+(dBphi)**2+(dBZ)**2),SS,label='MARS-F eval') #XXX added
dBR=rBRn3 #XXX added
dBphi=rBPn3 #XXX added
dBZ=rBZn3 #XXX added
axes[6].plot(phi,np.sqrt((dBR)**2+(dBphi)**2+(dBZ)**2),SS,label='MARS-F eval') #XXX added

axes[7].plot(phi,rBRn3+rBRn6,SS) #XXX added
axes[7].set_xlabel('$\phi$ [degrees]') #XXX added
axes[7].set_ylabel('$n=3+6 {\delta}B_R$ [Gauss]') #XXX added

for ax in axes:
    ax.set_xlim([0,360])

# get vacuum field from probe_g data
# perform Fourier decomposition along phi for n=3 and n=6 components

d={}
filename='probe_gb_TMB.out'
with open(filename) as file:
    lines=file.readlines()
    while 'phi_tor(deg)' not in lines[0]:
        del(lines[0])
    for column_number,variable in enumerate(lines[0].replace('%','').replace('(deg)','').replace('(m)','').split()): 
        d[column_number]={}
        d[column_number]['variable_name']=variable
        d[column_number]['data']=[]
    del(lines[0])
    for line in lines:
        for column_number,column in enumerate(line.split()):
            d[column_number]['data'].append(float(column))

    for column_number in list(d.keys()):
        #print(type(d[column_number]))
        #print(column_number)
        variable_name=d[column_number]['variable_name']
        d[variable_name]=d.pop(column_number)
        d[variable_name]=np.array(d[variable_name]['data'])

x = d['phi_tor']*np.pi/180.#np.linspace(0,2*np.pi,361)
y = np.array([d['B_phi'],d['B_R'],d['B_Z']]).T
yn3 = np.full((y.shape[1]),1,dtype=complex)
yn6 = np.full((y.shape[1]),1,dtype=complex)

for k in range(y.shape[1]):
    yn3[k] = np.sum(y[:,k]*np.exp(-1j*3*x,dtype=complex),dtype=complex)
    yn6[k] = np.sum(y[:,k]*np.exp(-1j*6*x,dtype=complex),dtype=complex)

yn3 = yn3*(x[1]-x[0])/2/np.pi*1e+4*2 #XXX original - (x[1]-x[0]) factor needed due to transition from continuous to DFT
yn6 = yn6*(x[1]-x[0])/2/np.pi*1e+4*2 #XXX original 

phi0 = 30. #probe_g data has phi starting from phi_ITER=+30 i.e. centred on first top/bottom coil centre 
Cphi = np.exp((d['phi_tor'])*n_ASCOT*1j*np.pi/180) 
rBRn3 = (yn3[1]*Cphi).real
rBPn3 = (yn3[0]*Cphi).real
rBZn3 = (yn3[2]*Cphi).real

Cphi = np.exp((d['phi_tor'])*6*1j*np.pi/180) 
rBRn6 = (yn6[1]*Cphi).real
rBPn6 = (yn6[0]*Cphi).real
rBZn6 = (yn6[2]*Cphi).real

'''
_fig,_ax=plt.subplots(1) #XXX for dignostics plot the sum of FT'd harmonics vs original signal
fft=np.fft.rfft(d['B_phi']) #perform numpy fourier transform...
fudge=55
#_ax.plot((fft[6]*np.exp(1j*6*x,dtype=complex)).real*fudge,'k-') #fundamental 
#_ax.plot(phi,rBPn3,'b-') #yueqiang's fundamental
#_ax.plot((fft[3]*np.exp(1j*3*x,dtype=complex)).real*fudge,'k-') #1st harmonic 
#_ax.plot(phi,rBPn6,'b-') #yueqiang's 1st harmonic
_ax.plot((fft[3]*np.exp(1j*3*x,dtype=complex)+fft[6]*np.exp(1j*6*x,dtype=complex)).real*fudge,'k-') #full
_ax.plot(x*180/np.pi,d['B_phi']*1e+4,'g-') #full
_ax.plot(phi,rBPn3+rBPn6,'b-') #yueqiang's full
'''

#plot vacuum field from probe_g
SS   = 'b-' #XXX added
for ax,quantity in zip(axes,[rBRn3,rBPn3,rBZn3,rBRn6,rBPn6,rBZn6]): #XXX added
    ax.plot(d['phi_tor']+phi0,quantity,SS) #XXX added
dBR=rBRn3+rBRn6 #XXX added
dBphi=rBPn3+rBPn6 #XXX added
dBZ=rBZn3+rBZn6 #XXX added
axes[6].plot(d['phi_tor']+phi0,np.sqrt((dBR)**2+(dBphi)**2+(dBZ)**2),SS,label='FFT probe_g') #XXX added
axes[6].plot(d['phi_tor']+phi0,np.sqrt((d['B_R']*1e4)**2+(d['B_phi']*1e4)**2+(d['B_Z']*1e4)**2),'k-',label='probe_g') #XXX added
axes[6].set_xlabel('$\phi$ [degrees]') #XXX added
axes[6].set_ylabel('mag [Gauss]') #XXX added

axes[7].plot(d['phi_tor']+phi0,rBRn3+rBRn6,SS) #XXX added
axes[7].set_xlabel('$\phi$ [degrees]') #XXX added
axes[7].set_ylabel('$n=3+6 {\delta}B_R$ [Gauss]') #XXX added

for coil_centre in phic_ASCOT: axes[6].axvline(np.abs(coil_centre)) #XXX added
for peak_centre in PHI_MARS: axes[0].axvline(np.abs(peak_centre)) #XXX added


#XXX I have checked and without any phi0 shifts the following code agrees EXACTLY with Yueqiang's EVAL code combined with the plotting method above
#XXX hence LOCUST sees exactly the field in data0_n3_V and data0_n6_V given by my EVAL call above 
#XXX so now can concentrating on just matching my data0_n3_V and data0_n6_V with the vacuum field

#open LOCUST BPLAS file for comparison
'''
import context
import settings
from classes.input_classes.perturbation import Perturbation
filename='BPLASMA_n3'
perturbation_n3=Perturbation(filename,data_format='LOCUST',filename=filename,mode_number=-3)
filename='BPLASMA_n6'
perturbation_n6=Perturbation(filename,data_format='LOCUST',filename=filename,mode_number=-6)
number_points_toroidal=1000
phi_toroidal=np.linspace(0.,2.*np.pi,number_points_toroidal)
R_toroidal=np.full(number_points_toroidal,6.2273)
Z_toroidal=np.full(number_points_toroidal,0.0571)

dB_R3,dB_tor3,dB_Z3=perturbation_n3.evaluate(R=R_toroidal,phi=phi_toroidal,Z=Z_toroidal,phase=0.,i3dr=-1) #evaluate toroidally
axes[0].plot(phi_toroidal*180/np.pi,dB_R3*1e4,'g-',label='LOCUST_IO eval')
axes[1].plot(phi_toroidal*180/np.pi,dB_tor3*1e4,'g-',label='LOCUST_IO eval')
axes[2].plot(phi_toroidal*180/np.pi,dB_Z3*1e4,'g-',label='LOCUST_IO eval')

dB_R6,dB_tor6,dB_Z6=perturbation_n6.evaluate(R=R_toroidal,phi=phi_toroidal,Z=Z_toroidal,phase=0.,i3dr=-1) #evaluate toroidally
axes[3].plot(phi_toroidal*180/np.pi,dB_R6*1e4,'g-',label='LOCUST_IO eval')
axes[4].plot(phi_toroidal*180/np.pi,dB_tor6*1e4,'g-',label='LOCUST_IO eval')
axes[5].plot(phi_toroidal*180/np.pi,dB_Z6*1e4,'g-',label='LOCUST_IO eval')

dB_mag=np.sqrt((dB_R3+dB_R6)**2+(dB_tor3+dB_tor6)**2+(dB_Z3+dB_Z6)**2)
axes[6].plot(phi_toroidal*180/np.pi,dB_mag*1e4,'g-',label='LOCUST_IO eval')
'''

axes[6].legend() #XXX added

plt.show() #XXX added
