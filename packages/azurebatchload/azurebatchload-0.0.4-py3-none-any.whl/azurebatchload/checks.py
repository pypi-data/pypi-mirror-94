import os
import logging
from subprocess import check_output, CalledProcessError, STDOUT


class Checks:
    def __init__(self, connection_string, account_key, account_name, directory):
        self.connection_string = connection_string
        self.account_key = (account_key,)
        self.account_name = account_name
        self.directory = directory

    def _create_connection_string(self):
        connection_string = (
            "DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1};"
            "EndpointSuffix=core.windows.net".format(self.account_name, self.account_key)
        )

        return connection_string

    def _check_connection_credentials(self):
        if self.connection_string or os.environ.get("AZURE_STORAGE_CONNECTION_STRING"):
            return True
        elif all([self.account_key, self.account_name]) or all(
            [os.environ.get("account_key", None), os.environ.get("account_name", None)]
        ):
            return True
        else:
            # if account_key and account_name arguments are not set,
            #   check for env variables else raise
            raise ValueError(
                "If account_key and account_name are not given as argument "
                "they have to be specified as environment variables named "
                " AZURE_STORAGE_KEY and AZURE_STORAGE_ACCOUNT"
            )

    def _check_dir(self):
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Source directory {self.directory} not found")

    def _create_dir(self):
        if not os.path.exists(self.directory):
            logging.info(f"Destination {self.directory} does not exist, creating..")
            os.makedirs(self.directory)
        else:
            logging.info("Destination directory already exists, skipping")

    @staticmethod
    def _check_azure_cli_installed():
        try:
            check_output(["az", "--version"], stderr=STDOUT, shell=True)
        except CalledProcessError:
            print("Azure CLI is not installed, please install before using azurebatchload")
