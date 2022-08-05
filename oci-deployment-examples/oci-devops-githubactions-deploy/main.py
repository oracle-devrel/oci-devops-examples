from typing import Optional

from fastapi import FastAPI

import os

app = FastAPI()


@app.get("/")
def read_root():
    version = os.getenv('image_url', default = '0.0.0')
    return {"Message": "With ❤️ from OCI DevOps via GitHub Actions","Version":version}
