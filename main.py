import datetime
import time

import mongodb_util as mu

from fastapi import FastAPI

app = FastAPI()
krx = mu.get_mongodb_collection('krx')
krx_storage = mu.get_mongodb_collection('krx_storage')

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
    time.sleep(10)
    return {'msg': 'Hi'}

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

@app.get("/krx/stock/readall/")
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
'''
@app.get("/test/")
async def test(symbol: str, number: str ):
    log_test(f'{symbol} : Before requests to MongoDB server', number)
    res = krx.find_one({'code': symbol})
    log_test(f'{symbol} : After gets response from MongoDB server', number)
    return {'data': res['data']}

@app.get("/krx/stock/read/")
async def krx_read(symbol: str, apikey: str):
    number = apikey
    log_test(f'{symbol} : Before requests to MongoDB server', number)
    res = krx.find_one({'code': symbol})
    log_test(f'{symbol} : After gets response from MongoDB server', number)
    return {'data': res['data']}
'''
