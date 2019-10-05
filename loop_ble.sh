#!/bin/sh
# BLE V2/loop around the script _ sleep if bug

cd /root/ble

LOG=/root/ble/loop.log
echo "START: $(date +'%Y-%m-%d %H:%M:%S')" >> $LOG

while  [ ! -f stop ]
do
    echo "LOOP: $(date +'%Y-%m-%d %H:%M:%S')" >> $LOG
    sudo python3 ./ble.py
    sleep 10
done
