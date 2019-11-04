#workflow.py

'''
Samuel Ward
28/09/2019
----
tools to construct generic workflows
---
notes: 
    anything that requires the ordered execution of functions can utilise this code
    contains methods which allow arbitrary execution of a set of functions, cutting repetitive code from future workflows
    custom steps can be added via add_command - essentially appending a dispatch table 
---
'''


##################################################################
#Preamble

try:
    import sys
    import subprocess
    import pathlib
    import shlex
except:
    raise ImportError("ERROR: initial modules could not be imported!\nreturning\n")
    sys.exit(1)

try:
    import support
except:
    raise ImportError("ERROR: LOCUST_IO/src/support.py could not be imported!\nreturning\n") 
    sys.exit(1)
try:
    import settings
except:
    raise ImportError("ERROR: LOCUST_IO/src/settings.py could not be imported!\nreturning\n") 
    sys.exit(1)

##################################################################
#Main

class Workflow:
    """
    class for running and defining generic workflows using dispatch tables
    
    notes:
    """

    def __init__(self):
        """
        notes:
            defines fundamental tools to define and execute a workflow
        """

        self.commands=[] #holds list of functions to execute in order during .run()
        self.commands_dispatch={} #mapping between available run commands and their associated workflow() methods

    def add_command(self,command_name,command_function,position=None):
        """
        notes:
            commands sharing same name will be overridden
        args:
            command_name - label string corresponding to run stage e.g. 'set up directories'
            command_function - python function that command corresponds to
            position - position in execution command list (1-n)
        usage:
            def a_nice_command():
                    pass
            workflow.add_command('a nice name for a command',a_nice_command,position=3)
        """

        if position is None: position=len(self.commands)
        self.commands.insert(position-1,command_name)
        self.commands_dispatch[command_name]=command_function

    def run_command(self,command,*args,**kwargs):
        """
        execute individual command/stage in workflow

        notes:
            uses a dispatch in order to control how functions are called 
        args:
            command - string denoting command to run (options stored in self.commands_dispatch)
        """

        if command not in self.commands_dispatch.keys():
            print("ERROR: Workflow.run_command() could not find {command}, available commands - '{commands_avail}'".format(command=command,commands_avail=[command_avail for command_avail in self.commands_dispatch.keys()]))
        else:
            try:
                self.commands_dispatch[command](*args,**kwargs)
            except:
                print("ERROR: Workflow.run_command() could not execute '{command}'".format(command=command))

    def run(self,*args,**kwargs):
        """
        execute all commands/stages in workflow

        notes:
            args,kwargs - passed to all run stages
        """

        for command in self.commands:
            self.run_command(command,*args,**kwargs)

#################################

##################################################################

###################################################################################################