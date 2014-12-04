#!/usr/bin/python

import prettytable                  # this lets us print it in a ... pretty table.


a=open('ina').read().splitlines()    # read file "ina" into list a
b=open('ine').read().splitlines()    # read file "ine" into list b
c=list(set(a+b))                     # combine the two list and identify the unique set members, convert to list c
c.sort()                             # sort c
e = prettytable.PrettyTable(['client','Report','Customer'])    # setup a nice table with headers
for x in c:                          # iterate through each member of x
     ina = ine = " "                 # default to not in either
     if x in a: ina = "x"            # table entry for "ina"
     if x in b: ine = "x"            # table entry for "inb"
     if ina == " " or ine == " ":
       e.add_row([x,ina,ine])          # add the row to the table

e.align['client']='l'                # left align the first column
print e                              # print the pretty table
#print e.get_html_string()
