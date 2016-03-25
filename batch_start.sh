#!/bin/bash
for (( i=1; i<=$1; i++ )); do
    python3 src/main.py --debug &
done
