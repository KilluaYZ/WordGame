#!/bin/bash
rm -r logs/err
rm -r logs/out
mkdir -p logs/err
mkdir -p logs/out
for i in {1..10}
do
    echo "------------------"
    echo $i
    python3 ./data_gen.py 2>logs/err/err_$i.log | tee logs/out/out_$i.log | ./word_game
    echo "------------------"
done