IR=0x10000517
z=int(str(IR),16)
print(z)
x=int("0x7f",16)
print(x)
opcode = int(str(IR),16) & int("0x7f",16)
print(opcode)


ans=IR & 0XFF0
print(ans)