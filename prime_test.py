from utils import prime_field, prime_field_group, mod_inverse, mod_inverse2, field_prime_value

n1 = int(input("Enter a prime number: "))
print('Prime field: ', prime_field(n1))

g = int(input("Enter a generator: "))
n2 = int(input("Enter a prime number: "))
print('Prime field group: ', prime_field_group(g, n2))

# print(field_prime_value(-1/3, 11))

a = float(input("Enter a number: "))
p = int(input("Enter a prime number: "))
print('Field prime value: ', field_prime_value(a, p))
