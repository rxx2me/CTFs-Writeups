import socket
import binascii

HOST = "pad.ctf.intigriti.io"
PORT = 1348

def recv_until(sock, delimiter):
    data = b""
    while delimiter not in data:
        data += sock.recv(1024)
    return data

def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def reverse_check_cat_box(ciphertext, cat_state):
    c = bytearray(ciphertext)
    if cat_state == 1:
        for i in range(len(c)):
            c[i] ^= 0xAC
            c[i] = (c[i] >> 1) & 0xFF
    else:
        for i in range(len(c)):
            c[i] ^= 0xCA
            c[i] = ((c[i] << 1) | (c[i] >> 7)) & 0xFF
    return bytes(c)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        welcome_msg = recv_until(s, b"Anyway, why don't you try it for yourself?\n")
        print(welcome_msg.decode())

        encrypted_flag_hex = welcome_msg.split(b"Encrypted (cat state=ERROR! 'cat not in box'): ")[1].split(b"\n")[0]
        encrypted_flag = bytes.fromhex(encrypted_flag_hex.decode())

        known_plaintext = b"A" * 160
        s.sendall(known_plaintext + b"\n")

        response = recv_until(s, b"\n")
        cat_state_str = response.split(b"Encrypted (cat state=")[1].split(b"): ")[0]
        encrypted_known_hex = response.split(b"): ")[1].split(b"\n")[0]
        encrypted_known = bytes.fromhex(encrypted_known_hex.decode())

        cat_state = 1 if b"alive" in cat_state_str else 0

        decrypted_known = reverse_check_cat_box(encrypted_known, cat_state)
        key = xor_bytes(decrypted_known, known_plaintext)

        decrypted_flag = xor_bytes(encrypted_flag, key)
        print(f"Decrypted Flag: {decrypted_flag.decode(errors='ignore')}")

if __name__ == "__main__":
    main()
