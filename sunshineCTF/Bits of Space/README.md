---
title: "Bits of Space — Write-up"
ctf: sunshineCTF    
track: Crypto           
layout: page
permalink: /ctf/sunshineCTF-2025/Crypto/Bits-of-Space
date: 2025-09-28 12:00:00 +0300
tags: [ctf, sunshinectf, Crypto]
---

# Bits of Space — writeup

---

## الخلاصة
كان هذا التحدّي مثالًا كلاسيكيًا على مشكلة **قابليّة العبث في CBC / هجوم padding-oracle وصولًا إلى تزوير IV**. استخدمنا padding-oracle لاستخراج كتل النصّ الصريح، ثم **عدّلنا IV** بحيث يصبح أوّل بلوك بعد فك تشفير AES-CBC يحتوي على معرّف جهاز مُجاز. إرسال الحزمة المزوّرة أعطى العلم (Flag).

---

## ملخّص التحدّي
- **الخدمة:** `nc sunshinectf.games 25401`
- **الهدف:** الوصول إلى  (relay) مقيّد؛ الخادم يزوّدك بحزمة مُشفّرة ثم يفحص هوية الجهاز بعد فك التشفير.
- **الملفّات المتاحة :** ملف مُشفّر ([`voyager.bin` ⬇️](https://github.com/rxx2me/CTFs-Writeups/raw/refs/heads/main/sunshineCTF/Bits%20of%20Space/voyager.bin)) و ([`relay.py` ⬇️](https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/sunshineCTF/Bits%20of%20Space/relay.py)).
- **الثغرة:** استخدام AES-CBC بدون توثيق ( MAC)، ما يسمح للمهاجم بـ:
  1. استخدام padding-oracle لفكّ تشفير كتل النصّ.
  2. قلب البتّات في **IV** (أو في الكتلة المشفّرة السابقة) للتحكّم بالنصّ المفكوك.

---

## الفكرة الأساسية
بالنسبة إلى AES-CBC:

<pre><code>P1 = D(C1) XOR IV
</code></pre>

إذا أردنا نصًا مختلفًا بعد الفك `P1'`، يمكننا صناعة IV جديد:

<pre><code>IV' = D(C1) XOR P1'
</code></pre>

نحن لا نعرف `D(C1)` مباشرة، لكن من padding-oracle يمكننا استرجاع:

<pre><code>P1 = D(C1) XOR IV
</code></pre>

بإعادة الترتيب:

<pre><code>D(C1) = P1 XOR IV
IV' = (P1 XOR IV) XOR P1'  = IV XOR P1 XOR P1'
</code></pre>

بمجرّد استعادة `P1`، نستطيع حساب `IV'` ليجعل الخادم يرى **أي** `P1'` نريده. في هذا التحدّي، جُعلت أوّل 4 بايتات من `P1'` تُطابق معرّف جهاز صحيح (المثال استخدم `0x13371337`) فتم منح الوصول.

---

## الخطوات المنفَّذة

### 1) الحصول على الحزم والـ oracle
- نتصل بمضيف التحدّي ونلاحظ أن الخادم يقبل حزمة مُشفّرة ويُسرّب ما إذا نجح الفك/التحقّق.
- الحزمة تحتوي على **IV** وكتل النصّ المشفّر (`IV`, `C1`, `C2`, ...).

### 2) استخدام padding-oracle لاسترجاع كتل النصّ الصريح
- تشغيل سكربت padding-oracle (مزوّد/أو سكربت شائع مثل `solve.py`) يقوم بـ:
  - تعديل بايتات من الكتلة السابقة/IV تكراريًا،
  - إرسال الاستعلام للخادم واستنتاج ردود صحة الحشو،
  - استرجاع `P1` وبقية الكتل.

**مثال (الأمر الذي استُخدم في المسابقة):**
<pre><code>python solve.py --host sunshinectf.games --port 25401 --in voyager.bin
</code></pre>

يُظهر السكربت **IV** والكتل بالهيكس، ويطبع النصّ الصريح المستعاد (هيكس خام). بعد الفك أصبح لدينا البلوك الذي يحتوي معرّف الجهاز.

### 3) حساب IV مزوّر لتعيين معرّف الجهاز
- نختار قيمة المعرّف المرغوبة — مثلًا `0x13371337` في أوّل 4 بايتات.
- لِنسمِّ الأصل `IV` (16 بايت) والنصّ المستعاد للبلوك الأوّل `P1` (16 بايت).
- نحسب `IV'` بحيث يرى الخادم `P1'` بأوّل 4 بايتات تساوي `0x13 0x37 0x13 0x37` (والباقي يمكن أن يبقى كما هو أو حسب المتطلّب).

**مقتطف Python لحساب IV الجديد (تعديل أوّل 4 بايتات):**
<pre><code># example values (replace with your actual hex strings)
old_iv = bytes.fromhex("5e60383e8ebbee04aa00a3bead867ef9")
p1     = bytes.fromhex("edf4f6a2fb241b9e21b4926b5134e3d2")  # recovered plaintext block
desired_first4 = bytes.fromhex("13371337")  # want the first 4 bytes of plaintext to become this

# compute new IV by changing only the first 4 bytes
new_iv = bytearray(old_iv)
for i in range(4):
    new_iv[i] = old_iv[i] ^ p1[i] ^ desired_first4[i]

print("new IV (hex):", new_iv.hex())
</code></pre>

(وبشكل مكافئ، إذا استعدت كامل البلوك، يمكنك استبدال الـ 16 بايت كاملة:)
<pre><code>new_iv = bytes(a ^ b ^ c for a, b, c in zip(old_iv, p1, desired_plaintext_block))
</code></pre>

### 4) بناء الحزمة المزوّرة وإرسالها
- نستبدل الـ **IV** الأصلي بـ `IV'` ونُبقي كتل النصّ المشفّر كما هي.
- نرسل الحزمة إلى الخادم (في التحدّي استُخدم ملف `forged.bin` مع سكربت مساعد).
- الخادم يفكّ باستخدام `IV'` فيرى `P1'` وفيه معرّف جهاز صالح → يمنح الوصول → يُرجع العلم.

**مخرجات مثال بعد نجاح تعديل IV:**
<pre><code>You have reached the restricted relay... here you go.
b'sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}\n'
</code></pre>

---

## لماذا ينجح هذا؟
- AES-CBC يمنح السرّية فقط، **بدون سلامة/تكامل**. تعديل النصّ المشفّر (أو IV) يُحدِث تغيّرات متوقَّعة في النصّ المفكوك.
- padding-oracle يتيح عمليًا فكّ تشفير الكتل عبر استعلامات متكرّرة للخادم.
- بدمج الاثنين، يستعيد المهاجم النصّ ثم يصنع `IV'` لضبط قيم نصّ معينة (مثل معرّف الجهاز) وتجاوز فحوصات تعتمد على النصّ.

---

## العلم (Flag)
<pre><code>sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}
</code></pre>

---

## Full Code
<pre><code>#!/usr/bin/env python3
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
</code></pre>


{% if page.tags and page.tags != empty %}
<hr>
<div class="tags-inline">
  {% for tag in page.tags %}
    <a class="tag-pill" href="/tags/?t={{ tag | slugify }}">{{ tag }}</a>
  {% endfor %}
</div>
{% endif %}
