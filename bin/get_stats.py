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

fieldsSagan = ['Type', 'Name', 'TTL', 'Class']
limit = 100

r = redis.StrictRedis(host='localhost', port=6379)

for field in fieldsSagan:
    c = r.zrange(field.upper(), 0, limit, desc=True, withscores=True)
    table = PrettyTable()
    table.field_names = ["Number of occurences",field.upper()]
    for value in c:
        table.add_row([value[1],value[0].decode()])
    print (table)
