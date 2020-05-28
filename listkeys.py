import gnupg
from pprint import pprint

gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
public_keys = gpg.list_keys()
private_keys = gpg.list_keys(True)
print ('public keys:')
pprint(public_keys)
print ('private keys:')
pprint(private_keys)