'''
Позволяет посылать запросы get и post на сервер
'''
## TODO: добавить полный список всех API и упорядочить 
import json
import time
import requests

PORT = 5000
BASE_URL = 'http://localhost:'+str(PORT)

'''
URL_TASKS = base_url + '/tasks'
URL_TASK_ORDER = base_url + '/tasks/'+'OrderB'
URL_ORDERS = base_url + '/orders'
URL_DURATION = base_url + '/duration/'+'OrderB'
'''

URL_TASKS = BASE_URL + '/tasks'
URL_TASK_ORDER = BASE_URL + '/orders/'+'1'
URL_ORDERS = BASE_URL + '/orders'
URL_DURATION = BASE_URL + '/duration/'+'1'
'''
URL_ORDERS = BASE_URL + '/orders'
URL_TASK_ORDER = BASE_URL + '/orders/'+'OrderB'
URL_ORDERS = BASE_URL + '/orders'
URL_DURATION = BASE_URL + '/duration/'+'OrderB'
'''

headers = {
    "Content-type": "application/json",
}
print("Тестирование:", "\nСоздание (обновление) \
    Order (если он уже есть в БД будет выдана ошибка, т.к. его нельзя удалить):")

data_mas = [
    {
        "task_id": 1,
        "task": "task1",
        "order_name": "OrderA",
        "duration": 1,
        "resource": 5,
        "pred": []
    },
    {
        "task_id": 3,
        "task": "task2",
        "order_name": "OrderA",
        "duration": 1,
        "resource": 5,
        "pred": []
    },
    {
        "task_id": 4,
        "task": "task3",
        "order_name": "OrderA",
        "duration": 5,
        "resource": 3,
        "pred": [1]
    },
]
for data in data_mas:
    # print(json.dumps(data))
    # r = requests.put(URL_TASKS, headers=headers, data=json.dumps(data))
    r = requests.post(URL_TASKS, headers=headers, data=json.dumps(data))
    print(r, "\n", r.text)

print("Проверка добавления:")
r=requests.get(URL_ORDERS)
print(r, "\n", r.text)

# r3=requests.get(URL_TASK_ORDER)

'''
print("Тестирование:", "\nСоздание (обновление) Order (если он уже есть в БД будет выдана ошибка, т.к. его нельзя удалить):")
# Создание (обновление) Order
data = {"order_name": "OrderA", "start_date":"2020-11-23"}
print("PUT:\n",json.dumps(data))
# r = requests.put(URL_ORDERS, headers=headers, data=json.dumps(data))
r = requests.post(URL_ORDERS, headers=headers, data=json.dumps(data))
print(r, "\n", r.text)
data = {"order_name": "OrderB", "start_date":"2020-11-23"}
print("PUT:\n",json.dumps(data))
r = requests.post(URL_ORDERS, headers=headers, data=json.dumps(data))
# r = requests.put(URL_ORDERS, headers=headers, data=json.dumps(data))
print(r, "\n" , r.text, "Создание (обновление) OrderC (для удаления)")
# Создание (обновление) Order (для удаления)
data = {"order_name": "OrderC", "start_date":"2020-11-23"}
print(json.dumps(data))
r = requests.post(URL_ORDERS, headers=headers, data=json.dumps(data))
# r = requests.put(URL_ORDERS, headers=headers, data=json.dumps(data))
print(r, "\n", r.text)
# Удаление Order
print("Удаление OrderC")
data = {"order_name": "OrderC"}
print(json.dumps(data))
r = requests.delete(URL_ORDERS, headers=headers, data=json.dumps(data))

print(r, "Добавление (обновление) списка tasks для расчетов:")
# {Order_name: "Order1", Start_date: "2020-10-22"}
# data = {"order_name": "Order4", "start_date":"2020-11-23"}
data = {"task": "3", "order_name": "OrderA", "duration": 4, "resource": 3, "pred": ["1"]}
print(json.dumps(data))
# r = requests.put(URL_TASKS, headers=headers, data=json.dumps(data))
r = requests.post(URL_TASKS, headers=headers, data=json.dumps(data))
# r2 = requests.post(URL1, headers=headers, data=json.dumps(data))
print(r, "\n", r.text)
#test1
# data = {"task": "3", "order_name": "OrderA", "duration": 4, "resource": 3, "pred": '["1"]'}

data_mas = [
    {"task": "1", "order_name": "OrderA", "duration": 1, "resource": 5, "pred": '[]'},
    {"task": "2", "order_name": "OrderA", "duration": 1, "resource": 5, "pred": '["1"]'},
    {"task": "1", "order_name": "OrderB", "duration": 1, "resource": 5, "pred": '[]'},
    {"task": "2", "order_name": "OrderB", "duration": 3, "resource": 6, "pred": '[]'},
    {"task": "3", "order_name": "OrderB", "duration": 3, "resource": 4, "pred": '["1"]'},
    {"task": "4", "order_name": "OrderB", "duration": 2, "resource": 3, "pred": '["1", "2"]'},
    {"task": "5", "order_name": "OrderB", "duration": 10,"resource": 7, "pred": '["3"]'}
]

for data in data_mas:
    # print(json.dumps(data))
    # r = requests.put(URL_TASKS, headers=headers, data=json.dumps(data))
    r = requests.post(URL_TASKS, headers=headers, data=json.dumps(data))
    print(r, "\n", r.text)

print("Проверка добавления:")
r3=requests.get(URL_TASK_ORDER)
print(r3, "\n", r3.text, "\n" , "Запрос duration")

start_time = time.time()

# Запрос duration
r = requests.get(URL_DURATION)
print(r, "\n", r.text, "\n", "%s seconds" % (time.time() - start_time))

# Запрос duration повторный
print("Повторный")
start_time = time.time()
r = requests.get(URL_DURATION)
print(r, "\n", r.text, "\n", "%s seconds" % (time.time() - start_time), "\n", "Добавление нового элемента:")
data = {"task": "6", "order_name": "OrderB", "duration": 4, "resource": 10, "pred": '["1"]'}
r = requests.put(URL_TASKS, headers=headers, data=json.dumps(data))
print(r, "\n", r.text, "\n", "Повторный с добавлением")

start_time = time.time()

# Запрос duration повторный2
r = requests.get(URL_DURATION)
print(r, "\n", r.text, "\n", "Повторный2 с добавлением")
start_time = time.time()

# Запрос duration повторный2
r = requests.get(URL_DURATION)
print(r, "\n", r.text, "\n", "%s seconds" % (time.time() - start_time))

# Удаление Task
data = {"order_name": "OrderB", "task": "6"}
print(json.dumps(data))
r = requests.delete(URL_TASKS, headers=headers, data=json.dumps(data))
input("Press any button to exit")
'''