# Trivial case of Hill's Cipher, which is a linear cipher
k = 'heyiamworldfuturestarandilikeclimbinghillsandshow'
import numpy as np
import string
import random

LETTER_MAP = {n: c for n, c in zip(range(26), string.ascii_lowercase)}
NUMBER_MAP = {char: n for n, char in LETTER_MAP.items()}

def enc(k, m):
    assert(int(len(k) ** 0.5) == len(k) ** 0.5)
    k = [NUMBER_MAP[c] for c in k]
    l = int(len(k) ** 0.5)
    k_m = np.array([[*row] for row in [k[i*l:(i+1)*l] for i in range(len(k) // l)]])

    m = np.array([[*row] for row in [m[i*l:(i+1)*l] for i in range(len(m) // l)]])

    full_c = ''

    for block in m:
        # Treats each message block and each cipher block as a column vector
        c_m = np.dot(k_m, np.array([NUMBER_MAP[char] for char in block])) % 26
        # Row vectors in message and cipher are hence actually column vectors
        full_c += ''.join([LETTER_MAP[n] for n in c_m])

    return full_c

m = ''.join([random.choice(string.ascii_lowercase) for _ in range(123)])
c = enc(k, m)


# Can you find k? FLAG: grifflesCTF{k}
m = 'XXXXXXXXXXXXXXXXXXXzeamicbubntdxppdtqstvpqrheeckyyoriozlncxkuvibdlhfqizxqypzshxanbhbfchtbnsbqgwknhxnsujsozjsuwsizqjezyixiqx' # X is redacted plaintext
c = 'lazehvupjgzwujqytkkrayuwnmdftztbgolnuvpvfnnnfjudzqefhgkbpbqtmdbfcebptjficsfxsnqvmxxkfnxagcmzdhkzeodqommqkzfbrqbvpijibdg'

''' SOLUTION '''
from cryptonita.mod import inv_matrix

def solve(m, c):
    '''
    Resources:
    http://practicalcryptography.com/ciphers/hill-cipher/
    https://book-of-gehn.github.io/articles/2019/01/02/Break-Hill-Cipher-with-a-Known-Plaintext-Attack.html
    '''

    '''
    Length of c is 119 (7 * 13) so l = 7 or l = 13. But if l = 13, we don't have enough plaintext, so let's try l = 7.
    '''
    l = 7

    # Trim m to start on the block for the first fully known multiple of l
    known_m = m[21:] # hardcoded here

    # Inverse may not exist for every block, so we try blocks until an inverse is found
    for offset in [i * l for i in range(len(known_m) // l)]:
        m_block = known_m[offset:l**2 + offset]
        at = m.find(m_block)
        partial_ct = c[at:at + l**2]

        c_lst = [NUMBER_MAP[char] for char in partial_ct]
        m_lst = [NUMBER_MAP[char] for char in m_block]

        c_mat = []
        m_mat = []
        for i in range(l):
            c_mat.append(c_lst[l * i:(i+1) * l])
            m_mat.append(m_lst[l * i:(i+1) * l])

        # Recall column vectors are represented in row vector form in the encryption process
        c_mat = np.array(c_mat).T
        m_mat = np.array(m_mat).T
        
        try:
            i_m_mat = inv_matrix(m_mat, 26)
            print(f"Inverse of m found for block {offset}")
            is_found = True
            break
        except ZeroDivisionError:
            # No inverse exists
            continue

    if not is_found:
        # No inverse exists for all blocks
        return "Inverse of m not found"

    k_mat = np.dot(c_mat, i_m_mat) % 26
    k = ''.join([LETTER_MAP[char] for char in k_mat.flatten().tolist()])
    
    return k

flag = solve(m, c)
print("FLAG:", flag)

