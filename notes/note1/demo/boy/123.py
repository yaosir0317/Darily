import binascii
import os


a = binascii.hexlify(os.urandom(20))

print(a.decode())