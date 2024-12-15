chall : ICMP Party

point : 100 

Author: vipolus

des:

Recently our network engineers noticed a weird icmp traffic. Can you find out what happened?

first : 
```
tshark -r NHACK.pcapng -Y  "icmp" -T fields -e ip.ttl
```
find this : 
```
 78, 64, 72, 64, 52, 64, 67, 64, 75, 64, 123, 64, 65, 64, 110, 64, 
    52, 64, 108, 64, 121, 64, 90, 64, 33, 64, 110, 64, 71, 64, 95, 64, 
    112, 64, 67, 64, 52, 64, 112, 64, 83, 64, 95, 64, 83, 64, 51, 64, 
    51, 64, 109, 64, 115, 64, 95, 64, 84, 64, 48, 64, 95, 64, 98, 64, 
    51, 64, 95, 64, 70, 64, 117, 64, 78, 64, 33, 64, 125, 64
```

Solve Code : 

```
ttl_values = [
    78, 64, 72, 64, 52, 64, 67, 64, 75, 64, 123, 64, 65, 64, 110, 64, 
    52, 64, 108, 64, 121, 64, 90, 64, 33, 64, 110, 64, 71, 64, 95, 64, 
    112, 64, 67, 64, 52, 64, 112, 64, 83, 64, 95, 64, 83, 64, 51, 64, 
    51, 64, 109, 64, 115, 64, 95, 64, 84, 64, 48, 64, 95, 64, 98, 64, 
    51, 64, 95, 64, 70, 64, 117, 64, 78, 64, 33, 64, 125, 64
]


unique_ttl_values = [value for value in ttl_values if value != 64]


decoded_text = ''.join(chr(value) for value in unique_ttl_values)


print("Decoded Text (Potential Flag):")
print(decoded_text)

```

Flag : 

Decoded Text (Potential Flag):

NH4CK{An4lyZ!nG_pC4pS_S33ms_T0_b3_FuN!}
