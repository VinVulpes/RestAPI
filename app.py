
from flask import Flask, jsonify, request
import json
import redis
# from db import connect_db_pg
import db
app = Flask(__name__)

#клиент (для теста)
client = app.test_client()

# http://127.0.0.1:5000/orders
# [[1,"order1","Fri, 31 Dec 1999 21:00:00 GMT"]]
'''

1) Создать задачу {order_name: "изготовить изделие", start_date: "01-01-2022"}, изменить, удалить

2) К задаче добавить работу {task: "задача 1", duration: 2, resource: 10}, удалить работу

3) К работе добавить массив предшествующих работ {pred: [1, 2, 3]}

'''

orders = [
    {
        "order_name": 'order1',
        'start_date': '01-01-2022'
    },
    {
        "order_name": 'order2',
        'start_date': '02-01-2022'
    }

]
tasks = [
    {
        'task_id': 1,
        'order_name': "order1",
        'task':'задача 1',
        'duration': 2,
        'resource': 10,
        'pred': []
    },
    {
        'task_id': 2,
        'order_name': "order1",
        'task':'задача 2',
        'duration': 5,
        'resource': 8,
        'pred': [1]
    },
    {
        'task_id': 3,
        'order_name': "order2",
        'task':'задача 3',
        'duration': 3,
        'resource': 15,
        'pred': []
    },
    # [[1,"order1","Fri, 31 Dec 1999 21:00:00 GMT"]]

]

#route обрабатывает запросы клиента к серверу
#сначала обработчик гет запросов
@app.route('/', methods=['GET'])
def start():
    a = '<h1>Hello Everyone!</h1><p> / orders - get all orders</p><h2>Laboratory Work 1</h2><p> / tasks - get all tasks</p><p>Set id after words and you get one personal line from Data Base</p><h2>Laboratory Work 2</h2><p>Redis - sum duration /orders/calc/<id></p>'
    return(a)
@app.route('/orders', methods=['GET'])
def get_list():
    db.cur.execute('''SELECT * FROM orders;''')
    arr_db = db.cur.fetchall()
    result_list=[]
    for curr_str in arr_db:
        result_list.append(
            {
                'order_id'  :curr_str[0],
                'order_name':curr_str[1],
                'start_date':curr_str[2]
            }
            )
    return jsonify(result_list)
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_list_id(order_id):
    db.cur.execute("SELECT * FROM orders WHERE id = %s;",(str(int(order_id)),))
    arr_db = db.cur.fetchall()
    result_list=[]
    for curr_str in arr_db:
        result_list.append(
            {
                'order_id'  :curr_str[0],
                'order_name':curr_str[1],
                'start_date':curr_str[2]
            }
            )
    return jsonify(result_list)
#список туториалов обновляется на сервере
#в него будет добавляться новый элемент
#по request получаем, когда отправляем от клиента к серверу

@app.route('/orders', methods=['POST'])
def post_list():
    data = json.loads(request.data)
    print(data)
    db.cur.execute("insert into orders (order_name, start_date) values \
    (%s, %s)", (data['order_name'], data['start_date']))
    db.con.commit()
    #получим данные с сервера
    # new_one = request.json
    # orders.append(new_one)
    # return jsonify(orders)
    return "done: post", 204

#добавить элементы в список
#нужен id
@app.route('/orders', methods=['PUT'])
def update_list():
    '''
    Updates order (by put)
    '''

    #получим тело запроса
    data = request.json #application/json
    # data = json.loads(request.data)#p
    print(data)
    #db.cur.execute(f"update orders SET order_name=\'{data['order_name']}\', \
    #    start_date=\'{data['start_date']}\' WHERE id=\'{data['order_id']}\'")
    if data.get("order_id"):
        db.cur.execute("INSERT INTO orders (id, order_name, start_date) VALUES \
            (%s,%s,%s) ON CONFLICT (id) DO UPDATE SET order_name=%s, start_date=%s",
            (data['order_id'],data['order_name'],data['start_date'],
            data['order_name'],data['start_date']))
    else:
        db.cur.execute(f"INSERT INTO orders (order_name, start_date) VALUES \
            (\'{data['order_name']}\', \'{data['start_date']}\') ON CONFLICT (id) DO UPDATE \
            SET order_name=\'{data['order_name']}\', \
            start_date=\'{data['start_date']}\'")
    db.con.commit()
    return "done: put", 200


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_list(order_id):
    # r=requests.put(lc/orders/1, headers=headers, data=json.dumps(data_mas_orders[0]))
    # http://localhost:5000/orders/1
    '''
        {
        "order_id": 10,
        "start_date": "22-02-2006",
        "order_name": "OrderA",
        }
    '''
    db.cur.execute("DELETE FROM orders WHERE id = %s;",(str(int(order_id)),))
    db.con.commit()
    row = db.cur.rowcount
    return jsonify({"deleted":row}), 200


#route обрабатывает запросы клиента к серверу
#сначала обработчик get запросов
@app.route('/tasks', methods=['GET'])
def get_list_tasks():
    db.cur.execute('''SELECT * FROM tasks;''')
    arr_db = db.cur.fetchall()
    result_list=[]
    for curr_str in arr_db:
        result_list.append(
            {
                'task_id': curr_str[0],
                'order_id': curr_str[1],
                'duration': curr_str[2],
                'resource': curr_str[3],
                'pred': curr_str[4]
            }
            )
    print(result_list)
    print(jsonify(result_list).json)
    return print(result_list)
#список туториалов обновляется на сервере
#в него будет добавляться новый элемент
#по request получаем, когда отправляем от клиента к серверу

@app.route('/tasks', methods=['POST'])
def post_list_tasks():
    #получим данные с сервера
    data = json.loads(request.data)
    print(data)
    db.cur.execute("insert into tasks (id,order_id, task_name, duration,resource,pred) values \
        (%s, %s, %s, %s, %s, %s)",(data['id'], data['order_id'], data['task_name'], 
        data['duration'], data['resource'], data['pred']))
    return "done: post", 200

#добавить элементы в список
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_list_tasks(task_id):
    data = request.json 
    print(data)
    if data.get("id"):
        db.cur.execute("INSERT INTO tasks(id, order_id, duration, resource, pred) VALUES \
            (%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET order_id=%s, duration=%s, resource=%s, pred=%s",
            (data['id'],data['order_id'],data['duration'],
            data['resource'],data['pred'],data['order_id'],data['duration'],
            data['resource'],data['pred']))
    else:
        db.cur.execute("INSERT INTO tasks(order_id, duration, resource, pred) VALUES \
            (%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE \
            SET order_id=%s, duration=%s, resource=%s, pred=%s",
            (data['order_id'],data['duration'],data['resource'],data['pred'],
            data['order_id'],data['duration'],data['resource'],data['pred']))
    db.con.commit()
    return "done: put", 200

@app.route('/tasks/<int:tasks_id>', methods=['GET'])
def get_id_task(tasks_id):
    db.cur.execute("SELECT * FROM orders WHERE id = %s;",(str(int(tasks_id)),))
    arr_db = db.cur.fetchall()
    result_list=[]
    for curr_str in arr_db:
        result_list.append(
            {
                'task_id': curr_str[0],
                'order_id': curr_str[1],
                'duration': curr_str[2],
                'resource': curr_str[3],
                'pred': curr_str[4]
            }
            )
    return jsonify(result_list)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_list_tasks(task_id):
    db.cur.execute(f"DELETE from tasks where id = \'{task_id}\'")
    db.con.commit()
    
    # # arr_db = db.cur.fetchall()
    # idx, _ = next((i for i in enumerate(orders) if i[1]['id'] == task_id), (None, None))
    # tasks.pop(idx)
    return "done: delete",200

    #Лаба 2##################################################
    
@app.get('/orders/calc/<order_id>')
def api_calc_plan3(order_id):
    connected = False
    db.cur.execute('''SELECT duration FROM tasks WHERE order_id = %s''',(str(int(order_id)),))
    dur_from_db = db.cur.fetchall()
    if dur_from_db is None: # тут надо проверить что возвращает если запрос ничего не нашел
        return 'заказ не найден', 404 # или у него нет работ
    else: 
        r = redis.Redis(decode_responses=True)
        if r.ping() == True:
            print('connection to redis')
            connected = True
        duration = r.get(order_id) #смотрит вносили мы в редис данные по duration
        if duration is None:
            duration =  sum(dur[0] for dur in dur_from_db)  # Highload
            r.setex(order_id, 100, duration)
        else:
            print('data retrieved from cache in redis')
        return {'duration': duration}, 201
            


if __name__ == '__main__':# this is main!
    db.connect_db_pg()
    with db.connect_db_pg() as connection: #это вообще работает?
        app.run(debug=True)
# проверить фунции get,put,post,delete