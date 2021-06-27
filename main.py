from fastapi import FastAPI
import mongodb_util as mu
import json

app = FastAPI()
krx = mu.get_mongodb_collection('krx')

def stock(symbol):
    res = krx.find_one({'code':symbol})
    with open(f'{symbol}.txt', 'w') as f:
        f.write(str(res['_id']))
    return  res['data'][0]

@app.get("/stock/")
async def get_stock(symbol: str):
    return stock(symbol)

