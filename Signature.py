import math
import random

print("Bienvenue! Ce programme va signer votre message contenu dans le fichier Message.txt\n")

# MD5 Implementation

def leftRotate(value: int, shift: int) -> int:
    """Performs a left rotation (circular shift) on a 32-bit integer."""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def MD5(message: str) -> str:
    """
    Calculates the MD5 hash of the input message.

    Args:
        message (str): The input message to hash.

    Returns:
        str: The hexadecimal representation of the MD5 hash.
    """
    # Initialize constants
    K = [int(abs(math.sin(i + 1)) * 2 ** 32) for i in range(64)]
    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4 # shifts values

    # Convert the message to bytes
    messageBytes = message.encode('utf-8')

    # Initialize state variables
    a, b, c, d = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    # Padding the message
    messageLength = len(messageBytes) * 8
    messageBytes += b'\x80'
    while len(messageBytes) % 64 != 56: # In fact len(messageBytes) * 8 must be equal to 56 * 8 (448) mod 64* 8 = 512
        messageBytes += b'\x00'
    messageBytes += messageLength.to_bytes(8, byteorder='little')

    # Process the message in Blocks of 64 bytes
    for i in range(0, len(messageBytes), 64):
        Block = messageBytes[i:i+64]
        SubBlocks = [int.from_bytes(Block[j:j+4], byteorder='little') for j in range(0, 64, 4)]

        A, B, C, D = a, b, c, d

        for j in range(64):
            if j <= 15:
                F_func = (B & C) | (~B & D)
                g = j
            elif j <= 31:
                F_func = (D & B) | (~D & C)
                g = (5 * j + 1) % 16
            elif j <= 47:
                F_func = B ^ C ^ D
                g = (3 * j + 5) % 16
            else:
                F_func = C ^ (B | ~D)
                g = (7 * j) % 16

            temp = D
            D = C
            C = B
            B = (B + leftRotate(A + F_func + K[j] + SubBlocks[g], s[j])) & 0xFFFFFFFF
            A = temp

        a = (a + A) & 0xFFFFFFFF
        b = (b + B) & 0xFFFFFFFF
        c = (c + C) & 0xFFFFFFFF
        d = (d + D) & 0xFFFFFFFF

    # Concatenate the final state variables to obtain the MD5 hash
    hashMD5 = (a.to_bytes(4, byteorder='little') +
                 b.to_bytes(4, byteorder='little') +
                 c.to_bytes(4, byteorder='little') +
                 d.to_bytes(4, byteorder='little'))

    # Convert the MD5 hash to hexadecimal representation
    hashMD5Hex = ''.join(format(byte, '02x') for byte in hashMD5)

    return hashMD5Hex

# RSA Generation Keys Implementation

def isPrimeMillerRabin(n:int, k:int = 100)-> bool:
    """
    Tests if n is prime using the Miller-Rabin primality test with k iterations.
    This test is based on the fact that if p is an odd prime number, then there exists an integer s and an odd number d such that p-1 = 2^s * d.
    The test consists of choosing a random number a between 2 and p-2, and computing a^d mod p. If this result is equal to 1 or to p-1, then p is probably prime.
    Otherwise, the calculation is repeated by multiplying the result by itself s times, and checking if p-1 is obtained at some point. If not, then p is not prime.
    If yes, then p is probably prime, but there is a small probability that it is a false positive. To reduce this probability, the test can be repeated several times with different values of a.

    Parameters:
        n (int): The number to test for primality. Must be greater than 3 and odd.
        k (int): The number of iterations of the test. Must be positive. Default value is 10.

    Returns:
        bool: True if n is probably prime, False if n is definitely composite.

    Complexity:
        O(k log^3(n)), where k is the number of iterations and n is the number to test.
        This is a polynomial complexity in the size of the number, which means that the computation time increases reasonably with the size of the number.
        This is much faster than deterministic primality testing methods, which have exponential or factorial complexity.

    Probability:
        The probability that a false positive occurs is less than (1/4)^k. For example, with k=10, this probability is less than 10^-6.
    """
    # Check if n is valid
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    # Find s and d such that n-1 = 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    # Repeat the test k times
    for i in range(k):
        # Choose a random number a between 2 and n-2
        a = random.randint(2, n-2)
        # Compute a^d mod n using fast exponentiation
        x = pow(a, d, n)
        # If x is equal to 1 or to n-1, go to the next iteration
        if x == 1 or x == n - 1:
            continue
        # Repeat the calculation by multiplying x by itself s times
        for j in range(s - 1):
            x = pow(x, 2, n)
            # If x is equal to 1, then n is not prime
            if x == 1:
                return False
            # If x is equal to n-1, go to the next iteration
            if x == n - 1:
                break
        else:
            # If no value of x is equal to n-1, then n is not prime
            return False
    # Otherwise, n is probably prime with high probability
    return True

def genPrimeMillerRabin(nbits:int) -> int:
    """
    Generates a random prime number of a given bit size using the Miller-Rabin primality test.

    Parameters:
        bits (int): The bit size of the prime number to generate. Must be positive.

    Returns:
        int: A random prime number of the given bit size.
    """
    while True:
        # Choose a random odd number between 2^(bits-1) and 2^bits - 1
        p = random.randrange(2**(nbits-1) + 1, 2**nbits+3, 2) # The Bretrand thoremen guarantees us to have at least a primer number in this interval
        # Test if n is prime using the miller_rabin function with k=10 iterations
        if isPrimeMillerRabin(p):
            return p

def modInv(a, n):
    """
    Finds the p-inverse of a modulo n where d = a^n, using the extended Euclidean algorithm.
    It returns (u, p), where au = p mod n.
    """
    # Initialize the variables for the algorithm
    u0, u1 = 1, 0 # The coefficients of a
    r0, r1 = a, n # The remainders of the Euclidean algorithm

    # Loop until r1 becomes zero
    while r1 != 0:
        # Compute the quotient and the remainder of r0 and r1
        r0, q, r1 = (r1,) + divmod(r0, r1)

        # Update the values of u0, u1
        u0, u1 = u1, u0 - q * u1

    return (u0, r0)

def genKeysRSA(nbits: int) -> tuple[int, int, int]:
    """
    Generates RSA key pair (public key, private key).

    Args:
        nbits (int): Number of bits for the key size.

    Returns:
        tuple[int, int, int]: (n, e, d) where:
            - n: modulus
            - e: public exponent
            - d: private exponent
    """
    # Generate two distinct prime numbers p and q
    while True:
        p = genPrimeMillerRabin(nbits)
        q = genPrimeMillerRabin(nbits)
        if p != q:
            break

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose a public exponent e such that gcd(phi, e) = 1
    while True:
        e = random.randrange(2, phi)
        d, _ = modInv(e, phi)
        if math.gcd(phi, e) == 1:
            break

    # Ensure d is positive
    if d < 0:
        d += phi

    return n, e, d

def cipherRSA(msg: str, n: int, key: int) -> int:
    """
    Encrypts a message using RSA encryption.

    Args:
        msg (str): The plaintext message.
        n (int): The modulus.
        key (int): The encryption/decryption key (either public or private).

    Returns:
        int: The ciphertext.
    """
    # Convert characters to their ASCII values and pad with zeros
    msg_padded = [str(ord(c)).zfill(3) for c in msg]

    # Determine the block size based on the length of n
    len_block = math.floor(len(str(n)) / 3)

    # Convert padded blocks to integers
    msg_blocks = [int("".join(msg_padded[i : i + len_block])) for i in range(0, len(msg_padded), len_block)]

    # Encrypt each block using modular exponentiation
    msg_cipher = [pow(i, key, n) for i in msg_blocks]

    # Combine ciphertext blocks into a single integer
    return sum([msg_cipher[i] * (n ** i) for i in range(len(msg_cipher))])

# Opening of the message to be signed

with open("Signature/Message.txt", "r") as f:
    message = f.read()

# Message hashing

hashMessage = MD5(message)

print("Message = \n", message)

print("\nMessage haché = \n", hashMessage)

# Generation and saving of the public and private encryption keys

nbits = 1024 # minimum number of bits used to generate the random prime numbers 
n, e, d = genKeysRSA(nbits)

with open("Signature/PublicKey.txt", "w") as f:
    f.write(str(n)+'\n')
    f.write(str(e))
with open("PrivateKey.txt", "w") as f:
    f.write(str(d))

print("\nModulo : n = ", n, "\nClé publique : e = ", e, "\nClé privée : d = ", d, sep = "\n")

# Ciphering and saving of the hashed message

SignedMessage = cipherRSA(hashMessage, n, d)

with open("Signature/SignedMessage.txt", "w") as f:
    f.write(str(SignedMessage))

print("\nMessage signé = \n", SignedMessage)

input("\nTout s'est bien déroulé!\nIl ne vous reste plus qu'à transférer le dossier Signature au destinataire contenant le message, la signature et la clé publique (n, e)")