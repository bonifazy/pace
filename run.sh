#!/bin/bash

# clear log file
truncate --size 0 ~/pace/log/bot.log

# run telegram bot
~/pace/env/bin/python3 bot.py
