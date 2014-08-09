#!/bin/bash

echo "Executing Bash Script"
echo "Executing searchDBForCurrentStars to create max_stars"
python searchDBForCurrentStars.py
echo "Running HNTableTests.py to create hn_event_table"
python hnTableTests.py
echo "Running chart.py to check the data"
python chart.py
echo "Complete"