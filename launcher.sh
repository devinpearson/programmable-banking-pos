#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/devinpearson/pos
# point to your venv python version to use the env
sudo /home/devinpearson/pos/env/bin/python pos.py
cd /