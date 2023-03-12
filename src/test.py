
import pandas as pd

opcode = 3
func3 = 0
func7 = "NA"
ALUop = 0
control=pd.read_csv("src\control.csv")
print(control["ALUop"][1])