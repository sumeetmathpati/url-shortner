import hashlib
import string

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)
tiny_to_long = {}

def convert_to_base(x):

        result = []
        while x:
            x, r = divmod(x, BASE)
            result.append(ALPHABET[r])
        return ''.join(result)


def encode(longUrl):
        """Encodes a URL to a shortened URL.

        :type longUrl: str
        :rtype: str
        """
        sha256_hash = hashlib.md5(longUrl.encode('utf8')).hexdigest()

        # sha256_hash has 32 bytes
        # get 3 slices and xor them so we end up with a shorter URL suffix of len 8
        size = len(sha256_hash)

        p = sha256_hash[0:8]
        q = sha256_hash[8:16]
        r = sha256_hash[16:24]
        s = sha256_hash[24:32]

        # print('p: ', p)
        # print('q: ', q)
        # print('r: ', r)
        # print('s: ', s)

        p_as_int = int(p, 16)
        q_as_int = int(q, 16)
        r_as_int = int(r, 16)
        s_as_int = int(s, 16)

        xored = p_as_int ^ q_as_int ^ r_as_int ^ s_as_int

        tiny_url = convert_to_base(xored)
        if tiny_url not in tiny_to_long:
            tiny_to_long[tiny_url] = longUrl

        return tiny_url
    
def decode(shortUrl):
        """Decodes a shortened URL to its original URL.

        :type shortUrl: str
        :rtype: str
        """
        return tiny_to_long.get(shortUrl)

