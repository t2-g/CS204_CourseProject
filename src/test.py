
ALUop=3
op1=0x12
op2=0x13
rs1=
rs2=
rm=


    if(ALUop==0): #add instruction
        rm=hex(int(op1,16)) + hex(int(op2,16))
        print("EXECUTE ","add",int(op1,16),"and",int(op2,16))
    elif(ALUop==1):# sub instruction
        rm=hex(int(op1,16)) - hex(int(op2,16))
        print("EXECUTE ","sub",int(rs1,16),"and",int(rs2,16))
    elif(ALUop==2): #xor
        rm=hex(int (int(op1,16))) ^ hex(int(int(rs2,16)))
        print("EXECUTE ","xor",int(rs1,16),"and",int(rs2,16))
    elif(ALUop==3): #or
        rm=hex(int (int(op1,16))) | hex(int(int(rs2,16)))
        print("EXECUTE ","or",int(rs1,16),"and",int(rs2,16))
    elif(ALUop==4): #and
        rm=hex(int (int(op1,16))) & hex(int(int(rs2,16)))
        print("EXECUTE ","and",int(rs1,16),"and",int(rs2,16))
    elif(ALUop==5): #sll
        if(int(op2, 16) < 0):
            print("ERROR: Shift by negative!\n")
            exit(1)
            return
        else:
            rm = hex(int(int(op1, 16) << int(op2, 16)))
            print("EXECUTE:","sll", int(op1, 16), "and", int(op2, 16))
    elif(ALUop==6):#srl
        if(int(op2, 16) < 0):
            print("ERROR: Shift by negative!\n")
            exit(1)
            return
        else:
            rm= hex(int(op1, 16) >> int(op2, 16))
            print("EXECUTE:","srl", int(op1, 16), "and", int(op2, 16))
        
        return
    elif(ALUop==7): #sra
        if(int(op2, 16) < 0):
            print("ERROR: Shift by negative!\n")
            exit(1)
            return
        else:
            rm = bin(int(int(op1, 16) >> int(op2, 16)))
            if op1[2] == '8' or op1[2] == '9' or op1[2] == 'a' or op1[2] == 'b' or op1[2] == 'c' or op1[2] == 'd' or operand1[2] == 'e' or operand1[2] == 'f':
                rm = '0b' + (34 - len(rm)) * '1' + rm[2:]
            rm = hex(int(rm, 2))
            print("EXECUTE:","sra" , int(op1, 16), "and", int(op2, 16))
        return
    elif(ALUop==8):#slt
        if (int(op1, 16) < int(op2, 16)):
            rm = hex(1)
        else:
            rm = hex(0)
        print("EXECUTE:","slt", int(op1, 16), "and", int(op2, 16))
        return