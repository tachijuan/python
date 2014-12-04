import csv


with open('/Users/juan/fff','rb') as cf:
  sr = csv.reader(cf)
  for row in sr:
    print 'id3 -n "%s" -a "%s" -t "%s" "%s"' % (row[1],row[2],row[3],row[0])
