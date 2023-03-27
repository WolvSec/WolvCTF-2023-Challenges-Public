from Crypto.Util.number import *
import math
from random import randint


def get_prime(limit, difficulty, smoothness=16):
    p = 1

    # In reality we only need 2 primes to make this work
    # but we need more to make it harder to solve
    # to prevent brute force factorization
    q_1 = getPrime(difficulty)
    q_2 = getPrime(difficulty) 
    q_3 = getPrime(difficulty)
    q_4 = getPrime(difficulty)
    q_5 = getPrime(difficulty)
    q_6 = getPrime(difficulty)

    p_factors = [2, q_1, q_2, q_3, q_4, q_5, q_6]

    p_minus_one_pt1 = math.prod(p_factors)

    while True:
        prime1 = getPrime(smoothness)
        prime2 = getPrime(smoothness)
        prime3 = getPrime(smoothness)
        prime4 = getPrime(smoothness)
        prime5 = getPrime(smoothness)
        prime6 = getPrime(smoothness)
        p_minus_one_pt2 = p_minus_one_pt1 * prime1 * prime2 * prime3 * prime4 * prime5 * prime6
        if len(bin(p_minus_one_pt2)) > limit:
            smoothness -= 1
            continue
        if isPrime(p_minus_one_pt2 + 1):
            p_factors.append(prime1)
            p_factors.append(prime2)
            p_factors.append(prime3)
            p_factors.append(prime4)
            p_factors.append(prime5)
            p_factors.append(prime6)
            p = p_minus_one_pt2 + 1
            break

    p_factors.sort()

    return (p, max(q_1, q_2, q_3, q_4, q_5, q_6), p_factors)

def generate():
    difficulty = 136  # Increase this to make the challenge harder and allow longer flags. Be warned it blows up quickly.
    p, q, _ = get_prime(4096, difficulty, 16)
    g = 1
    while g == 1:
        g = pow(randint(2, p - 1), math.floor(p - 1/q), p)
    return p, q, g
