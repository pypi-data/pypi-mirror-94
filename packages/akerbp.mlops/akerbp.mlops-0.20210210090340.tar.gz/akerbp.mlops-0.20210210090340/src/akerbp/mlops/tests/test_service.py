"""
test_service.py

Generic test for services (training or prediction)
"""
import os
from importlib import import_module

SERVICE_NAME = os.environ['SERVICE_NAME']
service = import_module(f"akerbp.mlops.{SERVICE_NAME}.service").service

from service_settings import mlops_settings #generated during deployment

model_code_folder = mlops_settings["model_code_folder"]
test_import_path = mlops_settings["test_import_path"]
ServiceTest=import_module(test_import_path).ServiceTest

api_keys = dict(
   data = os.environ['COGNITE_API_KEY_DATA'],
   files = os.environ['COGNITE_API_KEY_FILES']
)

def mock_saver(api_key_files, path, metadata):
    pass


def test_service():
   
   service_test = ServiceTest()
   input = getattr(service_test, f"{SERVICE_NAME}_input")
   check = getattr(service_test, f"{SERVICE_NAME}_check")

   
   if SERVICE_NAME == 'training':
      response = service(data=input, secrets=api_keys, saver=mock_saver)
   elif SERVICE_NAME == 'prediction':
      response = service(data=input, secrets=api_keys)
   else:
      raise Exception("Unknown service name")
   
   assert response['status'] == 'ok'
   assert check(response[SERVICE_NAME])
   