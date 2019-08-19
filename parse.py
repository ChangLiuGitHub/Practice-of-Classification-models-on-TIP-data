#!/usr/bin/python

import csv
import sys
import re
import fileinput

re_0 = re.compile(r'^(...)(.*)$')
re_10 = re.compile(r'^([^ ]+) +(.*)$')
re_11 = re.compile(r'^([^ ]+) +([^ ]+) +(.+), +(.*)$')
re_20 = re.compile(r'^(.*)$')
re_21 = re.compile(r'^([^ ]+) +(.+), +(.*)$')

def parse(fn, wr):
  f=open(fn,'r')
  lines=[x.strip('\n') for x in f.readlines()]
  empty4=("","","","")
  empty3=("","","")
  l1 = empty4
  l2 = empty4
  l3 = empty4
  state = 0
  d1 = ""
  d2 = ""
  d3 = ""
  i = 0
  n = 0
  rows = []
  while i < len(lines):
    m = re_0.match(lines[i])
    if m is not None:
      if m.group(1) == '###':
        state = 1
        mm = re_10.match(m.group(2))
        if mm is not None:
          mmm = re_11.match(m.group(2))
          if mmm is not None:
            l1 = (mmm.group(1), mmm.group(2), mmm.group(3), mmm.group(4))
          else:
            l1 = (mm.group(1), mm.group(2), "", "")
          l2 = empty4
          l3 = empty4
          d2 = ""
          d3 = ""
        else:
          print("!!# Not match [%d] %s" % (i, lines[i]))
          return None
      elif m.group(1) == '@@@':
        state = 2
        mm = re_10.match(m.group(2))
        if mm is not None:
          mmm = re_11.match(m.group(2))
          if mmm is not None:
            l2 = (mmm.group(1), mmm.group(2), mmm.group(3), mmm.group(4))
          else:
            l2 = (mm.group(1), mm.group(2), "", "")
          l3 = empty4
          d3 = ""
        else:
          print("!!@ Not match [%d] %s" % (i, lines[i]))
          return None
      elif m.group(1) == '$$$':
        state = 3
        mm = re_10.match(m.group(2))
        if mm is not None:
          mmm = re_11.match(m.group(2))
          if mmm is not None:
            l3 = (mmm.group(1), mmm.group(2), mmm.group(3), mmm.group(4))
          else:
            l3 = (mm.group(1), mm.group(2), "", "")
        else:
          print("!!$ Not match [%d] %s" % (i, lines[i]))
          return None
      elif m.group(1) == '===':
        state = 4
        mm = re_20.match(m.group(2))
        if mm is not None:
          mmm = re_21.match(m.group(2))
          if mmm is not None:
            l4 = (mmm.group(1), mmm.group(2), mmm.group(3))
          else:
            l4 = (mm.group(1), "", "")
        else:
          print("!!= Not match [%d] %s" % (i, lines[i]))
          return None
        i = i+1
        n = n+1
        row = [n, l1[0], l1[1], l1[2], l1[3], d1, l2[0], l2[1], l2[2], l2[3], d2, l3[0], l3[1], l3[2], l3[3], d3, l4[0], l4[1], l4[2], lines[i]]
        wr.writerow(row)
      else:
        if state == 1:
          d1 = d1 + lines[i] + "\n"
        elif state == 2:
          d2 = d2 + lines[i] + "\n"
        elif state == 3:
          d3 = d3 + lines[i] + "\n"
    i = i+1
##
with open('%s.csv' % sys.argv[1], 'w') as cf:
  writer = csv.writer(cf, delimiter=',', quoting=csv.QUOTE_ALL)
  title = ["count", "rank-1 label", "rank-1 name", "rank-1 author", "rank-1 date", "rank-1 description",
           "rank-2 label", "rank-2 name", "rank-2 author", "rank-2 date", "rank-2 description",
           "rank-3 label", "rank-3 name", "rank-3 author", "rank-3 date", "rank-3 description", 
           "rank-4 name", "rank-4 author", "rank-4 date", "rank-4 description"]
  writer.writerow(title)
  parse(sys.argv[1], writer)
