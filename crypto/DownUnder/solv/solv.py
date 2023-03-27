from sage.all import *
import random
import hashlib
import hmac
import requests
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes


session = requests.Session()

GLOB_URL = "https://down-under-tlejfksioa-ul.a.run.app/"

resp = session.get(url = GLOB_URL, params = {'A':1})
p = int(resp.json()["p"])
q = int(resp.json()["q"])
g = int(resp.json()["g"])

B = 0
j = (p-1) // q

key = {
    '0' : 0 , '1' : 1 , '2' : 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 ,
    'a' : 70, 'b' : 71, 'c' : 72, 'd' : 73, 'e' : 74, 'f' : 75, 'g' : 76, 'h' : 77, 'i' : 78, 'j' : 79, 
    'k' : 80, 'l' : 81, 'm' : 82, 'n' : 83, 'o' : 84, 'p' : 85, 'q' : 86, 'r' : 87, 's' : 88, 't' : 89, 
    'u' : 90, 'v' : 91, 'w' : 92, 'x' : 93, 'y' : 94, 'z' : 95, '_' : 96, '{' : 97, '}' : 98, '!' : 99, 
}

def long_to_bytes_flag(long_in):
    new_map = {v: k for k, v in key.items()}
    list_long_in = [int(x) for x in str(long_in)]
    str_out = ''
    i = 0
    while i < len(list_long_in):
        if list_long_in[i] < 7:
            str_out += new_map[list_long_in[i]]
        else:
            str_out += new_map[int(str(list_long_in[i]) + str(list_long_in[i + 1]))]
            i += 1
        i += 1
    return str_out.encode("utf_8")

def f(y, k):
    return  Integer(pow(2, (y.mod(k)), p))

def tame(g, b, k):
    N = 0
    for i in range(k):
        N += f(Integer(i), k + 1)
    N //= k + 1
    N *= 4
    print("N: ", N)
    xT = 0
    yT = pow(g, b, p)
    for i in range(N):
        xT = xT + f(Integer(yT), k)
        yT = (yT * pow(g, f(Integer(yT), k), p)) % p
    return xT, yT


def wild(g, y, a, b):
    k = floor(log(sqrt(b-a), 2) + log(log(sqrt(b-a), 2), 2) - 2)
    xT, yT = tame(g, b, k)
    xW = 0
    yW = y
    while xW < (b - a + xT):
        fVal = f(Integer(yW), k)
        xW = xW + fVal
        yW = (yW * pow(g, fVal, p)) % p
        if yW == yT:
            return b + xT - xW
    return 0

a = 2
r_list = []
bound = 1 << 16
print(j)
while a < bound:
    a = trial_division(j, bound=bound)
    if a == 1:
        break
    r_list.append(a)
    j //= a

r_i = []
b_i = []
total = 1

r_list.pop()

for (r) in r_list:
    print("r: ", r)
    A = 1
    while A == 1:
        ra = random.randint(1, p)
        o = int((p-1)/r)
        A = pow(ra, o, p)
    query = {'A':A, 'id': id, 'p': p, 'q': q, 'g': g }
    resp = session.get(url = GLOB_URL, params = query).json()
    B = resp["B"]
    target = resp["hmac"]
    message = b'My totally secure message to Alice'
    i = int(1)
    first_guess = long_to_bytes(int(pow(A, i, p)))
    guess = 0
    my_hmac = hmac.new(message, first_guess, hashlib.sha256)
    while int(target) != bytes_to_long(my_hmac.digest()) and first_guess != guess and i <= r:
        i += int(1)
        guess = pow(A, i, p)
        my_hmac = hmac.new(msg=message, key=long_to_bytes(int(guess)), digestmod=hashlib.sha256)
    if i > r:
        continue
    r_i.append(Integer(r))
    b_i.append(Integer(i % r))
    total *= r
    if total > q:
        break
    print("r_i: ", r_i)
    print("b_i: ", b_i)
    print("total", total)
    print("q:", q)

sol = CRT_list(b_i, r_i)
if total < q:
    n, r =  sol, total
    NEWB = B * pow(g, -n, p) % p
    NEWG = pow(g, r, p)
    i = 0  # infimum
    s = floor((q-1)/r)  # supremum
    a = wild(NEWG, NEWB, i, s)
    sol = a * r + n

try:
    print(long_to_bytes_flag(sol).decode('utf-8').strip())
except UnicodeDecodeError:
    print(long_to_bytes_flag(sol))
