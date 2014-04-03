#!/bin/bash
#
# Author - Bradley Jones
#
# generate a file full of random values
# to simulate log data
#

echo "Simulating ecommerce log data"
echo "Ctrl+c to exit"
echo ""

SALES_ITEMS=(
    'orange'
    'apple'
    'banana'
    'mango'
    'pineapple'
    'durian'
    'grapes'
  )

while true
do

  RANDOM_SALE=$[ ($RANDOM % 7) ]
  SALE_MADE=$(date)" SALE MADE: "${SALES_ITEMS[$RANDOM_SALE]}
  APPLE_SALE=$(date)" SALE MADE: "${SALES_ITEMS[1]}

  RANDOM_USER=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
  USER_CONNECTED=$(date)" USER CONNECTED: "$RANDOM_USER
  USER_DISCONNECTED=$(date)" USER DISCONNECTED: "$RANDOM_USER

  RANDOMNUM=$[ ($RANDOM % 10) ]

  if [ $RANDOMNUM -eq "0" ]
  then
    OUTPUT=$USER_CONNECTED
  elif [[ $RANDOMNUM -gt "0" && $RANDOMNUM -lt "6" ]]
  then
    OUTPUT=$SALE_MADE
  elif [[ $RANDOMNUM -gt "6" && $RANDOMNUM -lt "9" ]]
  then
    OUTPUT=$APPLE_SALE
  elif [ $RANDOMNUM -eq "9" ]
  then
    OUTPUT=$USER_DISCONNECTED
  fi

  echo $OUTPUT
  # write to file
  echo $OUTPUT >> /ecommerce.txt

  SLEEP_TIME=$[ ($RANDOM % 4 ) + 1 ]s
  #echo "sleeping for" $SLEEP_TIME
  sleep $SLEEP_TIME
done
