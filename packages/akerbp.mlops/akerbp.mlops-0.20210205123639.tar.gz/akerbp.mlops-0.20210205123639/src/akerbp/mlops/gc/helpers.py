"""
helpers.py

Functionality built on top of Google SDK (bash or python)
Requirement: SDK activated and GOOGLE_APPLICATION_CREDENTIALS defined
(see install_gc_sdk.sh)
"""

import subprocess
import os

import requests
import json


from akerbp.mlops.core import logger 

logging=logger.get_logger(name='gc_helper')

GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")


def create_service_account(service_account):
    """
    Create a service account if it doesn't exist
    """
    try:
        subprocess.check_call(
            f"gcloud iam service-accounts list | grep {service_account}",
            shell=True)
        logging.debug(f"Found service account {service_account}")
    except subprocess.CalledProcessError:
        subprocess.check_call(
            f"gcloud iam service-accounts create {service_account}",
            shell=True)
        logging.debug(f"Created service account {service_account}")


def access_secret_version(secret_id, version_id="latest"):
    """
    Read a secret

    See https://codelabs.developers.google.com/codelabs/secret-manager-python/index.html?index=..%2F..index#5
    See https://dev.to/googlecloud/serverless-mysteries-with-secret-manager-libraries-on-google-cloud-3a1p
    """
    logging.debug(f"Read secret {secret_id}")
    from google.cloud import secretmanager
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version.
    name = (
      f"projects/{GOOGLE_PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    )
    # Access the secret version.
    response = client.access_secret_version(name=name)
    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')


def create_image(image_name, folder='.'):
    """
    Build an image
    """
    subprocess.check_call(
        (f"gcloud builds submit {folder} "
         f"--tag gcr.io/{GOOGLE_PROJECT_ID}/{image_name} "
          "--quiet"
        ), shell=True)


def allow_access_to_secrets(service_account, secret_names=["mlops-cdf-keys"]):
    """
    Give a service account access to secrets stored in Secret Manager
    """
    s_a_id = f"{service_account}@{GOOGLE_PROJECT_ID}.iam.gserviceaccount.com"
    for secret_name in secret_names:
        subprocess.check_call(
            (f"gcloud secrets add-iam-policy-binding {secret_name} "
             f"--member serviceAccount:{s_a_id} "
              "--role roles/secretmanager.secretAccessor"
            ), shell=True)


def run_container(image_name, service_account):
    """
    Run container with a service account
    """
    envs = ["GOOGLE_PROJECT_ID", "SERVICE_NAME"]
    envs = [f"{env}={eval(env)}" for env in envs]
    env_list_string=','.join(envs)
    
    subprocess.check_call(
        (f"gcloud run deploy {image_name} "
         f"--image gcr.io/{GOOGLE_PROJECT_ID}/{image_name} "
          "--platform managed "
          "--region=europe-north1 "
          "--allow-unauthenticated " #"--no-allow-unauthenticated "
          "--no-user-output-enabled "
          "--memory=512M "
         f"--service-account {service_account} "
         f"--set-env-vars={env_list_string}"
        ), shell=True)


def deploy_function(
    function_name,
    folder='.',
    **kwargs
):
    """
    Deploys a Google Cloud Run function from a folder. 

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - kwargs: accept `handler_path` and possibly other args required by CDF
            but not GC
    """
    service_account = f"{function_name}-acc"
    logging.debug(f"Deploy function {function_name}")
    create_service_account(service_account)
    allow_access_to_secrets(service_account)
    create_image(function_name, folder)
    run_container(function_name, service_account)


def read_function_url(function_name):
    # Read service url
    url = subprocess.check_output(
        (f"gcloud run services list "
          "--platform managed "
         f"""--filter="metadata.name='{function_name}'" """
          '--format="value(URL)"'
        ), encoding='UTF-8', shell=True)
    return url.rstrip()


def call_function(function_name, data):
    """
    Call a function deployed in Google Cloud Run
    """
    logging.debug(f"{data=}")
    url = read_function_url(function_name)
    url+=f"/{SERVICE_NAME}"
    logging.debug(f"Post to {url}")
    response = requests.post(url, json={'data': json.dumps(data)})
    logging.debug(f"Status: {response.status_code}")
    if response.ok:
        return response.json()


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")