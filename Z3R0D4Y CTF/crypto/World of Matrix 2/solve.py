from math import sqrt

# Given encrypted matrix (enc_matrix) from the challenge description
enc_matrix = [
    [63, 115, 83, 113, 80, 86, 79, 86, 99, 91, 47, 120, 48, 75, 83, 59],
    [83, 40, 13, 4, 119, 41, 93, 90, 5, 77, 69, 55, 84, 33, 114, 72],
    [73, 12, 48, 103, 67, 92, 105, 110, 60, 86, 51, 53, 114, 93, 83, 70],
    [57, 123, 110, 118, 68, 8, 73, 115, 10, 104, 85, 85, 74, 61, 51, 47],
    [47, 122, 74, 62, 66, 45, 77, 81, 116, 56, 119, 69, 74, 87, 75, 47],
    [46, 43, 16, 105, 77, 10, 110, 68, 80, 74, 85, 87, 88, 27, 115, 83],
    [82, 88, 54, 63, 47, 51, 54, 104, 73, 87, 83, 109, 83, 57, 104, 116],
    [80, 63, 75, 45, 112, 96, 77, 99, 55, 79, 54, 96, 68, 100, 112, 71],
    [90, 62, 121, 12, 75, 41, 101, 50, 93, 107, 83, 90, 81, 42, 82, 60],
    [73, 91, 112, 116, 80, 51, 93, 112, 55, 73, 58, 62, 91, 88, 89, 119],
    [112, 77, 79, 92, 54, 114, 111, 46, 73, 93, 81, 62, 100, 59, 92, 61],
    [85, 93, 75, 70, 112, 46, 75, 69, 63, 95, 69, 107, 96, 116, 73, 68],
    [57, 62, 62, 52, 80, 67, 119, 64, 54, 70, 76, 69, 48, 52, 117, 60],
    [56, 7, 27, 5, 76, 8, 89, 83, 116, 58, 118, 71, 115, 49, 62, 103],
    [109, 93, 83, 90, 97, 64, 51, 76, 47, 108, 97, 48, 94, 105, 110, 81],
    [103, 108, 60, 53, 85, 73, 84, 70, 47, 53, 114, 71, 76, 81, 121, 111]
]

# Original s_max matrix from the challenge
s_max = [
    [63, 115, 83, 113, 80, 86, 79, 86, 99, 91, 47, 120, 48, 75, 83, 59], 
    [83, 82, 104, 118, 119, 70, 93, 90, 97, 77, 69, 55, 84, 64, 114, 72], 
    [73, 117, 75, 65, 67, 109, 105, 110, 81, 86, 51, 53, 114, 45, 83, 70], 
    [57, 74, 93, 85, 68, 101, 73, 115, 74, 104, 85, 85, 74, 73, 51, 47], 
    [47, 122, 74, 62, 66, 45, 77, 81, 116, 56, 119, 69, 74, 87, 75, 47], 
    [46, 67, 52, 54, 77, 59, 110, 68, 96, 74, 85, 87, 88, 58, 115, 83], 
    [82, 88, 54, 63, 47, 51, 54, 104, 73, 87, 83, 109, 83, 57, 104, 116], 
    [80, 63, 75, 45, 112, 96, 77, 99, 55, 79, 54, 96, 68, 100, 112, 71], 
    [90, 97, 72, 76, 75, 104, 101, 50, 59, 107, 83, 90, 81, 111, 82, 60], 
    [73, 91, 112, 116, 80, 51, 93, 112, 55, 73, 58, 62, 91, 88, 89, 119], 
    [112, 77, 79, 92, 54, 114, 111, 46, 73, 93, 81, 62, 100, 59, 92, 61], 
    [85, 93, 75, 70, 112, 46, 75, 69, 63, 95, 69, 107, 96, 116, 73, 68], 
    [57, 62, 62, 52, 80, 67, 119, 64, 54, 70, 76, 69, 48, 52, 117, 60], 
    [56, 51, 122, 117, 76, 61, 89, 83, 69, 58, 118, 71, 115, 76, 62, 103], 
    [109, 93, 83, 90, 97, 64, 51, 76, 47, 108, 97, 48, 94, 105, 110, 81], 
    [103, 108, 60, 53, 85, 73, 84, 70, 47, 53, 114, 71, 76, 81, 121, 111]
]

# Calculate Fibonacci sequence (same as in the original code)
a, b = 1, 1
c = [b]
for _ in range(256):
    a, b = b, a + b
    c.append(b)

# Calculate 'val' from the description
# We know that the flag matrix is 'val x val', and its length should be the square of val
val = int(sqrt(48))  # Since the flag length is 16 based on the code (flag length is sqrt(len(flag)))

# Decrypt the flag by reversing the XOR operation
flag_matrix = []
for i in range(val):
    row = []
    for j in range(val):
        decrypted_value = enc_matrix[c[i]][c[j]] ^ s_max[c[i]][c[j]]
        row.append(decrypted_value)
    flag_matrix.append(row)

# Convert the decrypted ASCII values back to characters to form the flag
flag = ''.join([chr(char) for row in flag_matrix for char in row])
print(flag)