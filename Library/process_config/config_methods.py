#-------------------------------------------------------------------------------
# Name:        Hanlde Configuration Files
# Purpose:     Methods for the processing of .ini config files
#
# Author:      jlist001
#
# Created:     14/02/2019
# Copyright:   (c) jlist001 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import ConfigParser
import sys

def config_parser(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config

def sections(config):
    sections =  config.sections()
    return sections

def map_section(section, config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1