#-------------------------------------------------------------------------------
# Name:        Sync Control
# Purpose:     Controlls the order of operations for logging the data from the source
#               smartsheet to the Logging Sheet
#
# Author:      John R Lister - GIS Applications Developer
#
# Created:     02/04/2019
# Copyright:   (c) jlist001 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Custom Module Imports
from mapped_schema.retrieve_schema_json import *
from gdb_methods.local_write_methods import *
from process_config.config_methods import *
from bec_decode.simplestic_plastic import *
from bec_smartsheet.bec_ss_client import *

#Set Local Environment Variables:
working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Working GDB
bec_osmose_GDB = os.path.join(os.path.dirname(working_dir), 'dev_gdb.gdb')
arcpy.env.workspace = bec_osmose_GDB

#Initialize the Configuration Methods
config_file = os.path.join(os.path.dirname(working_dir), r'config\ss_config.ini')
config = config_parser(config_file)
sections = sections(config)

#API Token & Sheet ID
ss_api = softplastic(map_section(sections[0],config)['ss_api'])
sheet_id = softplastic(map_section(sections[1],config)['osmose_sheet_id'])

#Construct Client and Sheet Objects
ss_client = build_ss(ss_api)
ss_sheet = build_ss_sheet(ss_client, sheet_id)