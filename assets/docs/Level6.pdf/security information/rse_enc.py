def rsa_enc (message,e,n) :
    encrypted_message = []
    c = pow (message,e,n)
    encrypted_message.append(c)
    return encrypted_message
p = 3
q = 11
e = 3
d = 7
n = p*q
message = 6
encrypted_message = rsa_enc(message,e,n)
print('encrypted message is:',encrypted_message)