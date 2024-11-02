# Chemical elements data with atomic numbers for elements used in the sequence
elements_data = {
    "Te": 52, "Sb": 51, "I": 53, "La": 57, "Sn": 50, "No": 102, "Cs": 55, "Dy": 66,
    "Cd": 48, "Ba": 56, "Yb": 70, "Xe": 54, "Ho": 67, "Fm": 100, "Md": 101, "Er": 68,
    "In": 49
}

# Challenge code
challenge_code = "TeSbILaTeSnTeNoISnTeCsCsDyICdTeIISnTeLaSbCdTeTeTeLaTeSbINoTeSbSbInICdTeBaSbSbISnIYbSbCdTeXeINoSbSbTeHoTeITeFmTeITeMdITeSbICsEr"

# Step 1: Split the sequence into chemical element symbols
symbols = []
i = 0
while i < len(challenge_code):
    if challenge_code[i:i+2] in elements_data:
        symbols.append(challenge_code[i:i+2])
        i += 2
    elif challenge_code[i] in elements_data:
        symbols.append(challenge_code[i])
        i += 1
    else:
        i += 1

# Step 2: Convert symbols to atomic numbers
atomic_numbers = [elements_data[symbol] for symbol in symbols if symbol in elements_data]

# Step 3: Convert atomic numbers to hexadecimal representation, then to ASCII
hex_string = ''.join(f"{num:02x}" for num in atomic_numbers)  # Convert each atomic number to 2-digit hex
ascii_from_hex = bytes.fromhex(hex_string).decode('ascii', errors='ignore')
utf8_string = bytes.fromhex(ascii_from_hex).decode('utf-8')

# Print the final output
print("Hex String:", hex_string)
print("Hex flag:", ascii_from_hex)
print("Flag:", utf8_string)  # Print the flag as a readable ASCII string
