#!/bin/bash
module unload python
module load python
python /home/arpank/Scripts/cube2ipr/cube2ipr.py $*
module unload python

