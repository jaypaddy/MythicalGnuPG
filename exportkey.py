import gnupg

gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg') 
key = 'CA9574181E259C6022B558094DA23EC606F909B0'
ascii_armored_public_keys = gpg.export_keys(key)
ascii_armored_private_keys = gpg.export_keys(key, secret=True, passphrase="my passphrase")
with open('mykeyfile.asc', 'w') as f:
    f.write(ascii_armored_public_keys)
    f.write(ascii_armored_private_keys)