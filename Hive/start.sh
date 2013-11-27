#!/bin/bash

source ./localrc

function add_to_screen {
  NL=`echo -ne '\015'`
  echo "Starting ... $1"
  screen -S $SCREEN_NAME -X screen -t $1
  sleep 1.5
  screen -S $SCREEN_NAME -p $1 -X stuff "$1$NL"
}

if [ $MULTIPLEXER == SCREEN ]; then
  SCREEN_NAME=${SCREEN_NAME:-hive}

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

  if $DEAMONS; then 
    add_to_screen "mongod"
    add_to_screen "rabbitmq-server"
    sleep 1
  fi

  add_to_screen "apiary-honeycomb"
  add_to_screen "apiary-agentmanager"
  add_to_screen "apiary-agentmonitor"
  add_to_screen "apiary-sting"

elif [ $MULTIPLEXER == TMUX ]; then
  NAME=Hive

  tmux has-session -t $NAME
  if [ $? != 0 ]
  then
    tmux new-session -s $NAME -d
    
    if $DEAMONS; then 
      tmux new-window -n mongo -t $NAME:1
      tmux send-keys -t $NAME:1 "mongod" C-m

      tmux new-window -n rabbit -t $NAME:2
      tmux send-keys -t $NAME:2 "rabbitmq-server" C-m

      sleep 1
    fi

    tmux new-window -n control -t $NAME:3
    tmux send-keys -t $NAME:3 "apiary-agentmanager" C-m

    tmux new-window -n control-statemachine -t $NAME:4
    tmux send-keys -t $NAME:4 "apiary-agentmonitor" C-m

    tmux new-window -n honeycomb -t $NAME:5
    tmux send-keys -t $NAME:5 "apiary-honeycomb" C-m

    tmux new-window -n sting -t $NAME:6
    tmux send-keys -t $NAME:6 "apiary-sting" C-m

    tmux select-window -t $NAME:1
  fi

  #tmux attach -t $NAME
fi
