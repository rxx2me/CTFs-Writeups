def g_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def decrypt(msg, key):
    decrypted_text = []
    key = g_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('A'))
        elif char.islower():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)

# Encrypted flag
encrypted_flag = "zhdwqmj{CPro5khGjcezVyag}"

# Read passwords from the file
password_file = 'phished.txt'  # Update this path if necessary

# Open the file and read passwords
with open(password_file, 'r') as file:
    passwords = file.readlines()

# Strip extra whitespace from each password
passwords = [password.strip() for password in passwords]

# Try each password to find the one that decrypts the flag correctly
correct_password = None
for password in passwords:
    try:
        decrypted_flag = decrypt(encrypted_flag, password)
        if decrypted_flag.startswith("zeroday"):
            correct_password = password
            break
    except Exception:
        pass  # Skip any decryption errors

# Display the result
if correct_password:
    print(f"Correct password: {correct_password}")
    print(f"Decrypted flag: {decrypted_flag}")
else:
    print("No correct password found.")
