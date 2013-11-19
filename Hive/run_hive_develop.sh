#!/bin/bash
screen -d -m bash -c "apiary-honeycomb"
screen -d -m bash -c "apiary-honeycomb-statemachine"
screen -d -m bash -c "apiary-control"
screen -d -m bash -c "apiary-control-statemachine"
