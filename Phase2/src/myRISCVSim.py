from collections import defaultdict
import pandas as pd
import sys
import time
import threading
global null_control_sig,null_imm,null_dec_pr,null_ex_pr,null_ma_pr,null_wb_pr 
null_control_sig = {"ALUop": 0, "Op2_Select": 0, "Mem_op": 0, "Result_select": 0,
                    "Branch_trg_sel": 0, "is_branch": 0, "RFWrite": 0, "Mem_read": 0, "Mem_write": 0}

null_imm = {"imm_I": 0, "imm_S": 0, "imm_B": 0, "imm_U": 0, "imm_J": 0}
null_dec_pr =  {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32]}
null_ex_pr = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32], "_num_b": [0, 0], "_rs1": [0, 0], "_rd": [0, 0], "_rs2": [
    0, 0], "_imm": [null_imm, null_imm], "_op1": [0, 0], "_ALUop": [0, 0], "_control_sig": [null_control_sig, null_control_sig]}
null_ma_pr = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32], "_num_b": [0, 0], "_rs1": [0, 0],
              "_rd": [0, 0], "_rs2": [0, 0], "_pc_new": [0, 0], "_Alu_result": [0, 0], "_rm": [0, 0], "_control_sig": [null_control_sig, null_control_sig], "_imm": [null_imm, null_imm], "_Branch_target_add": [0, 0]}
null_wb_pr = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32], "_rd": [0, 0], "_pc_new": [0, 0], "_Alu_result": [0, 0],
              "_Branch_target_add": [0, 0], "_ma": [0, 0], "_rm": [0, 0], "_control_sig": [null_control_sig, null_control_sig], "_imm": [null_imm, null_imm]}

x = ["0x00000000"]*32  # Register File
# x[2] = "0x7FFFFFF0"  # sp - stack pointer
# x[3] = "0x10000000"  # the beginning address of data segment of memory

global pipelining_knob, data_forwarding_knob, register_file_knob, pipeline_registers_knob, specify_instruction_knob

pipelining_knob = 1
data_forwarding_knob = 1
register_file_knob = 1
pipeline_registers_knob = 1
specify_instruction_knob = 1

global pc, clk, flags
pc = 0
clk = 1
flags = [0, 0, 0 , 0]

instruction_memory = {}  # Memory for Instructions
data_memory = defaultdict(lambda: "00")  # Memory for Data

dec_pipeline_reg = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32]}
ex_pipeline_reg = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32],"_num_b":[0,0], "_rs1": [0,0], "_rd": [0, 0], "_rs2": [0, 0], "_imm": [null_imm, null_imm] , "_op1": [0, 0], "_ALUop": [0, 0], "_control_sig": [null_control_sig, null_control_sig]}
ma_pipeline_reg = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32], "_num_b": [0, 0], "_rs1": [0, 0],
                   "_rd": [0, 0], "_rs2": [0, 0], "_pc_new": [0, 0], "_Alu_result": [0, 0], "_rm": [0, 0], "_control_sig": [null_control_sig, null_control_sig], "_imm": [null_imm, null_imm], "_Branch_target_add": [0, 0]}
wb_pipeline_reg = {"_pc": [-4, -4], "_binary_instruction": ['1'*32, '1'*32], "_rd": [0, 0], "_pc_new": [0, 0], "_Alu_result": [0, 0],
                   "_Branch_target_add": [0, 0], "_ma": [0, 0], "_rm": [0, 0], "_control_sig": [null_control_sig, null_control_sig], "_imm": [null_imm, null_imm]}


def read_from_file(file_name):
    flag = 0  # To distinguish between instruction and data
    try:
        file = open(file_name, 'r')
        for line in file:
            tmp = line.split()
            if len(tmp) == 2:
                address, instruction = tmp[0], tmp[1]
            if flag == 0:  # Storing Instruction in instruction_memory
                if (instruction == '$'):
                    flag = 1
                    continue
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
    # global Op2_Select, Mem_op, ALUop, Result_select, Branch_trg_sel, is_branch, RFWrite, mem_read, mem_write
    # ALUop = _ALUop
    # Op2_Select = _Op2_Select
    # Mem_op = _Mem_op
    # Result_select = _Result_select
    # Branch_trg_sel = _Branch_trg_sel
    # is_branch = _is_branch
    # RFWrite = _RFWrite
    # mem_read = _mem_read
    # mem_write = _mem_write
    print("control generated")
    return {"ALUop": _ALUop, "Op2_Select": _Op2_Select, "Mem_op": _Mem_op, "Result_select": _Result_select, "Branch_trg_sel": _Branch_trg_sel, "is_branch": _is_branch, "RFWrite": _RFWrite, "Mem_read": _mem_read, "Mem_write": _mem_write}


def sign_extend(binary_instruction):
    # global immI, immU, immJ, immB, immS, binary_instruction
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
    
    # print(tempI, tempS, tempB, tempU, tempJ)

    immI = immS = immB = immU = immJ = 0

    if tempI[0] == '0' or tempS[0] == '0' or tempB[0] == '0' or tempU[0] == '0' or tempJ[0] == '0':
        # extending signs for positive numbers
        # print("here 1")
        immI = '0'*(32-len(tempI))+tempI
        immS = '0'*(32-len(tempS))+tempS
        immB = '0'*(32-len(tempB))+tempB
        immU = tempU + '0'*12
        immJ = '0'*(32-len(tempJ))+tempJ
    elif tempI[0] == '1' or tempS[0] == '1' or tempB[0] == '1' or tempU[0] == '1' or tempJ[0] == '1':
        # extending signs for negative nubmers
        # print("here 2")
        immI = '1'*(32-len(tempI))+tempI
        immS = '1'*(32-len(tempS))+tempS
        immB = '1'*(32-len(tempB))+tempB
        immU = tempU + '0'*12
        immJ = '1'*(32-len(tempJ))+tempJ
    # print(immI, immS, immB, immU, immJ)
    return {"imm_I": immI, "imm_S": immS, "imm_B": immB, "imm_U": immU, "imm_J": immJ}

# To fetch the instruction from instruction_memory


def fetch():
    print("pc = " + str(pc))
    if (pc < 0):
        print("pc negative")
        exit(1)
    try:
        print("Executing Fetch for instruction at pc = " + str(pc))
        IR = '0x'+instruction_memory["0x"+'0'*(8-(len(hex(pc))-2))+hex(pc)[2:]]+instruction_memory["0x"+'0'*(8-(len(hex(pc+1))-2))+hex(pc+1)[
            2:]] + instruction_memory["0x"+'0'*(8-(len(hex(pc+2))-2))+hex(pc+2)[2:]]+instruction_memory["0x"+'0'*(8-(len(hex(pc+3))-2))+hex(pc+3)[2:]]
        binary_instruction = bin(int(IR, 16))[2:]
        binary_instruction = '0' * (32-len(binary_instruction)) + binary_instruction
        dec_pipeline_reg["_pc"][0] = pc
        dec_pipeline_reg["_binary_instruction"][0] = binary_instruction
        print(f"fetch complete")
    except:
        print("No Instruction to Fetch")
        print("Fetch Complete")
        terminate()

# To decode the instruction and reading from register file and generating control signals


def decode():
    # global rs1, rs2, rd, op1, opcode, func3, func7, immB, immJ, immI, immS, immU, Op2_Select, Mem_op, ALUop, Result_select, Branch_trg_sel, is_branch, RFWrite, mem_read, mem_write, binary_instruction, num_b
    binary_instruction = dec_pipeline_reg["_binary_instruction"][1]
    pc = dec_pipeline_reg["_pc"][1]
    opcode = int(binary_instruction[25:], 2)
    func3 = int(binary_instruction[17:20], 2)
    func7 = int(binary_instruction[0:7], 2)
    rs2 = int(binary_instruction[7:12], 2)
    rs1 = int(binary_instruction[12:17], 2)
    rd = int(binary_instruction[20:25], 2)
    imm = sign_extend(binary_instruction)
    # decoded operand 1
    # 2**32 = 4294967296
    print("Executing Decode for pc = " + str(pc))
    if(pc < 0):
        print("It is a stall. Time to wait!!")
        print("Decode Complete")
        return
    
    # print(rs1)
    if x[rs1][2] == 'f':
        print("here1")
        op1 = int(x[rs1], 16)-4294967296
    else:
        # print("here2")
        op1 = int(x[rs1], 16)
    print(x[rs1])
    if (imm["imm_I"][0] == '0'):
        imm["imm_I"] = int(imm["imm_I"], 2)
    else:
        imm["imm_I"] = int(imm["imm_I"], 2)-4294967296
    if (imm["imm_S"][0] == '0'):
        imm["imm_S"] = int(imm["imm_S"], 2)
    else:
        imm["imm_S"]= int(imm["imm_S"], 2)-4294967296
    if (imm["imm_B"][0] == '0'):
        imm["imm_B"] = int(imm["imm_B"], 2)
    else:
        imm["imm_B"] = int(imm["imm_B"], 2)-4294967296
    if (imm["imm_J"][0] == '0'):
        imm["imm_J"] = int(imm["imm_J"], 2)
    else:
        imm["imm_J"] = int(imm["imm_J"], 2)-4294967296
    if (imm["imm_U"][0] == '0'):
        imm["imm_U"] = int(imm["imm_U"], 2)
    else:
        imm["imm_U"] = int(imm["imm_U"], 2)-4294967296
    control_file = pd.read_csv(r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\control.csv")
    control_sig = null_control_sig
    num_b = 0
    if opcode == 51:
        if func3 == 0 and func7 == 0:
            print("And operation")
            control_sig = control_signal(control_file["ALUop"][0], control_file["Op2_Select"][0], control_file["Mem_op"][0], control_file["Mem_read"][0], control_file["Mem_write"]
                                         [0], control_file["Result_select"][0], control_file["Branch_trg_sel"][0], control_file["is_branch"][0], control_file["RFWrite"][0])
        elif func3 == 0 and func7 == 32:  # SUB
            print("Sub operation")
            control_sig = control_signal(control_file["ALUop"][1], control_file["Op2_Select"][1], control_file["Mem_op"][1], control_file["Mem_read"][1], control_file["Mem_write"]
                                         [1], control_file["Result_select"][1], control_file["Branch_trg_sel"][1], control_file["is_branch"][1], control_file["RFWrite"][1])
        elif func3 == 4 and func7 == 0:  # XOR
            print("XOR operation")
            control_sig = control_signal(control_file["ALUop"][2], control_file["Op2_Select"][2], control_file["Mem_op"][2], control_file["Mem_read"][2], control_file["Mem_write"]
                                         [2], control_file["Result_select"][2], control_file["Branch_trg_sel"][2], control_file["is_branch"][2], control_file["RFWrite"][2])
        elif func3 == 6 and func7 == 0:  # OR
            print("OR operation")
            control_sig = control_signal(control_file["ALUop"][3], control_file["Op2_Select"][3], control_file["Mem_op"][3], control_file["Mem_read"][3], control_file["Mem_write"]
                                         [3], control_file["Result_select"][3], control_file["Branch_trg_sel"][3], control_file["is_branch"][3], control_file["RFWrite"][3])
        elif func3 == 7 and func7 == 0:  # AND
            print("And operation")
            control_sig = control_signal(control_file["ALUop"][4], control_file["Op2_Select"][4], control_file["Mem_op"][4], control_file["Mem_read"][4], control_file["Mem_write"]
                                         [4], control_file["Result_select"][4], control_file["Branch_trg_sel"][4], control_file["is_branch"][4], control_file["RFWrite"][4])
        elif func3 == 1 and func7 == 0:  # SLL
            print("sll operation")
            control_sig = control_signal(control_file["ALUop"][5], control_file["Op2_Select"][5], control_file["Mem_op"][5], control_file["Mem_read"][5], control_file["Mem_write"]
                                         [5], control_file["Result_select"][5], control_file["Branch_trg_sel"][5], control_file["is_branch"][5], control_file["RFWrite"][5])
        elif func3 == 5 and func7 == 0:  # SRL
            print("srl operation")
            control_sig = control_signal(control_file["ALUop"][6], control_file["Op2_Select"][6], control_file["Mem_op"][6], control_file["Mem_read"][6], control_file["Mem_write"]
                                         [6], control_file["Result_select"][6], control_file["Branch_trg_sel"][6], control_file["is_branch"][6], control_file["RFWrite"][6])
        elif func3 == 5 and func7 == 32:  # SRA
            print("sra operation")
            control_sig = control_signal(control_file["ALUop"][7], control_file["Op2_Select"][7], control_file["Mem_op"][7], control_file["Mem_read"][7], control_file["Mem_write"]
                                         [7], control_file["Result_select"][7], control_file["Branch_trg_sel"][7], control_file["is_branch"][7], control_file["RFWrite"][7])
        elif func3 == 2 and func7 == 0:  # SLT
            print("slt operation")
            control_sig = control_signal(control_file["ALUop"][8], control_file["Op2_Select"][8], control_file["Mem_op"][8], control_file["Mem_read"][8], control_file["Mem_write"]
                                         [8], control_file["Result_select"][8], control_file["Branch_trg_sel"][8], control_file["is_branch"][8], control_file["RFWrite"][8])
        else:
            if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 19:  # I - type
        if func3 == 0:  # addi
            print("addi operation")
            control_sig = control_signal(control_file["ALUop"][9], control_file["Op2_Select"][9], control_file["Mem_op"][9], control_file["Mem_read"][9], control_file["Mem_write"]
                                         [9], control_file["Result_select"][9], control_file["Branch_trg_sel"][9], control_file["is_branch"][9], control_file["RFWrite"][9])
        elif func3 == 6:  # ori
            print("ori operation")
            control_sig = control_signal(control_file["ALUop"][10], control_file["Op2_Select"][10], control_file["Mem_op"][10], control_file["Mem_read"][10], control_file["Mem_write"]
                                         [10], control_file["Result_select"][10], control_file["Branch_trg_sel"][10], control_file["is_branch"][10], control_file["RFWrite"][10])
        elif func3 == 7:  # andi
            print("andi operation")
            control_sig = control_signal(control_file["ALUop"][11], control_file["Op2_Select"][11], control_file["Mem_op"][11], control_file["Mem_read"][11], control_file["Mem_write"]
                                         [11], control_file["Result_select"][11], control_file["Branch_trg_sel"][11], control_file["is_branch"][11], control_file["RFWrite"][11])
        else:
            if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "0x00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 3:
        if func3 == 0:  # lb
            print("lb operation")
            control_sig = control_signal(control_file["ALUop"][12], control_file["Op2_Select"][12], control_file["Mem_op"][12], control_file["Mem_read"][12], control_file["Mem_write"]
                                         [12], control_file["Result_select"][12], control_file["Branch_trg_sel"][12], control_file["is_branch"][12], control_file["RFWrite"][12])
            num_b = 1
        elif func3 == 1:  # lh
            print("lh operation")
            control_sig = control_signal(control_file["ALUop"][13], control_file["Op2_Select"][13], control_file["Mem_op"][13], control_file["Mem_read"][13], control_file["Mem_write"]
                                         [13], control_file["Result_select"][13], control_file["Branch_trg_sel"][13], control_file["is_branch"][13], control_file["RFWrite"][13])
            num_b = 2
        elif func3 == 2:  # lw
            print("lw opeartion")
            control_sig = control_signal(control_file["ALUop"][14], control_file["Op2_Select"][14], control_file["Mem_op"][14], control_file["Mem_read"][14], control_file["Mem_write"]
                                         [14], control_file["Result_select"][14], control_file["Branch_trg_sel"][14], control_file["is_branch"][14], control_file["RFWrite"][14])
            num_b = 4
        else:
            if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 35:
        if func3 == 0:  # sb
            print("sb operation")
            control_sig = control_signal(control_file["ALUop"][15], control_file["Op2_Select"][15], control_file["Mem_op"][15], control_file["Mem_read"][15], control_file["Mem_write"]
                                         [15], control_file["Result_select"][15], control_file["Branch_trg_sel"][15], control_file["is_branch"][15], control_file["RFWrite"][15])
            num_b = 1
        elif func3 == 1:  # sh
            print("sh operation")
            control_sig = control_signal(control_file["ALUop"][16], control_file["Op2_Select"][16], control_file["Mem_op"][16], control_file["Mem_read"][16], control_file["Mem_write"]
                                         [16], control_file["Result_select"][16], control_file["Branch_trg_sel"][16], control_file["is_branch"][16], control_file["RFWrite"][16])
            num_b = 2
        elif func3 == 2:  # sw
            print("sw operation")
            control_sig = control_signal(control_file["ALUop"][17], control_file["Op2_Select"][17], control_file["Mem_op"][17], control_file["Mem_read"][17], control_file["Mem_write"]
                                         [17], control_file["Result_select"][17], control_file["Branch_trg_sel"][17], control_file["is_branch"][17], control_file["RFWrite"][17])
            num_b = 4
        else:
            if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 99:
        if func3 == 0:  # beq
            print("beq opeartion")
            control_sig = control_signal(control_file["ALUop"][18], control_file["Op2_Select"][18], control_file["Mem_op"][18], control_file["Mem_read"][18], control_file["Mem_write"]
                                         [18], control_file["Result_select"][18], control_file["Branch_trg_sel"][18], control_file["is_branch"][18], control_file["RFWrite"][18])
        elif func3 == 1:  # bne
            print("bne operation")
            control_sig = control_signal(control_file["ALUop"][19], control_file["Op2_Select"][19], control_file["Mem_op"][19], control_file["Mem_read"][19], control_file["Mem_write"]
                                         [19], control_file["Result_select"][19], control_file["Branch_trg_sel"][19], control_file["is_branch"][19], control_file["RFWrite"][19])
        elif func3 == 4:  # blt
            print("blt operation")
            control_sig = control_signal(control_file["ALUop"][20], control_file["Op2_Select"][20], control_file["Mem_op"][20], control_file["Mem_read"][20], control_file["Mem_write"]
                                         [20], control_file["Result_select"][20], control_file["Branch_trg_sel"][20], control_file["is_branch"][20], control_file["RFWrite"][20])
        elif func3 == 5:  # bge
            print("bge operation")
            control_sig = control_signal(control_file["ALUop"][21], control_file["Op2_Select"][21], control_file["Mem_op"][21], control_file["Mem_read"][21], control_file["Mem_write"]
                                         [21], control_file["Result_select"][21], control_file["Branch_trg_sel"][21], control_file["is_branch"][21], control_file["RFWrite"][21])
        else:
            if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                print("Invalid instruction")
            else:
                print("End of the Program")
            terminate()
    elif opcode == 111:  # jal
        print("jal operation")
        control_sig = control_signal(control_file["ALUop"][22], control_file["Op2_Select"][22], control_file["Mem_op"][22], control_file["Mem_read"][22], control_file["Mem_write"]
                                     [22], control_file["Result_select"][22], control_file["Branch_trg_sel"][22], control_file["is_branch"][22], control_file["RFWrite"][22])
    elif opcode == 103 and func3 == 0:  # jalr
        print("Jalr operation")
        control_sig = control_signal(control_file["ALUop"][23], control_file["Op2_Select"][23], control_file["Mem_op"][23], control_file["Mem_read"][23], control_file["Mem_write"]
                                     [23], control_file["Result_select"][23], control_file["Branch_trg_sel"][23], control_file["is_branch"][23], control_file["RFWrite"][23])
    elif opcode == 55:  # lui
        print("lui operation")
        control_sig = control_signal(control_file["ALUop"][24], control_file["Op2_Select"][24], control_file["Mem_op"][24], control_file["Mem_read"][24], control_file["Mem_write"]
                                     [24], control_file["Result_select"][24], control_file["Branch_trg_sel"][24], control_file["is_branch"][24], control_file["RFWrite"][24])
    elif opcode == 23:  # auipc
        print("Auipc operation")
        control_sig = control_signal(control_file["ALUop"][25], control_file["Op2_Select"][25], control_file["Mem_op"][25], control_file["Mem_read"][25], control_file["Mem_write"]
                                     [25], control_file["Result_select"][25], control_file["Branch_trg_sel"][25], control_file["is_branch"][25], control_file["RFWrite"][25])
    elif binary_instruction == '1'*32:
        print("It is a stall, Time to wait!!")
    else:
        if(instruction_memory["0x"+'0'*(8-(len(hex(pc))-2)) + hex(pc)[2:]] +
           instruction_memory["0x"+'0'*(8-(len(hex(pc+1))-2)) + hex(pc)[2:]] + instruction_memory["0x"+'0'*(8-(len(hex(pc+2))-2)) + hex(pc)[2:]] +
           instruction_memory["0x"+'0' *(8-(len(hex(pc+3))-2)) + hex(pc)[2:]] == "00000000"
           ):
            print("End of the Program")
        else:
            print("Invalid Instruction")
        terminate()
    # print(control_sig)
    ex_pipeline_reg["_control_sig"][0] = control_sig
    ex_pipeline_reg["_binary_instruction"][0] = binary_instruction
    ex_pipeline_reg["_imm"][0] = imm
    ex_pipeline_reg["_op1"][0] = op1
    ex_pipeline_reg["_pc"][0] = pc
    ex_pipeline_reg["_rs1"][0] = rs1
    ex_pipeline_reg["_rs2"][0] = rs2
    ex_pipeline_reg["_rd"][0] = rd
    ex_pipeline_reg["_ALUop"][0] = control_sig["ALUop"]
    ex_pipeline_reg["_num_b"][0] = num_b
    print("Decode Complete")
# Here handle the case of ending the program.


def execute():
    # global rm, is_branch, Branch_trg_sel, offset, Branch_target_add, num_b, pc_new, pc, op1, op2, Op2_Select, Mem_op, Alu_result
    global pc, flags
    pc_old = ex_pipeline_reg["_pc"][1]
    ALUop = ex_pipeline_reg["_ALUop"][1]
    control_signal = ex_pipeline_reg["_control_sig"][1]
    rs2 = ex_pipeline_reg["_rs2"][1]
    rs1 = ex_pipeline_reg["_rs1"][1]
    op1 = ex_pipeline_reg["_op1"][1]
    rd = ex_pipeline_reg["_rd"][1]
    imm = ex_pipeline_reg["_imm"][1]
    pc_new = pc_old + 4
    print("Executing instruction for pc = " + str(pc_old))
    if(pc_old < 0):
        print("It is a stall. Time to wait!!")
        print("Execute Complete")
        return
    # selection of the second operand
    if control_signal["Op2_Select"] == 0:
        # print("here 1")
        if x[rs2][3] == 'f':
            # print("here 11")
            op2 = int(x[rs2], 16)-4294967296
        else:
            # print("here 12")
            op2 = int(x[rs2], 16)
    elif control_signal["Op2_Select"] == 1:
        # print("here 2")
        # print(imm)
        # print(imm["imm_I"])
        op2 = imm["imm_I"]
    else:
        # print("here 3")
        op2 = imm["imm_S"]

    rm = Alu_result = is_branch = Branch_target_add = offset = 0 
    # selection of the type of immediate to branch at
    if control_signal["Branch_trg_sel"] == 0:
        offset = imm["imm_B"]
    else:
        offset = imm["imm_J"]
    # print("ALUop = " + str(ALUop))
    # print(op1, op2)
    if (ALUop == 0):  # add instruction
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "ADD operation on ", op1, "and", op2)

    elif (ALUop == 1):  # sub instruction
        rm = op1 - op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "SUB operation on ", op1, "and", op2)
        
    elif (ALUop == 2):  # xor
        rm = op1 ^ op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "XOR operation on ", op1, "and", op2)

    elif (ALUop == 3):  # or
        rm = op1 | op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "OR operation on ", op1, "and", op2)

    elif (ALUop == 4):  # and
        rm = op1 & op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "AND operation on ", op1, "and", op2)

    elif (ALUop == 5):  # sll
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            exit(1)
        else:
            rm = op1 << op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "SLL operation on ", op1, "and", op2)

    elif (ALUop == 6):  # srl
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            exit(1)
        else:
            if op1 >= 0:
                rm = hex(op1 >> op2)
            else:
                rm = hex((op1+4294967296) >> op2)
        if (rm > 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ", "SRL operation on ", op1, "and", op2)
        
    elif (ALUop == 7):  # sra
        if (op2 < 0 | op2 > 31):
            print("ERROR: Shift by negative!\n")
            exit(1)
        else:
            rm = op1 >> op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE:", "SRA operation on ", op1, "and", op2)
        
    elif (ALUop == 8):  # slt
        if (op1 < op2):
            rm = hex(1)
        else:
            rm = hex(0)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE:", "SLT operation on ", op1, "and", op2)

    elif (ALUop == 9):  # addi
        rm = op1+op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ADDI operation on ", op1, "and", op2)
 
    elif (ALUop == 10):  # ori
        rm = op1 | op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ORI operation on ", op1, "and", op2)

    elif (ALUop == 11):  # andi
        rm = op1 & op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: ANDI operation on ", op1, "and", op2)

    elif (ALUop == 12):  # lb
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LB operation on ", op1, "and", op2)

    elif (ALUop == 13):  # lh
        rm = op1 + op2
        if (rm > 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LH operation on ", op1, "and", op2)

    elif (ALUop == 14):  # lw
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LW operation on ", op1, "and", op2)

    elif (ALUop == 15):  # sb
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SB operation on ", op1, "and", op2)

    elif (ALUop == 16):  # sh
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SH operation on ", op1, "and", op2)

    elif (ALUop == 17):  # sw
        rm = op1 + op2
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: SW opeartion on ", op1, "and", op2)

    elif (ALUop == 18):  # beq
        # print(op1,op2)
        if (op1 == op2):
            is_branch = 1
            Branch_target_add = pc+offset
            pc_new = Branch_target_add
        print("EXECUTE: BEQ operation on ", op1, "and", op2)

    elif (ALUop == 19):  # bne
        if (op1 != op2):
            is_branch = 1
            Branch_target_add = pc+offset
            pc_new = Branch_target_add
        print("EXECUTE: BNE operation on ", op1, "and", op2)

    elif (ALUop == 20):  # blt
        if (op1 < op2):
            is_branch = 1
            Branch_target_add = pc+offset
            pc_new = Branch_target_add
        print("EXECUTE: BLT operation on ", op1, "and", op2)

    elif (ALUop == 21):  # bge
        if (op1 >= op2):
            is_branch = 1
            Branch_target_add = pc+offset
            pc_new = Branch_target_add
        print("EXECUTE: BGE operation on ", op1, "and", op2)

    elif (ALUop == 22):  # jal
        rm = hex(pc+4)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        Alu_result = pc+offset
        pc_new = Alu_result
        # Branch_target_add = pc+offset
        is_branch = 2
        print("EXECUTE: JAL operation")

    elif (ALUop == 23):  # jalr
        rm = hex(pc+4)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        Alu_result = rs1+op2
        pc_new = Alu_result
        # pc = rs1+op2
        is_branch = 2
        print("EXECUTE: JALR operation")

    elif (ALUop == 24):  # lui
        rm = imm["imm_U"]
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: LUI operation")

    elif (ALUop == 25):  # auipc
        rm = pc+imm["imm_U"]
        if (rm >= 0):
            rm = hex(rm)
        else:
            rm = hex(4294967296+rm)
        rm = "0x"+'0'*(8-(len(rm)-2))+rm[2:]
        print("EXECUTE: AUIPC operation")

    elif (ex_pipeline_reg["_binary_instruction"] == '1'*32):
        print("It's a Stall. Time to Wait!!")
    else:
        print("error: no matching ALU operation is possible for this instruction")
        terminate()
    # print("pc_new", pc_new)
    # print("ex[pc][0] =", ex_pipeline_reg["_pc"][0])
    ma_pipeline_reg["_pc_new"][0]=pc_new
    control_signal["is_branch"]=is_branch
    if(pc_old+4 != ma_pipeline_reg["_pc_new"][0]):
        flags[0] = 1
        flags[1] = 1
        print("flags =", flags)
        pc = ma_pipeline_reg["_pc_new"][0]
    ma_pipeline_reg["_Alu_result"][0] = Alu_result
    ma_pipeline_reg["_binary_instruction"][0] = ex_pipeline_reg["_binary_instruction"][1]
    ma_pipeline_reg["_control_sig"][0] = control_signal
    ma_pipeline_reg["_pc"][0] = pc_old
    ma_pipeline_reg["_rm"][0] = rm
    ma_pipeline_reg["_num_b"][0] = ex_pipeline_reg["_num_b"]
    ma_pipeline_reg["_rs1"][0] = rs1
    ma_pipeline_reg["_rs2"][0] = rs2
    ma_pipeline_reg["_rd"][0] = rd
    ma_pipeline_reg["_Branch_target_add"][0] = Branch_target_add
    ma_pipeline_reg["_pc_new"][0] = pc_new

    print("Execute Complete")


def memory_access():
    Mem_op = ma_pipeline_reg["_control_sig"][1]["Mem_op"]
    mem_read = ma_pipeline_reg["_control_sig"][1]["Mem_read"]
    num_b = ma_pipeline_reg["_num_b"][1]
    rm = ma_pipeline_reg["_rm"][1]
    rs2 = ma_pipeline_reg["_rs2"]
    pc = ma_pipeline_reg["_pc"][1]
    print("Performing Memory Instruction for instruction at pc = " + str(pc))
    if(pc < 0):
        print("It is a stall. Time to wait!!")
        print("Memory Access Complete")
        return
    
    ma = 0
    if (Mem_op == 0):
        print("no memory operation")
    else:
        if mem_read == 1:
            if (num_b == 1):  # lb
                ma = "0x000000"+data_memory[rm]
                print("MEMORY ACCESSING: LOAD BYTE", ma, " from ", rm)
            elif (num_b == 2):  # lh
                ma = "0x0000"+data_memory[rm] + data_memory["0x"+'0' *
                                                            (8-(len(hex(int(rm, 16)+1))-2))+hex(int(rm, 16)+1)[2:]]
                print("MEMORY ACCESSING: LOAD HALFWORD", ma, " from ", rm)
            elif (num_b == 4):  # lw
                ma = "0x"+data_memory[rm] + data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+1))-2))+hex(int(rm, 16)+1)[2:]] + data_memory["0x"+'0'*(
                    8-(len(hex(int(rm, 16)+2))-2))+hex(int(rm, 16)+2)[2:]] + data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+3))-2))+hex(int(rm, 16)+3)[2:]]
                print("MEMORY ACCESSING: LOAD WORD", ma, " from ", rm)
            else:
                if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                    print("Invalid Memory Operation")
                else:
                    print("End of the Program")
                terminate()
        else:
            if (num_b == 1):  # sb
                data_memory[rm] = x[rs2][2:4]
                print("MEMORY ACCESSING: STORE BYTE", rs2, " to ", rm)
            elif (num_b == 2):  # sh
                data_memory[rm] = x[rs2][2:4]
                data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+1))-2)) +
                            hex(int(rm, 16)+1)[2:]] = x[rs2][4:6]
                print("MEMORY ACCESSING: STORE HALFWORD", rs2, " to ", rm)
            elif (num_b == 4):  # sw
                data_memory[rm] = x[rs2][2:4]
                data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+1))-2)) +
                            hex(int(rm, 16)+1)[2:]] = x[rs2][4:6]
                data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+2))-2)) +
                            hex(int(rm, 16)+2)[2:]] = x[rs2][6:8]
                data_memory["0x"+'0'*(8-(len(hex(int(rm, 16)+1))-3)) +
                            hex(int(rm, 16)+3)[2:]] = x[rs2][8:10]
                print("MEMORY ACCESSING: STORE WORD", rs2, " to ", rm)
            else:
                if (instruction_memory[pc]+instruction_memory[pc+1]+instruction_memory[pc+2]+instruction_memory[pc+3] != "00000000"):
                    print("Invalid Memory Operation")
                else:
                    print("End of the Program")
                terminate()
    wb_pipeline_reg["_binary_instruction"][0] = ma_pipeline_reg["_binary_instruction"][1]
    wb_pipeline_reg["_pc"][0] = ma_pipeline_reg["_pc"][1]
    wb_pipeline_reg["_control_sig"][0] = ma_pipeline_reg["_control_sig"][1]
    wb_pipeline_reg["_rd"][0] = ma_pipeline_reg["_rd"][1]
    wb_pipeline_reg["_ma"][0] = ma
    wb_pipeline_reg["_rm"][0] = rm
    wb_pipeline_reg["_Branch_target_add"][0] = ma_pipeline_reg["_Branch_target_add"][1]
    wb_pipeline_reg["_imm"][0] = ma_pipeline_reg["_imm"][1]
    wb_pipeline_reg["_Alu_result"][0] =  ma_pipeline_reg["_Alu_result"][1]
    wb_pipeline_reg["_pc_new"][0] = ma_pipeline_reg["_pc_new"][1]
    
    print("Memory Access Complete")

def write_back():
    # global result_write, pc_new, pc, Branch_target_add, ma, Alu_result
    RFWrite = wb_pipeline_reg["_control_sig"][1]["RFWrite"]
    Result_select = wb_pipeline_reg["_control_sig"][1]["Result_select"]
    rm = wb_pipeline_reg["_rm"][1]
    rd = wb_pipeline_reg["_rd"][1]
    ma = wb_pipeline_reg["_ma"][1]
    imm = wb_pipeline_reg["_imm"][1]
    pc_new = wb_pipeline_reg["_pc_new"][1]
    pc = wb_pipeline_reg["_pc"][1]
    print("Writing Back for instruction at pc = " + str(pc))

    if(pc < 0):
        print("It is a stall. Time to wait!!")
        print("WriteBack Complete")
        return
    # control_signal = wb_pipeline_reg["_control_sig"][1]
    # Branch_target_add = wb_pipeline_reg["_Branch_target_add"][1]
    # Alu_result = wb_pipeline_reg["_Alu_result"][1]

    if (RFWrite == 1):
        if (Result_select == 0):
            result_write = rm
        elif (Result_select == 1):
            result_write = ma
        elif (Result_select == 2):
            result_write = hex(imm["imm_U"])
            result_write = "0x"+'0'*(8-(len(result_write)-2))+result_write[2:]
        elif (Result_select == 3):
            pc_new = hex(pc_new)
            pc_new = "0x"+'0'*(8-(len(pc_new)-2))+pc_new[2:]
            result_write = pc_new
        x[rd] = result_write
    # if control_signal["is_branch"] == 0:
    #     pc = pc_new
    # elif control_signal["is_branch"] == 1:
    #     pc = Branch_target_add
    # else:
    #     pc = Alu_result
    # print("pc=", pc)
    # print("WRITING REGISTER FILE ", rd, " with ", result_write)
    print("Writeback Complete")
    return


def terminate():
    OutputFile_txt(r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\abc.txt")
    exit(1)


def OutputFile_txt(file_name):
    file = open(file_name, "w")
    m = "0x00000000"
    j = 0
    k = "0x00000000"
    # print(sys.getsizeof(instruction_memory))
    # print(instruction_memory)
    file.write("Instruction Memory\n\n")
    for i in instruction_memory.keys():
        # print(i,'\n')
        if (j == 0):
            curr = '0x'
        curr = curr + instruction_memory[i]
        j = j + 1
        if (j == 4):
            file.write(k + " " + curr + "\n")
            k = "0x"+'0'*(8-(len(hex(int(i, 16)+1))-2))+hex(int(i, 16)+1)[2:]
            j = 0

    file.write("\nData Memory\n\n")
    l = 0
    k = ""
    curr2 = ""
    for j in data_memory:
        if (l == 0):
            k = j
            curr2 = "0x"
        curr2 = curr2 + data_memory[j]
        j = hex(int(j, 16) + 1)
        l += 1
        if (l == 4):
            file.write(k + " " + curr2 + "\n")
        l %= 4

    file.write("\nRegisterFile\n\n")
    for i in range(len(x)):
        file.write('x'+str(i)+' = '+str(x[i])+'\n')


def update_pipeline_regs(register, index):
    # print(name)
    # print("before")
    # print(register)
    # print("after")
    if(flags[index] == 1):
        if(index == 0):
            print("flushed dec")
            register = null_dec_pr
        if(index == 1):
            print("flushed ex")
            register = null_ex_pr
        if(index == 2):
            print("flushed ma")
            register = null_ma_pr
        if(index == 3):
            print("flushed wb")
            register = null_wb_pr
        
    for i in register:
        register[i][1] = register[i][0]
    # print(register)
    # print("")


def clock_cycle_time():
    global clk
    clk += 1
    time.sleep(1)
    # print("Cycle CYCLE:", clk, '\n')


if __name__ == "__main__":
    read_from_file(r"C:\Users\sanya\Desktop\Vasu Bansal\CS204_Course Project\CS204_CourseProject\Phase2\src\test.mc")
    if(pipelining_knob == 1):
        while (True):
            print("CLOCK CYCLE " + str(clk))
            clock_cycle = threading.Thread(target=clock_cycle_time())
            update_pipeline_regs(dec_pipeline_reg, 0)
            update_pipeline_regs(ex_pipeline_reg, 1)
            update_pipeline_regs(ma_pipeline_reg, 2)
            update_pipeline_regs(wb_pipeline_reg, 3)
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
            pc+=4
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

