from .client import Client
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

class BlobClient(Client):
    def __init__(self, parameters_file = None):
        super().__init__(parameters_file)

    def run(self):
        """
        Create export file with parameters given.
        """
        pass