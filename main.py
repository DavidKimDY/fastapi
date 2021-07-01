import time

import mongodb_util as mu

from fastapi import FastAPI

app = FastAPI()
krx = mu.get_mongodb_collection('krx')
krx_storage = mu.get_mongodb_collection('krx_storage')

with open('.apikey', 'r') as f:
    TEMP_API_KEY = f.read().rstrip('\n')


@app.get('/')
async def home():
    return {'msg': 'Hi'}


@app.get("/krx/stock/read/")
async def krx_read(symbol: str, apikey: str):
    now = time.time()
    print('krx_read_start =', now)
    if apikey != TEMP_API_KEY:
        return {'msg' : 'Wrong Api key'}
    print('before_mdb_requests = ', now)
    res = krx.find_one({'code': symbol})
    print('after_mdb_requests = ', time.time())
    if res is None:
        return {'msg': 'No data in database'} 
    return {'data': res['data']}


@app.get("/krx/stock/readall/")
async def krx_read_allr(date: str, apikey: str):
    if apikey != TEMP_API_KEY:
        return {'msg' : 'Wrong Api key'}
    res = krx_storage.find_one({'date': date})
    if res is None:
        return {'msg': 'No data in database'} 
    return {'data': res['data']}


