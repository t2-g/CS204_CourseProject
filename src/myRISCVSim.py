from collections import defaultdict
import pandas as pd

x=[0]*32
x[2]=int("0x7FFFFFF0",16) #sp - stack pointer
x[3]=int("0x10000000",16) #the beginning address of data segment of memory

op2select_array=[]
pc=0
clk=0

instruction_memory=defaultdict(lambda:"00")
data_memory=defaultdict(lambda:"00")

global rs1,rs2,rd,opcode,func3,func7,immB,immJ,immI,immS,immU,Op2_Select,Mem_op,ALU_op,Result_select,Branch_trg_sel,is_branch,RFWrite,mem_read,mem_write

def read_from_file(file_name):
    flag=0
    try:
        file = open(file_name, 'r')
        for line in file:
            tmp = line.split()
            if len(tmp) == 2:
                address, instruction = tmp[0], tmp[1]
                
            if flag==0:
                mem_location = int(address[2:], 16)
                instruction_memory[mem_location] =  instruction[2:4]
                instruction_memory[mem_location + 1] = instruction[4:6]
                instruction_memory[mem_location + 2] = instruction[6:8]
                instruction_memory[mem_location + 3] = instruction[8:10]
            if tmp[1]=='$':
                flag=1
            elif flag==1:
                mem_location = int(address[2:], 16)
                data_memory[mem_location] =  instruction[2:4]
                data_memory[mem_location + 1] = instruction[4:6]
                data_memory[mem_location + 2] = instruction[6:8]
                data_memory[mem_location + 3] = instruction[8:10]
        file.close()
    except:
        print("Error opening input .mc file\n")
        exit(1)


def control_signal(_ALUop,_Op2_Select,_Mem_op,_mem_read,_mem_write,_Result_select,_Branch_trg_sel,_is_branch,_RFWrite):
    ALUop=_ALUop
    Op2_Select=_Op2_Select
    Mem_op=_Mem_op
    Result_select=_Result_select
    Branch_trg_sel=_Branch_trg_sel
    is_branch=_is_branch
    RFWrite=_RFWrite
    mem_read=_mem_read
    mem_write=_mem_write
   

def fetch():
    global binary_instruction
    IR='0x'+instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3]
    binary_instruction=bin(int(IR,16))[2:]
    binary_instruction='0'*(32-len(binary_instruction))+binary_instruction 

# def hex_negative():

# def int_negative():


def decode():
    opcode=int(binary_instruction[25:],2)
    func3=int(binary_instruction[17:20],2)
    func7=int(binary_instruction[0:7],2)
    rs2=int(binary_instruction[7:12],2)
    rs1=int(binary_instruction[12:17],2)
    rd=int(binary_instruction[20:25],2)
    sign_extend()
    control_file=pd.read_csv("src\Control.csv")
    if opcode==51:
        if func3==0 and func7==0:
            control_signal(control_file["ALUop"][0],control_file["Op2_Select"][0],control_file["Mem_op"][0],control_file["Mem_read"][0],control_file["Mem_write"][0],control_file["Result_select"][0],control_file["Branch_trg_sel"][0],control_file["is_branch"][0],control_file["RFWrite"][0])
        elif func3==0 and func7==32:
            control_signal(control_file["ALUop"][1],control_file["Op2_Select"][1],control_file["Mem_op"][1],control_file["Mem_read"][1],control_file["Mem_write"][1],control_file["Result_select"][1],control_file["Branch_trg_sel"][1],control_file["is_branch"][1],control_file["RFWrite"][1])            
        elif func3==4 and func7==0:
            control_signal(control_file["ALUop"][2],control_file["Op2_Select"][2],control_file["Mem_op"][2],control_file["Mem_read"][2],control_file["Mem_write"][2],control_file["Result_select"][2],control_file["Branch_trg_sel"][2],control_file["is_branch"][2],control_file["RFWrite"][2])
        elif func3==6 and func7==0:
            control_signal(control_file["ALUop"][3],control_file["Op2_Select"][3],control_file["Mem_op"][3],control_file["Mem_read"][3],control_file["Mem_write"][3],control_file["Result_select"][3],control_file["Branch_trg_sel"][3],control_file["is_branch"][3],control_file["RFWrite"][3])
        elif func3==7 and func7==0:
            control_signal(control_file["ALUop"][4],control_file["Op2_Select"][4],control_file["Mem_op"][4],control_file["Mem_read"][4],control_file["Mem_write"][4],control_file["Result_select"][4],control_file["Branch_trg_sel"][4],control_file["is_branch"][4],control_file["RFWrite"][4])
        elif func3==1 and func7==0:
            control_signal(control_file["ALUop"][5],control_file["Op2_Select"][5],control_file["Mem_op"][5],control_file["Mem_read"][5],control_file["Mem_write"][5],control_file["Result_select"][5],control_file["Branch_trg_sel"][5],control_file["is_branch"][5],control_file["RFWrite"][5])
        elif func3==5 and func7==0:
            control_signal(control_file["ALUop"][6],control_file["Op2_Select"][6],control_file["Mem_op"][6],control_file["Mem_read"][6],control_file["Mem_write"][6],control_file["Result_select"][6],control_file["Branch_trg_sel"][6],control_file["is_branch"][6],control_file["RFWrite"][6])
        elif func3==5 and func7==32:
            control_signal(control_file["ALUop"][7],control_file["Op2_Select"][7],control_file["Mem_op"][7],control_file["Mem_read"][7],control_file["Mem_write"][7],control_file["Result_select"][7],control_file["Branch_trg_sel"][7],control_file["is_branch"][7],control_file["RFWrite"][7])
        elif func3==2 and func7==0:
            control_signal(control_file["ALUop"][8],control_file["Op2_Select"][8],control_file["Mem_op"][8],control_file["Mem_read"][8],control_file["Mem_write"][8],control_file["Result_select"][8],control_file["Branch_trg_sel"][8],control_file["is_branch"][8],control_file["RFWrite"][8])
        else:
            print("Invalid instruction")
            exit(1)
    elif opcode==19:
        if func3==0:
            control_signal(control_file["ALUop"][9],control_file["Op2_Select"][9],control_file["Mem_op"][9],control_file["Mem_read"][9],control_file["Mem_write"][9],control_file["Result_select"][9],control_file["Branch_trg_sel"][9],control_file["is_branch"][9],control_file["RFWrite"][9])
        elif func3==6:
            control_signal(control_file["ALUop"][10],control_file["Op2_Select"][10],control_file["Mem_op"][10],control_file["Mem_read"][10],control_file["Mem_write"][10],control_file["Result_select"][10],control_file["Branch_trg_sel"][10],control_file["is_branch"][10],control_file["RFWrite"][10])
        elif func3==7:
            control_signal(control_file["ALUop"][11],control_file["Op2_Select"][11],control_file["Mem_op"][11],control_file["Mem_read"][11],control_file["Mem_write"][11],control_file["Result_select"][11],control_file["Branch_trg_sel"][11],control_file["is_branch"][11],control_file["RFWrite"][11])
        else:
            print("Invalid instruction")
            exit(1)
    elif opcode==3:
        if func3==0:
            control_signal(control_file["ALUop"][12],control_file["Op2_Select"][12],control_file["Mem_op"][12],control_file["Mem_read"][12],control_file["Mem_write"][12],control_file["Result_select"][12],control_file["Branch_trg_sel"][12],control_file["is_branch"][12],control_file["RFWrite"][12])
        elif func3==1:
            control_signal(control_file["ALUop"][13],control_file["Op2_Select"][13],control_file["Mem_op"][13],control_file["Mem_read"][13],control_file["Mem_write"][13],control_file["Result_select"][13],control_file["Branch_trg_sel"][13],control_file["is_branch"][13],control_file["RFWrite"][13])
        elif func3==2:
            control_signal(control_file["ALUop"][14],control_file["Op2_Select"][14],control_file["Mem_op"][14],control_file["Mem_read"][14],control_file["Mem_write"][14],control_file["Result_select"][14],control_file["Branch_trg_sel"][14],control_file["is_branch"][14],control_file["RFWrite"][14])
        else:
            print("Invalid Instruction")
            exit(1)
    elif opcode==35:
        if func3==0:
            control_signal(control_file["ALUop"][15],control_file["Op2_Select"][15],control_file["Mem_op"][15],control_file["Mem_read"][15],control_file["Mem_write"][15],control_file["Result_select"][15],control_file["Branch_trg_sel"][15],control_file["is_branch"][15],control_file["RFWrite"][15])
        elif func3==1:
            control_signal(control_file["ALUop"][16],control_file["Op2_Select"][16],control_file["Mem_op"][16],control_file["Mem_read"][16],control_file["Mem_write"][16],control_file["Result_select"][16],control_file["Branch_trg_sel"][16],control_file["is_branch"][16],control_file["RFWrite"][16])
        elif func3==2:
            control_signal(control_file["ALUop"][17],control_file["Op2_Select"][17],control_file["Mem_op"][17],control_file["Mem_read"][17],control_file["Mem_write"][17],control_file["Result_select"][17],control_file["Branch_trg_sel"][17],control_file["is_branch"][17],control_file["RFWrite"][17])
        else:
            print("Invalid Instruction")
            exit(1)
    elif opcode==99:
        if func3==0:
            control_signal(control_file["ALUop"][18],control_file["Op2_Select"][18],control_file["Mem_op"][18],control_file["Mem_read"][18],control_file["Mem_write"][18],control_file["Result_select"][18],control_file["Branch_trg_sel"][18],control_file["is_branch"][18],control_file["RFWrite"][18])
        if func3==1:
            control_signal(control_file["ALUop"][19],control_file["Op2_Select"][19],control_file["Mem_op"][19],control_file["Mem_read"][19],control_file["Mem_write"][19],control_file["Result_select"][19],control_file["Branch_trg_sel"][19],control_file["is_branch"][19],control_file["RFWrite"][19])
        if func3==4:
            control_signal(control_file["ALUop"][20],control_file["Op2_Select"][20],control_file["Mem_op"][20],control_file["Mem_read"][20],control_file["Mem_write"][20],control_file["Result_select"][20],control_file["Branch_trg_sel"][20],control_file["is_branch"][20],control_file["RFWrite"][20])
        if func3==5:
            control_signal(control_file["ALUop"][21],control_file["Op2_Select"][21],control_file["Mem_op"][21],control_file["Mem_read"][21],control_file["Mem_write"][21],control_file["Result_select"][21],control_file["Branch_trg_sel"][21],control_file["is_branch"][21],control_file["RFWrite"][21])
        else:
            print("Invalid Instruction")
            exit(1)
    elif opcode==111:
        control_signal(control_file["ALUop"][22],control_file["Op2_Select"][22],control_file["Mem_op"][22],control_file["Mem_read"][22],control_file["Mem_write"][22],control_file["Result_select"][22],control_file["Branch_trg_sel"][22],control_file["is_branch"][22],control_file["RFWrite"][22])
    elif opcode==103 and func3==0:
        control_signal(control_file["ALUop"][23],control_file["Op2_Select"][23],control_file["Mem_op"][23],control_file["Mem_read"][23],control_file["Mem_write"][23],control_file["Result_select"][23],control_file["Branch_trg_sel"][23],control_file["is_branch"][23],control_file["RFWrite"][23])
    elif opcode==55:
        control_signal(control_file["ALUop"][24],control_file["Op2_Select"][24],control_file["Mem_op"][24],control_file["Mem_read"][24],control_file["Mem_write"][24],control_file["Result_select"][24],control_file["Branch_trg_sel"][24],control_file["is_branch"][24],control_file["RFWrite"][24])
    elif opcode==23:
        control_signal(control_file["ALUop"][25],control_file["Op2_Select"][25],control_file["Mem_op"][25],control_file["Mem_read"][25],control_file["Mem_write"][25],control_file["Result_select"][25],control_file["Branch_trg_sel"][25],control_file["is_branch"][25],control_file["RFWrite"][25])
    else:
        print("Invalid instruction")
        exit(1)
    



            

            
def sign_extend():
    global immI,immU,immJ,immB,immS
    #I-Type
    tempI = binary_instruction[20:]
    #S-Type
    tempS = binary_instruction[0:7] + binary_instruction[20:25]
    #B-Type
    tempB = binary_instruction[0]+ binary_instruction[24] + binary_instruction[2:7] + binary_instruction[20:24]
    #U-Type
    tempU=binary_instruction[0:20]
    #J-Type
    tempJ=binary_instruction[0] + binary_instruction[12:20] + binary_instruction[11] + binary_instruction[1:11]
    
    if(tempI[:-1]=='0' or tempS[:-1]=='0' or tempB[:-1]=='0' or tempU[:-1]=='0' or tempJ[:-1]='0'):
        immI=int('0'*(32-len(tempI)),2)
        immS=int('0'*(32-len(tempS)),2)
        immB=int('0'*(32-len(tempB)),2)
        immU=int('0'*(32-len(tempU)),2)
        immJ=int('0'*(32-len(tempJ)),2)
    elif(tempI[:-1]=='1' or tempS[:-1]=='1' or tempB[:-1]=='1' or tempU[:-1]=='1' or tempJ[:-1]='1'):
        immI=int('1'*(32-len(tempI)),2)
        immS=int('1'*(32-len(tempS)),2)
        immB=int('1'*(32-len(tempB)),2)
        immU=int('1'*(32-len(tempU)),2)
        immJ=int('1'*(32-len(tempJ)),2)
        
def execute():
    global ALUop,rm,op1,op2,rs1,rs2,mem_address

    op1=rs1
    #
    op2=op2select_array[Op2_Select]

    # instruction_set=pd.read_csv("src\Instruction_Set_List.csv")
    
    #-------------------------------------------
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
    elif(ALUop==9):#addi
        rm=hex(int(op1,16)+int(op2,2,len(op2)))
        print("EXECUTE: ADDI", int(op1, 16), "and", int(op2, 2, len(op2)))
        return
    
    elif(ALUop==10):#ori
        rm=hex(int(op1,16) | int(op2,2,len(op2)))
        print("EXECUTE: ORI", int(op1, 16), "and", int(op2, 2, len(op2)))
        return
    elif(ALUop==11):#andi
        rm=hex(int(op1,16) | int(op2,2,len(op2)))
        print("EXECUTE: ANDI", int(op1, 16), "and", int(op2, 2, len(op2)))
        return
    elif(ALUop==12): #lb
        mem_address=int(op1,16)+int(op2,2,len(op2))
        print("EXECUTE: ADD", int(op1), "and", int(op2, 2, len(op2)))
    elif(ALUop==13): #lh

        return
    elif(ALUop==14):#lw
        return
    elif(ALUop==15):#sb
        return
    elif(ALUop==16):
        return
    elif(ALUop==17):
        return
    elif(ALUop==18):
        return
    elif(ALUop==19):
        return
    elif(ALUop==20):
        return
    elif(ALUop==21):
        return
    elif(ALUop==22):
        return
    elif(ALUop==23):
        return
    elif(ALUop==24):
        return
    elif(ALUop==25):
        return
    else:
        return



def memory_access():
    if(ALUop == 12):
        ma = data_memory[rm] + data_memory[rm+1]
    

def write_back():
    return

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
