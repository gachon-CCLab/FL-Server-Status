from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
import json, logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)8.8s] %(message)s",
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

#버킷과 파일 이름은 여기서 결정된다. 다른 곳에서는 이 값을 받아와 사용
#
class ServerStatus(BaseModel):

    S3_bucket: str = 'fl-gl-model'
    Latest_GL_Model: str = '' # 모델 가중치 파일 이름
    Play_datetime: str = ''
    FLSeReady: bool = False
    GL_Model_V: int = 0 #모델버전
    client_list: list = []


app = FastAPI()

FLSe = ServerStatus()

@app.get("/FLSe/info")
def read_status():
    global FLSe

    server_status_result = {"S3_bucket": FLSe.S3_bucket, "Latest_GL_Model": FLSe.Latest_GL_Model, "Play_datetime": FLSe.Play_datetime,
                            "FLSeReady": FLSe.FLSeReady, "GL_Model_V": FLSe.GL_Model_V, "client_list": FLSe.client_list}
    json_server_status_result = json.dumps(server_status_result)
    logging.info(f'server_status - {json_server_status_result}')
    # print(FLSe)
    return {"Server_Status": FLSe}


@app.put("FLSe/register_client")
def register_client(client_name: str):
    global FLSe
    if client_name in FLSe.client_list:
        client_num = FLSe.client_list.index(client_name)
    else: 
        FLSe.client_list.append(client_name)
        client_num = FLSe.client_list.index(client_name)

    return {'client_num':client_num}


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


@app.put("/FLSe/FLSeClosed")
def server_closed(FLSeReady: bool):
    global FLSe
    print('server closed')
    FLSe.FLSeReady = FLSeReady
    return {"Server_Status": FLSe}



if __name__ == "__main__":    

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
