"""
Input : EncryptedFile, GnuPG_PrivateKey
Output : DecryptedFile
"""
import os
import gnupg
from azure.storage.blob import BlobServiceClient
from pprint import pprint

class BlobClass(object):
    connection_string = os.getenv("GNUPG_BLOB")
    container_name = os.getenv("GNUPG_CONTAINER")

    def download_blob(self,srcBlob, dstFile):
        # Instantiate a new BlobServiceClient using a connection string
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client(self.container_name)
        try:
            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client(srcBlob)
            # [START download_blob]
            with open(dstFile, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
            # [END download_blob]
        finally:
            # Do the cleanup as required....
            print("Finally")

    def upload_blob(self, srcFile, dstBlob):
        # Instantiate a new BlobServiceClient using a connection string
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        # Instantiate a new BlobClient
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=dstBlob)

        # Upload the created file
        with open(srcFile, "rb") as data:
            blob_client.upload_blob(data)

class GnuPGClass(object):
    recipients = []
    recipients.append(os.getenv("GNUPG_RECIPIENTS"))
    passphrase = os.getenv("GNUPG_PASSPHRASE")
    keyfile = os.getenv("GNUPG_KEYFILE")
    fingerprint = os.getenv('GNUPG_FINGERPRINT')
    # Encrypt the given file and save it as dstFile
    def encrypt_file(self, srcFile, dstFile):
        gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
        with open(srcFile, 'rb') as f:
            status = gpg.encrypt_file(
                f, self.recipients,
                output=dstFile)
        print ('ok: ', status.ok)
        print ('status: ', status.status)
        print ('stderr: ', status.stderr)

    def download_encrypt_and_upload_blob(self,srcBlob, dstBlob):
        # Download the SrcBlob
        bObj = BlobClass()
        # Download to a temp file by appending .tmp to the srcBlob name
        localOriginalFile = srcBlob + '.original.tmp'
        localEncryptedFile = srcBlob + '.encrypted.tmp'
        bObj.download_blob(srcBlob,localOriginalFile)
        self.encrypt_file(localOriginalFile,localEncryptedFile)
        bObj.upload_blob(localEncryptedFile,dstBlob)
        os.remove(localOriginalFile)
        os.remove(localEncryptedFile)

    def decrypt_file(self, srcFile, dstFile):
        gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
        with open(srcFile, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase=self.passphrase, output=dstFile)
        print ('ok: ', status.ok)
        print ('status: ', status.status)
        print ('stderr: ', status.stderr)

    def download_decrypt_and_upload_blob(self,srcBlob, dstBlob):
        # Download the SrcBlob
        bObj = BlobClass()

        localEncryptedFile = srcBlob + '.encrypted.tmp'
        localDecryptedFile = dstBlob + '.decrypted.tmp'
        # Download the source blob as an local Encrypted File
        bObj.download_blob(srcBlob,localEncryptedFile)
        # Decrypt the local file encrypted file
        self.decrypt_file(localEncryptedFile,localDecryptedFile )
        bObj.upload_blob(localDecryptedFile,dstBlob)
        os.remove(localEncryptedFile)
        os.remove(localDecryptedFile)

    def import_keys(self):
        # download from Blob - to be replaced with KeyVault
        bObj = BlobClass()
        # Download to a temp file by appending .tmp to the srcBlob name
        print("Downloading ", self.keyfile)
        bObj.download_blob(self.keyfile,self.keyfile)
        gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
        key_data = open(self.keyfile).read()
        import_result = gpg.import_keys(key_data)
        gpg.trust_keys(self.fingerprint, 'TRUST_ULTIMATE')
        pprint(import_result.results)
        os.remove(self.keyfile)

if __name__ == '__main__':
    gnuObj = GnuPGClass()
    gnuObj.import_keys()
    print('Keys Imported')
    gnuObj.download_encrypt_and_upload_blob(os.getenv('GNUPG_ORIGINAL_FILE'),os.getenv('GNUPG_ENCRYPTED_FILE'))
    print('Download ',os.getenv('GNUPG_ORIGINAL_FILE'), ' and encrypt ', )
    print("Completed Download-Encrypt-Upload")
    gnuObj.download_decrypt_and_upload_blob(os.getenv('GNUPG_ENCRYPTED_FILE'),os.getenv('GNUPG_DECRYPTED_FILE'))



