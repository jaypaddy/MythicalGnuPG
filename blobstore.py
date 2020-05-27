"""
Input : EncryptedFile, GnuPG_PrivateKey
Output : DecryptedFile
"""
import os
from azure.storage.blob import BlobServiceClient

# set up
SOURCE_FILE = 'SampleSource.txt'
DEST_FILE = 'BlockDestination.txt'

class BlobClass(object):
    connection_string = os.getenv("GNUPG_BLOB")
    container_name = os.getenv("GNUPG_CONTAINER")
    sourceblob_name = os.getenv("SRCBLOB")
    dstblob_name = os.getenv("DSTBLOB")


    def download_blob(self):
        # Instantiate a new BlobServiceClient using a connection string
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client(self.container_name)
        try:
            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client(self.sourceblob_name)

            # [START download_a_blob]
            with open(self.dstblob_name, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
            # [END download_a_blob]
        finally:
            # Do the cleanup as required....
            print("Finally")

    def upload_blob(self, srcBlob, dstBlob):
        # Instantiate a new BlobServiceClient using a connection string
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        # Instantiate a new BlobClient
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=dstBlob)

        # Upload the created file
        with open(srcBlob, "rb") as data:
            blob_client.upload_blob(data)


if __name__ == '__main__':
    bObj = BlobClass()
    #bObj.download_blob()
    bObj.upload_blob('blobstore.py','store.py')



