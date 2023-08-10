def reconstruct(shares, prime):
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

def secret(shares, prime):
    return reconstruct(shares, prime)

def input_shares(k:int):
    shares = []
    for _ in range(k):
            x = int(input("Enter index: "))
            y = int(input("Enter value(HEX): "),16)
            shares.append((x, y))
    return shares

# Example usage:
p = int(input("Enter the prime number(HEX):"),16)
k = int(input("Enter the threshold value:"))
# Get shares from the user
shares = input_shares(k)

# Cracking the secret
reconstructed_secret = secret(shares, p)
print("Reconstructed Secret(HEX):", reconstructed_secret)