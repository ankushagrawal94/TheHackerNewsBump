#!/bin/bash

echo "Executing Bash Script"
echo "Running deleteMe.py to create hn_event_table_two"
python deleteMe.py
echo "Running chart.py to check the data"
python chart.py
echo "Complete"