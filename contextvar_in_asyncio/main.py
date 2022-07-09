import contextvars

import fastapi
import uvicorn as uvicorn
from fastapi import FastAPI

app = FastAPI()

x = contextvars.ContextVar('x', default='NO_VALUE')

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    app.run(port=8000)
