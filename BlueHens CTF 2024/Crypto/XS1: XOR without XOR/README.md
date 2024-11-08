XS1: XOR without XOR

This is how XOR makes me feel.

This series of problems is called the XOR SCHOOL. For whatever reason I just love xor problems and over the years there are many that have charmed my soul. This sequence is an homage to the many many ways that xor shows up in CTFs. I hope you can see some of the beauty that I see through them. -ProfNinja

![0](https://github.com/rxx2me/CTFs-Writeups/blob/main/BlueHens%20CTF%202024/Crypto/XS1%3A%20XOR%20without%20XOR/xorwithout.png)

Solve :

```
encrypted_string = 'u_cnfrj_sr_b_34}yd1tt{0upt04lbmb'
flag_chars = (encrypted_string * 32)[::17][:32]
flag = ''.join(flag_chars)
print(flag)

```
