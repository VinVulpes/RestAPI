'''
Testing DELETE
'''
# from app import app, client
import json
import requests
import url_base
#----------------------------------
# Проверка delete
headers = {
    "Content-type": "application/json",
}
data_mas_orders = [
    {},
    ]
print("Проверка до удаления:")
r=requests.get(url_base.URL_ORDERS)
print(r, "\n", r.text)
r=requests.delete(url_base.URL_POST_ORDER+'/1', headers=headers, data=json.dumps(data_mas_orders[0]))
print(r, "\n", r.text)
print("Проверка после удаления:")
r=requests.get(url_base.URL_ORDERS)
print(r, "\n", r.text)
