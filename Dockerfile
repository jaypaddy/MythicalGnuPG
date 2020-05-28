FROM python:3.7-buster
RUN pip install python-gnupg
RUN pip install azure-storage-blob
#RUN apk add --no-cache gnupg
ENV GNUPG_BLOB="DefaultEndpointsProtocol=https;AccountName=mythicalspa;AccountKey=NGlfooNqhxr6SOl3Xnh8MR8DKpv3OkM4VP9K3TbsOpwPBYHcLjrJafetnwEf4Y+10WK/4yv/MWnxxMyG1udkhg==;EndpointSuffix=core.windows.net"
ENV GNUPG_CONTAINER="gnupg"
ENV GNUPG_PASSPHRASE="my passphrase"
ENV GNUPG_RECIPIENTS="testgpguser@mydomain.com"
ENV GNUPG_FINGERPRINT="CA9574181E259C6022B558094DA23EC606F909B0"
ENV GNUPG_KEYFILE="keyfile.asc"
ENV GNUPG_ORIGINAL_FILE="blobstore.py"
ENV GNUPG_ENCRYPTED_FILE="blobstore.encrypted.py"
ENV GNUPG_DECRYPTED_FILE="blobstore.decrypted.py"
RUN mkdir /app 
ADD gnuPG.py /app