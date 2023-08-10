import urllib.request, json

def read_data(web_url):
    with urllib.request.urlopen(web_url) as url:
        data = json.loads(url.read().decode())
        print(data)
        return data



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

json_data = read_data("https://hash-effect.onrender.com/sss/shares")
p = int(json_data["shares"][0]["value"]["prime"],16)
n = int(json_data["n"])
k = int(json_data["k"])
shares = []
for share in json_data["shares"]:
    index = share["index"]
    value = int(share["value"]["value"],16)
    shares.append((index,value))

reconstructed_secret = secret(shares, p)
print("Reconstructed Secret:", reconstructed_secret)