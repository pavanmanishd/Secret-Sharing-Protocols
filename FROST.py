import hashlib
from utils import is_prime, get_prime
import random

public_commitments = dict()
public_sigma = dict()

signing_list = dict()
signing_dict = dict()

class Node:
    def __init__(self, t, g, q, identifier):
        self.identifier = identifier
        self.threshold = t
        self.polynomial_coefficients = [random.randint(0, 5) + 1 for i in range(t)]
        self.g = g
        self.q = q
        self.commitments = self.get_commitments()
        self.p = self.get_p()
        self.k = random.randint(1, self.q - 1)
        self.R = pow(self.g, self.k, self.p)
        self.c = self.get_c()
        self.u = self.get_u(self.c, self.k, self.polynomial_coefficients[0]) % q
        public_commitments[identifier] = self.commitments
        sigma = (self.R, self.u)
        public_sigma[identifier] = sigma
        self.func_values = dict()

    def get_u(self, c, k, a):
        return (k + (c * a))

    def get_c(self):
        return int(hashlib.sha256((str(self.identifier) + str(self.commitments[0]) + str(self.R)).encode()).hexdigest(), 16)

    def get_p(self):
        while True:
            p = 2 * self.q + 1
            if is_prime(p):
                return p
            self.q = get_prime(self.q)

    def get_commitments(self):
        commitment_set = []
        for i in range(self.threshold):
            commitment_set.append(pow(self.g, self.polynomial_coefficients[i], self.q))
        return commitment_set

    def get_func_value(self, x: int) -> int:
        sum = 0
        for i in range(self.threshold):
            sum += (self.polynomial_coefficients[i] * (x ** i)) % self.q
        return sum % self.q

    def store_shares(self, x, value):
        self.func_values[x] = value

    def verify_sigma(self):
        for i in self.func_values.keys():
            R_i, u_i = public_sigma[i]
            try:
                c_i = int(hashlib.sha256((str(i) + str(public_commitments[i][0]) + str(R_i)).encode()).hexdigest(), 16)
                if R_i == pow(self.g, u_i, self.p) * pow(public_commitments[i][0], -c_i, self.p):
                    print("Verified")
                    return True
                else:
                    print("Not Verified")
                    return False
            except:
                print("Not Verified")
                return False
        return True

    def verify_shares(self):
        for i in self.func_values.keys():
            lhs = pow(self.g, self.func_values[i], self.p)
            rhs = 1
            for j in range(self.threshold):
                rhs = (rhs * pow(pow(public_commitments[i][j], i), pow(i, j))) % self.p
            if lhs != rhs:
                print("Not Verified")
                return False
        return True

    def signing_share(self):
        sum = 0
        for i in self.func_values.keys():
            sum = (sum + self.func_values[i])
        self.signing_share = sum % self.q
        return sum % self.q

    def public_verification_share(self):
        self.y = pow(self.g, self.signing_share, self.p)

    def calc_public_verification_share_other_nodes(self, z):
        y0 = 1
        for i in public_commitments.keys():
            for j in range(self.threshold):
                y0 = (y0 * pow(pow(public_commitments[i][j], z), self.k)) % self.p
        return y0

    def lagranges_coeff(self, i, B):
        num = 1
        den = 1
        for j in range(self.threshold):
            if i != j and j in B.keys():
                num *= -j
                den *= (i - j)
        return num * pow(den, -1, self.q)

    def verify_msg(self, signature, S, i, Y):
        msg, B = signature
        binding_val = hash1(i, msg, B)
        R = 1
        r = (B[i][0] * pow(B[i][1], binding_val, self.p)) % self.p
        for j in S:
            R *= (B[j][1] * pow(B[j][1], binding_val, self.p)) % self.p
        c = hash2(R, Y, msg)
        lam = self.lagranges_coeff(i, B)
        z = (signing_dict[i][0][0] + (signing_dict[i][1][0] * binding_val) + (lam * c * self.signing_share)) % self.q
        return z, r, lam, c,R


# def send_msg(signature, S, Y):
#     msg, B = signature
#     z = 0
#     for i in S:
#         z_i, R_i, lam_i, c_i,R = Nodes[i - 1].verify_msg(signature, S, i, Y)
#         z += z_i
#         lhs = pow(Nodes[i - 1].g, z_i, Nodes[i - 1].p)
#         rhs = (R_i * pow(Nodes[i - 1].y, ((c_i) * int(lam_i)), Nodes[i - 1].p)) % Nodes[i - 1].p
#         print(lhs, rhs, z)
#         if lhs != rhs:
#             print("Not Verified")
#             exit()
#         print("Verified Node", i)
#     return z,R,c_i
def send_msg(signature, S, Y):
    msg, B = signature
    z_values = []
    for i in S:
        z_i, R_i, lam_i, c_i, R = Nodes[i - 1].verify_msg(signature, S, i, Y)
        z_values.append((i, pow(Nodes[i - 1].g, z_i, Nodes[i - 1].p), (R_i * pow(Nodes[i - 1].y, (c_i * lam_i), Nodes[i - 1].p)) % Nodes[i - 1].p))
    return z_values


def hash1(i, msg, B):
    return int(hashlib.sha256((str(i) + str(msg) + str(B)).encode()).hexdigest(), 16)


def hash2(R, y, msg):
    return int(hashlib.sha256((str(R) + str(y) + str(msg)).encode()).hexdigest(), 16)

Node1 = Node(3, 2, 11, 1)
Node2 = Node(3, 2, 11, 2)
Node3 = Node(3, 2, 11, 3)
Node4 = Node(3, 2, 11, 4)
Node5 = Node(3, 2, 11, 5)
Nodes = [Node1, Node2, Node3, Node4, Node5]

def main():

    print("Polynomial coeff :")
    for i in range(len(Nodes)):
        print(Nodes[i].polynomial_coefficients)

    print(public_commitments)
    print(public_sigma)

    # verify
    for i in range(0, 5):
        status = Nodes[i].verify_sigma()
        if status == False:
            print("Sigma Verification Failed for Node", i + 1)
            return
        else:
            print("Sigma Verification Successful for Node", i + 1)

    # store func values
    for i in range(0, 5):
        for j in range(0, 5):
            Nodes[i].store_shares(j + 1, Nodes[j].get_func_value(i))

    print(Nodes[0].func_values)
    print(Nodes[1].func_values)
    print(Nodes[2].func_values)
    print(Nodes[3].func_values)
    print(Nodes[4].func_values)

    # private signing share
    for i in range(0, 5):
        sum = Nodes[i].signing_share()
        print("Signing Share for Node", i + 1, "is", sum)

    # public verification share
    for i in range(0, 5):
        Nodes[i].public_verification_share()

    # group's public verification share
    Y = 1
    for i in public_commitments.keys():
        Y = (Y * public_commitments[i][0]) % Nodes[0].p
    print("Group's Public Verification Share is", Y)

    # calc public verification share for other nodes
    print("Node 4's public key calc from Node 3 is: " + str(Node3.calc_public_verification_share_other_nodes(4)))

    pi = 1
    for i in range(0, 5):
        d = random.randint(1, Node1.q - 1)
        e = random.randint(1, Node1.q - 1)
        D = (Node1.g ** d) % Node1.p
        E = (Node1.g ** e) % Node1.p
        signing_dict[i + 1] = ((d, D), (e, E))
        signing_list[i + 1] = (D, E)

    print(signing_list)
    print(signing_dict)

    # signing
    SA = Node(3, 2, 11, 6)

    alpha = 3
    S = list(range(1, alpha + 1))
    message = "Team 1o1"
    B = dict()
    for i in S:
        temp = (signing_list[i][0], signing_list[i][1])
        B[i] = temp
    print(B)

    signature = (message, B)
    z_values = send_msg(signature, S, Y)
    print(z_values)

    for i, lhs, rhs in z_values:
        print(f"Node {i} - lhs: {lhs}, rhs: {rhs}")
        if lhs != rhs:
            print("Not Verified")
            exit()

    print("Verified")

if __name__ == "__main__":
    main()
