#!/bin/bash


ls

for i in $(seq 01 10);
do 
    formatted_number=$(printf "%02d" $i)

    echo "[LOG]: Running instance $formatted_number"

    python3 pacman.py "Instances/i$formatted_number"
done