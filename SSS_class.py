import random
from utils import field_prime_value, get_prime, mod_inverse

class SSS():
    def __init__(self,secret:int, n:int, k:int):
        self.secret = secret
        self.n = n
        self.k = k
        self.p = get_prime(self.secret)
        self.polynomial_coefficients = [secret] + [random.randint(0, self.p-1) for i in range(k-1)]

    def get_func_value(self, x: int) -> int:
        return sum([self.polynomial_coefficients[i] * (x ** i) for i in range(self.k)])
    
    def shares(self) -> dict:
        share_set = dict()
        for i in range(self.n):
            share_set[i+1] = field_prime_value(self.get_func_value(i+1), self.p)
        return share_set          
    
    def reconstruct_from_all(self, shares: dict) -> int:
        if len(shares) < self.k:
            print("Secret cannot be reconstructed")
            return None
        s = 0
        for i in shares.keys():
            numerator = 1
            denominator = 1
            for j in shares.keys():
                if i != j:
                    numerator *= -j
                    denominator *= i - j
            if denominator == 0:
                continue
            s += shares[i] * numerator * mod_inverse(denominator, self.p)
        return field_prime_value(s, self.p)
    
    def reconstruct(self, shares, prime):
        def interpolate(x, shares, prime):
            result = 0
            for i in range(len(shares)):
                xi, yi = shares[i]
                numerator, denominator = 1, 1
                for j in range(len(shares)):
                    if i != j:
                        xj, yj = shares[j]
                        numerator = (numerator * (x - xj)) % prime
                        denominator = (denominator * (xi - xj)) % prime
                result = (result + (numerator * pow(denominator, -1, prime) * yi)) % prime
            return result

        return interpolate(0, shares, prime)

    def reconstruct_secret(self, shares, prime):
        return self.reconstruct(shares, prime)

def input_shares(k:int):
    shares = []
    for i in range(k):
        x = input("Enter index: ")
        if not x.isnumeric():
            break
        y = input("Enter value: ")
        if not y.isnumeric():
            break
        shares.append((int(x), int(y, 16)))
    return shares