#!/usr/bin/python3
# Alice c3eb8407c7a92004ee28611da0e6b213dc1eadbbe28b545083de5834a66ff381
# Bob   9aa4c713bae9614e47ef86ab58cc335d624272aab728244ac5a3b223f0db1dd5

def pohlig_hellman_base2(result, base, modulus):
	result_powers = []
	power = 0
	while result != 1:
		result_powers.append(result)
		result = result * result % modulus
		power += 1
	result_powers.append(1)
	shift = 0
	result = pow(base, 2 ** power, modulus)
	while result != 1:
		result = result * result % modulus
		shift += 1
	result = 0
	while power > 0:
		power -= 1
		if result_powers[power] != pow(base, result * (2 ** power), modulus):
			result += 2 ** shift
		shift += 1
	return result

base = 5
modulus = 2 ** 258

file = open("output.txt")
alice_public_result = int(file.readline(), 16)
bob_public_result = int(file.readline(), 16)

alice_private_exponent = pohlig_hellman_base2(alice_public_result * 4 + 1, base, modulus)
# bob_private_exponent = pohlig_hellman_base2(bob_public_result, base, modulus)
print((pow(bob_public_result * 4 + 1, alice_private_exponent, modulus) // 4).to_bytes(32, 'big').decode('ascii'))