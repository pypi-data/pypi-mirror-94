# helpers.py
import sys
import os

from importlib import resources as importlib_resources
import shutil
import subprocess

from akerbp.mlops.core import logger 


logging=logger.get_logger(name='MLOps')

ENV = os.environ['ENV']

def get_version():
    tag = subprocess.check_output(
        ['git', 'describe', '--tags', '--exact-match'],
        encoding='UTF-8'
    ).rstrip()
    if ENV in ['dev', 'test']:
        version = '0.' + tag
    elif ENV == 'prod':
        version = '1.' + tag
    return version


def get_repo_origin():
    origin = subprocess.check_output(
        ['git', 'remote', 'get-url', '--push', 'origin'],
        encoding='UTF-8'
    ).rstrip()
    return origin


def replace_string_file(s_old, s_new, file):
    """
    Replaces all occurrences of s_old with s_new in a file
    """
    with open(file) as f:
        s = f.read()
        if s_old not in s:
            logging.warning(f"Didn't find '{s_old}' in {file}")

    with open(file, 'w') as f:
        s = s.replace(s_old, s_new)
        f.write(s)


def set_mlops_import(req_file):
    package_version = get_version()
    replace_string_file('MLOPS_VERSION', package_version, req_file)
    logging.info(f"Set akerbp.mlops=={package_version} in requirements.txt")


def read_config():
    logging.info(f"Read project configuration")
    from mlops_settings import model_names, model_files, model_req_files
    from mlops_settings import model_artifact_folders, infos, model_test_files
    return zip(
        model_names, 
        model_files, 
        model_req_files, 
        model_artifact_folders,
        infos,
        model_test_files
    )


def get_top_folder(s):
    return s.split(os.sep)[0]


def as_import_path(file_path):
    if file_path:
        return file_path.replace(os.sep,'.').replace('.py','')
    else:
        logging.debug(f"Empty file path -> empty import path returned")


def to_folder(path, folder_path):
    """
    Copy folders, files or package data to a given folder
    Input:
      - path: supported formats
            - folder path (string): e,g, "my/folder" 
            - file path (string): e.g. "my/file" (string)
            - module file (tuple/list): e.g. ("my.module", "my_file") 
    """
    if isinstance(path,(tuple,list)):
        if importlib_resources.is_resource(*path):
            with importlib_resources.path(*path) as file_path:
                shutil.copy(file_path, folder_path)
        else:
            raise ValueError(f"Didn't find {path[1]} in {path[0]}")
    elif os.path.isdir(path):
        shutil.copytree(
            path, 
            os.path.join(folder_path, path), 
            dirs_exist_ok=True
        )
    elif os.path.isfile(path):
        shutil.copy(path, folder_path)
    else:
        raise ValueError(f"{path} should be a file, folder or package resource")


def run_tests(test_path, path_type='file'):
    """
    Run tests with pytest
    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)
    """
    command = [sys.executable, "-m", "pytest"]
    if path_type == 'module':
        command.append("--pyargs")
    if isinstance(test_path, str):
        command.append(test_path)
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logging.info(f"Run tests: {test_path}")
    subprocess.check_call(command)


def set_up_model_artifact(artifact_folder, model_name):
    """
    Set up model artifacts. 
    When the prediction service is deployed, we need the model artifacts. These
    are downloaded, unless there's already a folder (local development
    environment only)
    Input:
      - artifact_folder 
      - model_name
    Output:
      - model_id: either the model id provided by the model manager, a hardcoded
        value (existing folder in dev) or None (training service)
    """
    
    from akerbp.mlops.cdf.helpers import download_model_version 
    from akerbp.mlops.cdf.helpers import set_up_cdf_client
    set_up_cdf_client()

    if os.path.isdir(artifact_folder):
        if ENV=='dev':
            logging.info(f"Use model artifacts in {artifact_folder=}")
            model_id=f'{model_name}/dev/1'
            return model_id
        else:
            message = f"Existing artifacts won't be used ({ENV=})"
            logging.warning(message)
    logging.info("Download serialized model")
    model_id = download_model_version(model_name, ENV, artifact_folder)

    return model_id