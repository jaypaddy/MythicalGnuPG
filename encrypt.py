import gnupg                                                                                                                               
                                                                                                                                           
gpg = gnupg.GPG(gpgbinary='/usr/bin/gpg')                                                                                                  
unencrypted_string = 'Who are you? How did you get in my house?'                                                                           
encrypted_data = gpg.encrypt(unencrypted_string, 'testgpguser@mydomain.com')                                                               
encrypted_string = str(encrypted_data)                                                                                                     
print ('ok: ', encrypted_data.ok )                                                                                                           
print ('status: ', encrypted_data.status )                                                                                                   
print ('stderr: ', encrypted_data.stderr )                                                                                                   
print ('unencrypted_string: ', unencrypted_string   )                                                                                        
print ('encrypted_string: ', encrypted_string )