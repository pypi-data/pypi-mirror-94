"""
cdf_helpers.py

High level functionality built on top of Cognite's Python SDK

Most functions require the global cdf client to be set up before using them.

Files handling functions work on an `mlops` folder. This is hard-coded,
but it can be easily modified.
"""
import time
import os 
import json
from shutil import make_archive, unpack_archive

from cognite.client.exceptions import CogniteNotFoundError, CogniteAPIError

from akerbp.mlops.core import logger 

logging=logger.get_logger(name='cdf_helper')

global_client = {}

api_keys = dict(
    functions = os.getenv('COGNITE_API_KEY_FUNCTIONS'),
    data = os.getenv('COGNITE_API_KEY_DATA'),
    files = os.getenv('COGNITE_API_KEY_FILES')
)

def set_up_cdf_client(context='run'):
    """
    Set up the global client used by most helpers. This needs to be called before using any helper. Should be called once with all required keys.

    Input:
      - context: string either 'run' (access to data and functions) or 'deploy'
        (access to 'functions' also).
    """
    if context == 'run':
        api_key_labels=["data", "files"]
    elif context == 'deploy':
        api_key_labels=["data", "files", "functions"]
    else:
        raise ValueError("Context should be either 'run' or 'deploy'")

    for k in api_key_labels:
        global_client[k] = get_client(api_keys[k], k)
        
    logging.info("CDF client was set up correctly")


def get_client(api_key, api_key_label=None):
    """
    Create a CDF client with a given api key
    """
    if api_key_label == 'functions':
        from cognite.experimental import CogniteClient
        logging.warning("Imported CogniteClient from cognite.experimental")
    else:
        from cognite.client import CogniteClient
    
    client = CogniteClient(
        api_key=api_key,
        project='akbp-subsurface',
        client_name="mlops-client",
        base_url='https://api.cognitedata.com'
    )
    assert client.login.status().logged_in
    logging.debug(f"{client.version=}")
    logging.debug(f"{client.config.client_name=}")
    
    return client


def create_function(
    function_name, 
    folder, 
    handler_path,  
    description='',
    owner='',
    secrets={}
):
    """
    Create a Cognite function from a folder. Any existing function with the same
    name is deleted first.

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
    """
    client = global_client["functions"]
    try:
        client.functions.delete(external_id=function_name)
        logging.debug(f"Deleted function {function_name}")
    except CogniteNotFoundError:
        pass
    function = client.functions.create( 
        name=function_name, 
        folder=folder, 
        function_path=handler_path,
        external_id=function_name,
        description=description,
        owner=owner,
        secrets=secrets
    )
    logging.debug(f"Created {function_name}: {folder=}, {handler_path=}")

    return function


def deploy_function(
    function_name,
    folder='.',
    handler_path='handler.py',
    secrets=api_keys,
    info={'description':'', 'owner':''}
):
    """
    Deploys a Cognite function from a folder. The function is created first,
    and then it waits until the function status is ready or failed. If it fails,
    it will try again `max_error` times

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
    """
    max_errors = 3

    for trial in range(max_errors):
        function = create_function(
            function_name, 
            folder, 
            handler_path, 
            info['description'],
            info['owner'],
            secrets
        )
        status = wait_function_status(function)
        logging.debug(f"Function status is {status}")
        if function.status == 'Ready':
            break
        if function.status == 'Failed' and trial < max_errors-1:
            logging.debug(f"Try to create function again")
        else:
            raise Exception(f"Function deployment error: {function.error=}")


def call_function(function_name, data):
    """
    Call a function deployed in CDF
    """
    client = global_client["functions"]
    function = client.functions.retrieve(external_id=function_name)
    logging.debug(f"Retrieved function {function_name}")
    call = function.call(data)
    logging.debug(f"Called function (call_id={call.id})")
    response = call.get_response()
    logging.debug(f"Called function: {response=}")
    return response


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")


def wait_function_status(function, status=["Ready", "Failed"]):
    """
    Wait until function status is in `status`
    By default it waits for Ready or Failed, which is useful when deploying.
    It implements some control logic, since polling status can fail.
    """
    polling_wait_seconds_base = 10
    polling_wait_seconds = polling_wait_seconds_base
    max_api_errors_base = 5
    max_api_errors = max_api_errors_base
    
    logging.debug(f"Wait for function to be ready or to fail")
    while not (function.status in status):
        try:
            time.sleep(polling_wait_seconds)
            function.update()
            logging.debug(f"{function.status=}")
            polling_wait_seconds = polling_wait_seconds_base
            max_api_errors = max_api_errors_base
        except CogniteAPIError as e:
            max_api_errors -= 1
            logging.warning(f"Could not update function status, will try again")
            polling_wait_seconds *= 1.2          
            if not max_api_errors:
                logging.error(f"Could not update function status.")
                raise e

    return function.status


def download_file(id, path):
    """
    Download file from Cognite
    
    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
        - path: path of local file to write
    """
    client = global_client["files"]
    
    logging.debug(f"Download file with {id=} to {path}")
    client.files.download_to_path(path, **id)


def upload_file(
    external_id, 
    path, 
    metadata={}, 
    directory='/mlops',
    overwrite=True):
    """
    Upload file to Cognite
    
    Params:
        - external_id: external id
        - path: path of local file to upload
        - metadata: dictionary with file metadata
        - overwrite: what to do when the external_id exists already
    """
    client = global_client["files"]
    
    metadata = {k:v if isinstance(v, str) else json.dumps(v) 
        for k,v in metadata.items()}

    logging.debug(f"Upload file {path} with {external_id=} and {metadata=}")
    file_info = client.files.upload(
        path, 
        external_id, 
        metadata=metadata, 
        directory=directory, 
        overwrite=overwrite
    )
    logging.info(f"Uploaded file: {file_info=}")
    return file_info


def upload_folder(external_id, path, metadata={}, overwrite=False):
    """
    Upload folder content to Cognite. It compresses the folder and uploads it.
    
    Params:
        - external_id: external id (should be unique in the CDF project)
        - path: path of local folder where content is stored
        - metadata: dictionary with file metadata
        - overwrite: if overwrite==False and `external_id` exists => exception
    """
    base_name = os.path.join(path, 'archive')
    archive_name = make_archive(base_name, 'gztar', path)
    file_info = upload_file(
        external_id, 
        archive_name, 
        metadata=metadata,
        overwrite=overwrite
    )
    os.remove(archive_name)
    logging.info(f"Folder content uploaded: {file_info=}")
    return file_info


def download_folder(external_id, path):
    """
    Download content from Cognite to a folder. It is assumed to have been
    uploaded using `upload_folder()`, so it downloads a file and decompresses
    it.

    Params:
    - external_id: external id
    - path: path of local folder where content will be stored
    """
    base_name = os.path.join(path, 'archive.tar.gz')
    download_file(dict(external_id=external_id), base_name)
    unpack_archive(base_name, os.path.dirname(base_name))
    os.remove(base_name)
    logging.info(f"Model file/s downloaded to {path}")


def log_system_info():
    """
    Can be called from a handler to log CDF environment information
    """
    logging.debug(os.popen('python --version').read())
    logging.debug(os.popen('ls -la *').read())
    logging.debug(os.popen('pip freeze').read())


def count_file_versions(
    external_id_prefix, 
    directory_prefix='/mlops'
):
    """
    How many files have the given `external_id_prefix` and `directory_prefix`
    This can be used for file versioning.

    Returns an integer (>=0)
    """
    client = global_client["files"]
    result = client.files.aggregate(filter={
        "external_id_prefix": external_id_prefix, 
        "directory_prefix": directory_prefix
    })
    return result[0]["count"]


def upload_new_model_version(model_name, env, folder, metadata):
    """
    Upload a new model version. Files in a folder are archived and stored 
    with external id `model_name/env/version`, where version is automatically increased. 

    Input:
        -model_name: name of the model 
        -env: name of the environment ('dev', 'test', 'prod')
        -folder: path to folder whose content will be uploaded
        -metadata: dictionary with metadata (it should not contain a 'version'
        key)
    
    Output:
        - model metadata (dictionary)
    """

    filter = f"{model_name}/{env}/"
    version = count_file_versions(filter) + 1
    metadata["version"] = version
    external_id = f"{model_name}/{env}/{version}"

    folder_info = upload_folder(
        external_id, 
        folder, 
        metadata
    )
    logging.info(f"Uploaded model with {external_id=} from {folder}")
    return folder_info


def find_model_version(model_name, env, metadata):
    """
    Model external id is specified by the model name and the environment
    (starts with `{model_name}/{env}`), and a query to the metadata. If this is
    not enough, the latest version is chosen.

    Input:
        -model_name: name of the model 
        -env: name of the environment ('dev', 'test', 'prod')
        -metadata: query to the metadata (dictionary), it can contain a
        'version' key
    """
    client = global_client["files"]
    file_list = client.files.list(
        limit=-1, 
        directory_prefix='/mlops', 
        external_id_prefix=f"{model_name}/{env}",
        metadata=metadata
    ).to_pandas()

    if (n_models := file_list.shape[0]) == 0:
        message = f"No model found with {model_name=} in {env=} and {metadata}"
        raise Exception(message)
    elif n_models > 1:
        logging.debug(f"Found {n_models} model files. Will choose the latest.")
    
    # Get latest in case there are more than one
    external_id = file_list.loc[file_list.uploadedTime.argmax(), "externalId"]
    return external_id


def download_model_version(model_name, env, folder, metadata={}):
    """
    Download a model version to a folder. First the model's external id is
    found, and then it is downloaded to the chosen folder (creating the folder
    if necessary).

    Input: 
        -model_name: name of the model 
        -env: name of the environment ('dev', 'test', 'prod')
        -folder: path to folder where the content will be uploaded
        -metadata: query to the metadata (dictionary)
    """
    external_id = find_model_version(model_name, env, metadata)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    download_folder(external_id, folder)
    logging.info(f"Downloaded model with {external_id=} to {folder}")
    return external_id