import hashlib
import math
import urllib.request, json

from utils import mod_inverse2

def schnorr_verify(signature, publicKey, message, group):
    g = group["generator"]["data"]["value"]
    p = group["p"]
    r = signature["r"]["data"]["value"]
    sigma = signature["sigma"]["value"]
    prime = signature["r"]["data"]["prime"]
    g = int(g, 16)
    p = int(p, 16)
    prime = int(prime, 16)
    r = int(r, 16)
    sigma = int(sigma, 16)
    publicKey = int(publicKey["data"]["value"], 16)

    k = math.ceil(math.log(r, g))
    h = data["hash"]["value"]
    h = int(h, 16)
    # h_inverse = mod_inverse2(h, p)
    lhs = pow(g, sigma, prime) % prime
    rhs = r * pow(publicKey, h, prime) % prime
    print(lhs, rhs)
    return lhs == rhs

import json
web_url = "https://hash-effect.onrender.com/schnorr/sign"
data = None
with urllib.request.urlopen(web_url) as url:
    data = json.loads(url.read().decode())
    print(data)


if schnorr_verify(data['signature'], data['publicKey'], data['message'], data['group']):
  print('The signature is valid.')
else:
  print('The signature is invalid.')
