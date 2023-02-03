from hashlib import sha256
import random
private_key = sha256(str(random.randint(1, 9999999999999999999999999999999999999999999999999999999999999999999999999999999)).encode()).hexdigest()
public_key = sha256(str(private_key).encode()).hexdigest()
with open('my_private_rsa_key', 'w') as f:
    f.write(str(private_key))

with open('my_rsa_public', 'w') as f:
    f.write(str(public_key))
