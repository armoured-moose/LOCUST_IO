#3D_beam_depo_combine.py

 
"""
Samuel Ward
16/04/2019
----
takes the 157418 3D field beam depositions which are dumped to LOCUST format and produces a combined deposition list which is in the correct energy fractions 
--- 
notes:
	assumes all given deposition files from spiral are the same length - due to the way it draws ratios of particles from these files         
---
"""


import context
from classes.input_classes.beam_deposition import Beam_Deposition as bd
import support
import glob
import pathlib
import numpy as np

files=pathlib.Path(support.dir_input_files / '157418' / 'SPIRAL').glob('*')
files=[file for file in files]

beam_depo_combined=bd(ID='fully-combined beam deposition') #make a blank beam deposition object

response=True
response_tag='wresp' if response else 'noresp'
for file in files: #ec_# refers to the energy component
	filename=file.parts[-1]
	if response_tag in filename: #check if it has plasma response included or not
		print(filename)
		if 'ec_0' in filename: #full energy fraction = 0.539352 
			fraction=0.539352*(1./0.539352) #scale up the fractions such that the largest fraction=1 (uses an entire file), and the other fractions use fractions of this fraction
											#that way we maximise file usage
		if 'ec_1' in filename: #half energy fraction = 0.276227 
			fraction=0.276227*(1./0.539352)
		if 'ec_2' in filename: #third energy fraction = 0.184421 
			fraction=0.184421*(1./0.539352)
		tmp=bd('','SPIRAL_FO',file)
		for variable in ['R','Z','phi','V_R','V_Z','V_tor','E']:
			variable_len=len(tmp[variable])
			tmp[variable]=tmp[variable][0:int(fraction*variable_len)]
		beam_depo_combined.combine(tmp)


#check we have correct fractions
full=beam_depo_combined['E'][(beam_depo_combined['E']>70000)&(beam_depo_combined['E']<100000)]
half=beam_depo_combined['E'][(beam_depo_combined['E']>35000)&(beam_depo_combined['E']<50000)]
third=beam_depo_combined['E'][(beam_depo_combined['E']>0)&(beam_depo_combined['E']<30000)]
print(len(full)/len(beam_depo_combined['E']))
print(len(half)/len(beam_depo_combined['E']))
print(len(third)/len(beam_depo_combined['E']))

print(len(full))
print(len(half))
print(len(third))

beam_depo_combined.plot(real_scale=True,weight=False,number_bins=500)
beam_depo_combined.plot(axes=['X','Y'],real_scale=True,weight=False,number_bins=500)
beam_depo_combined.plot(axes=['E'],weight=False,number_bins=300)	

#beam_depo_combined.dump_data(data_format='LOCUST_FO',filename=pathlib.Path('157418') / 'LOCUST' / ('response' if response else 'vacuum') / 'ptcles.dat_{}'.format(response_tag))
