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
import argparse
import logging

# Fields name are different in sagan and cousteau for parsed DNS
fields = ['TYPE', 'NAME']
fieldsSagan = ['Type', 'Name', 'TTL', 'Class', 'Serial', 'Rname', 'MasterServerName', 'MaintainerName', 'Data']
filters = None
defaultloglevel = logging.INFO
def process_answers(data=None, sagan=False):
    data = filterout(filters=filters, data=data)
    if data is None:
        return False
    if args.debug:
        print("{}".format(data))
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

def filterout(filters=None, data=None):
    if filters is None:
        return data
    flag = False
    for filter_rule in filters:
        k, v = filter_rule
        if k in data:
            if v in data[k]:
                if data[k] == v:
                    flag = True
    if flag is False:
        return None
    else:
        return data

def on_result_response(*args ):
    #Store probe statistics in Redis
    #print (args[0]['prb_id'])
    if 'result' in args[0]:
        result = args[0]['result']
        if 'answers' in result:
            #process_answers(data=result['answers'])
            logging.disable(logging.WARNING)
            res = DnsResult.get(args[0],parse_buf=True)
            logging.basicConfig(level=defaultloglevel)
            if res.is_error:
                return True
            if (res.responses[0].abuf.answers):
                for answer in res.responses[0].abuf.answers:
                    process_answers(data=answer['raw_data'], sagan=True)

           # print (result['answers'])
        else:
            # Some of the records are not automatically decoded and need to pass
            # into ripe.atlas.sagan firat
            logging.disable(logging.WARNING)
            res = DnsResult.get(args[0],parse_buf=True)
            logging.basicConfig(level=defaultloglevel)
            if res.is_error:
                return True
            if (res.responses[0].abuf.answers):
                for answer in res.responses[0].abuf.answers:
                    process_answers(data=answer['raw_data'], sagan=True)
                    #print (answer['raw_data'])
            ## TO add in debug option dns.message verus sagan (sagan seems faster)
            #print (dns.message.from_wire(base64.b64decode(args[0]['result']['abuf'])))


parser = argparse.ArgumentParser(description='passive-dns-atlas')
parser.add_argument("-d","--debug", default=False, action='store_true')
parser.add_argument("-t","--timeout", default=400, type=float, help="set atlas stream timeout, default is 400 sec")
parser.add_argument("-o","--only", action='append', default=None, help="set a filter to allow check a specifity key and value in DNS. IN,A")
args = parser.parse_args()

if args.debug:
    defaultloglevel = logging.DEBUG

logging.basicConfig(level=defaultloglevel)


if args.only is not None:
    filters = []
    for v in args.only:
        filters.append(v.split(","))
    logging.info("Filter applied: {}".format(filters))

atlas_stream = AtlasStream()
atlas_stream.connect()

channel = "atlas_result"
#channel = "atlas_subscribe"
atlas_stream.bind_channel(channel, on_result_response)

stream_parameters = {"type": "dns"}
#stream_parameters = {"startTime": 1489568000, "stopTime": 1489569100, "msm": 30001}
atlas_stream.start_stream(stream_type="result", **stream_parameters)

atlas_stream.timeout(seconds=args.timeout)
atlas_stream.disconnect()
