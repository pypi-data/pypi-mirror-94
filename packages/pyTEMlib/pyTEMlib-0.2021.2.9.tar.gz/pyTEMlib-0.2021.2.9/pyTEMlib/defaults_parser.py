"""
Default files will be copied to default directory when installed for first time
"""
# Gleaned from
# Copyright © 2007 Francisco Javier de la Peña
# file of EELSLab.
#

import os
import tarfile

from pyTEMlib.config_dir import config_path, os_name, data_path

defaults_file = os.path.join(config_path, 'TEMlibrc')
bool_keys = ['fs_state', 'synchronize_cl_with_ll', 'plot_on_load']
str_keys = ['microscope', 'GOS_dir', 'fitter', 'file_format']
float_keys = ['fs_emax', 'preedge_safe_window_width', 
'knots_factor', 'min_distance_between_edges_for_fine_structure' ]

Gos_file = os.path.join(data_path, 'GOS.tar.gz')
f = open(defaults_file, 'r')
defaults_dict = {}
for line in f:
    if line[0] != "#":
        line_list = line.split()
        if line_list != []:
            if line_list[0] in float_keys:
                key, value = line_list
                defaults_dict[key] = float(value)
            elif line_list[0] in str_keys:
                key =  line_list[0]
                
                for i in range(1,len(line_list)):
                    if i > 1:
                        value = value+' '+line_list[i]
                    else:
                        value = line_list[i]
                    
                defaults_dict[key] = value
            elif line_list[0] in bool_keys:
                key, value = line_list[0:2]
                defaults_dict[key] = bool(int(value))
f.close()

if defaults_dict['GOS_dir'] == 'None':
    if os_name == 'windows':
        # If DM is installed, use the GOS tables from the default installation
        # location in windows
        program_files = os.environ['PROGRAMFILES']
        
        gos = '\Gatan\EELS Reference Data\H-S GOS Table\ ' 
        gos_path ='C:\ProgramData\Gatan\EELS Reference Data\H-S GOS Tables'

        
        
        # Check whether it is in the (x86) Program folder of windows 7
        if os.path.isdir(gos_path) is False:
            program_files += ' (x86)'
            gos_path = os.path.join(program_files, gos)
            if os.path.isdir(gos_path) is False:
                # Else, use the default location in the .eelslab folder
                gos_path = os.path.join(config_path, 'GOS')
    else:
        gos_path = os.path.join(config_path, 'GOS')
    
    if os.path.isdir(gos_path) is False and os.path.isfile(Gos_file) is True:
        #messages.alert("Installing the GOS files in: %s" % gos_path) 
        tar = tarfile.open(Gos_file)
        os.mkdir(gos_path)
        tar.extractall(gos_path)
    if os.path.isdir(gos_path):
        defaults_dict['GOS_dir'] = gos_path
        
class Defaults:
    pass

defaults = Defaults()
defaults.__dict__ = defaults_dict


# Install the tutorial in the home folder if the file is available
tutorial_file = os.path.join(data_path, 'tutorial.tar.gz')
tutorial_directory = os.path.expanduser('~/eelslab_tutorial')
if os.path.isfile(tutorial_file) is True:
    if os.path.isdir(tutorial_directory) is False:
        #messages.alert("Installing the tutorial in: %s" % tutorial_directory) 
        tar = tarfile.open(tutorial_file)
        os.mkdir(tutorial_directory)
        tar.extractall(tutorial_directory)
