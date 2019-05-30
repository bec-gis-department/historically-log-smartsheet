#-------------------------------------------------------------------------------
# Name:        Sync Control
# Purpose:     Controlls the order of operations for logging the data from the source
#               smartsheet to the Logging Sheet
#
# Author:      John R Lister - GIS Applications Developer
#
# Created:     04/08/2019
# Copyright:   (c) jlist001 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Custom Module Imports
from mapped_schema.retrieve_schema_json import *
from process_config.config_methods import *
from bec_decode.simplestic_plastic import *
from bec_smartsheet.bec_ss_client import *

#Standard Python Libraries
import datetime
import uuid
import json
import sys

#Set Local Environment Variables:
working_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_dir = os.path.join(os.path.dirname(working_dir), 'config')
datestamp = datetime.date.today()
date_value = datestamp.strftime('%Y-%m-%d')
month_stamp = datestamp.strftime('%B')

'''
##Potential use case if weekend data is not desired
#Test if we are executing on a weekday
weekno = datestamp.weekday()
if weekno<5:
    print "Executing on a Weekday, system initializing"
else:
    print "Executing on a Weekend, system must exit"
    sys.exit()
'''

#Project Coordinators
##Just testing some shit
coord_hours_dict = {
                        'Shawn Ely':[],
                        'Bill Scoggins':[],
                        'Rodney Gerik':[],
                        'Shane Mathison':[],
                        'Clemente Verastegui':[]
                        }

#Initialize the Configuration Methods
lp_id_file = os.path.join(config_dir, 'lp_search_ids.json')
config_file = os.path.join(config_dir, 'ss_config.ini')
config = config_parser(config_file)
sections = sections(config)

#API Token & Sheet ID
ss_api = softplastic(map_section(sections[0],config)['ss_api'])
lp_sheet_id = softplastic(map_section(sections[1],config)['lp_sheet_id'])
log_sheet_id = softplastic(map_section(sections[1],config)['tracking_sheet_id'])

#Construct Client and Sheet Objects
ss_client = build_ss(ss_api)
ss_lp_sheet = build_ss_sheet(ss_client, lp_sheet_id)
ss_log_sheet = build_ss_sheet(ss_client, log_sheet_id)


lp_read_ids = ['4586663482550148', '3459685182400388', '1767515668932484']
proj_coord_id = lp_read_ids[0]
job_hours_id = lp_read_ids[1]
job_status_id = lp_read_ids[2]
print(build_col_dict(ss_log_sheet))
for row in ss_lp_sheet.rows:
    main_row_list = []
    for i in range(len(row.cells)):
        lp_col_id = str(row.cells[i].column_id)
        lp_cell_value =  str(row.cells[i].display_value)
        #If the Column ID is in the list of IDs we want to read from
        if lp_col_id == proj_coord_id:
            main_row_list.append(lp_cell_value)
        elif lp_col_id == job_hours_id:
            main_row_list.append(lp_cell_value)
        elif (lp_col_id == job_status_id) and (lp_cell_value == 'Active'):
            main_row_list.append(lp_cell_value)
        elif (lp_col_id == job_status_id) and (lp_cell_value != 'Active'):
            main_row_list.append(None)
    #Fetch only the rows that pas sthe criteria
    if not any(elem is None for elem in main_row_list):
        ##main_row_list.remove(main_row_list[1])
        print(main_row_list)
        coordinator = main_row_list[0]
        #Test if Hours value is valid
        try:
            hours = int(main_row_list[-1])
        except ValueError:
            hours = 0
        #Append Hours Value to coord_hours_dict
        try:
            coordinator_list = coord_hours_dict[coordinator]
        except KeyError:
            print("{} needs to be added".format(coordinator))
            sys.exit()
        coordinator_list.append(hours)
        coord_hours_dict[coordinator] = coordinator_list

# Iterate through the dictionary to prepare the row
for key, value in coord_hours_dict.iteritems():
    row_id = str(uuid.uuid4())
    total_active = len(value)
    sum_hours = sum(value)
    #SS ADD Row method
    row_a = ss_client.models.Row()
    row_a.to_top = True
    #Source Row ID From LP Sheet
    row_a.cells.append({
          'column_id': 1806618137520004,
          'value': row_id
        })
    #Month Value %B
    row_a.cells.append({
          'column_id': 5709437739526020,
          'value': month_stamp,
        })
    #Datestamp ID
    row_a.cells.append({
          'column_id': 6310217764890500,
          'value': date_value,
        })
    #Project Coordinator
    row_a.cells.append({
          'column_id': 8562017578575748,
          'value': key,
        })
    #Project Sum Hours
    row_a.cells.append({
          'column_id': 4058417951205252,
          'value': sum_hours,
        })
    #Sum Active Jobs
    row_a.cells.append({
          'column_id': 5832866778113924,
          'value': total_active,
        })
    #Send the data
    response = ss_client.Sheets.add_rows(log_sheet_id, row_a) #Comment out when testing to avoid sending data
##[('1806618137520004', [u'row_id']), ('5709437739526020', [u'Month']), ('6310217764890500', [u'Datestamp']), ('4058417951205252', [u'Sum Hours']), ('8562017578575748', [u'Project Coordinator']), ('5832866778113924', [u'Number of Active Jobs'])])

del ss_log_sheet, ss_lp_sheet, ss_client



