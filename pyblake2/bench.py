from pyblake2 import Blake2b

b = Blake2b()
payload = ''.join(chr(i) for i in xrange(256)) * 4000

b(payload)
