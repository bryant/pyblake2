from pyblake2 import Blake2b, hexstr
import struct
import pytest

def test_blake2b_nokey():
    from fixtures import unkeyed_checksums

    inp = "".join(chr(i) for i in xrange(256))
    for n in xrange(len(inp)):
        assert hexstr(struct.pack("< 8Q", *Blake2b()(inp[:n]))) == \
               unkeyed_checksums[n].lower()

if __name__ == "__main__":
    pytest.main()
