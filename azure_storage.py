from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
import uuid

class AzureBlobStorage:
    def __init__(self, connection_string, container_name):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name

    def upload_file(self, file):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=unique_filename)
        blob_client.upload_blob(file.stream)
        return blob_client.url
