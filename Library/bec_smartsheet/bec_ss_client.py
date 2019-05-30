#-------------------------------------------------------------------------------
# Name:        bec_ss_client
# Purpose:     Establishes connection
#
# Author:      John R Lister - GIS Applications Developer
#
# Created:     05/03/2019
# Copyright:   (c) John R Lister 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import smartsheet
import logging
import collections
import json

def build_ss(ss_api):
    """
    Created:
        03/08/2019 11:23AM
    Description:
        Builds the Client communication object for the BEC Bot Account System API Token
        Also initiates a loggin object accessible in the syslogs directory
    Author:
        John R Lister - GIS Applications Developer
    """
    ss_client = smartsheet.Smartsheet(ss_api)
    ss_client.errors_as_exceptions(True)
    logging.basicConfig(filename=r'Path to logging file', level=logging.INFO) #I hate this hardcode but whatevs
    return ss_client

def build_ss_sheet(ss_client, sheetid):
    """
    Created:
            03/08/2019 11:24AM
    Description:
        Builds the sheet object from the Client Communication and Sheet ID
    Author:
        John R Lister - GIS Applications Developer
    """
    ss_sheet = sheet = ss_client.Sheets.get_sheet(sheetid)
    return ss_sheet

def build_col_dict(ss_sheet):
    """
       Created:
            03/08/2019 12:29PM
       Description:
            Construct a JSON Object of the Fields in the Sheet Object
            Primarily used to generate the JSON for the schema config
    """
    columns = ss_sheet.columns
    ss_col_info = collections.OrderedDict()
    for col in columns:
        ss_col_info[str(col.id)] = [col.title]

    return ss_col_info

def matched_col_dict(ss_sheet, title_list):
    """
       Created:
            04/08/2019 12:12PM
       Description:
            Construct a JSON Object of the Fields in the Sheet Object
            Primarily used to generate the JSON for the schema config
            Only returns defined titles
    """
    columns = ss_sheet.columns
    ss_col_info = {} ##collections.OrderedDict()
    for col in columns:
        if col.title in title_list:
            ss_col_info[str(col.id)] = [col.title]

    return ss_col_info






