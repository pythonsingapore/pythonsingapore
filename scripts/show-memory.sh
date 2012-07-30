#!/bin/bash
source $HOME/bin/script-settings-pysg.sh

ps -u $USERNAME -o pid,rss,command | awk '{print $0}{sum+=$2} END {print "Total", sum}'
