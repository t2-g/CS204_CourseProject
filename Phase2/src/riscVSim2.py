from collections import defaultdict
# from multiprocessing import Process
import time
import threading
import pandas as pd

x = ["0x00000000"]*32  # Register File
x[2] = "0x7FFFFFF0"  # sp - stack pointer
x[3] = "0x10000000"  # the beginning address of data segment of memory

global pc, clk
global pipelining_knob, data_forwarding_knob, register_file_knob, pipeline_registers_knob, specify_instruction_knob

pipelining_knob = 1
data_forwarding_knob = 1
register_file_knob = 1
pipeline_registers_knob = 1
specify_instruction_knob = 1

pc = 0
clk = 0

instruction_memory = defaultdict(lambda: "00")  # Memory for Instructions
data_memory = defaultdict(lambda: "00")  # Memory for Data


def read_from_file(file_name):
    flag = 0  # To distinguish between instruction and data
    try:
        file = open(file_name, 'r')
        for line in file:
            tmp = line.split()
            # print(tmp)
            if len(tmp) == 2:
                address, instruction = tmp[0], tmp[1]
            if flag == 0:  # Storing Instruction in instruction_memory
                if(instruction == '$'):
                    flag = 1
                    continue
                # print(address, instruction)
                mem_location = int(address[2:], 16)
                instruction_memory["0x"+'0'*(8-(len(hex(mem_location))-2)) +
                                   hex(mem_location)[2:]] = instruction[2:4]
                instruction_memory["0x"+'0'*(8-(len(hex(mem_location + 1))-2))+hex(
                    mem_location + 1)[2:]] = instruction[4:6]
                instruction_memory["0x"+'0'*(8-(len(hex(mem_location + 2))-2))+hex(
                    mem_location + 2)[2:]] = instruction[6:8]
                instruction_memory["0x"+'0'*(8-(len(hex(mem_location + 3))-2))+hex(
                    mem_location + 3)[2:]] = instruction[8:10]
            else:  # Storing Data in Data_memory
                mem_location = int(address[2:], 16)
                data_memory["0x"+'0'*(8-(len(hex(mem_location))-2)) +
                            hex(mem_location)[2:]] = instruction[2:4]
                data_memory["0x"+'0'*(8-(len(hex(mem_location + 1))-2)) +
                            hex(mem_location + 1)[2:]] = instruction[4:6]
                data_memory["0x"+'0'*(8-(len(hex(mem_location + 2))-2)) +
                            hex(mem_location + 2)[2:]] = instruction[6:8]
                data_memory["0x"+'0'*(8-(len(hex(mem_location + 3))-2)) +
                            hex(mem_location + 3)[2:]] = instruction[8:10]
        print("File read complete")
        file.close()
    except:
        print("Error opening input .mc file\n")
        return

 # To define control signals


def control_signal(_ALUop, _Op2_Select, _Mem_op, _mem_read, _mem_write, _Result_select, _Branch_trg_sel, _is_branch, _RFWrite):
    global Op2_Select, Mem_op, ALUop, Result_select, Branch_trg_sel, is_branch, RFWrite, mem_read, mem_write
    ALUop = _ALUop
    Op2_Select = _Op2_Select
    Mem_op = _Mem_op
    Result_select = _Result_select
    Branch_trg_sel = _Branch_trg_sel
    is_branch = _is_branch
    RFWrite = _RFWrite
    mem_read = _mem_read
    mem_write = _mem_write
    print("control generated")


def sign_extend():
    global immI, immU, immJ, immB, immS, binary_instruction
    # I-Type
    tempI = binary_instruction[0:12]
    # S-Type
    tempS = binary_instruction[0:7] + binary_instruction[20:25]
    # B-Type
    tempB = binary_instruction[0] + binary_instruction[24] + \
        binary_instruction[1:7] + binary_instruction[20:24] + '0'
    # U-Type
    tempU = binary_instruction[0:20]
    # J-Type
    tempJ = binary_instruction[0] + binary_instruction[12:20] + \
        binary_instruction[11] + binary_instruction[1:11] + '0'

    if tempI[0] == '0' or tempS[0] == '0' or tempB[0] == '0' or tempU[0] == '0' or tempJ[0] == '0':
        # extending signs for positive numbers
        immI = '0'*(32-len(tempI))+tempI
        immS = '0'*(32-len(tempS))+tempS
        immB = '0'*(32-len(tempB))+tempB
        immU = tempU + '0'*12
        immJ = '0'*(32-len(tempJ))+tempJ
    elif tempI[0] == '1' or tempS[0] == '1' or tempB[0] == '1' or tempU[0] == '1' or tempJ[0] == '1':
        # extending signs for negative nubmers
        immI = '1'*(32-len(tempI))+tempI
        immS = '1'*(32-len(tempS))+tempS
        immB = '1'*(32-len(tempB))+tempB
        immU = tempU + '0'*12
        immJ = '1'*(32-len(tempJ))+tempJ
# To fetch the instruction from instruction_memory


def fetch():
    global binary_instruction, clk
    IR = '0x'+instruction_memory["0x"+'0'*(8-(len(hex(pc))-2))+hex(pc)[2:]]+instruction_memory["0x"+'0'*(8-(len(hex(pc+1))-2))+hex(pc+1)[
        2:]] + instruction_memory["0x"+'0'*(8-(len(hex(pc+2))-2))+hex(pc+2)[2:]]+instruction_memory["0x"+'0'*(8-(len(hex(pc+3))-2))+hex(pc+3)[2:]]
    binary_instruction = bin(int(IR, 16))[2:]
    binary_instruction = '0'*(32-len(binary_instruction))+binary_instruction
    print("fetch complete for {clk}")
# To decode the instruction and reading from register file and generating control signals


dec_pipeline_reg = {'pc': [0, 0], 'binary_instruction': [0, 0]}


def decode():
    global rs1, rs2, rd, op1, opcode, func3, func7, immB, immJ, immI, immS, immU, Op2_Select, Mem_op, ALUop, Result_select, Branch_trg_sel, is_branch, RFWrite, mem_read, mem_write, binary_instruction, num_b
    opcode = int(binary_instruction[25:], 2)
    func3 = int(binary_instruction[17:20], 2)
    func7 = int(binary_instruction[0:7], 2)
    rs2 = int(binary_instruction[7:12], 2)
    rs1 = int(binary_instruction[12:17], 2)
    rd = int(binary_instruction[20:25], 2)
    sign_extend()
    op1 = int(x[rs1], 16)  # decoded operand 1
    if (immI[0] == '0'):
        immI = int(immI, 2)
    else:
        immI = int(immI, 2)-4294967296
    if (immS[0] == '0'):
        immS = int(immS, 2)
    else:
        immS = int(immS, 2)-4294967296
    if (immB[0] == '0'):
        immB = int(immB, 2)
    else:
        immB = int(immB, 2)-4294967296
    if (immJ[0] == '0'):
        immJ = int(immJ, 2)
    else:
        immJ = int(immJ, 2)-4294967296
    if (immU[0] == '0'):
        immU = int(immU, 2)
    else:
        immU = int(immU, 2)-4294967296
    control_file = pd.read_csv(
        r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\test\control.csv")
    if opcode == 51:
        if func3 == 0 and func7 == 0:
            print("And operation")
            control_signal(control_file["ALUop"][0], control_file["Op2_Select"][0], control_file["Mem_op"][0], control_file["Mem_read"][0], control_file["Mem_write"]
                           [0], control_file["Result_select"][0], control_file["Branch_trg_sel"][0], control_file["is_branch"][0], control_file["RFWrite"][0])
        elif func3 == 0 and func7 == 32:  # SUB
            print("Sub operation")
            control_signal(control_file["ALUop"][1], control_file["Op2_Select"][1], control_file["Mem_op"][1], control_file["Mem_read"][1], control_file["Mem_write"]
                           [1], control_file["Result_select"][1], control_file["Branch_trg_sel"][1], control_file["is_branch"][1], control_file["RFWrite"][1])
        elif func3 == 4 and func7 == 0:  # XOR
            print("XOR operation")
            control_signal(control_file["ALUop"][2], control_file["Op2_Select"][2], control_file["Mem_op"][2], control_file["Mem_read"][2], control_file["Mem_write"]
                           [2], control_file["Result_select"][2], control_file["Branch_trg_sel"][2], control_file["is_branch"][2], control_file["RFWrite"][2])
        elif func3 == 6 and func7 == 0:  # OR
            print("OR operation")
            control_signal(control_file["ALUop"][3], control_file["Op2_Select"][3], control_file["Mem_op"][3], control_file["Mem_read"][3], control_file["Mem_write"]
                           [3], control_file["Result_select"][3], control_file["Branch_trg_sel"][3], control_file["is_branch"][3], control_file["RFWrite"][3])
        elif func3 == 7 and func7 == 0:  # AND
            print("And operation")
            control_signal(control_file["ALUop"][4], control_file["Op2_Select"][4], control_file["Mem_op"][4], control_file["Mem_read"][4], control_file["Mem_write"]
                           [4], control_file["Result_select"][4], control_file["Branch_trg_sel"][4], control_file["is_branch"][4], control_file["RFWrite"][4])
        elif func3 == 1 and func7 == 0:  # SLL
            print("sll operation")
            control_signal(control_file["ALUop"][5], control_file["Op2_Select"][5], control_file["Mem_op"][5], control_file["Mem_read"][5], control_file["Mem_write"]
                           [5], control_file["Result_select"][5], control_file["Branch_trg_sel"][5], control_file["is_branch"][5], control_file["RFWrite"][5])
        elif func3 == 5 and func7 == 0:  # SRL
            print("srl operation")
            control_signal(control_file["ALUop"][6], control_file["Op2_Select"][6], control_file["Mem_op"][6], control_file["Mem_read"][6], control_file["Mem_write"]
                           [6], control_file["Result_select"][6], control_file["Branch_trg_sel"][6], control_file["is_branch"][6], control_file["RFWrite"][6])
        elif func3 == 5 and func7 == 32:  # SRA
            print("sra operation")
            control_signal(control_file["ALUop"][7], control_file["Op2_Select"][7], control_file["Mem_op"][7], control_file["Mem_read"][7], control_file["Mem_write"]
                           [7], control_file["Result_select"][7], control_file["Branch_trg_sel"][7], control_file["is_branch"][7], control_file["RFWrite"][7])
        elif func3 == 2 and func7 == 0:  # SLT
            print("slt operation")
            control_signal(control_file["ALUop"][8], control_file["Op2_Select"][8], control_file["Mem_op"][8], control_file["Mem_read"][8], control_file["Mem_write"]
                           [8], control_file["Result_select"][8], control_file["Branch_trg_sel"][8], control_file["is_branch"][8], control_file["RFWrite"][8])
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 19:  # I - type
        if func3 == 0:  # addi
            print("addi operation")
            control_signal(control_file["ALUop"][9], control_file["Op2_Select"][9], control_file["Mem_op"][9], control_file["Mem_read"][9], control_file["Mem_write"]
                           [9], control_file["Result_select"][9], control_file["Branch_trg_sel"][9], control_file["is_branch"][9], control_file["RFWrite"][9])
        elif func3 == 6:  # ori
            print("ori operation")
            control_signal(control_file["ALUop"][10], control_file["Op2_Select"][10], control_file["Mem_op"][10], control_file["Mem_read"][10], control_file["Mem_write"]
                           [10], control_file["Result_select"][10], control_file["Branch_trg_sel"][10], control_file["is_branch"][10], control_file["RFWrite"][10])
        elif func3 == 7:  # andi
            print("andi operation")
            control_signal(control_file["ALUop"][11], control_file["Op2_Select"][11], control_file["Mem_op"][11], control_file["Mem_read"][11], control_file["Mem_write"]
                           [11], control_file["Result_select"][11], control_file["Branch_trg_sel"][11], control_file["is_branch"][11], control_file["RFWrite"][11])
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 3:
        if func3 == 0:  # lb
            print("lb operation")
            control_signal(control_file["ALUop"][12], control_file["Op2_Select"][12], control_file["Mem_op"][12], control_file["Mem_read"][12], control_file["Mem_write"]
                           [12], control_file["Result_select"][12], control_file["Branch_trg_sel"][12], control_file["is_branch"][12], control_file["RFWrite"][12])
            num_b = 1
        elif func3 == 1:  # lh
            print("lh operation")
            control_signal(control_file["ALUop"][13], control_file["Op2_Select"][13], control_file["Mem_op"][13], control_file["Mem_read"][13], control_file["Mem_write"]
                           [13], control_file["Result_select"][13], control_file["Branch_trg_sel"][13], control_file["is_branch"][13], control_file["RFWrite"][13])
            num_b = 2
        elif func3 == 2:  # lw
            print("lw opeartion")
            control_signal(control_file["ALUop"][14], control_file["Op2_Select"][14], control_file["Mem_op"][14], control_file["Mem_read"][14], control_file["Mem_write"]
                           [14], control_file["Result_select"][14], control_file["Branch_trg_sel"][14], control_file["is_branch"][14], control_file["RFWrite"][14])
            num_b = 4
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 35:
        if func3 == 0:  # sb
            print("sb operation")
            control_signal(control_file["ALUop"][15], control_file["Op2_Select"][15], control_file["Mem_op"][15], control_file["Mem_read"][15], control_file["Mem_write"]
                           [15], control_file["Result_select"][15], control_file["Branch_trg_sel"][15], control_file["is_branch"][15], control_file["RFWrite"][15])
            num_b = 1
        elif func3 == 1:  # sh
            print("sh operation")
            control_signal(control_file["ALUop"][16], control_file["Op2_Select"][16], control_file["Mem_op"][16], control_file["Mem_read"][16], control_file["Mem_write"]
                           [16], control_file["Result_select"][16], control_file["Branch_trg_sel"][16], control_file["is_branch"][16], control_file["RFWrite"][16])
            num_b = 2
        elif func3 == 2:  # sw
            print("sw operation")
            control_signal(control_file["ALUop"][17], control_file["Op2_Select"][17], control_file["Mem_op"][17], control_file["Mem_read"][17], control_file["Mem_write"]
                           [17], control_file["Result_select"][17], control_file["Branch_trg_sel"][17], control_file["is_branch"][17], control_file["RFWrite"][17])
            num_b = 4
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 99:
        if func3 == 0:  # beq
            print("beq opeartion")
            control_signal(control_file["ALUop"][18], control_file["Op2_Select"][18], control_file["Mem_op"][18], control_file["Mem_read"][18], control_file["Mem_write"]
                           [18], control_file["Result_select"][18], control_file["Branch_trg_sel"][18], control_file["is_branch"][18], control_file["RFWrite"][18])
        elif func3 == 1:  # bne
            print("bne operation")
            control_signal(control_file["ALUop"][19], control_file["Op2_Select"][19], control_file["Mem_op"][19], control_file["Mem_read"][19], control_file["Mem_write"]
                           [19], control_file["Result_select"][19], control_file["Branch_trg_sel"][19], control_file["is_branch"][19], control_file["RFWrite"][19])
        elif func3 == 4:  # blt
            print("blt operation")
            control_signal(control_file["ALUop"][20], control_file["Op2_Select"][20], control_file["Mem_op"][20], control_file["Mem_read"][20], control_file["Mem_write"]
                           [20], control_file["Result_select"][20], control_file["Branch_trg_sel"][20], control_file["is_branch"][20], control_file["RFWrite"][20])
        elif func3 == 5:  # bge
            print("bge operation")
            control_signal(control_file["ALUop"][21], control_file["Op2_Select"][21], control_file["Mem_op"][21], control_file["Mem_read"][21], control_file["Mem_write"]
                           [21], control_file["Result_select"][21], control_file["Branch_trg_sel"][21], control_file["is_branch"][21], control_file["RFWrite"][21])
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 111:  # jal
        print("jal operation")
        control_signal(control_file["ALUop"][22], control_file["Op2_Select"][22], control_file["Mem_op"][22], control_file["Mem_read"][22], control_file["Mem_write"]
                       [22], control_file["Result_select"][22], control_file["Branch_trg_sel"][22], control_file["is_branch"][22], control_file["RFWrite"][22])
    elif opcode == 103 and func3 == 0:  # jalr
        print("Jalr operation")
        control_signal(control_file["ALUop"][23], control_file["Op2_Select"][23], control_file["Mem_op"][23], control_file["Mem_read"][23], control_file["Mem_write"]
                       [23], control_file["Result_select"][23], control_file["Branch_trg_sel"][23], control_file["is_branch"][23], control_file["RFWrite"][23])
    elif opcode == 55:  # lui
        print("lui operation")
        control_signal(control_file["ALUop"][24], control_file["Op2_Select"][24], control_file["Mem_op"][24], control_file["Mem_read"][24], control_file["Mem_write"]
                       [24], control_file["Result_select"][24], control_file["Branch_trg_sel"][24], control_file["is_branch"][24], control_file["RFWrite"][24])
    elif opcode == 23:  # auipc
        print("Auipc operation")
        control_signal(control_file["ALUop"][25], control_file["Op2_Select"][25], control_file["Mem_op"][25], control_file["Mem_read"][25], control_file["Mem_write"]
                       [25], control_file["Result_select"][25], control_file["Branch_trg_sel"][25], control_file["is_branch"][25], control_file["RFWrite"][25])
    else:
        if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
            print("Invalid instruction")
        else:
            print("End of the Program")
        terminate()


ex_pipeline_reg = {'pc': [0, 0], 'rs2': [0, 0], 'immI': [0, 0], 'immS': [
    0, 0], 'immB': [0, 0], 'immJ': [0, 0], 'op1': [0, 0], 'ALUop': [0, 0]}


def execute():
    # print("Execute Started")
    global rm, is_branch, Branch_trg_sel, offset, Branch_target_add, num_b, pc_new, pc, op2, Op2_Select, Mem_op
    pc_new = pc+4

    # selection of the second operand
    if Op2_Select == 0:
        op2 = int(x[rs2], 16)
    elif Op2_Select == 1:
        op2 = immI
    else:
        op2 = immS

    # selection of the type of immediate to branch at
    if Branch_trg_sel == 0:
        offset = immB
    else:
        offset = immJ
    # print("ALUop", ALUop)
    if (ALUop == 0):  # add instruction
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "ADD operation on", op1, "and", op2)
    elif (ALUop == 1):  # sub instruction
        rm = hex(op1 - op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "SUB operation on", op1, "and", op2)
    elif (ALUop == 2):  # xor
        rm = hex(op1 ^ op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "XOR operation on", op1, "and", op2)
    elif (ALUop == 3):  # or
        rm = hex(op1 | op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "OR operation on", op1, "and", op2)
    elif (ALUop == 4):  # and
        rm = hex(op1 & op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "AND operation on", op1, "and", op2)
    elif (ALUop == 5):  # sll
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            exit(1)
        else:
            rm = hex(op1 << op2)
            rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
            print("EXECUTE: ", "SLL operation on", op1, "and", op2)
    elif (ALUop == 6):  # srl
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            return
        else:
            if op1 >= 0:
                rm = hex(op1 >> op2)
            else:
                rm = hex((op1+4294967296) >> op2)
            rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
            print("EXECUTE: ", "SRL operation on", op1, "and", op2)
        return
    elif (ALUop == 7):  # sra
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            return
        else:
            rm = op1 >> op2
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE:", "SRA", op1, "and", op2)
        return
    elif (ALUop == 8):  # slt
        if (op1 < op2):
            rm = hex(1)
        else:
            rm = hex(0)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE:", "SLT", op1, "and", op2)
        return
    elif (ALUop == 9):  # addi
        rm = hex(op1+op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ADDI", op1, "and", op2)
        return

    elif (ALUop == 10):  # ori
        rm = hex(op1 | op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ORI", op1, "and", op2)
        return

    elif (ALUop == 11):  # andi
        rm = hex(op1 & op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ANDI", op1, "and", op2)
        return

    elif (ALUop == 12):  # lb
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LB", op1, "and", op2)

    elif (ALUop == 13):  # lh
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LH ", op1, "and", op2)
        return
    elif (ALUop == 14):  # lw
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LW ", op1, "and", op2)
        return
    elif (ALUop == 15):  # sb
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SB ", op1, "and", op2)
        return
    elif (ALUop == 16):  # sh
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SH ", op1, "and", op2)
        return
    elif (ALUop == 17):  # sw
        rm = hex(op1 + op2)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SW ", op1, "and", op2)
        return
    elif (ALUop == 18):  # beq
        if (op1 == op2):
            is_branch = 1
            Branch_target_add = pc+offset
        print("EXECUTE: BEQ ", op1, "and", op2)
        return
    elif (ALUop == 19):  # bne
        if (op1 != op2):
            is_branch = 1
            Branch_target_add = pc+offset
        print("EXECUTE: BNE ", op1, "and", op2)
        return

    elif (ALUop == 20):  # blt
        if (op1 < op2):
            is_branch = 1
            Branch_target_add = pc+offset
        print("EXECUTE: BLT ", op1, "and", op2)
        return
    elif (ALUop == 21):  # bge
        if (op1 >= op2):
            is_branch = 1
            Branch_target_add = pc+offset
        print("EXECUTE: BGE ", op1, "and", op2)
        return
    elif (ALUop == 22):  # jal
        rm = hex(pc+4)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        Branch_target_add = pc+offset
        print("EXECUTE: JAL")
        return
    elif (ALUop == 23):  # jalr
        rm = hex(pc+4)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        pc = rs1+op2
        print("EXECUTE: JALR")
        return
    elif (ALUop == 24):  # lui
        rm = hex(immU)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LUI")
        return
    elif (ALUop == 25):  # auipc
        rm = hex(pc+immU)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: AUIPC")
        return
    else:
        print("error: no matching ALU operation is possible for this instruction")
        exit(1)


ma_pipeline_reg = {'pc': [0, 0], 'rm': [0, 0], 'mem_read': [0, 0]}


def memory_access():
    if (Mem_op == 0):
        print("no memory operation")
        return
    global ma
    if mem_read == 1:
        if (num_b == 1):  # lb
            ma = "0x"+data_memory[rm]
            print("MEMORY ACCESSING: LOAD BYTE", ma, " from ", rm)
            return
        elif (num_b == 2):  # lh
            ma = "0x"+data_memory[rm] + data_memory[hex(int(rm, 16)+1)]
            print("MEMORY ACCESSING: LOAD HALFWORD", ma, " from ", rm)
            return
        elif (num_b == 4):  # lw
            ma = "0x"+data_memory[rm] + data_memory[hex(int(rm, 16)+1)] + data_memory[hex(
                int(rm, 16)+2)] + data_memory[hex(int(rm, 16)+3)]
            print("MEMORY ACCESSING: LOAD WORD", ma, " from ", rm)
            return
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid Memory Operation")
            else:
                print("End of the Program")
            terminate()
    else:
        print(num_b, x[rs2], rm)
        if (num_b == 1):  # sb
            data_memory[rm] = x[rs2][2:4]
            print("MEMORY ACCESSING: STORE BYTE", rs2, " to ", rm)
            return
        elif (num_b == 2):  # sh
            data_memory[rm] = x[rs2][2:4]
            data_memory[hex(int(rm, 16)+1)] = x[rs2][4:6]
            print("MEMORY ACCESSING: STORE HALFWORD", rs2, " to ", rm)
            return
        elif (num_b == 4):  # sw
            data_memory[rm] = x[rs2][2:4]
            data_memory[hex(int(rm, 16)+1)] = x[rs2][4:6]
            data_memory[hex(int(rm, 16)+2)] = x[rs2][6:8]
            data_memory[hex(int(rm, 16)+3)] = x[rs2][8:10]
            print("MEMORY ACCESSING: STORE WORD", rs2, " to ", rm)
            return
        else:
            if(instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid Memory Operation")
            else:
                print("End of the Program")
            terminate()


wb_pipeline_reg = {pc_new: [0, 0], pc: [0, 0], result_write: [
    0, 0], Branch_target_add: [0, 0], ma: [0, 0]}


def write_back():
    global result_write, pc_new, pc, Branch_target_add, ma
    if (RFWrite == 1):
        if (Result_select == 0):
            result_write = rm
        elif (Result_select == 1):
            result_write = ma
        elif (Result_select == 2):
            result_write = hex(immU)
            result_write = "0x"+'0'*(8-(len(result_write)-2))+result_write[2:]
        elif (Result_select == 3):
            pc_new = hex(pc_new)
            pc_new = "0x"+'0'*(8-(len(pc_new)-2))+pc_new[2:]
            result_write = pc_new
        x[rd] = result_write
    # print(is_branch)
    if is_branch == 0:
        pc = pc_new
    elif is_branch == 1:
        pc = Branch_target_add
    else:
        # print(rm,pc)
        pc = int(rm, 16)
    print("WRITING REGISTER FILE ", rd, " with ", result_write)
    # print(pc)
    return


def terminate():
    OutputFile_txt(
        r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\test\abc.txt")
    # OutputFile_txt("abc.txt")
    exit(1)


def OutputFile_txt(file_name):
    file = open(file_name, "w")
    m = "0x0"
    j = 0
    k = "0x0"
    file.write("Instruction Memory\n\n")
    for i in instruction_memory:
        # print(instruction_memory[i])
        if(j == 0):
            curr = '0x'
        curr = curr + instruction_memory[i]
        j = j + 1
        i = hex(int(m, 16) + 1)
        if(j == 4):
            file.write(k + " " + curr + "\n")
            k = i
        j %= 4

    file.write("\nData Memory\n\n")
    l = 0
    k = ""
    curr2 = ""
    for j in data_memory:
        if(l == 0):
            k = j
            curr2 = "0x"
        curr2 = curr2 + data_memory[j]
        j = hex(int(j, 16) + 1)
        l += 1
        if(l == 4):
            file.write(k + " " + curr2 + "\n")
        l %= 4

    file.write("\nRegisterFile\n\n")
    for i in range(len(x)):
        file.write('x'+str(i)+' = '+str(x[i])+'\n')


nop = 0x00000000

def update_pipeline_regs(register):
    for i in register:
        register[i][1] = register[i][0]


def clock_cycle_time():
    clk += 1
    time.sleep(1)
    print("Cycle CYCLE:", clk, '\n')


if __name__ == "__main__":
    read_from_file(
        r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\test\nsum.mc")
    if(pipelining_knob == 1):
        while (True):
            clock_cycle = threading.Thread(target=clock_cycle_time())
            p1 = threading.Thread(target=fetch())
            p2 = threading.Thread(target=decode())
            p3 = threading.Thread(target=execute())
            p4 = threading.Thread(target=memory_access())
            p5 = threading.Thread(target=write_back())
            clock_cycle.start()
            p1.start()
            p2.start()
            p3.start()
            p4.start()
            p5.start()
            clock_cycle.join()
    else:
        while(True):
            fetch()
            decode()
            execute()
            if terminate:
                exit(1)
            memory_access()
            write_back()
            print(pc)
            clk += 1
            print("Clock CYCLE:", clk, '\n')
    # print(instruction_memory)
    # print(data_memory)
