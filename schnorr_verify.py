# Description: This program will generate a Schnorr signature and verify it using the Hash Effect API.


import json
import random
import hashlib
import requests



def set_values():
    private_key = random.choice(primes)

    generator = random.choice(primes[:primes.index(private_key)])
    public_key = pow(generator, private_key, primes[-1])

    prime = random.choice(primes)
    p = random.choice(primes)
    k = random.choice(primes[:primes.index(p)])
    return private_key, generator, public_key, prime, p, k

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307]
def get_small_hash(message):
    full_hash = hashlib.sha256(message.encode()).hexdigest()
    small_hash = full_hash[:8]  
    return int(small_hash, 16)

def encrypt_message(message, private_key, generator, prime, p):
    z = random.choice(primes)

    R = (pow(generator, z, prime), pow(generator, z, p))

    message_hash = get_small_hash(message)
    s = (message_hash + private_key * R[0]) % prime
    v = (R[0] - s * generator) % prime

    return R, s, v

def main():
    private_key, generator, public_key, prime, p, k = set_values()
    message = input("Enter a message: ")

    R, s, v = encrypt_message(message, private_key, generator, prime, p)
    r = pow(generator, k)

    api_body = {
        "group": {
            "generator": {
                "tag": "prime",
                "data": {
                    "value": str(hex(generator)),
                    "prime": str(hex(prime))
                }
            },
            "p": str(p)
        },
        "hash": {
            "value": hashlib.sha256(message.encode()).hexdigest(),
            "prime": str(hex(prime))
        },
        "message": message,
        "publicKey": {
            "tag": "prime",
            "data": {
                "value": str(hex(public_key)),
                "prime": str(hex(prime))
            }
        },
        "signature": {
            "r": {
                "tag": "prime",
                "data": {
                    "value": str(hex(r)),
                    "prime": str(hex(prime))
                }
            },
            "sigma": {
                "value": str(hex(s)),
                "prime": str(hex(prime))
            }
        }
    }

    # Print the API request body
    print(json.dumps(api_body, indent=4))

    # Make the API request
    url = "https://hash-effect.onrender.com/schnorr/verify"
    response = requests.post(url, json=api_body)

    # Check if the signature is valid
    if response.status_code:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")

if __name__ == "__main__":
    main()
