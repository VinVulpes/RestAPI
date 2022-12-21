#Лаба 2##################################################

from flask import Flask, jsonify, request
import json
import lab2
# from db import connect_db_pg
import db
import redis
app = Flask(__name__)

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
    with db.connect_db_pg() as connection:
        app.run(port=5001,debug=True)