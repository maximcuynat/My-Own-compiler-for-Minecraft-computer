# Instruction set table
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


# Class Assembler
class Assembler:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    # Function to convert a register to binary (R0 to R7)
    def register_to_binary(self, register):
        # Check if the register is valid
        if register.startswith("R"):
            reg_num = int(register[1:])
            return f"{reg_num:03b}"  # Convert to 3 bits
        else:
            raise ValueError(f"Invalid register: {register}")

    # Function to compile assembly code to binary
    def compile_assembly(self):
        # Read the assembly file
        with open(self.input_file, "r") as asm_file:
            lines = asm_file.readlines()

        binary_output = []

        for line_no, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith(";"):  # Ignore empty lines or comments
                continue

            parts = line.split()
            mnemonic = parts[0]
            if mnemonic not in instruction_set:
                raise ValueError(f"Unknown instruction: {mnemonic}")

            opcode = instruction_set[mnemonic]

            # Handle different instruction formats
            if mnemonic == "LDI":  # Format: LDI Reg Immediate
                reg = self.register_to_binary(parts[1])
                immediate = int(parts[2])
                binary_line = f"{opcode}{reg}{immediate:08b}"  # Immediate on 8 bits

            elif mnemonic in {"JMP", "BIF"}:  # Format: JMP Address
                address = int(parts[1])
                binary_line = f"{opcode}000{address:08b}"  # Address on 8 bits

            elif mnemonic in {"LOD", "STR"}:  # Format: LOD/STR Reg
                reg = self.register_to_binary(parts[1])
                binary_line = f"{opcode}{reg}00000000"  # No address, fill with zeros

            elif mnemonic in {"HLT", "NOP"}:  # Instructions without operands
                binary_line = f"{opcode}0000000000"  # Fill with zeros

            else:  # Instructions with registers: ADD, SUB, etc.
                reg_dest = self.register_to_binary(parts[1])
                reg_a = self.register_to_binary(parts[2])
                reg_b = self.register_to_binary(parts[3])
                binary_line = f"{opcode}{reg_dest}{reg_a}{reg_b}"

            # Separate into two bytes, always filling to 8 bits
            byte1 = binary_line[:8].zfill(8)  # Fill with zeros at the beginning if necessary
            byte2 = binary_line[8:].zfill(8)  # Fill with zeros at the beginning if necessary

            # Add opcode and operands separated for each instruction
            formatted_line = f"{byte1} {byte2}"

            binary_output.append(formatted_line)

        # Write the text file with the formatted binary instructions
        with open(self.output_file, "w") as txt_file:
            txt_file.write("\n".join(binary_output))       