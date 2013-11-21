#!/bin/bash

if [ -z "$MULTIPLEXER" ]; then
  MULTIPLEXER="SCREEN" #SCREEN   Or  TMUX
fi

if [ $MULTIPLEXER == SCREEN ]; then
  echo "$MULTIPLEXER"
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
  #screen -r $SCREEN_NAME -X setenv PROMPT_COMMAND "HIVEMODE"

  NL=`echo -ne '\015'`

  function add_to_screen {
    echo "Starting ... $1"
    screen -S $SCREEN_NAME -X screen -t $1
    sleep 1.5
    screen -S $SCREEN_NAME -p $1 -X stuff "$1$NL"
  }

  add_to_screen "apiary-honeycomb"
  add_to_screen "apiary-agentmanager"
  add_to_screen "apiary-agentmonitor"
  add_to_screen "apiary-sting"

elif [ $MULTIPLEXER == TMUX ]; then
  echo "$MULTIPLEXER is better :D"
  NAME=Hive

  tmux has-session -t $NAME
  if [ $? != 0 ]
  then
    tmux new-session -s $NAME -d

    tmux new-window -n control -t $NAME:2
    tmux send-keys -t $NAME:2 "apiary-agentmanager" C-m

    tmux new-window -n control-statemachine -t $NAME:3
    tmux send-keys -t $NAME:3 "apiary-agentmonitor" C-m

    tmux new-window -n honeycomb -t $NAME:4
    tmux send-keys -t $NAME:4 "apiary-honeycomb" C-m

    tmux new-window -n sting -t $NAME:5
    tmux send-keys -t $NAME:5 "apiary-sting" C-m

    tmux select-window -t $NAME:1
  fi

  #tmux attach -t $NAME
fi
