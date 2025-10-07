---
title: "Save Files are Fun — Write-up"
ctf: BlackHat-MEA-CTF-Final-2024    
track: Reversing           
layout: page
permalink: /ctf/BlackHat-MEA-CTF-Final-2024/Reversing/save-files-are-fun/
date: 2024-11-30 12:00:00 +0300
tags: [ctf, blackhat, Reversing]
---

**سم التحدي :**  Save Files are Fun
**وصف التحدي:** none
**الملف المرفق:** [map.wbox](https://github.com/rxx2me/CTFs-Writeups/raw/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/map.wbox)


**الملف:** `map.wbox` — وهو يخص لعبة **WorldBox.God.Simulator**.

**الخطوات:**

1) افتح لعبة **WorldBox.God.Simulator**.

<img src="https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/1%20(2).png" alt="s1" width="500">

2) أنشئ خريطة جديدة ثم قم بحفظها.

3) انتقل إلى المسار التالي: 
```C:\Users\(username)\AppData\LocalLow\mkarpenko\WorldBox\saves\save1```

4) استبدل الملف الموجود باسم **map.wbox** بملف التحدّي.

5) ارجع إلى **WorldBox.God.Simulator** ثم إلى زر **Save**.

<img src="https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/2.png" alt="s2" width="500">

6) ستجد الخريطة بتاريخ التحدّي — قم بتحديدها.

<img src="https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/3.png" alt="s3" width="500">

7) تم استخراج العلم كما في الصورة:

<img src="https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/4.png" alt="s4" width="500">



{% if page.tags and page.tags != empty %}
<hr>
<div class="tags-inline">
  {% for tag in page.tags %}
    <a class="tag-pill" href="/tags/?t={{ tag | slugify }}">{{ tag }}</a>
  {% endfor %}
</div>
{% endif %}
