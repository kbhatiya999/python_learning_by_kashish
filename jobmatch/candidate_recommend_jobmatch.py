import json

import uvicorn as uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

# @app.post('/send')
async def test(request: Request):
    json_ = await request.json()
    json_indented = json.dumps(json_, indent=2)
    print(json_indented)
    return json.loads(json_indented)

@app.get('/send')
async def test2(request: Request):
    # json_ = await request.json()
    # json_indented = json.dumps(json_, indent=2)
    params = dict(request.query_params)
    print(params)
    return {"message": "Thank You"}

async def dummy():
    return Requirement

if __name__ == "__main__":
    uvicorn.run(app, host="5.161.95.212", port=9000)