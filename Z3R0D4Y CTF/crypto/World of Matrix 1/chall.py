import numpy as np

flag = "REDACTED"

if len(flag) < 20:
    flag = flag.ljust(20, ' ')
ascii_values = [ord(char) for char in flag]

matrix1 = np.array(ascii_values).reshape(5, 4)

password = "REDACTED"
matrix2 = np.array([ord(c) for c in password]).reshape(4, 4)

result_matrix = np.dot(matrix1, matrix2)

print("\nResultant Matrix: ")
print(result_matrix)