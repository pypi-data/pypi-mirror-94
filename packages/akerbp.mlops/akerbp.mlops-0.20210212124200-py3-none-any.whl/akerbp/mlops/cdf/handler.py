# handler.py
import os
import traceback
from importlib import import_module
import warnings
warnings.simplefilter("ignore")

from akerbp.mlops.core import logger
SERVICE_NAME = os.getenv("SERVICE_NAME")
service = import_module(f"akerbp.mlops.services.{SERVICE_NAME}").service

logging=logger.get_logger()


def handle(data, secrets):
   try:
      return service(data, secrets)
   except Exception:
      trace = traceback.format_exc()
      error_message = f"{SERVICE_NAME} service failed.\n{trace}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
