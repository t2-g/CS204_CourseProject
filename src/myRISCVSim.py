from collections import defaultdict

x=[0]*32
x[2]=int("0x7FFFFFF0",16) #sp - stack pointer
x[3]=int("0x10000000",16) #the beginning address of data segment of memory

clk=0

RS1,RS2,RD,PC,IR,MuxB_select,_MuxC_select,MuxINC_select,_MuxY_select,MuxPC_select,MuxMA_select,RegFileAddrA,RegFileAddrB,RegFileAddrC,RegFileInp,RegFileAOut,RegFileBOut,MAR,MDR,opcode,numBytes,RF_Write,immed,PC_Temp,Mem_Write,Mem_Read=[0]*31
#MuxB_select==op2select
#MuxINC_select==IsBranch

ALUOp=[0]*26

data_memory= defaultdict()
instruction_memory=defaultdict()

def IAG():
    global PC 
    if (MuxPC_select==0)
        PC=RA
    else:
        if()

def fetch():
    global IR,MAR,PC_Temp,PC

    MAR=hex(PC)
    ans = instruction_memory[MAR]
    IR=""
    z=len(ans)
    for i in range(len(ans))
        IR+=ans[z-i-1]
    IR= '0X'+IR
    PC_Temp=PC+4

def decode():
    global opcode,immed,RS1,RS2,RD,RF_Write,numBytes,RM,RA,RB,reg,ALUOp
    ALUOp=[0]*26
    opcode = int(str(IR),16) & int("0x7f",16)
    fun3 = (int(str(IR),16) & int("0x7000",16)) >> 12

    message=""

def ImmediateSign(num):
    global immed
    if(immed & 2**(num-1)==0):
        return 
    immed = immed^(2**num-1)
    immed+=1
    immed *= (-1)


