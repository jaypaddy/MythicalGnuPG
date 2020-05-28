import gnupg
from pprint import pprint

gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
key_data = open('mykeyfile.asc').read()
import_result = gpg.import_keys(key_data)
gpg.trust_keys('', TRUST_ULTIMATE)
pprint(import_result.results)