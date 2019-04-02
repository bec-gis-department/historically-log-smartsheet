#-------------------------------------------------------------------------------
# Name:         build schema config
# Purpose:     Generate a JSON containing the mapped schema from Input Tables to Output Tables
#              Adjust variables accordingly
# Author:      John R Lister - GIS Applications Developer
#
# Created:     12/02/2019
# Copyright:   (c) jlist001 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import sys
import json

#Set the Workspcae to the Scratch GDB where the Schema Rules are exported
arcpy.env.workspace = r"C:\Dev\Osmose Reporting\dev_gdb.gdb"

#Osmose Main Sync table
# Inputs: From Shapefile Drops
# Destination: osmose_main_sync
master_sync_schema = 'fieldmapping_main_ss' #Table I exported the rules to...

# Fields to get the Input [0] and Destination [2] plus the other shit...Type [1] Len [3]
##srch_fields = ['IN_FIELDNAME', 'FIELTYPE', 'DEST_FIELDNAME', 'FIELDLEN']
#Main to SS
srch_fields = ['ss_fieldname', 'ss_fieldid', 'main_fieldname', 'main_fieldtype']
#SS to main
##srch_fields = ['ss_fieldname', 'ss_fieldid', 'main_fieldname', 'main_fieldtype]

# Build the Search Cursor
srch_cursor = arcpy.da.SearchCursor(master_sync_schema, srch_fields)

# Compile the Rows
row_data = [x for x in srch_cursor]
del srch_cursor #Kill it because we no longer need it

# List the Input Names
in_names = [x[1] for x in row_data]
dest_names = [x[2] for x in row_data]
dest_types = [x[3] for x in row_data]
##dest_len = [x[3] for x in row_data]

#Build a nested Dictionary
# Upper Level
mapped_schema = {}
for i in range(len(in_names)):
    # Mapped Schema
    mapped_item = {
                        int(in_names[i]) : {
                                        'destname' : dest_names[i],
                                        'desttype' : dest_types[i]
                                            }
                    }
    mapped_schema.update(mapped_item)

#Build JSON
json_dump = json.dumps(mapped_schema)

print(json_dump)





