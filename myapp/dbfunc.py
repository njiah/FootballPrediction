#Callum Stevens - 21032708

import mysql.connector, dbfunc, sys
from sqlalchemy import null
from mysql.connector import errorcode

#MYSQL CONFIG SETTINGS
hostname = "localhost"
username = "root"
passwd = "BaconLettuceTomato"

def getConnection():
    conn = null
    try:
        conn = mysql.connector.connect(host=hostname,
                    user=username, 
                    password=passwd,
                    database = 'horizon_hotels',
                    auth_plugin='mysql_native_password')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally: #will execute if there is no exception raised in try block
        return conn