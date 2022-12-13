from app import app, client
import json
import requests
import url_base
#----------------------------------
# Проверка orders post
headers = {
    "Content-type": "application/json",
}
data_mas_orders = [
    {
        "order_id": 7,
        "start_date": "22-02-2014",
        "order_name": "OrderJujuJu",
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
#200 - успех
# Проверка tasks post
headers = {
    "Content-type": "application/json",
}
data_mas_tasks = [
    {
        'task_id': 7,
        'order_name': "order1",
        'task':'задача 77',
        'duration': 23,
        'resource': 99,
        'pred': [0]
    },
    ]
print("Проверка до добавления:")
r=requests.get(url_base.URL_TASKS)
print(r, "\n", r.text)
r=requests.put(url_base.URL_POST_TASKS, headers=headers, data=json.dumps(data_mas_tasks[0]))
print(r, "\n", r.text)
print("Проверка после добавления:")
r=requests.get(url_base.URL_TASKS)
print(r, "\n", r.text)
#200 - успех

