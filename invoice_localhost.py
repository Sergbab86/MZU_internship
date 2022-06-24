import requests

import mysql.connector
from mysql.connector import errorcode

url = 'https://uabudget.phc.org.ua/api.budget/hs/humanitarian/v1/' \
      'GetInvoices?token=fabf5ed02a2d4426ad49de1f0599582c'

response = requests.get(url)
json_response = response.json()

config = {
    'user': 'root',
    'password': 'Qazx1324!',
    'host': 'localhost',
    'database': 'NZU',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

DB_NAME = 'NZU'
TABLE = {'invoice': (
    "CREATE TABLE `invoice` ("
    "  invoice_num int(14) NOT NULL ,"
    "  invoice_date timestamp ,"
    "  application_id int(14) ,"
    "  act_id int(14) ,"
    "  act_date timestamp ,"
    "   id varchar(250) ,"
    "   region varchar(250) ,"
    "   region_edrpou varchar(250) ,"
    "   item_id int(14) ,"
    "   group_name varchar(250) ,"
    "   name varchar(250) ,"
    "   dosage varchar(250) ,"
    "   release_form varchar(250) ,"
    "   unit varchar(250) ,"
    "   trade_name varchar(250) ,"
    "   multiplicity varchar(250) ,"
    "   distribution int(14) "
    ") ENGINE=InnoDB")}


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLE:
    table_description = TABLE[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

new_list = []
for invoice in json_response:
    list_values = list(invoice.values())
    tuple_values = tuple([i or None for i in list_values])
    new_list.append(tuple_values)

sql = "INSERT INTO invoice " \
      "VALUES (%s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"

cursor.executemany(sql, new_list)

cnx.commit()
cursor.close()
cnx.close()
