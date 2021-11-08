#!/bin/bash

# Declare a string array with type
declare -a StringArray=(FQ_BNS-1_SNIa-binned FQ_BNS-2_SNIa-binned FQ_BNS-3_SNIa-binned FQ_BNS-4_SNIa-binned FQ_BNS-5_SNIa-binned FQ_MBHB-10_SNIa-binned_BNS-1 FQ_MBHB-10_SNIa-binned FQ_MBHB-11_SNIa-binned FQ_MBHB-12_SNIa-binned_BNS-1 FQ_MBHB-12_SNIa-binned FQ_MBHB-13_SNIa-binned FQ_MBHB-14_SNIa-binned FQ_MBHB-15_SNIa-binned FQ_MBHB-1_SNIa-binned_BNS-1 FQ_MBHB-1_SNIa-binned FQ_MBHB-2_SNIa-binned_BNS-1 FQ_MBHB-2_SNIa-binned FQ_MBHB-3_SNIa-binned_BNS-1 FQ_MBHB-3_SNIa-binned FQ_MBHB-4_SNIa-binned FQ_MBHB-5_SNIa-binned FQ_MBHB-6_SNIa-binned FQ_MBHB-7_SNIa-binned FQ_MBHB-8_SNIa-binned FQ_MBHB-9_SNIa-binned_BNS-1 FQ_MBHB-9_SNIa-binned)

# Read the array values with space
for val in "${StringArray[@]}"; do
  mv $val/log $val/archive
done
