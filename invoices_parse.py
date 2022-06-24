import requests
import json
import time
import pymysql
import json

import schedule

url = 'https://uabudget.phc.org.ua/api.budget/hs/humanitarian/v1/' \
      'GetInvoices?token=fabf5ed02a2d4426ad49de1f0599582c'

response = requests.get(url)
json_response = response.json()

list_invoice = []
for invoice in json_response:
    list_values = [i or None for i in list(invoice.values())]
    # tuple_values = tuple([i or None for i in list_values])
    # list_invoice.append(tuple_values[0:2])
    print(list_values)
# print(list_invoice)


# while True:
#
#     with open('invoice.json', 'w', encoding='utf-8') as f:
#         json.dump(response.json(), f, ensure_ascii=False, indent=4)
#     time.sleep(60)


# def write_file():
#     with open('invoice.json', 'w', encoding='utf-8') as f:
#         json.dump(response.json(), f, ensure_ascii=False, indent=4)
#
#
# schedule.every(1).minutes.do(write_file())
#
while True:
    schedule.run_pending()
    time.sleep(1)
