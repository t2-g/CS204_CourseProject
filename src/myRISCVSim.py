from collections import defaultdict

x=[0]*32
x[2]=int("0x7FFFFFF0",16) #sp - stack pointer
x[3]=int("0x10000000",16) #the beginning address of data segment of memory

clk=0

instruction_memory=defaultdict(lambda:[0,0,0,0])
data_memory=defaultdict(lambda:[0,0,0,0])

global rs1,rs2,opcode,func3,func7,immB,immJ,immR,immS,immU,alu_result,pc

def fetch():


