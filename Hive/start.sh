#!/bin/bash
SCREEN_NAME=${SCREEN_NAME:-hive}
TOP_DIR=$(cd $(dirname "$0") && pwd)

if type -p screen >/dev/null && screen -ls | egrep -q "[0-9].$SCREEN_NAME"; then
    echo "You are already running a hive dev session."
    echo "To rejoin this session type 'screen -x hive'."
    echo "To destroy this session, type './stop.sh'."
    exit 1
fi

screen -d -m -S $SCREEN_NAME -t shell -s /bin/bash
sleep 1

if [ -z "$SCREEN_HARDSTATUS" ]; then
    SCREEN_HARDSTATUS='%{= .} %-Lw%{= .}%> %n%f %t*%{= .}%+Lw%< %-=%{g}(%{d}%H/%l%{g})'
fi

screen -r $SCREEN_NAME -X hardstatus alwayslastline "$SCREEN_HARDSTATUS"
#screen -r $SCREEN_NAME -X setenv PROMPT_COMMAND "HIVEMODE"

SCREENRC=$TOP_DIR/$SCREEN_NAME-screenrc
if [[ -e $SCREENRC ]]; then
    rm -f $SCREENRC
fi

NL=`echo -ne '\015'`

function add_to_screen {
  echo "Starting ... $1"
  screen -S $SCREEN_NAME -X screen -t $1
  sleep 1.5
  screen -S $SCREEN_NAME -p $1 -X stuff "$2$NL"  
}

add_to_screen "a-h" "apiary-honeycomb"
add_to_screen "a-h-s" "apiary-honeycomb-statemachine"
add_to_screen "a-c" "apiary-control"
add_to_screen "a-c-s" "apiary-control-statemachine"
