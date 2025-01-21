# Instruction set table
instruction_set = {
    "NOP": "0000",
    "HLT": "0001",  # HLT is included here
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
    @staticmethod
    def register_to_binary(register):
        """Convert register to 3-bit binary representation."""
        if register.startswith("R"):
            try:
                reg_num = int(register[1:])
                if reg_num < 0 or reg_num > 7:
                    raise ValueError(f"Invalid register '{register}'. Only registers R0 to R7 are allowed.")
                return f"{reg_num:03b}"
            except ValueError:
                raise ValueError(f"Invalid register '{register}'. It should be in the format R0 to R7.")
        raise ValueError(f"Invalid register format: {register}. It should start with 'R' followed by a number.")

    def process_instruction(self, mnemonic, parts, line_no):
        """Process each instruction based on its mnemonic."""
        opcode = instruction_set.get(mnemonic)

        if not opcode:
            return f"Error in line {line_no}: Unknown instruction '{mnemonic}'"

        try:
            # Validate the number of operands for each instruction
            if mnemonic == "LDI":
                if len(parts) != 3:
                    return f"Error in line {line_no}: LDI instruction requires 2 operands (Reg Immediate)."
                reg = self.register_to_binary(parts[1])
                immediate = int(parts[2])
                return f"{opcode}{reg} {immediate:08b}"

            elif mnemonic in {"JMP", "BIF"}:
                if len(parts) != 2:
                    return f"Error in line {line_no}: {mnemonic} instruction requires 1 operand (Address)."
                address = int(parts[1])
                return f"{opcode}0000 {address:08b}"

            elif mnemonic in {"LOD", "STR"}:
                if len(parts) != 2:
                    return f"Error in line {line_no}: {mnemonic} instruction requires 1 operand (Reg)."
                reg = self.register_to_binary(parts[1])
                return f"{opcode}{reg} 00000000"  # No address, fill with zeros

            elif mnemonic in {"HLT", "NOP"}:
                if len(parts) != 1:
                    return f"Error in line {line_no}: {mnemonic} instruction requires no operands."
                return f"{opcode}000 00000000"

            else:
                if len(parts) != 4:
                    return f"Error in line {line_no}: {mnemonic} instruction requires 3 operands (RegDest RegA RegB)."
                reg_dest = self.register_to_binary(parts[1])
                reg_a = self.register_to_binary(parts[2])
                reg_b = self.register_to_binary(parts[3])
                print(f"{opcode}{reg_dest} 0{reg_a}0{reg_b}")
                return f"{opcode}{reg_dest} 0{reg_a}0{reg_b}"

        except ValueError as e:
            return f"Error in line {line_no}: {str(e)}"
        except Exception as e:
            return f"Error in line {line_no}: {str(e)}"

    def compile_assembly(self):
        """Compile the assembly code into binary format."""
        with open(self.input_file, "r") as asm_file:
            lines = asm_file.readlines()

        binary_output = []
        has_hlt = False

        for line_no, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith(";"):
                continue

            parts = line.split()
            mnemonic = parts[0]

            # Process instruction and handle errors
            result = self.process_instruction(mnemonic, parts, line_no)
            if "Error" in result:
                return result  # Return error message if there's an issue

            # Add the result to the binary output
            binary_output.append(result)

            if mnemonic == "HLT":
                has_hlt = True

        # Ensure 'HLT' is added at the end if missing
        if not has_hlt:
            binary_output.append(f"{instruction_set['HLT']}0000000000")

        # Write the binary output to the file
        with open(self.output_file, "w") as txt_file:
            txt_file.write("\n".join(binary_output))

        return "Compilation successful!"  # Return success message
