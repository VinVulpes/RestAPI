import random
from typing import List
from urllib import request
import flask, requests, lab2
from flask import jsonify, json, render_template, request
import heapq as hq

app = flask.Flask('__main__')

order = {
    'key001': {
            'order_id': 1,
            'order_name': 'Разработать бд', 
            'start_date': '01-01-2022',
            'tasks':
            [
                    {'name': 'концептуальное моделирование', 'dur': 10, 'resource': 1, 'id': 1},
                    {'name': 'развернуть базу', 'dur': 1, 'resource': 1, 'id': 2, 'pred': [1]},
                    {'name': 'загрузить данные', 'dur': 2, 'resource': 1, 'id': 3, 'pred': [2]},
                    {'name': 'разработать приложение', 'dur': 10, 'resource': 4, 'id': 4, 'pred': [3]}
            ]
},
 'key002': {
            'order_id': 2,
            'order_name': 'Разработать бд', 
            'start_date': '01-01-2022',
            'tasks':
            [
                    {'name': 'концептуальное моделирование', 'dur': 10, 'resource': 1, 'id': 1},
                    {'name': 'развернуть базу', 'dur': 1, 'resource': 1, 'id': 2, 'pred': [1]},
                    {'name': 'загрузить данные', 'dur': 2, 'resource': 1, 'id': 3},
                    {'name': 'разработать приложение', 'dur': 10, 'resource': 5, 'id': 4, 'pred': [2, 3]}
            ]
},
'key003': {
            'order_id': 2,
            'order_name': 'Разработать бд', 
            'start_date': '01-01-2022',
            'tasks':
            [
                    {'name': '0', 'dur': 0, 'resource': 0, 'id': 0},
                    {'name': '1', 'dur': 3, 'resource': 2, 'id': 1, 'pred': [0]},
                    {'name': '2', 'dur': 4, 'resource': 3, 'id': 2, 'pred': [0]},
                    {'name': '3', 'dur': 2, 'resource': 4, 'id': 3, 'pred': [1]},
                    {'name': '4', 'dur': 3, 'resource': 4, 'id': 4, 'pred': [2]},
                    {'name': '5', 'dur': 1, 'resource': 3, 'id': 5, 'pred': [3]},
                    {'name': '6', 'dur': 4, 'resource': 2, 'id': 6, 'pred': [4]},
                    {'name': '7', 'dur': 0, 'resource': 0, 'id': 7, 'pred': [5, 6]}
            ]
}

}


def random_seq(key: str) -> list:
    qu = []
    seq = []
    visited = set()
    tasks = order[key]['tasks']
    for _, task in enumerate(tasks):
        if  'pred' not in task or len(task['pred']) == 0:
            hq.heappush(qu, (random.randint(0, 100000), task)) 
        if 'succ' not in task:
            task['succ'] = []
        if 'pred' in task:
            for pred in task['pred']:
                tasks[pred]['succ'].append(task['id'])

    while qu:
        _, task = hq.heappop(qu)
        seq.append(task)
        visited.add(task['id'])
        for i in task['succ']:
            succ_task = tasks[i]
            if 'pred' not in succ_task  or set(succ_task['pred']) <= visited: 
                hq.heappush(qu, (random.randint(0, 100000), succ_task)) 
    return seq


s = random_seq('key003')
print([task['id'] for task in s])



def plan_duration(order):
    return


@app.get('/api/orders')
def get_orders():
    return jsonify(order), 201

@app.get('/api/orders/<id>')
def get_tasks(id):
    if id not in order:
        return 'заказ не найден', 404
    if 'tasks' not in order[id]:
        return 'заказ пустой', 404
    return jsonify(order[id]['tasks']), 201

@app.delete('/api/orders/delete/<id>')
def delete_task(id):
    if id not in order:
        return 'заказ не найден', 404
    order.pop(id)
    return jsonify({id: 'removed'}), 201

@app.put('/api/orders/tasks/create/<order_id>')
def add_task(order_id):
    task = request.json
    if order_id not in order:
        return 'заказ не найден', 404
    if 'tasks' not in order[order_id]:
        tasks = []
    else:
        tasks = order[order_id]['tasks']
    tasks.append(task)
    order[order_id]['tasks'] = tasks
    return jsonify(order[order_id]), 201


@app.get('/api/orders/calc/<order_id>')
def api_calc_plan3(order_id):
    connected = False
    if order_id not in order:
        return 'заказ не найден', 404
    if 'tasks' not in order[order_id]:
        return {'duration' :0}, 201
    else: 
        r = lab2.Redis(decode_responses=True)
        if r.ping() == True:
            print('connection to redis')
            connected = True
        tasks = order[order_id]['tasks']
        duration = r.get(order_id)
        if duration is None:
            duration =  sum([task['dur'] for task in tasks if 'dur' in task])  # Highload
            r.setex(order_id, 100, duration)
        else:
            print('data retrieved from cache in redis')
        return {'duration': duration}, 201


@app.post('/api/orders/recivefromcalc')
def api_calc_plan():
    tasks = request.json
    duration =  sum([task['dur'] for task in tasks if 'dur' in task])
    return {'duration': duration}, 201


@app.post('/api/orders/sendtocalc/<order_id>')
def api_calc_plan2(order_id):
    if order_id not in order:
        return 'заказ не найден', 404
    if 'tasks' not in order[order_id]:
        return {'duration' :0}, 201
    else: 
        tasks = {'tasks': order[order_id]['tasks'], 'order_id': order_id}
        #result = requests.post('http://localhost:5001/api/orders/recivefromcalc', json=tasks)
        try:
            #r = redis.Redis(decode_responses=True)
            r = lab2.Redis(host='localhost', port=6379) 
            p = r.pubsub()  
            if r.ping() == True:
                r.publish('rating', json.dumps(tasks).encode('utf-8')) 
        except Exception as e:
            print(e)
        return {'status': 'OK'}, 201

@app.get('/content/orders/<id>')
def get_tasks_with_html(id):
    if id not in order:
        return 'заказ не найден'
    if 'tasks' not in order[id]:
        return 'заказ пустой'
    return render_template('tasks.html',  order=order[id]['order_name'], tasks=order[id]['tasks'])


app.run(port=5000)



