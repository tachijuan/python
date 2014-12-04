#!/usr/bin/python
#
# (C) 2014 Datalink Corp - Juan Orlandini
#
# This script is provided as-is with no implied warranties
#
#
# A simple script to parse the output from EMC CTA appliances
# There's very little error checking. The assumption is that all lines from the output include a time stamp and that the
# first line of the output file has the start time code and the last time has the end time code.
#
# Usage:
# python parse_cta.py <list of files>
#
# All output goes to stdout
#
# Revision history:
# 1.0 12-Nov-2014 - Initial working version
# 1.1 18-Nov-2014 - Reworked to make code clearer and use a "fields" list. Hoping to make this more generic for other CTA logs.
#                   This code makes it easier to add fields, remove fields, and also re-order fields for output. Just change the "fields" list
#                   Reworked time parsing to be more consistent with the rest of the code.
# 1.2 18-Nov-2014 - Added proper time parsing to calculate the year **** NOTE **** this code will report inaccurate run time  if the run starts 
#                   before midnight December 31 and runs into the next year
#

import sys                                                                  # needed for argv
import re                                                                   # we use this to strip unnecessary characters and stuff in parens
from datetime import datetime                                               # date time calculation stuff

fields = ("share","tag_id","total_dirs_processed","total_files_processed","total_files_archived","total_bytes_archived",
          "total_fileops_failed","disk_capacity","disk_usage_start","disk_usage_end","total_files_stubbed",
          "total_bytes_stubbed","total_files_delay_stubbed","total_bytes_delay_stubbed","run_date","runtime")

if len(sys.argv) < 2:                                                       # check for the appropriate number of command line scripts
  print "You need to enter more one or more files as the arguments to this script"
  sys.exit(42)
else:                                                                       # we have a good list of files
  print ','.join(fields)                                                    # print out our header by joining all the fields with a comma
  for myfile in sys.argv[1:]:                                               # process each file in the argument list
    sl = [line.strip() for line in open(myfile)]                            # slurp the whole file

    d=dict()                                                                # blank dictionary to add our keys
    for i in sl:                                                            # process each line
      if 'Commands:' in i:                                                  # if we have the host/share add it to the dict
        left = i.find('-Cs')
        right = i.find(' ',left+4)
        d['share']=i[left+4:right]
      elif 'START SUPPORT' in i:                                            # else if we find the START SUPPORT message
        left = i.find('SUPPORT:')
        rstarttime = datetime.strptime(i[left+9:],"%a %b %d %H:%M:%S %Y")   # Use this to get the run date
        starttime = datetime.strptime(sl[0][0:15],"%b %d %H:%M:%S")         # use this to calculate run time
        endtime = datetime.strptime(sl[len(sl)-1][0:15],"%b %d %H:%M:%S")
        d['runtime'] = str((endtime-starttime).total_seconds())             # add runtime to the dict
        d['run_date'] = rstarttime.strftime('%m-%d-%Y')                     # add run_date to the dict
      else:
        if i.count('=')==1:                                                 # look for lines that have a single = 
          for k,v in [i.split('=')]:                                        # split on the equal
            val = re.sub('\(.*\)|[," ]','',v)                                # get rid of " and , and also stuff in parens 
            k = k[42:]                                                      # get the key value from the line (strip out the time stamp stuff)
            d[k.strip()]=val                                                # store the value

    # build the ouput string by using a lambda func to map keys in fields to values in dict and joining them with a comma
    print ','.join(map(lambda x: d[x],fields))
