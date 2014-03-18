#!/bin/bash
# generate a file full of random values
# to simulate log data
#

echo "Simulating random log data"
echo "Ctrl+c to exit"
echo ""

while true
do
  RANDOM_STRING=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

  echo $(date) $RANDOM_STRING
  # write to file
  echo $(date) $RANDOM_STRING >> /test.txt

  SLEEP_TIME=$[ ($RANDOM % 6 ) + 1 ]s
  echo "sleeping for" $SLEEP_TIME
  sleep $SLEEP_TIME
done
