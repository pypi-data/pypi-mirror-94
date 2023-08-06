# handler.py
import warnings
warnings.simplefilter("ignore")

from akerbp.mlops.training.service import service
from akerbp.mlops.core import logger

logging=logger.get_logger()


def handle(data, secrets):
   try:
      return service(data, secrets)
   except Exception as error:
      error_type = type(error).__name__
      error_message = f" Training service failed. {error_type}: {error}"
      logging.critical(error_message)
      return dict(status='error', error_message=error_message)
    