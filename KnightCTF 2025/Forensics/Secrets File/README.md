Name : 

Des : 


My friend's company's employees faced some attacks from hackers. Siam is a very close person to the company owner. Every employee knows that if Siam tells our CEO about anything, he can provide assistance without any hesitation. So, all employees made a statement, and here is the statement: "Triggers don't always require a spark. Sometimes, a simple change can set the stage for transformation. Where might such a trigger reside?" And guess what—the CEO granted him permission to hire an ethical hacker. So, he gave me that finding part. Are you able to help me with this issue?

Note: There are almost six users in their company, so anyone can be a victim. Thank you in advance.

Findout that One of the user hide some commercial data. Are you able to see that data?

Flag Format: KCTF{value_here} and replace space with underscore (_)


username : siam 
password : pmsiam

Download file : 

![image]()

we have file : kali-linux-2024.ova

and login whit username siam 
but we dont have any "sudo Privilege"

So I changed the root password using GRUB 

2

```
linux /boot/vmlinuz-6.11.2-amd64 root=UUID=... ro quiet splash init=/bin/bash
```
and 
```
$ mount -o remount,rw /
$ passwd
$ root
$ exec /sbin/init
```

Ok .. Login with " root " 
and find 6 users 

3 

we find 2 file in "/home/bob/Downloads"

4


5



ok we found : PartialPass: Null_

6

and try to unzip it : 

7

Ok Find Full password : Null_V4luE_M3

8


9













