"""
service.py

Training service
"""

from tempfile import TemporaryDirectory
from importlib import import_module

from service_settings import mlops_settings

model_module = import_module(mlops_settings["model_import_path"])
train = model_module.train
ModelException = model_module.ModelException

import akerbp.mlops.cdf.helpers as helpers
from akerbp.mlops import __version__ as version
from akerbp.mlops.core import logger 

logging=logger.get_logger()

logging.debug(f"MLOps framework version {version}")


def _saver(api_keys, path, metadata):
    """
    Upload model folder to CDF Files
    """
    model_name = mlops_settings['model_name']
    env = mlops_settings['env']
    helpers.api_keys=api_keys
    helpers.set_up_cdf_client()
    model_info = helpers.upload_new_model_version(
        model_name, 
        env,  
        path,
        metadata
    )
    return model_info


def service(data, secrets, saver=_saver):
    """
    Training service
    Inputs:
        - data: dictionary, data passed by the user through the API
        - secrets: dictionary with api keys
        - saver: an object that saves the model folder

    Output:
        - Dictionary with status 'ok' or 'error' as keys.
            status == 'ok'    -> there is a 'training' key as well  
                                (data on the model file)
            status == 'error' -> there is a 'message' key as well
    """
    try:
        with TemporaryDirectory() as temp_dir:
            metadata = train(data=data, folder_path=temp_dir, secrets=secrets)
            logging.debug(f"{metadata=}")
            model_info = saver(secrets, temp_dir, metadata)
        return dict(status="ok", training=model_info)
    except ModelException as e:
        error_message = f"Training failed. Message: {e}"
        logging.error(error_message)
        return dict(status='error', message=error_message)
        
        
    
