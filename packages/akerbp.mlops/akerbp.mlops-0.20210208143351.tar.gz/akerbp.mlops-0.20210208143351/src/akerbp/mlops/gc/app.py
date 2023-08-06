"""
app.py

Web service (training or prediction).

Requires SERVICE_NAME env variable to be set.
"""

import os 
from importlib import import_module

from fastapi import FastAPI
from pydantic import Json, BaseModel

from akerbp.mlops.gc.helpers import access_secret_version
from akerbp.mlops.core import logger
SERVICE_NAME = os.getenv("SERVICE_NAME")
service = import_module(f"akerbp.mlops.{SERVICE_NAME}.service").service

logging=logger.get_logger()


secrets_string = access_secret_version('mlops-cdf-keys') 
secrets = eval(secrets_string)


app = FastAPI()

class Data(BaseModel):
    data: Json

@app.post(f"/{SERVICE_NAME}")
def api(input: Data):
    data = input.data
    logging.debug(f"{data=}")
    try:
        return service(data, secrets)
    except Exception as error:
      error_type = type(error).__name__
      service_name = SERVICE_NAME.capitalize()
      error_message = f"{service_name} service failed. {error_type}: {error}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
