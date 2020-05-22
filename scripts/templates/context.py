#context.py

'''
Samuel Ward
13/12/2017
----
Add this file to any LOCUST_IO projects so visibility is automatically handled
---
notes:
    when using a project interactively, just import this file first
---
'''



##################################################################
#Preamble

import sys
import os
import pathlib

##################################################################
#Main

thisdirectory=pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
parts=list(thisdirectory.parts)
parts.reverse()
for counter,level in enumerate(parts): #find LOCUST_IO directory by looking for licence, then if user deletes licence code will not work
    if 'LOCUST_IO_LICENCE.md' in [str(list(path.parts)[-1]) for path in thisdirectory.parents[counter].glob('*')]:
        dir_locust_io=thisdirectory.parents[counter]
        dir_locust_io_src=dir_locust_io / 'src'
        sys.path.insert(1,str(dir_locust_io_src)) #append Python sys path
        break
#################################

##################################################################

###################################################################################################