from tokenize import group
from kafka import KafkaProducer
import json
from json import dumps
from lab2 import api_calc_plan3
import time

def get_partition(key, all, available):
    return 0

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))                        

if __name__ == "__main__":
    while True:
        calc_orders = api_calc_plan3(1)
    #     all_orders = [{
    #     "order_name": 'order1',
    #     'start_date': '01-01-2022'
    # },
    # {
    #     "order_name": 'order2',
    #     'start_date': '02-01-2022'
    # }]
        print(all_orders)
        producer.send("app_redis", calc_orders)
        time.sleep(4)