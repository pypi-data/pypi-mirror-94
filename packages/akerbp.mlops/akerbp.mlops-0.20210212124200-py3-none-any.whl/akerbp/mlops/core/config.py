# config.py
import os
from dataclasses import dataclass
from typing import List

from akerbp.mlops.gc.helpers import deploy_function as gc_deploy
from akerbp.mlops.gc.helpers import test_function as gc_test
from akerbp.mlops.cdf.helpers import deploy_function as cdf_deploy
from akerbp.mlops.cdf.helpers import test_function as cdf_test
from akerbp.mlops.cdf.helpers import set_up_cdf_client
from akerbp.mlops.core import helpers 
from akerbp.mlops.core import logger

logging=logger.get_logger(name='MLOps')

@dataclass
class EnvVar:
    env: str
    service_name: str
    local_deployment: str

    def __post_init__(self):
        envs = ["dev", "test", "prod"]
        if self.env not in envs:
            m = f"Environment: allowed values are {envs}"
            raise ValueError(m)

        service_names = ["training", "prediction"]
        if self.service_name not in service_names:
            m = f"Service name: allowed values are {service_names}"
            raise ValueError(m)

        local_deployments = ["True", None]
        if self.local_deployment not in local_deployments:
            m = f"Local deployment: allowed values are {local_deployments}"
            raise ValueError(m)


# Read environmental variables
getenv=EnvVar(
    env=os.getenv('ENV'), 
    service_name=os.getenv('SERVICE_NAME'), 
    local_deployment=os.getenv('LOCAL_DEPLOYMENT')
)

env = getenv.env
service_name = getenv.service_name
local_deployment = getenv.local_deployment


@dataclass
class ModelConfig:
    model_name: str
    model_file: str
    model_req_file: str
    model_artifact_folder: str
    info: str
    model_test_file: str
    deployment_platform: str

    def __post_init__(self):
        # Validation
        if self.deployment_platform not in ["cdf", "gc", "local"]:
            m = f"Deployment platform should be either 'cdf', 'gc' or 'local'"
            raise ValueError(m)

        # Derived fields
        if getenv.env == 'dev' and not getenv.local_deployment:
            self.deployment_platform = 'local'

        if self.deployment_platform == 'cdf':
            set_up_cdf_client(context='deploy')
            self.deploy_function, self.test_function = cdf_deploy, cdf_test
        elif self.deployment_platform == 'gc': 
            self.deploy_function, self.test_function = gc_deploy, gc_test
        elif self.deployment_platform == 'local': 
            self.deploy_function=self.test_function=lambda *args,**kargs: None

        self.model_code_folder = helpers.get_top_folder(self.model_file)
        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.model_test_file)

        self.files = {
            "model code": self.model_code_folder, 
            "handler": (f"akerbp.mlops.cdf","handler.py"),
            "project config": 'mlops_settings.py',
            "artifact folder": self.model_artifact_folder
        }
        if self.deployment_platform == "gc":
            files_gc = {
                "Dockerfile": ("akerbp.mlops.gc", "Dockerfile"),
                "requirements.app": ("akerbp.mlops.gc", "requirements.app"),
                "install_req_file.sh": ("akerbp.mlops.gc", "install_req_file.sh")
            }
            self.files = {**self.files, **files_gc}


@dataclass
class ProjectConfig:
    model_settings: List[ModelConfig]


def read_config():
    logging.info(f"Read project configuration")
    from mlops_settings import model_names, model_files, model_req_files
    from mlops_settings import model_artifact_folders, infos, model_test_files
    from mlops_settings import model_platforms
    settings =  zip(
        model_names, 
        model_files, 
        model_req_files, 
        model_artifact_folders,
        infos,
        model_test_files,
        model_platforms
    )
    model_settings = [ModelConfig(*s) for s in settings]
    project_settings = ProjectConfig(model_settings)
    logging.debug(f"{project_settings=}")
    
    return project_settings

project_settings = read_config()