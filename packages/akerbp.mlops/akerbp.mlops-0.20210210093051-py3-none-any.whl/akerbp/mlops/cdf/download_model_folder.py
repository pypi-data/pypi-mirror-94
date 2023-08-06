# download_model_folder.py
import os

from akerbp.mlops.cdf.helpers import download_folder 


if __name__ == "__main__":
    """
    Read env vars and call the download file function
    """
    api_key_file = os.environ['COGNITE_API_KEY_FILES']
    external_id = os.environ['FILE_EXTERNAL_ID']
    folder = os.environ['FOLDER_PATH']
    
    download_folder(api_key_file, external_id, folder)