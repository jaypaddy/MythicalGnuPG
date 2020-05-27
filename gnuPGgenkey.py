import os
import gnupg


gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg')
input_data = gpg.gen_key_input(
    name_email='testgpguser@mydomain.com',
    passphrase='my passphrase')
key = gpg.gen_key(input_data)
print(key)