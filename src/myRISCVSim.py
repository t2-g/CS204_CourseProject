from collections import defaultdict

x=[0]*32
x[2]=int("0x7FFFFFF0",16) #sp - stack pointer
x[3]=int("0x10000000",16) #the beginning address of data segment of memory

clk=0

instruction_memory=defaultdict(lambda:"00")
data_memory=defaultdict(lambda:"00")

global rs1,rs2,opcode,func3,func7,immB,immJ,immR,immS,immU,pc,Op2_Select,Mem_op,Result_select,Branch_trg_sel,is_branch

def read_from_file(file_name):
    try:
        file = open(file_name, 'r')
        for line in file:
            tmp = line.split()
            if len(tmp) == 2:
                address, instruction = tmp[0], tmp[1]
                mem_location = int(address[2:], 16)
                instruction_memory[mem_location] =  instruction[2:4]
                instruction_memory[mem_location + 1] = instruction[4:6]
                instruction_memory[mem_location + 2] = instruction[6:8]
                instruction_memory[mem_location + 3] = instruction[8:10]
        file.close()
    except:
        print("ERROR: Error opening input .mc file\n")
        exit(1)



def control_signal():
def fetch():
def decode():
def execute():
def memory_access():
def write_back():

if __name__=="__main__":
    while(True):
        fetch()
        decode()
        if terminate:
            return
        execute()
        if terminate:
            return
        memory_access()
        write_back()
        clk += 1
        if clk > 16:
            return
        print("Clock CYCLE:", clk, '\n')
