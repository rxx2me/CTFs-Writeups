def add_key(s, k):
    return [[s[i][j] ^ k[i][j] for j in range(6)] for i in range(6)]
def string2matrix(text):
    t = [ord(k) for k in text]
    return [t[i:i+6] for i in range(0, len(t), 6)]
def col(m):
    return [i[1:] + i[:1] for i in m]
def row(m):
    return (m[1:] + m[:1])
flag = "REDACTED"
passwd = ["REDACTED"]
flag_matrix = string2matrix(flag)
for i in range(12):
    passwd = row(passwd) if i % 2 == 0 else col(passwd)
    flag_matrix = add_key(flag_matrix, passwd)
print(f"enc flag is : \n {flag_matrix}")
print(f"at the end passwd is :\n {passwd}")


"""
enc flag is : 
 [
    [107, 120, 37, 97, 35, 115], 
    [107, 106, 107, 47, 58, 113], 
    [49, 106, 37, 90, 31, 100], 
    [65, 49, 113, 107, 107, 28], 
    [1, 56, 36, 107, 105, 92], 
    [104, 46, 67, 44, 89, 108]
 ]
at the end passwd is :  
 [
    [100, 52, 53, 52, 57, 50],
    [84, 52, 78, 56, 100, 67],
    [55, 99, 69, 103, 51, 52],
    [74, 53, 100, 103, 55, 67],
    [104, 100, 103, 67, 66, 105],
    [52, 53, 100, 118, 89, 90]
]
"""