from get_data_vss import get_data
from utils import field_prime_value


def validate(index, value, commitments, g, p, p1):
    val_value = pow(g, value, p1)
    product = 1

    for i, j in enumerate(commitments):
        product = (product * pow(j, index ** i, p1)) % p1

    val_value = field_prime_value(val_value, p1)
    product = field_prime_value(product, p1)

    print(val_value, product)
    return val_value == product

if __name__ == "__main__":
    url_valid = 'https://hash-effect.onrender.com/vss/share/valid'
    url_invalid = 'https://hash-effect.onrender.com/vss/share/invalid'

    index, value, commitments, g, p, p1 = get_data(url_valid).values()

    is_valid = validate(index, value, commitments, g, p, p1)
    print("Is Valid:", is_valid)
