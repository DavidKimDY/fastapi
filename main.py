from fastapi import FastAPI
import mongodb_util as mu
import json

app = FastAPI()
krx = mu.get_mongodb_collection('krx')
krx_storage = mu.get_mongodb_collection('krx_storage')


@app.get('/')
async def home():
    return {'msg': 'Hi'}


@app.get("/krx/stock/read/")
async def krx_read(symbol: str):
    res = krx.find_one({'code': symbol})
    return {'data': res['data']}


@app.get("/krx/stock/readall/")
async def krx_read_allr(date: str):
    res = krx_storage.find_one({'date': date})
    return {'data': res['data']}


