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
data_mas_tasks = [
    {},
    ]
print("Проверка до удаления:")
r=requests.get(url_base.URL_TASKS)
print(r, "\n", r.text)
r=requests.delete(url_base.URL_TASK+'/1', headers=headers, data=json.dumps(data_mas_tasks[0]))
print(r, "\n", r.text)
print("Проверка после удаления:")
r=requests.get(url_base.URL_TASKS)
print(r, "\n", r.text)