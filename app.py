from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
import requests, asyncio, logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)8.8s] %(message)s",
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

#버킷과 파일 이름은 여기서 결정된다. 다른 곳에서는 이 값을 받아와 사용
#
class ServerStatus(BaseModel):

    S3_bucket: str = 'fl-gl-model'
    S3_key: str = '' # 모델 가중치 파일 이름
    play_datetime: str = ''
    FLSeReady: bool = False
    GL_Model_V: int = 0 #모델버전 


app = FastAPI()

FLSe = ServerStatus()

@app.get("/FLSe/info")
def read_status():
    global FLSe

    # asyncio.run(fl_server_check()) # fl-server 동작 check

    logging.info(f'Server_status: {FLSe}')
    return {"Server_Status": FLSe}


@app.put("/FLSe/FLSeUpdate")
def update_status(Se: ServerStatus):
    global FLSe
    FLSe = Se
    return {"Server_Status": FLSe}

@app.put("/FLSe/FLRoundFin")
def update_ready(FLSeReady: bool):
    global FLSe
    FLSe.FLSeReady = FLSeReady
    if FLSeReady==False:
        FLSe.GL_Model_V += 1
    return {"Server_Status": FLSe}

if __name__ == "__main__":    

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
