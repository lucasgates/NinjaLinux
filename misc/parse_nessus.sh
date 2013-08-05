#!/bin/bash

echo "This script produces statistics based on CSV of vulnerabilities exported from Nessus."

if [ -z "$1" ]; then
  echo "Usage: $0 nessus_export.csv"
  exit
fi

OUT="$(mktemp)"
OUT=/tmp/nessus.txt

awk -F, '{print $4 "," $5 }' "$1"  |grep -E "Critical|High|Medium|Low|None" | sort | uniq > $OUT 

echo -n "Total systems: "
awk -F, '{print $2 }' $OUT | sort | uniq | wc -l

echo "Findings:"
echo -n "    * Critical "
cat $OUT |grep Critical | sort | uniq | wc -l

echo -n "    * High     "
cat $OUT |grep High     | sort | uniq | wc -l

echo -n "    * Medium   "
cat $OUT |grep Medium   | sort | uniq | wc -l

echo -n "    * Low      "
cat $OUT |grep Low      | sort | uniq | wc -l

#rm $OUT
