from typing import Optional

from fastapi import FastAPI

import os

app = FastAPI()


@app.get("/")
def read_root():
    version = os.getenv('version', default = 'latest')
    instance_name = os.getenv('instance_name',default= 'OCI CI Host')
    return {"Message": f"With ❤️ from OCI Devops via OCI Container instance,Details Host:{instance_name} Image:{version}"}
