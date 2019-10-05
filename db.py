# db/insert
# BLE V2/db.py: insert BLE data into database + file

import db_password
import time
import psycopg2

def db_connect():
    db_connection = None
    db_cursor = None
    try:
        db_connection = psycopg2.connect( user = db_password.user
                                     , password = db_password.password
                                     , host = db_password.host
                                     , port = db_password.port
                                     , database = db_password.database)
        db_cursor = db_connection.cursor()

    except (Exception, psycopg2.Error) as error :
        print ("ERROR PsycoPG2 (db_connect) : ", error)
        return None, None

    return db_connection, db_cursor

def db_close(db_connection, db_cursor):
    try:
        if (db_cursor):
            db_cursor.close()

        if (db_connection):
            db_connection.close()

    except (Exception, psycopg2.Error) as error :
        print ("ERRO PsycoPG2 (db_close): ", error)

    return

def db_insert_device(db_cursor, p_address, p_address_type, p_rssi, p_timestamp):
    global db_connection, db_cursor
    try:
        sql_s = """select *
                 from device
                 where address=%s
                 and   address_type=%s ;"""
        db_cursor.execute(sql_s, (p_address,p_address_type))
        device = db_cursor.fetchone()
        if device is None:
            sql_id = ''' INSERT INTO device
                      (address, address_type, firstseen, lastseen)
                      VALUES (%s,%s,to_timestamp(%s),to_timestamp(%s)) ;'''
            db_cursor.execute(sql_id, (p_address, p_address_type, p_timestamp, p_timestamp) )
        else:
            sql_ud = ''' UPDATE device
                      SET lastseen=to_timestamp(%s)
                      WHERE address=%s
                      and   address_type=%s ;'''
            db_cursor.execute(sql_ud, (p_timestamp, p_address, p_address_type) )
        db_connection.commit()

        sql_is = ''' INSERT INTO scan
                  (address, address_type, timestamp, rssi)
                  VALUES(%s, %s, to_timestamp(%s), %s)
                  ON CONFLICT (address, address_type, timestamp) DO NOTHING; '''
        db_cursor.execute(sql_is, (p_address, p_address_type, p_timestamp, p_rssi))
        db_connection.commit()

    except: # psycopg2.Error as error:
        with open("degraded.log", "a") as file:
            ts = int(time.time())
            file.write("\ndb_insert_device: %d, %s, %s, %d, %d" % (ts, p_address, p_address_type, p_rssi, p_timestamp))
    return

def db_insert_scan_data(db_cursor, p_address, p_address_type, p_advertising_data_type, p_name, p_value, p_timestamp):
    global db_connection, db_cursor
    try:
        sql = """select *
                 from  scan_data
                 where address=%s
                 and   address_type=%s
                 and   name=%s
                 and   value=%s ;"""
        db_cursor.execute(sql, (p_address,p_address_type, p_name, p_value))
        scan_data = db_cursor.fetchone()
        if scan_data is None:
            sql = ''' INSERT INTO scan_data
                      (address, address_type, name, value, timestamp)
                      VALUES (%s,%s,%s,%s,to_timestamp(%s)) ;'''
            db_cursor.execute(sql, (p_address, p_address_type, p_name, p_value, p_timestamp) )
            db_connection.commit()
    except: # psycopg2.Error as error:
        with open("degraded.log", "a") as file:
            ts = int(time.time())
            file.write( "\ndb_insert_scan_data: %d, %s, %s, %s, %s, %s, %d" % (ts, p_address, p_address_type, p_advertising_data_type, p_name, p_value, p_timestamp))
    return
