with open("./dump.txt", "r") as dump_file:
    dump_contents = dump_file.readlines()

memory_values = []
for line in dump_contents:
    memory_values.append(line)

with open("./output.mc", "w") as mc_file:
    for i, memory_value in enumerate(memory_values):
        address = str(hex(i*4))
        mc_file.write(f"{address} {memory_value}")
    address = str(hex((i+1)*4))
    mc_file.write(f"{address} $")
