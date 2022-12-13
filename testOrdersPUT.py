'''
Testing PUT
'''
# from app import app, client
import json
import requests
import url_base
#----------------------------------
# Проверка put
headers = {
    "Content-type": "application/json",
}
data_mas_orders = [
    {
        "order_id": 1,
        "start_date": "22-02-2004",
        "order_name": "OrderA",
    },
    ]
print("Проверка до добавления:")
r=requests.get(url_base.URL_ORDERS)
print(r, "\n", r.text)
r=requests.put(url_base.URL_POST_ORDER, headers=headers, data=json.dumps(data_mas_orders[0]))
print(r, "\n", r.text)
print("Проверка после добавления:")
r=requests.get(url_base.URL_ORDERS)
print(r, "\n", r.text)

#посмотреть результат res.get_json()
