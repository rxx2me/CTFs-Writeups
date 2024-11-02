from sympy import mod_inverse

# Constants provided in the challenge
m = 57983

# Encoded message in hex format
encoded_message_hex = "3FB60 4F510 42930 31058 DEA8 4A818 DEA8 1AA88 65AE0 1C590 17898 1C590 29170 3FB60 55D10 29170 42930 6A7D8 4C320 4F510 5FC0 193A0 4F510 2E288 29170 643F8 31058 6A7D8 4A818 1AA88 1AA88"

# Step 1: Convert hex values to integers
encoded_message = [int(x, 16) for x in encoded_message_hex.split()]

# Step 2: Define reverse functions to decode
def reverse_churn(encoded_values):
    """Reverse the churn operation to restore the original order."""
    return encoded_values[-16:] + encoded_values[:-16]

def reverse_butter(values, p, m):
    """Reverse the butter function using the modular inverse of p modulo m."""
    inv_p = mod_inverse(p, m)
    return [(x * inv_p) % m for x in values]

def reverse_pop(values):
    """Reverse the pop function by applying XOR with 42."""
    return ''.join(chr(x ^ 42) for x in values)

# Step 3: Attempt to find `p` by brute-forcing potential values
def find_p(encoded_values, m, max_p=50000):
    reversed_churn = reverse_churn(encoded_values)
    for p_guess in range(1, max_p):
        try:
            inv_p = mod_inverse(p_guess, m)
            reversed_butter = [(x * inv_p) % m for x in reversed_churn]
            decoded_message = reverse_pop(reversed_butter)
            if all(32 <= ord(c) <= 126 for c in decoded_message):  # Check if the message is readable ASCII
                print(f"Found possible p: {p_guess}")
                return p_guess
        except ValueError:
            continue
    return None

# Step 4: Decode the message using the found `p`
def decode_message(encoded_message, p, m):
    reversed_churn = reverse_churn(encoded_message)
    reversed_butter = reverse_butter(reversed_churn, p, m)
    decoded_message = reverse_pop(reversed_butter)
    return decoded_message

# Run the brute-force to find `p`, then decode the message
p = find_p(encoded_message, m)
if p:
    flag = decode_message(encoded_message, p, m)
    print("Decoded Flag:", flag)
else:
    print("Could not find a suitable value for p.")
