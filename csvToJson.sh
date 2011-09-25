#!/bin/bash
COUNT=`wc -l $1 | awk '{ print $1}'`
echo > stops.json
echo > stops.malformed.json
while read csvLine; do
  latAndLong=`echo $csvLine | awk -F, -v OFS=, '{ print $5,$6 }'`
  name=`echo $csvLine | awk -F, -v OFS=, '{ print $2 }' | sed 's/\"//g'`
  id=`echo $csvLine | awk -F, -v OFS=, '{ print $8 }'`
  #echo $csvLine | awk -F, -v OFS=, '{ print "{loc:["$5,$6"]","\"name\":\""$2"\"","\"id\":"$8"}" }' >> stops.json
  
  #skip entries that don't have numeric stop id
  if [[ $id =~ ^[0-9]+$ ]]; then
    echo "{loc:[$latAndLong],\"name\":\"$name\",\"id\":$id}" >> stops.json
  else
    echo "{loc:[$latAndLong],\"name\":\"$name\",\"id\":$id}" >> stops.malformed.json
  fi

  (( COUNT-- ))
  printf "Lines left to process $COUNT             \r"
done < $1
