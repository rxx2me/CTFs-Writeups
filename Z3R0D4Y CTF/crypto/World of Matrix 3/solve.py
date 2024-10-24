def reverse_row(m):
    return m[-1:] + m[:-1]

def reverse_col(m):
    return [i[-1:] + i[:-1] for i in m]

def add_key_reverse(s, k):
    return [[s[i][j] ^ k[i][j] for j in range(6)] for i in range(6)]

# Final provided data
enc_flag = [
    [107, 120, 37, 97, 35, 115], 
    [107, 106, 107, 47, 58, 113], 
    [49, 106, 37, 90, 31, 100], 
    [65, 49, 113, 107, 107, 28], 
    [1, 56, 36, 107, 105, 92], 
    [104, 46, 67, 44, 89, 108]
]

passwd = [
    [100, 52, 53, 52, 57, 50],
    [84, 52, 78, 56, 100, 67],
    [55, 99, 69, 103, 51, 52],
    [74, 53, 100, 103, 55, 67],
    [104, 100, 103, 67, 66, 105],
    [52, 53, 100, 118, 89, 90]
]

# Reverse the operations (12 steps)
for i in range(11, -1, -1):
    enc_flag = add_key_reverse(enc_flag, passwd)
    passwd = reverse_row(passwd) if i % 2 == 0 else reverse_col(passwd)

# Convert the flag matrix to text
flag = ''.join([chr(c) for row in enc_flag for c in row])
print(f"Flag: {flag}")
