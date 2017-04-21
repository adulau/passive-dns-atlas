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

parser = argparse.ArgumentParser(description='passive-dns-atlas statistics extractor')
parser.add_argument("-t","--table", default=False, action='store_true', help="Dump statistics table in ASCII")
parser.add_argument("-c","--csvd3js", default=False, action='store_true', help="Generate D3.js Bubble Chart")
parser.add_argument("-l","--limit", type=int, default=100, help="Limit of values to export per ZRANK - default 100")
parser.add_argument("-o","--outputdir", default="./stats/", help="Output directory")
parser.add_argument("-s","--skip", default=None, action="append", help="Skip a specific value from the statistics")
args = parser.parse_args()

if args.skip is None:
    args.skip = ['']

if not os.path.exists(args.outputdir):
    os.makedirs(args.outputdir)

r = redis.StrictRedis(host='localhost', port=6379)

for field in fieldsSagan:
    c = r.zrange(field.upper(), 0, args.limit, desc=True, withscores=True)

    if args.table:
        table = PrettyTable()
        table.field_names = ["Number of occurences",field.upper()]
        for value in c:
            if value[0] in args.skip:
                continue
            table.add_row([int(value[1]),value[0].decode()])
        print (table)
    elif args.csvd3js:
        with open("{}/{}.csv".format(args.outputdir,field.upper()), 'w') as f:
            f.write("id,value\n")
            for value in c:
                if value[0].decode() in args.skip:
                    continue
                f.write("{},\n".format(value[0].decode()))
                f.write("{},{}\n".format(value[0].decode(),int(value[1])))

    else:
        print ("You need a specify an output like --table or at least one of the options below")
        parser.print_help()
        sys.exit(2)



