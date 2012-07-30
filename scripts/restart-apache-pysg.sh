#!/bin/bash
source $HOME/bin/script-settings-pysg.sh

cd ~/webapps/$DJANGO_APP_NAME/apache2/bin
./restart
