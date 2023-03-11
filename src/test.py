    
import pandas as pd

opcode=3
func3=0
func7="NA"
ALUop=0


instruction_set=pd.read_csv("src\Instruction_Set_List.csv")


if(instruction_set.loc[int(str(instruction_set['opcode']),2)==opcode and int(str(instruction_set['func3']),2)== func3 and str(instruction_set['func7'])== "NA"] ):
        ALUop=instruction_set.loc[int(str(instruction_set['opcode']),2)==opcode and int(str(instruction_set['func3']),2)== func3 and str(instruction_set['func7'])== "NA"]
        
elif(instruction_set.loc[int(str(instruction_set['opcode']),2)==opcode and int(str(instruction_set['func3']),2)== func3 and int(str(instruction_set['func7']),2)== func7]):
        ALUop=instruction_set.loc[int(str(instruction_set['opcode']),2)==opcode and int(str(instruction_set['func3']),2)== func3 and int(str(instruction_set['func7']),2)== func7]
else:
    print("error wrong machine code\n")
    
print( ALUop )  