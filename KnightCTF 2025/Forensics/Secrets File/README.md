---
title: "Secret File — Write-up"
ctf: KnightCTF-2025    
track: Forensics           
layout: page
permalink: /ctf/KnightCTF-2025/Forensics/Secrets-File
date: 2025-01-21 12:00:00 +0300
tags: [ctf, Knightctf, Forensics]
---

#Secret File



**اسم التحدي :** 

Secret File

**وصف التحدي : **

My friend's company's employees faced some attacks from hackers. Siam is a very close person to the company owner. Every employee knows that if Siam tells our CEO about anything, he can provide assistance without any hesitation. So, all employees made a statement, and here is the statement: "Triggers don't always require a spark. Sometimes, a simple change can set the stage for transformation. Where might such a trigger reside?" And guess what—the CEO granted him permission to hire an ethical hacker. So, he gave me that finding part. Are you able to help me with this issue?

Note: There are almost six users in their company, so anyone can be a victim. Thank you in advance.

Findout that One of the user hide some commercial data. Are you able to see that data?

Flag Format: KCTF{value_here} and replace space with underscore (_)


username : siam 
password : pmsiam

---

## الشرح (Write-up)

**تحميل الملف:**

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/1.png?raw=true" alt="download" width="500">

لدينا ملف: `kali-linux-2024.ova`

سجّل الدخول بحساب **siam**، لكن لا توجد لدينا **صلاحيات sudo**.

لذلك قمتُ بتغيير كلمة مرور المستخدم **root** عبر **GRUB**:

<pre><code>linux /boot/vmlinuz-6.11.2-amd64 root=UUID=... ro quiet splash init=/bin/bash
</code></pre>

ثم نفّذت الأوامر التالية:

<pre><code>$ mount -o remount,rw /
$ passwd
$ root
$ exec /sbin/init
</code></pre>

الان… سجّل الدخول الآن كمستخدم **root**، وستجد 6 مستخدمين:

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/3.png?raw=true" alt="users" width="500">

وجدنا ملفّين داخل المسار: `/home/bob/Downloads`

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/4.png?raw=true" alt="bob-downloads-1" width="500">

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/5.png?raw=true" alt="bob-downloads-2" width="500">

حصلنا على تلميح كلمة مرور جزئية: **PartialPass: Null_**

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/6.png?raw=true" alt="partial-pass" width="500">

جرّبنا فك الضغط:

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/7.png?raw=true" alt="unzip-try" width="500">

ثم عثرنا على كلمة المرور الكاملة: **Null_V4luE_M3**

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/8.png?raw=true" alt="full-pass-1" width="500">

<img src="https://github.com/rxx2me/CTFs-Writeups/blob/main/KnightCTF%202025/Forensics/Secrets%20File/9.png?raw=true" alt="full-pass-2" width="500">

**تم.**

{% if page.tags and page.tags != empty %}
<hr>
<div class="tags-inline">
  {% for tag in page.tags %}
    <a class="tag-pill" href="/tags/?t={{ tag | slugify }}">{{ tag }}</a>
  {% endfor %}
</div>
{% endif %}
