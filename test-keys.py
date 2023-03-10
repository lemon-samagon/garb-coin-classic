import rsa
(public_key, private_key) = rsa.newkeys(2048)
with open('my_private_key', 'w') as f:
    f.write(str(private_key))

with open('my_public_key', 'w') as f:
    f.write(str(public_key))
