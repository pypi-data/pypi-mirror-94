#!/bin/bash -e
test_script=/home/jclark/Projects/igwn-rucio-lfn2pfn/bin/test_lfn2pfn
input_file=$1

while IFS=" " read -r scope lfn pfn
do
  echo "Checking ${lfn}"
  ${test_script} ${lfn} --true-pfn ${pfn} --scope ${scope} --rse LIGO-CIT-ARCHIVE > /dev/null
done < ${input_file}
