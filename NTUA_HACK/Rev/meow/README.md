Chall : meow

point : 100 

Author: souvlakia


Solve Code : 

```
vals = [46096, 29310, 35786, 34250, 1682, 11703, 61757, 3732, 9259, 35900, 
        51157, 33143, 711, 15574, 10828, 33537, 40680, 50187, 18386, 31483]
finals = [13660, 20137, 19784, 1306, 978, 10684, 36366, 1167, 6038, 4071, 
          28503, 2856, 363, 1268, 7100, 9711, 21216, 17029, 17033, 25654]

password = ""

for i in range(len(finals)):
    f = finals[i]
    v = vals[i]

    for c in range(32, 127):  # Test all printable ASCII characters
        temp = c ^ 0x1337  # Reverse XOR
        temp = (temp * 0xdead) & 0xFFFFFFFF  # Simulate 32-bit overflow
        temp = temp >> 4  # Reverse shift right
        if temp % v == f:  # Check if remainder matches final
            password += chr(c)
            print(f"Found character {chr(c)} for position {i}")
            break

print("Recovered Password:", password)
```




Flag : 

"Recovered Password: NH4CK{r3v3r51n_m1p5}"


