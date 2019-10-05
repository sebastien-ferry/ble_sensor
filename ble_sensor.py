#!/usr/bin/python
# BLE V2: Collect of BLE

import db

import os.path
import time

from bluepy.btle import Scanner

if __name__ == '__main__':
    scanner = Scanner()
    while not os.path.exists('stop'):
        time.sleep(1)
        devices=scanner.scan(5)

        ts = int(time.time())
        db_connection, db_cursor = db.db_connect()
        for dev in devices:
            db.db_insert_device(db_cursor, dev.addr, dev.addrType,dev.rssi, ts)
            for (adtype, name, value) in dev.getScanData():
                db.db_insert_scan_data(db_cursor, dev.addr, dev.addrType, adtype, name, value, ts)
        db.db_close(db_connection, db_cursor)
