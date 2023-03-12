op1=-10
print(bin(op1))
op2=2
if op1>=0:
    rm=op1>>op2
else:
    rm=(op1+4294967296)>>op2
print(rm)