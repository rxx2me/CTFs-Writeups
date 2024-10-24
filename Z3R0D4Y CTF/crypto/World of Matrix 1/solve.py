import numpy as np

# Known output matrix (the outputs we have)
known_output = np.array([[47215, 49497, 46361, 50001],
                         [46514, 48663, 45640, 49133],
                         [45977, 48147, 45130, 48619],
                         [41294, 42276, 39740, 42577],
                         [13536, 14112, 13216, 14272]])

# The known flag we're searching for starts with "zeroday"
known_flag_start = "zeroday"

# Reading the password list from the rockyou.txt file
with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='utf-8', errors='ignore') as f:
    passwords = f.read().splitlines()

# Function to convert the password into a 4x4 matrix of ASCII values
def password_to_matrix(password):
    if len(password) != 16:
        return None  # The password must be 16 characters long (4x4)
    
    ascii_values = [ord(c) for c in password]
    return np.array(ascii_values).reshape(4, 4)

# Attempt to decrypt using each password
for password in passwords:
    matrix2 = password_to_matrix(password)
    if matrix2 is None:
        continue  # If the password is not 16 characters, move to the next one
    
    try:
        # Calculate the inverse matrix for the password
        matrix2_inverse = np.linalg.inv(matrix2)
        
        # Decrypt by multiplying the known output matrix with the inverse matrix
        original_matrix = np.dot(known_output, matrix2_inverse)
        
        # Round the values to the nearest integer
        original_matrix = np.round(original_matrix).astype(int)
        
        # Convert the ASCII values to characters, ensuring the values are in the valid range
        flag_chars = []
        for value in original_matrix.flatten():
            if 0 <= value <= 0x10FFFF:  # Ensure the value is within the Unicode range
                flag_chars.append(chr(value))
            else:
                flag_chars.append('?')  # Replace invalid values with the '?' symbol
        
        flag = ''.join(flag_chars).strip()  # Remove excess spaces
        
        # Check if the flag starts with "zeroday"
        if flag.startswith(known_flag_start):
            print(f"Password found: {password}")
            print(f"The flag is: {flag}")
            break
    
    except np.linalg.LinAlgError:
        # Ignore errors that occur when unable to compute the inverse matrix
        continue
