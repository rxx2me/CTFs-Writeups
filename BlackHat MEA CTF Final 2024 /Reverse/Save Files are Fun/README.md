---
title: "Save Files are Fun — Write-up"
ctf: BlackHat-MEA-CTF-Final-2024    
track: Reversing           
layout: page
permalink: /ctf/BlackHat-MEA-CTF-Final-2024/Reversing/save-files-are-fun/
date: 2024-11-30 12:00:00 +0300
tags: [ctf, blackhat, Reversing]
---


Save Files are Fun

The file is : map.wbox its belong to " WorldBox.God.Simulator"

1- Open WorldBox.God.Simulator

![alt text](https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/1%20(2).png)

2- Create a new map and then save it

3- Go to : 
```
C:\Users\(username)\AppData\LocalLow\mkarpenko\WorldBox\saves\save1
```
4- Replace the existing file named: map.wbox with the challenge file

5- Go back to WorldBox.God.Simulator and go to Save button

![alt text](https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/2.png)

6- You will find the map on the date of the challenge and select it

![alt text](https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/3.png)


7- You got it : 

![alt text](https://raw.githubusercontent.com/rxx2me/CTFs-Writeups/refs/heads/main/BlackHat%20MEA%20CTF%20Final%202024%20/Reverse/Save%20Files%20are%20Fun/4.png)




{% if page.tags and page.tags != empty %}
<hr>
<div class="tags-inline">
  {% for tag in page.tags %}
    <a class="tag-pill" href="/tags/?t={{ tag | slugify }}">{{ tag }}</a>
  {% endfor %}
</div>
{% endif %}

