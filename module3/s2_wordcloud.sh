#!/usr/bin/env bash

# Building a wordcloud based on one year of bulletins

YEAR=$1
cat data/txt/*_${YEAR}_*.txt > module3/results/${YEAR}.txt
python module3/filtering.py 'module3/results/' $YEAR
wordcloud_cli --text module3/results/${YEAR}_keywords.txt \
              --imagefile module3/results/${YEAR}.png \
              --width 2000 --height 1000
display module3/results/${YEAR}.png
