import datetime
import time

import mongodb_util as mu

from fastapi import FastAPI

app = FastAPI()
krx_stock = mu.get_mongodb_collection('krx_stock')
krx_storage = mu.get_mongodb_collection('krx_stock_date')

with open('.apikey', 'r') as f:
    TEMP_API_KEYS = f.read().rstrip('\n').split()

def log(msg):
    time = datetime.datetime.today().isoformat()
    with open('log.txt' , 'a') as f:
        f.write(f'{time} - {msg} \n')

def time_stamp():
    return datetime.datetime.today().isoformat()

@app.get('/')
async def home():
    return {'msg': 'Hi'}

"""
@app.get("/krx/stock/read/")
async def krx_read(symbol: str, apikey: str):
    if apikey not in TEMP_API_KEYS:
        log(f'{apikey} -  Wrong Api key')
        return {'msg' : 'Wrong Api key'}
    res = krx.find_one({'code': symbol})
    if res is None:
        log(f'{apikey} - No data in database. symbol : {symbol}')
        return {'msg': 'No data in database'} 
    log(f'{apikey} - krx_read ok, symbol : {symbol} ')
    return {'data': res['data']}
"""

@app.get("/krx/stock/read/")
def krx_read(symbol: str, start: str, end:str, apikey:str):
    if apikey not in TEMP_API_KEYS:
        log(f'{apikey} -  Wrong Api key')
        return {'msg' : 'Wrong Api key'}
    res = krx_stock.find({'symbol': symbol, 'date' : {'$gte': start, '$lte': end}}, {'_id':0})
    if res is None:
        log(f'{apikey} - No data in database. symbol : {symbol}, start : {start}, end : {end}')
        return {'msg': 'No data in database'}
    log(f'{apikey} - krx_read ok, symbol : {symbol}, start : {start}, end : {end}')
    return {'data': list(res)}


@app.get("/krx/stock/read-date/")
async def krx_read_date(date: str, apikey: str):
    if apikey not in TEMP_API_KEYS:
        log(f'{apikey} - wrong Api key')
        return {'msg' : 'Wrong Api key'}
    res = krx_storage.find_one({'date': date})
    if res is None:
        log(f'{apikey} - No data in database. date : {date}')
        return {'msg': 'No data in database'} 
    log(f'{apikey} - krx_read_date ok, date : {date}')
    return {'data': res['data']}


def log_test(msg, n):
    with open(f'test_log1/log_{n}.txt', 'a') as f:
        f.write(msg + '\n')
