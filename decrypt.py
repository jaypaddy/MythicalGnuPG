import gnupg

gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg')   
unencrypted_string = 'Who are you? How did you get in my house?'
encrypted_data = gpg.encrypt(unencrypted_string, 'testgpguser@mydomain.com')
encrypted_string = str(encrypted_data)
decrypted_data = gpg.decrypt(encrypted_string, passphrase='my passphrase')

print ('ok: ', decrypted_data.ok)
print ('status: ', decrypted_data.status)
print ('stderr: ', decrypted_data.stderr)
print ('decrypted string: ', decrypted_data.data)