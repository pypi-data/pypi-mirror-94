"""
deploy.py

Deploy services in either Google Cloud Run or CDF Functions. 
Model registry uses CDF Files.
""" 
import os
import traceback

import shutil
import subprocess
from functools import partial
from importlib import import_module

from akerbp.mlops.deployment import helpers
from akerbp.mlops.core import logger
from akerbp.mlops.model_manager import set_up_model_artifact

logging=logger.get_logger(name='MLOps')

# Read environmental variables
ENV = os.environ['ENV'] # Must be set
SERVICE_NAME = os.environ['SERVICE_NAME']
LOCAL_DEPLOYMENT = os.getenv('LOCAL_DEPLOYMENT') # Optional


def deploy(model_settings):
    failed_models = {}
    base_path = os.getcwd()
    for setting in model_settings:
        try:
            (model_name, model_file, model_req_file, model_artifact_folder,
            info, model_test_file, deployment_platform) = setting
            
            logging.debug(" ")
            logging.info(f"Deploy model {model_name}")

            deployment_folder =f'mlops_{model_name}'
            function_name=f"{model_name}-{SERVICE_NAME}-{ENV}"
            
            model_code_folder = helpers.get_top_folder(model_file)

            if SERVICE_NAME == 'prediction':
                model_id = set_up_model_artifact(
                    model_artifact_folder, 
                    model_name
                )
            else:
                model_id = None

            m = "Create deployment folder and move required files/folders"
            logging.info(m)
            os.mkdir(deployment_folder)
            to_deployment_folder = partial(
                helpers.to_folder, 
                folder_path=deployment_folder
            )
            logging.debug("model code => deployment folder")
            to_deployment_folder(model_code_folder)
            logging.debug("handler => deployment folder")
            to_deployment_folder((f"akerbp.mlops.cdf","handler.py"))
            logging.debug("project config => deployment folder")
            to_deployment_folder('mlops_settings.py')
            logging.debug("artifact folder => deployment folder")
            to_deployment_folder(model_artifact_folder)
            if deployment_platform == "gc":
                logging.debug("Dockerfile => deployment folder")
                to_deployment_folder(("akerbp.mlops.gc", "Dockerfile"))
                logging.debug("requirements.app => deployment folder")
                to_deployment_folder(("akerbp.mlops.gc", "requirements.app"))
                logging.debug("install_req_file.sh => deployment folder")
                to_deployment_folder(("akerbp.mlops.gc", "install_req_file.sh"))

            logging.debug(f"cd {deployment_folder}")
            os.chdir(deployment_folder)

            logging.info("Write service settings file")
            model_import_path = helpers.as_import_path(model_file)
            test_import_path = helpers.as_import_path(model_test_file)

            mlops_settings=dict(
                model_name=model_name,
                model_artifact_folder=model_artifact_folder,
                model_import_path=model_import_path,
                model_code_folder=model_code_folder,
                model_id=model_id,
                test_import_path=test_import_path
            )
            # File name can't be mlops_settings.py, or there will be an
            # importing error when the service test is run (user settings <-
            # model test <- service test)
            with open('service_settings.py', 'w') as config:
                config.write(f'{mlops_settings=}')
            
            logging.info("Create CDF requirement file")
            if (
                "akerbp/mlops" in helpers.get_repo_origin() 
                and (ENV != "dev" or LOCAL_DEPLOYMENT)
            ):
                helpers.set_mlops_import(model_req_file)
            shutil.move(model_req_file, 'requirements.txt')
            if ENV != "dev":
                m = (f"Install python requirements from model {model_name}")
                logging.info(m)
                c = ["pip", "install", "--quiet", "-r", 'requirements.txt']
                subprocess.check_call(c)

            # * Dependencies: (user settings <- model test). Either run before
            #   going to the dep. folder or copy project config to dep. folder. 
            # * It is important to run tests after setting up the artifact
            #   folder in case it's used to test prediction service.
            # * Tests need the model requirements installed!
            logging.info(f"Run model and service tests")
            if model_test_file:
                helpers.run_tests(model_test_file)
                helpers.run_tests('akerbp.mlops.services', path_type='module')
            else:
                logging.warning("Model test file is missing! " \
                                "Didn't run tests")
            # Project settings file isn't needed anymore
            logging.debug("Delete project settings from deployment folder")
            os.remove('mlops_settings.py')

            if ENV != "dev" or LOCAL_DEPLOYMENT:
                logging.info(f"Deploy {function_name} to {deployment_platform}")
                
                if deployment_platform == 'cdf':
                    from akerbp.mlops.cdf.helpers import deploy_function
                    from akerbp.mlops.cdf.helpers import test_function
                    from akerbp.mlops.cdf.helpers import set_up_cdf_client
                    set_up_cdf_client(context='deploy')
                elif deployment_platform == 'gc': 
                    from akerbp.mlops.gc.helpers import deploy_function
                    from akerbp.mlops.gc.helpers import test_function
                else:
                    m = f"Expected 'cdf' or 'gc', got {deployment_platform=}"
                    raise ValueError(m)
                
                logging.info("Deploy function")
                deploy_function(function_name, info=info[SERVICE_NAME])
                
                if test_import_path:
                    logging.info("Test call")
                    ServiceTest=import_module(test_import_path).ServiceTest  
                    input = getattr(ServiceTest(), f"{SERVICE_NAME}_input")
                    test_function(function_name, input)
                else:
                    logging.warning("No test file was set up. " \
                                    "End-to-end test skipped!")
        except Exception:
            trace = traceback.format_exc()
            error_message = f"Model failed to deploy!\n{trace}"
            logging.error(error_message)
            failed_models[model_name] = error_message

        finally:
            logging.debug(f"cd ..")
            os.chdir(base_path)
            logging.debug(f"Delete deployment folder")
            if os.path.isdir(deployment_folder):
                shutil.rmtree(deployment_folder)

    if failed_models:
        for model_name, error_message in failed_models.items():
            logging.debug(" ")
            logging.info(f"Model {model_name} failed: {error_message}")
        raise Exception("At least one model failed.")


if __name__ == '__main__':
    model_settings = helpers.read_config()
    deploy(model_settings)