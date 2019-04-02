#-------------------------------------------------------------------------------
# Name:        Retrieve Schema JSON
# Purpose:     Read an Input (in->dest) JSON Schema file and produce workable variables
#
# Author:      John R Lister - GIS Applications Developer
#
# Created:     12/02/2019
# Copyright:   (c) jlist001 2019
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------

#Custom Module Imports

#Standard Python Library Imports
import os
import json
import sys

# ##############################################################################
# Name: retrieve_json_schema
# Author: John R Lister - GIS Applications Devloper
# Purpose: Map Table Schema JSON's into Workable Variables
# Date: 02/12/2019
# ##############################################################################
## No matches are found as  except ValueError
class retrieve_json_schema:
    def __init__(self, json_file):
        """
            Description: Initialize Method
            Paramater(s):
                json_file: Path to JSON file with defined mapping
            Usage:
                Returns the matching Mapped-Schema:
                    [0] Dest Field Name
                    [1] Dest Field Type
                    [2] Dest Field Length
            Sample Call:
                retrieval_obj = retrieve_json_schema(test_json)
                loaded_json = retrieval_obj.load_json()
                test_list = [u'STRUCTNUM', u'CUSTDATAID', u'ALTSTRUCNU']

                for i in test_list:
                    dest_schema  = retrieval_obj.return_schema(i, loaded_json)
                print(dest_schema)
                retrieval_obj.close_json()

                del retrieval_obj

            Sampe Return:
                [u'String', u'ACCESSIBLE_', 100]
        """
        self.file_ = open(json_file, 'r')
        self.in_fieldnames = []
        ##self.dest_schema = []

    def load_json(self):
        f = self.file_
        json_data = json.load(f)
        return json_data

    def return_schema(self, inField, loaded_json):
        ##data = self.load_json()
        ##print(inField)
        dest_schema = []
        mapped_schema = loaded_json[inField]
        for mapped_id in mapped_schema:
            dest_schema.append(mapped_schema[mapped_id])
        return dest_schema

    def close_json(self):
        self.file_.close()


"""
#Json with the SHP to Main Mapping
test_json = r"C:\Dev\Osmose Reporting\config\drop_main_schema.json"

retrieval_obj = retrieve_json_schema(test_json)
loaded_json = retrieval_obj.load_json()
test_list = [u'LOCATIONID']

for i in test_list:
    dest_schema  = retrieval_obj.return_schema(i, loaded_json)
    print(dest_schema)


retrieval_obj.close_json()


del retrieval_obj
"""
