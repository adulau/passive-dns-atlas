#!/usr/bin/env python3
# coding=utf-8
#
# passive-dns-atlas
#
# Experimental Passive DNS collector and stats from the RIPE Atlas Stream
#
# Free Software released under the GNU Affero General Public License v3.0

import redis

r = redis.StrictRedis(host='localhost', port=6379)

from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import Result
from ripe.atlas.sagan import DnsResult
import dns.message
import base64

# Fields name are different in sagan and cousteau for parsed DNS
fields = ['TYPE', 'NAME']
fieldsSagan = ['Type', 'Name', 'TTL', 'Class', 'Serial', 'Rname', 'MasterServerName', 'MaintainerName', 'Data']

def process_answers(data=None, sagan=False):
    if data is None:
        return False
    if not sagan:
        for answer in data:
            for field in fields:
                r.zincrby(field, answer[field], 1)
            #r.zincrby('mname', answer['MNAME'], 1)
    else:
        for field in fieldsSagan:
                if field not in data:
                    continue
                r.zincrby(field.upper(), data[field], 1)

def truncating(default=50):
    r.truncating
    #ZREMRANGEBYRANK name 20 -1

def on_result_response(*args ):
    #Store probe statistics in Redis
    #print (args[0]['prb_id'])
    if 'result' in args[0]:
        result = args[0]['result']
        if 'answers' in result:
            #process_answers(data=result['answers'])
            res = DnsResult.get(args[0],parse_buf=True)
            if res.is_error:
                return True
            if (res.responses[0].abuf.answers):
                for answer in res.responses[0].abuf.answers:
                    process_answers(data=answer['raw_data'], sagan=True)

           # print (result['answers'])
        else:
            # Some of the records are not automatically decoded and need to pass
            # into ripe.atlas.sagan firat
            res = DnsResult.get(args[0],parse_buf=True)
            if res.is_error:
                return True
            if (res.responses[0].abuf.answers):
                for answer in res.responses[0].abuf.answers:
                    process_answers(data=answer['raw_data'], sagan=True)
                    #print (answer['raw_data'])
            ## TO add in debug option dns.message verus sagan (sagan seems faster)
            #print (dns.message.from_wire(base64.b64decode(args[0]['result']['abuf'])))
            print ('no answers')

atlas_stream = AtlasStream()
atlas_stream.connect()

channel = "atlas_result"
atlas_stream.bind_channel(channel, on_result_response)

stream_parameters = {"type": "dns"}
atlas_stream.start_stream(stream_type="result", **stream_parameters)

atlas_stream.timeout(seconds=400)
atlas_stream.disconnect()
