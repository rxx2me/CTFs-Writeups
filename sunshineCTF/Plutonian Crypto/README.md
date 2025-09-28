# Plutonian Crypto — Writeup (Challenge 2)


---

## TL;DR
التحدي كان عبارة عن **رسائل متكرّرة مشفّرة** باستخدام تيار مفتاح قابل لإعادة الاستخدام (stream cipher / OTP reuse). استغلّينا جزءًا معروفًا من النصّ ("Greetings, Earthlings.") لاستنتاج جزء من سلسلة المفاتيح (keystream) ثم طبّقناه على الرسائل المشفّرة الأخرى لفكّ بقية النصّ والحصول على العلم:



---

## وصف المشكلة باختصار
- الخدمة كانت تبث رسائل متكرّرة "من بلوتو" بصيغة مشفّرة. المُحكّم قدّم لنا أن المفتاح يعاد استخدامه عبر مرات البث، وأن جزءًا من النصّ الواضح متاح: "Greetings, Earthlings.".
- الهدف: فكّ باقي الرسالة/الحصول على رمز الإرسال (flag).

---

## الفكرة الأساسية (high-level)
عند استعمال تيار مفاتيح (مثل OTP / stream cipher) **إعادة استخدام نفس المفتاح عبر رسائل مختلفة** تُعرِّض النظام لهجوم بسيط وفعّال:

إذا: C = P XOR K  (حيث C: ciphertext, P: plaintext, K: keystream)

وعند معرفة جزء من P (مثلاً P_known) وطولها L، يمكننا حساب جزء من K:

```
K_prefix = C_prefix XOR P_known
```

ثم نستخدم `K_prefix` لفكّ نفس الموضع في أي رسالة أخرى المشفّرة بنفس المفتاح:

```
P_other_prefix = C_other_prefix XOR K_prefix
````

وبالتدرّج/التمدد (crib-dragging) يمكن استخراج بقية النصّ.

---

## الخطوات التي اتبعتُها عمليًا
1. جمعت ciphertext للرسالة المرصودة التي حصلت عليها من السيرفر (أو ملف الحزمة). لنفترض أن لدينا السلسلة `cipher.hex()` أو `cipher.bin`.
2. حددت الجزء المعروف من الـplaintext: `known = b"Greetings, Earthlings."` (طوله L بايت).
3. حسبت keystream الجزئي: `keystream_prefix = xor(cipher_prefix, known)`.
4. طبّقت `keystream_prefix` على بقية البلوك/الملف (عند وجود رسائل متكررة أو نفس الرسالة في أوقات مختلفة) لفك ما يمكن فكّه. حيثما ظهر نص إنساني مفهوم، استخدمت ذلك "crib" لتوسيع المفتاح أكبر.
5. كررت عملية التوسيع/تطبيق حتى فكّت كامل الرسالة وحصلت على العلم.

---

## مثال كود (Python)
السكريبت أدناه هو مثال بسيط يُظهر الطريقة: قراءة ملف ciphertext ثنائي، حساب keystream باستخدام الجزء المعروف ثم فك بقية البيانات.

```
#!/usr/bin/env python3
# simple_keystream_recover.py

from binascii import unhexlify

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# مثال: نحمّل الـcipher كنص hex أو كملف ثنائي
cipher_hex = "..."  # أو اقرأ من ملف
cipher = unhexlify(cipher_hex)

known = b"Greetings, Earthlings."
L = len(known)

# نفترض أن known يتطابق مع أول L بايت من plaintext المراد
keystream_prefix = xor_bytes(cipher[:L], known)

# نفك أول L بايت من أي ciphertext آخر المشفّر بنفس keystream
# هنا نفك نفس الرسالة (اذا كانت مُكررة)
recovered_prefix = xor_bytes(cipher[:L], keystream_prefix)
print(recovered_prefix)

# لتطبيقه على رسالة كاملة (لو نملك keystream كافياً), نفعل:
# plaintext = xor_bytes(cipher, keystream)

# إذا لم يكن keystream كاملًا، نستخدم أسلوب "crib-dragging" لتخمين مقاطع نصية
# قابلة للظهور ومن ثم تحديث keystream بإعطاء قيم جديدة.
````

> أثناء السباق استخدمت نفس المبدأ: استخرجت مفاتيح جزئية، طبّقتها على السلاسل، ووسّعت عن طريق الملاحظة اليدوية (وقراءة ناتج XOR للعثور على كلمات إنجليزية/عبارات متوقعة) حتى فُكّت الرسالة كليًا.

---

## لماذا نجحت الطريقة هنا؟

* لأنَّ نفس keystream أُعيد استخدامه عبر مرات البث. إعادة استخدام keystream = كارثة بالنسبة لتيارات المفاتيح؛ فهي تقلّل الأمان إلى حدّ يسمح باستعادة النصوص بمجرد وجود قليل من المعلومات المعروفة أو عن طريق مفتاحية التوزيع (crib-dragging).

---

## نصائح واحتياطات (Mitigations)

* لا تُعِد استخدام keystream/OTP مطلقًا على أكثر من رسالة واحدة. كل رسالة يجب أن تستخدم مفتاحًا/nonce مختلفًا.
* استعمل بروتوكولات حديثة مضمونة: AEAD (مثل AES-GCM أو ChaCha20-Poly1305) بدلاً من تيارات مفاتيح قديمة بدون تحقق تكاملي.
* إذا كان لابد من التعمية المتكررة استعمل nonce فريد لكل رسالة (لا تُستخدم قيمة ثابتة أبداً).

---

## العلم (flag)

```
sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}
```

---

## Full Code : 

```
#!/usr/bin/env python3
"""
solve_pluto.py

Usage:
  python3 solve_pluto.py --host chal.sunshinectf.games --port 25403 --n 300

What it does:
- Connects to host:port and reads n ciphertext lines (hex).
- Attempts to reconstruct plaintext using the known prefix "Greetings, Earthlings."
  and the block-shift relation between consecutive transmissions.
- Prints recovered plaintext as it grows.
"""
import socket
import argparse
from binascii import unhexlify
from collections import defaultdict

KNOWN_PREFIX = b"Greetings, Earthlings."

def fetch_ciphertexts(host, port, n_lines=200, timeout=5):
    """Connect and read n_lines ciphertext hex strings (one per line)."""
    s = socket.create_connection((host, port), timeout=timeout)
    s.settimeout(timeout)
    data = b""
    # consume banner until transmission lines start; we will collect lines that look like hex
    ciphertexts = []
    try:
        while len(ciphertexts) < n_lines:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            # split lines
            lines = data.split(b"\n")
            # keep last partial
            data = lines.pop() if lines else b""
            for L in lines:
                Ls = L.strip()
                # accept lines that are long hex strings (ciphertext lines)
                if len(Ls) >= 4 and all(c in b"0123456789abcdef" for c in Ls.lower()):
                    try:
                        ct = unhexlify(Ls)
                        ciphertexts.append(ct)
                        print(f"[+] got ciphertext #{len(ciphertexts)} len={len(ct)}")
                        if len(ciphertexts) >= n_lines:
                            break
                    except Exception:
                        pass
    finally:
        s.close()
    return ciphertexts

def recover_plain(ciphertexts, block_size=16, known_prefix=KNOWN_PREFIX):
    """
    ciphertexts: list indexed by t (t=0..)
    returns recovered plaintext bytes (as bytearray) as far as possible
    Approach:
     - maintain dict known[pos] = byte
     - seed known[0..len(prefix)-1] with prefix
     - for pos increasing, if known[pos] known, try to recover pos+block_size using any t where:
         ciphertexts[t] has byte at pos+block_size and ciphertexts[t+1] has byte at pos
       formula: P[pos+block_size] = CT_t[pos+block_size] ^ CT_{t+1}[pos] ^ P[pos]
     - repeat until no progress
    """
    known = dict()
    for i, b in enumerate(known_prefix):
        known[i] = b

    max_ct_len = max(len(c) for c in ciphertexts)
    made_progress = True

    while made_progress:
        made_progress = False
        # try all positions that are known
        for pos in list(known.keys()):
            target = pos + block_size
            if target in known:
                continue
            # try find t such that ciphertexts[t] has byte at target and ciphertexts[t+1] has byte at pos
            for t in range(len(ciphertexts)-1):
                ct_t = ciphertexts[t]
                ct_t1 = ciphertexts[t+1]
                if target < len(ct_t) and pos < len(ct_t1):
                    val = ct_t[target] ^ ct_t1[pos] ^ known[pos]
                    known[target] = val
                    made_progress = True
                    # debug print
                    print(f"[+] Recovered byte at {target} using t={t}: {val:02x} (char={chr(val) if 32<=val<127 else '.'})")
                    break
    # build plaintext bytearray up to highest known index contiguous from 0
    # but we may have holes; we'll return full array up to max known index filling unknowns with '?'
    if known:
        max_known = max(known.keys())
    else:
        max_known = -1
    out = bytearray(max_known+1)
    for i in range(max_known+1):
        out[i] = known.get(i, ord('?'))
    return out, known

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--n", type=int, default=300, help="how many ciphertexts to fetch")
    args = parser.parse_args()

    print("[*] Fetching ciphertexts...")
    cts = fetch_ciphertexts(args.host, args.port, args.n)
    print(f"[*] Collected {len(cts)} ciphertexts; longest len = {max(len(c) for c in cts)} bytes")

    plaintext_bytes, known_map = recover_plain(cts)
    print("\n=== Recovered (partial) plaintext ===\n")
    try:
        print(plaintext_bytes.decode('utf-8', errors='replace'))
    except:
        print(plaintext_bytes)
    print("\n=== Known byte positions ===")
    for i in sorted(known_map.keys())[:200]:
        print(f"{i:04d}: 0x{known_map[i]:02x} {chr(known_map[i]) if 32<=known_map[i]<127 else ''}")
    print("\nDone.")

if __name__ == "__main__":
    main()
```

