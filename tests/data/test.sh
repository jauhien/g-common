#!/bin/bash
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

echo arguments: $@

rm -rf $1/../tst.args

for i in $@
do
    echo $i >> $1/../tst.args
done
