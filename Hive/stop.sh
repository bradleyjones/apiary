#!/bin/bash

if [ -z "$MULTIPLEXER" ]; then
  MULTIPLEXER="TMUX" #SCREEN   Or  TMUX
fi

if [ $MULTIPLEXER == SCREEN ]; then
  SCREEN_NAME=${SCREEN_NAME:-hive}

  screen -S $SCREEN_NAME -X quit

elif [ $MULTIPLEXER == TMUX ]; then
  NAME=Hive

  tmux kill-session -t $NAME
fi
