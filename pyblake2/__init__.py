import struct

SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0],
]

IV = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
]

uint64 = lambda n: n & ((1<<64)-1)

def rotate_right(n, bits, width=64):
    return uint64(n << (width-bits)) | (n >> bits)

def compress(chain, msg, counter, last):
    v = chain + IV[:4] + [counter[0] ^ IV[4], counter[1] ^ IV[5],
                          last[0] ^ IV[6], last[1] ^ IV[7]]

    def g_function(index, round_, a, b, c, d):
        j = SIGMA[round_%10][2*index]
        k = SIGMA[round_%10][2*index+1]
        v[a] = uint64(v[a] + v[b] + msg[j])
        v[d] = rotate_right(v[d]^v[a], 32)
        v[c] = uint64(v[c] + v[d])
        v[b] = rotate_right(v[b]^v[c], 24)
        v[a] = uint64(v[a] + v[b] + msg[k])
        v[d] = rotate_right(v[d]^v[a], 16)
        v[c] = uint64(v[c] + v[d])
        v[b] = rotate_right(v[b]^v[c], 63)

    for round_ in xrange(12):
        g_function(0, round_, 0, 4, 8, 12)
        g_function(1, round_, 1, 5, 9, 13)
        g_function(2, round_, 2, 6, 10, 14)
        g_function(3, round_, 3, 7, 11, 15)
        g_function(4, round_, 0, 5, 10, 15)
        g_function(5, round_, 1, 6, 11, 12)
        g_function(6, round_, 2, 7, 8, 13)
        g_function(7, round_, 3, 4, 9, 14)

    return map(lambda h, v1, v2: h ^ v1 ^ v2, chain, v[:8], v[8:])

class Blake2b(object):
    params = struct.Struct("< 4B L Q 2B 14s 16s 16s")
    as_chain = struct.Struct("< 8Q")
    as_msg = struct.Struct("< 16Q")
    pad = struct.Struct("< 128s")
    blen = 128

    def __init__(self, digest_length=64, key=None, salt=None, personal=None):
        b = self.params.pack(digest_length, 0, 1, 1, 0, 0, 0, 0, "", "", "")
        self.chain = map(lambda p, iv: p^iv, self.as_chain.unpack(b), IV)

    def __call__(self, s):
        pos, counter = 0, [0, 0]
        penultimate = (len(s)-1) / self.blen * self.blen

        while pos < penultimate:
            msg = self.as_msg.unpack(s[pos:pos+self.blen])
            counter[0] = uint64(counter[0] + self.blen)
            counter[1] += uint64(counter[0] < self.blen)
            self.chain = compress(self.chain, msg, counter, (0, 0))
            pos += self.blen

        msg = self.as_msg.unpack(self.pad.pack(s[pos:]))
        counter[0] = uint64(counter[0] + len(s[pos:]))
        counter[1] += uint64(counter[0] < len(s[pos:]))
        self.chain = compress(self.chain, msg, counter, (uint64(-1), 0))
        return self.chain

def hexstr(s):
    return "".join("%02x" % ord(c) for c in s)

def blake2(s):
    checksum = Blake2b()(s)
    return hexstr(struct.pack("< 8Q", *checksum))

if __name__ == "__main__":
    print blake2('tm'*521521)
