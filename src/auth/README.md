shell

#Generate private key
openssl genrsa -out jwt-private.pem 2048                                    


shell

#Generate public key
openssl rsa -in  jwt-private.pem -outform PEM -pubout -out jwt-public.pem

