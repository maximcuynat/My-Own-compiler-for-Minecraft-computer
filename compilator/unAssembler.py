instruction_set = {
    "NOP": "0000",
    "HLT": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "ORR": "0100",
    "NOR": "0101",
    "AND": "0110",
    "XOR": "0111",
    "INC": "1000",
    "DEC": "1001",
    "RSH": "1010",
    "LDI": "1011",
    "LOD": "1100",
    "STR": "1101",
    "JMP": "1110",
    "BIF": "1111",
}


class UnAssembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    # Function to convert binary register to assembly format
    def binary_to_register(self, binary):
        reg_num = int(binary, 2)  # Convert binary string to an integer
        return f"R{reg_num}"

    # Function to decompile binary code to assembly
    def decompile_binary(self):
        # Read the binary file
        with open(self.input_file, "r") as bin_file:
            lines = bin_file.readlines()

        assembly_output = []

        for line_no, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:  # Ignore empty lines
                continue

            byte1, byte2 = line.split()
            binary_line = f"{byte1}{byte2}"

            # Extract opcode (first 4 bits)
            opcode = binary_line[:4]
            operands = binary_line[4:]  # Remaining bits

            # Find the corresponding mnemonic
            mnemonic = next((key for key, value in instruction_set.items() if value == opcode), None)

            if mnemonic is None:
                raise ValueError(f"Unknown opcode: {opcode}")

            # Handle different instruction formats
            if mnemonic == "LDI":  # Format: LDI Reg Immediate
                reg = self.binary_to_register(operands[:3])
                immediate = int(operands[3:], 2)  # Convert immediate from binary to integer
                assembly_line = f"{mnemonic} {reg} {immediate}"

            elif mnemonic in {"JMP", "BIF"}:  # Format: JMP Address
                address = int(operands[3:], 2)  # Convert address from binary to integer
                assembly_line = f"{mnemonic} {address}"

            elif mnemonic in {"LOD", "STR"}:  # Format: LOD/STR Reg
                reg = self.binary_to_register(operands[:3])
                assembly_line = f"{mnemonic} {reg}"

            elif mnemonic in {"HLT", "NOP"}:  # Instructions without operands
                assembly_line = mnemonic

            else:  # Instructions with registers: ADD, SUB, etc.
                reg_dest = self.binary_to_register(operands[:3])
                reg_a = self.binary_to_register(operands[3:6])
                reg_b = self.binary_to_register(operands[6:])
                assembly_line = f"{mnemonic} {reg_dest} {reg_a} {reg_b}"

            assembly_output.append(assembly_line)

        # Write the text file with the decompiled assembly instructions
        with open(self.output_file, "w") as asm_file:
            asm_file.write("\n".join(assembly_output))
