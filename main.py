'''
Sources:

Last Names obtained from: https://github.com/arineng/arincli/blob/master/lib/last-names.txt then modified to be not all caps
First, Middle Names from: https://github.com/dominictarr/random-name/blob/master/first-names.txt 
Adjectives from: https://gist.github.com/hugsy/8910dc78d208e40de42deb29e62df913 
Nouns from: https://github.com/hugsy/stuff/blob/main/random-word/english-nouns.txt 

Implementation based on: https://www.cs.toronto.edu/~david/course-notes/csc110-111/08-cryptography/05-rsa-cryptosystem-implementation.html
'''

#Code to modify the last names file
'''
with open(f'last-names.txt', 'r') as f:
    names = f.readlines()

for i in range(len(names)):
    names[i] = names[i].capitalize()

with open(f'last-names.txt', 'w') as f:
    for name in names:
        f.write(name)
'''

#Imports
import random
import math
# random.seed(69)

def RSA_key_generation(p = None, q = None):
    #Use primes to generate RSA keys - I just used two randomly generated 32-bit ones to speed up computation a bit

    #Select some defaults if nothing passed in
    if p is None:
        p = 73
    if q is None:
        q = 131
    
    #Compute the prime product that is used in the public key
    n = p * q

    #Compute the Euler totient. Since p,q are primes, this is easy
    phi = (p - 1) * (q - 1)

    #Now find a number coprime with the totient. Use the common initial guess of 2^16 + 1
    if phi > 2 ** 16 + 1:
        e = 2 ** 16 + 1
    else:
        e = random.randint(2, phi)
    
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi)

    #After this, find the modular inverse which is our private key exponent
    d = pow(e, -1, phi)

    private_key = {'p': p, 'q': q, 'd': d}
    public_key = {'n': n, 'e': e}
    return private_key, public_key

def RSA_key_encryption(public_key, first_name, last_name):
    n, e = public_key['n'], public_key['e']
    encrypted_str = ''
    encrypted_nums = []

    for letter in f'{first_name},{last_name}':
        encrypted_nums.append((ord(letter) ** e) % n)
        encrypted_str += chr((ord(letter) ** e) % n)
    
    return encrypted_str, encrypted_nums

def generate_username(encrypted_nums):
    #This has several issues related to hashing conflicts, but I need a hotfix
    username = ''
    with open('adjectives.txt', 'r') as f:
        username += f.read().splitlines()[encrypted_nums[0] % 1437].capitalize() #there are 1437 adjectives
    with open('nouns.txt', 'r') as f:
        username += f.read().splitlines()[encrypted_nums[-1] % 1525].capitalize() #there are 1525 nouns
    return username

def random_guess(first_name, last_name):
    with open('first-names.txt', 'r') as f:
        first_names = f.read().splitlines()
    with open('last-names.txt', 'r') as f:
        last_names = f.read().splitlines()
    
    guess_count = 0
    found = False
    first_name_guess, last_name_guess = '', ''

    while not found and guess_count < 10000:
        if first_name == first_name_guess and last_name == last_name_guess: 
            found = True
            print(f'Found in {guess_count} guesses!')
            break
        else:
            first_name_guess = random.choice(first_names)
            last_name_guess = random.choice(last_names)
            guess_count += 1
    if guess_count >= 10000: 
        print(f'Username not found by random guessing with 100 000 guesses...')
    return


if __name__ == "__main__":
    #Pick a random first name and random last name for our patient
    with open('first-names.txt', 'r') as f:
        first_name = random.choice(f.read().splitlines())

    with open('last-names.txt', 'r') as f:
        last_name = random.choice(f.read().splitlines())

    # print(f'Patient name is {first_name} {last_name}')
    private_key, public_key = RSA_key_generation()
    encrypted_str, encrypted_nums = RSA_key_encryption(public_key, first_name, last_name)

    username = generate_username(encrypted_nums)

    print(f'Patient name is {first_name} {last_name}')
    print(f'Username is {username}')

    random_guess(first_name, last_name)