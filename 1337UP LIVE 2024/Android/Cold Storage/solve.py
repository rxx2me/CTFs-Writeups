def hex_to_bytes(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

def reverse_string(s):
    return s[::-1]

def keygen():
    hex_str = '9425749445e494332757363353f5d6f50353b79445d7336343270373270366f586365753f546c60336f5'
    parts = [
        hex_str[0:14], hex_str[14:28], hex_str[28:42],
        hex_str[42:56], hex_str[56:70], hex_str[70:84]
    ]
    reordered_parts = [parts[3], parts[5], parts[1], parts[4], parts[2], parts[0]]
    reversed_hex = reverse_string(''.join(reordered_parts))
    bytes_data = hex_to_bytes(reversed_hex)
    a, b, xor_key = 9, 7, 51
    decrypted_bytes = [(a * byte + b) % 256 ^ xor_key for byte in bytes_data]
    flag = ''.join(f'{byte:02x}' for byte in decrypted_bytes)
    return flag

def affine_decrypt(byte, a_inverse, b):
    return (a_inverse * (byte - b)) % 256

def decrypt_flag(encrypted_hex):
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    a = 9
    b = 7
    xor_key = 51
    a_inverse = pow(a, -1, 256)
    decrypted_bytes = [(affine_decrypt(byte ^ xor_key, a_inverse, b)) for byte in encrypted_bytes]
    return bytes(decrypted_bytes).decode('utf-8')

encrypted_hex = keygen()
flag = decrypt_flag(encrypted_hex)
print(flag)
