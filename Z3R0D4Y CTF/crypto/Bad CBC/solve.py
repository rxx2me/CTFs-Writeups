from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# The known part of the key
known_key_part = b"kjceucr74bc843"

# Correct IV with 16 bytes
IV = b"foeyf93nvlwitksu"

# The ciphertext
ciphertext = binascii.unhexlify("edd33e67670056d1ea1ac21ce0cf12d6f24627bef750a4614d64f05e7b76fe7cfdd6761c55fadbee2e76e4ce629c94f4")

# Function to decrypt using the key
def decrypt_with_key(key):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()  # If the text is readable, return it as a string
    except Exception as e:
        return None  # If there is an error, return None

# Brute force the last two characters of the key
for i in range(256):
    for j in range(256):
        # The last two characters of the key are tested from "00" to "zz"
        key = known_key_part + bytes([i]) + bytes([j])  # Try all possibilities
        plaintext = decrypt_with_key(key)
        if plaintext and plaintext.startswith("zeroday"):  # Stop if text starts with "zeroday"
            print(f"The correct key is: {key}")
            print(f"The plaintext: {plaintext}")
            exit(0)  # Exit if the correct key is found

print("The correct key was not found.")
