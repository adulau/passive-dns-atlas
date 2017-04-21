#!/bin/bash
#
# Quick-and-dirty(tm) hack to generate the D3 js bubble charts from the
# CSV files exported from get_stats.py. The template.html contains the source file.

for file in *.csv ; do
        field=$( echo ${file} | cut -f1 -d.)
        echo ${field}
        cat "template.html" | sed -e "s/##FIELD##/${field}/g" >${field}.html
done
