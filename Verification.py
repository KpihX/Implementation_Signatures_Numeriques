import math

print("Ce script python vise à vérifier si le message reçu se trouvant dans Signature n'a pas été altéré en chemin!")

# Functions used in the program

def decipherRSA(ciphertext: int, n: int, key: int) -> str:
    """
    Decrypts an RSA ciphertext using the private key.

    Args:
        ciphertext (int): The encrypted message.
        n (int): The modulus.
        key (int): The decryption key (private exponent).

    Returns:
        str: The original plaintext message.
    """
    # Extract individual digits from the ciphertext
    msg_cipher = []
    while ciphertext != 0:
        ciphertext, remainder = divmod(ciphertext, n)
        msg_cipher.append(remainder)

    # Decrypt each block using modular exponentiation
    msg_block = [str(pow(i, key, n)) for i in msg_cipher]

    # Convert blocks back to characters
    msg_padded = []
    for block in msg_block:
        block_padded = []
        for i in range(len(block), 3, -3):
            block_padded.append(chr(int(block[i - 3 : i])))
        block_padded.append(chr(int(block[: i - 3])))
        msg_padded.extend(reversed(block_padded))

    return "".join(msg_padded)

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

# Loading of the signed message, the public key and the message itself

with open("Signature/SignedMessage.txt", "r") as f:
    signedMessage = int(f.read())

with open("Signature/PublicKey.txt", "r") as f:
    n = int(f.readline())
    e = int(f.readline())

with open("Signature/Message.txt", "r") as f:
    message = f.read()


# Deciphering of the signed message

ReceivedhashMessage = decipherRSA(signedMessage, n, e)

# Received message hashing

hashMessage = MD5(message)

# Results

print("\nMessage signé = \n", signedMessage)

print("\nMessage reçu = \n", message)

print("\nMessage haché reçu = \n", ReceivedhashMessage)

print("\nMessage reçu haché = \n", hashMessage)

if ReceivedhashMessage == hashMessage:
    print("\nVérification réussie! Le message n'a pas été altéré. Vous pouvez le lire en toute quiétude!")
else:
    print("\nEchec de la vérification! Le message a été altéré! Veuillez démander qu'on vous le renvoie!")

input("\nRavi de vous avoir servi!")
