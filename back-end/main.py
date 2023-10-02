from fastapi import FastAPI
import requests, time

app = FastAPI()

@app.get("/")
def init():
    ts = round(time.time() * 1000)
    url = 'https://zaisen.tid-keisei.jp/kr/data/traffic_info.json?ts=' + str(ts)
    response = requests.get(url)
    return response.json()
init()