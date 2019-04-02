#-------------------------------------------------------------------------------
# Name:        bec_sync
# Purpose:     Uses bec_client and ss sdk to synchronize local datasource and Sheet
#
# Author:      John Lister, Bluebonnet GIS Department
#
# Created:     18/07/2018
# Copyright:   (c) jlist001 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import smartsheet
import json
import pypyodbc
import arcpy
import os
#-------------------------------------------------------------------------------
#-----------------------------Smartsheet----------------------------------------
class _Smartsheet_:
    """
        Build Smartsheet Client and Sheet Object
        ***Probably a redundant class but I neeed to learn them***

        __init__:
            Build the Smartsheet Client Object using the API token
        build_sheet:
            Build Sheet Object from SS Client using Sheet ID
    """
    def __init__(self, ss_api_token):
            self.client = smartsheet.Smartsheet(ss_api_token)
    def build_sheet(self, ss_sheet_id):
        return self.client.Sheets.get_sheet(ss_sheet_id)

#----------------------------Column Info----------------------------------------
class _columns_:
    """
        Retrieve Column/Field Information from Smartsheet and osmose Sync
            __init__:
                Build the Sheet Column Object List
                Build the Local Field Object List
            build_col_dict:
                build the dictionaries of field information
    """

    def __init__(self, sheet, table):
        self.columns = sheet.columns
        self.fields = [i for i in arcpy.ListFields(table)]

    def build_col_dict(self):
        ss_col_info = collections.OrderedDict()
        for col in self.columns:
            ss_col_info[str(col.id)] = [col.title]
        local_col_info = collections.OrderedDict()
        for col in self.fields:
            local_col_info[col.aliasName] = [col.name]
        return (ss_col_info, local_col_info)

    def match_col_info(self, ss_info, local_info):
        ss_col_ids = []
        local_matched_fields =[]
        for key, value in ss_col_info.iteritems():
            if str(key) not in local_col_info:
                print("Add Field ID: {0}, Value: {1}".format(key, value))
                try:
                    print("Add Field")
                    arcpy.AddField_management(
                                                osmose_sync,
                                                value,
                                                "TEXT",
                                                field_length=250,
                                                field_alias=key,
                                                field_is_nullable="NULLABLE"
                                                )
                except Exception:
                    e = sys.exc_info()[1]
                    print(e.args)
            else:
                ss_col_ids.append(key)
                local_matched_fields.append(local_col_info.get(key)[0])
        return(local_matched_fields, ss_col_ids)


