#!/usr/bin/env python3
# coding=utf-8
#
# passive-dns-atlas - basic stats extractor
#
# Experimental Passive DNS collector and stats from the RIPE Atlas Stream
#
# Free Software released under the GNU Affero General Public License v3.0

import redis
from prettytable import PrettyTable
import argparse
import sys
import os

fieldsSagan = ['Type', 'Name', 'TTL', 'Class', 'Serial', 'Rname', 'MasterServerName', 'MaintainerName', 'Data']
limit = 100

parser = argparse.ArgumentParser(description='passive-dns-atlas statistics extractor')
parser.add_argument("-t","--table", default=False, action='store_true', help="Dump statistics table in ASCII")
parser.add_argument("-c","--csvd3js", default=False, action='store_true', help="Generate D3.js Bubble Chart")
parser.add_argument("-o","--outputdir", default="./stats/", help="Output directory")
args = parser.parse_args()

if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)

r = redis.StrictRedis(host='localhost', port=6379)

for field in fieldsSagan:
    c = r.zrange(field.upper(), 0, limit, desc=True, withscores=True)

    if args.table:
        table = PrettyTable()
        table.field_names = ["Number of occurences",field.upper()]
        for value in c:
            table.add_row([value[1],value[0].decode()])
        print (table)
    elif args.csvd3js:
        with open("{}/{}.csv".format(args.outputdir,field.upper()), 'w') as f:
            f.write("id,value\n")
            for value in c:
                f.write("{},\n".format(value[0].decode()))
                f.write("{},{}\n".format(value[0].decode(),int(value[1])))

    else:
        print ("You need a specify an output like --table or at least one of the options below")
        parser.print_help()
        sys.exit(2)



