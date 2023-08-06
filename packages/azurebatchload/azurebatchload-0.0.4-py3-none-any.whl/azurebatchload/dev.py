# flake8: noqa

import os
from azurebatchload import UploadBatch
from azurebatchload.download import DownloadBatch
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

if not os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
    raise ValueError("No connection string")


source = "/Users/erfannariman/Workspace/zypp/azure-batch-load/data"
account_key = os.environ.get("account_key")
account_name = os.environ.get("account_name")
az_batch = UploadBatch(destination="test", source=source, pattern="*.PDF")
az_batch.upload()


# az_batch = DownloadBatch(destination=".", source="test", pattern="*.PDF")
# az_batch.download()
