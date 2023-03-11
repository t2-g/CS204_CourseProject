x="0x00000011"
y=bin(int(x,16))[2:]
y='0'*(32-len(y))+y
print(y,len(y))