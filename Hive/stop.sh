#!/bin/bash

SCREEN_NAME=${SCREEN_NAME:-hive}

screen -S $SCREEN_NAME -X quit
