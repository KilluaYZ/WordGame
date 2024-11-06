#!/bin/bash
CASE_DIR=$1
for file in $(ls $CASE_DIR/*.in)
do
    echo "-------------------"
    echo $file;
    ./word_game < $file
    echo "-------------------"
done