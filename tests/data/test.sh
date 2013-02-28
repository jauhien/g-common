#!/bin/bash

echo arguments: $@

rm -rf $1/../tst.args

for i in $@
do
    echo $i >> $1/../tst.args
done
