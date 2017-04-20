# passive-dns-atlas

Passive DNS collection (and statistics) from RIPE Atlas Sensors

The goal is to use RIPE Atlas Sensors as a source of DNS information for passive collection but also to provide
additional information and statistics to Passive DNS users from the DNS measurements performed by the RIPE Atlas sensors.

# Requirements

- Python 3
- [ripe.atlas.cousteau](https://github.com/RIPE-NCC/ripe-atlas-cousteau)
- [ripe.atlas.sagan](https://github.com/RIPE-NCC/ripe.atlas.sagan)
- Redis compatible server
- RIPE Atlas API key

# Usage

~~~~
./bin/pdns.py
~~~~

# Current Statistics

~~~~
127.0.0.1:6379> ZREVRANGE NAME 0 12
 1) "hostname.bind"
 2) "."
 3) "id.server"
 4) "pt."
 5) "by."
 6) "xn--90ais."
 7) "com."
 8) "se."
 9) "es."
10) "ie."
11) "net."
12) "version.bind"
13) "il."
127.0.0.1:6379> ZREVRANGE TYPE 0 12
1) "TXT"
2) "SOA"
3) "A"
4) "CNAME"
5) "MX"
6) "NS"
7) "AAAA"
127.0.0.1:6379> ZREVRANGE TYPE 0 12 WITHSCORES
 1) "TXT"
 2) "249269"
 3) "SOA"
 4) "118628"
 5) "A"
 6) "1275"
 7) "CNAME"
 8) "118"
 9) "MX"
10) "65"
11) "NS"
12) "48"
13) "AAAA"
14) "31"
~~~~

# License

