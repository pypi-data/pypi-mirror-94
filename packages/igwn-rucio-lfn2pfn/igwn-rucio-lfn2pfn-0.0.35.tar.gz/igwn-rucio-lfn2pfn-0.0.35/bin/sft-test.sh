#!/bin/bash -e
#for sft in `rucio list-dids O2:\*sft --filter type=FILE --short` ; do
#for sft in "O3:H-H1_TUKEYWIN_C00-1164562334-1800.sft"; do


scope=O2
for name in H-H1_TUKEYWIN_C01-1164564134-1800.sft H-H1_TUKEYWIN_C00-1164562334-1800.sft H-H1_TUKEYWIN_C01-1164562334-1800.sft H-H1_TUKEYWIN_C00-1164564134-1800.sft; do

#for sft in "O2:H-H1_TUKEYWIN_C00-1164562334-1800.sft"; do

  #scope=$(echo $sft | cut -d ":" -f 1)
  #name=$(echo $sft | cut -d ":" -f 2)

  time python -c "import igwn_lfn2pfn; print(igwn_lfn2pfn.ligo_legacy('${scope}', '${name}'))"
done
