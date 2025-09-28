
# Bits of Space — writeup
*(GitHub-style — focused on Challenge 1 only)*

---

## TL;DR
This challenge was a classic **CBC malleability / padding-oracle → IV forgery** problem.
We used a padding-oracle to recover plaintext blocks, then *modified the IV* so that after AES-CBC decryption the first plaintext block contained an allowed device id. Sending the forged packet produced the flag:

---

## Challenge summary
- Service: `nc sunshinectf.games 25401`
- Goal: get access to a restricted relay; the server gives you an encrypted packet and checks device identity after decrypting.
- Provided files (in the contest environment): an encrypted file (e.g. `voyager.bin`) and some helper scripts (padding-oracle client).
- Vulnerability: AES-CBC without authenticity (no MAC) — attacker can:
  1. use a padding oracle to decrypt ciphertext blocks, and
  2. flip bits in the IV (or previous ciphertext block) to control the decrypted plaintext.

---

## Key idea
For AES-CBC:
```

P1 = D(C1) XOR IV

```
If we want a different plaintext `P1'` after decryption, we can craft a new IV:
```

IV' = D(C1) XOR P1'

```
We do not know `D(C1)` directly, but from a padding-oracle decryption we can recover `P1 = D(C1) XOR IV`. Rearranging:

```

D(C1) = P1 XOR IV
IV' = (P1 XOR IV) XOR P1'  = IV XOR P1 XOR P1'

````

So once we recover the original plaintext `P1`, we can compute `IV'` to make the server see *any* `P1'` we like. In this challenge `P1'` was set to a valid device id (the example used `0x13371337` in the first 4 bytes), and that granted access.

---

## Steps performed

### 1. Obtain packets and oracle
- Connect to the challenge host and observe that the server accepts an encrypted packet and leaks whether decryption/auth succeeds.
- The challenge provided a packet with IV and ciphertext blocks (call them `IV`, `C1`, `C2`, ...).

### 2. Use padding-oracle to recover plaintext blocks
- Run a padding-oracle script (the challenge provided / or we used a typical `solve.py`) that:
  - Iteratively modifies bytes of the previous block/IV,
  - Queries the server and infers correct padding responses,
  - Recovers `P1` and subsequent plaintext blocks.

Example (what I ran in the contest):
```bash
python solve.py --host sunshinectf.games --port 25401 --in voyager.bin
````

This produced the recovered plaintext blocks and the original IV / ciphertext displayed in hex.

> The solver printed the IV and ciphertext blocks and showed recovered plaintext (raw hex).
> After decryption we had the plaintext bytes for the block containing the device id.

### 3. Compute forged IV to set device ID

* Decide on the desired device id value we want the server to see — e.g. `0x13371337` in the first 4 bytes (as done during the solve).
* Let `IV` be the original IV (16 bytes) and `P1` be the recovered first plaintext block (16 bytes).
* Compute new IV `IV'` that will cause the server to see `P1'` where the first 4 bytes equal `0x13 0x37 0x13 0x37` (rest of block can be the original bytes or whatever is required).

Small Python snippet used to compute the new IV (first-4-bytes example):

```python
# example values (replace with your actual hex strings)
old_iv = bytes.fromhex("5e60383e8ebbee04aa00a3bead867ef9")
p1     = bytes.fromhex("edf4f6a2fb241b9e21b4926b5134e3d2")  # recovered plaintext block
desired_first4 = bytes.fromhex("13371337")  # want the first 4 bytes of plaintext to become this

# compute new IV by changing only the first 4 bytes
new_iv = bytearray(old_iv)
for i in range(4):
    new_iv[i] = old_iv[i] ^ p1[i] ^ desired_first4[i]

print("new IV (hex):", new_iv.hex())
```

(Equivalently, if you recovered the *entire* plaintext block you can replace the whole 16 bytes: `new_iv = bytes(a ^ b ^ c for a,b,c in zip(old_iv, p1, desired_plaintext_block))`.)

### 4. Build forged packet and send

* Replace the IV in the original packet with `IV'` and keep the ciphertext blocks unchanged.
* Send the forged packet to the server (the challenge used a `forged.bin` and `player.py` helper).
* The server decrypts (with your `IV'`) and now sees `P1'` containing a valid device id → grants access → returns the flag.

Example output after successful IV tweak:

```
You have reached the restricted relay... here you go.
b'sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}\n'
```

---

## Why this works

* AES-CBC provides confidentiality but **no integrity**. Without a MAC (or AEAD), ciphertext (and IV) modifications lead to predictable changes in the decrypted plaintext.
* Padding-oracle grants an attacker the ability to decrypt ciphertext blocks offline by repeatedly querying the server.
* Combining both, attacker recovers plaintext and then crafts an `IV'` to set desired plaintext values (device id), bypassing any plaintext-based authentication checks.

---

## Mitigations / fixes

Server-side developers should **never** accept unauthenticated ciphertext. Fixes include:

1. **Use authenticated encryption** — AES-GCM or ChaCha20-Poly1305 (AEAD) so modifications are detected.
2. **Encrypt-then-MAC** (if using CBC) — compute a MAC (HMAC) over IV||ciphertext and verify before decryption.
3. **Reject any decryption error details** — don’t reveal padding/format errors in a way that yields an oracle. (But this is only a partial defense; the fundamental fix is MAC/AEAD.)
4. **Do not rely on unauthenticated decrypted fields for authentication** — authenticate the whole message with a MAC.
5. **Include replay / freshness checks** as an extra defense (nonces/counters/timestamps), though not a replacement for integrity.

---

## Notes / lessons learned

* Padding oracle attacks remain practical when services leak padding validity (or other decryption error behavior).
* The simplest programmatic exploit is:

  1. run padding-oracle to recover `P1`,
  2. compute `IV' = IV XOR P1 XOR P1_desired`,
  3. send IV' + ciphertext to obtain desired decrypted plaintext.
* Always treat encryption as **confidentiality + integrity**. Without integrity the ciphertext stream is malleable.

---

## Flag

```
sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}
```

---

## Appendix: references & helpful utilities

* Typical padding-oracle implementations (many public PoC scripts) — look for `cbc padding oracle python` or `padding oracle attack`.
* For one-liners, Python `pycryptodome` helps compute XORs and conversions.


Full Code : 
```
#!/usr/bin/env python3
import socket
from pathlib import Path

HOST = "sunshinectf.games"
PORT = 25401
INFILE = "voyager.bin"

VALID = [
    0x13371337,
    0x1337babe,
    0xdeadbeef,
    0xdeadbabe
]

TARGET = 0xdeadbabe  # نريد أن نظهر للـ server أن packet ينتمي لهذا الجهاز

def send_and_recv(host, port, payload):
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect((host, port))
        # read initial banner (some bytes)
        try:
            _ = s.recv(4096)
        except:
            pass
        s.sendall(payload + b"\n")
        data = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            except:
                break
        return data.decode(errors="ignore")
    finally:
        s.close()

data = Path(INFILE).read_bytes()
iv = bytearray(data[:16])
ct = data[16:]

print("Original IV:", iv.hex())
for orig in VALID:
    orig_bytes = orig.to_bytes(4, "little")
    target_bytes = TARGET.to_bytes(4, "little")
    # compute new IV: flip first 4 bytes
    new_iv = bytearray(iv)  # copy
    for i in range(4):
        new_iv[i] = iv[i] ^ orig_bytes[i] ^ target_bytes[i]
    forged = bytes(new_iv) + ct
    print(f"\nTrying orig=0x{orig:08x} -> new IV first4 = {new_iv[:4].hex()}")
    resp = send_and_recv(HOST, PORT, forged)
    print("Server response snippet:")
    print(resp.strip()[:400])
    # check if we hit the restricted device or flag
    if "restricted" in resp.lower() or "flag" in resp.lower() or "you have reached the restricted relay" in resp.lower():
        print("=> Likely success! Full response:\n")
        print(resp)
        break
else:
    print("\nTried all 4 candidate origins — none produced the restricted relay. Next steps:")
    print(" - We may need to fully recover the plaintext P1 via a working padding-oracle (debug the oracle detection).")
    print(" - Or the original device isn't one of the 4, so the 4-try method fails.")

```

ذذذ
