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

    # Fonction pour convertir un registre binaire en format assembleur
    def binary_to_register(self, binary):
        try:
            reg_num = int(binary, 2)  # Convertir la chaîne binaire en entier
            return f"R{reg_num}"
        except ValueError as e:
            raise ValueError(f"Erreur lors de la conversion binaire du registre: {binary}") from e

    # Fonction pour décompiler le code binaire en assembleur
    def decompile_binary(self):
        try:
            # Lecture du fichier binaire
            with open(self.input_file, "r") as bin_file:
                lines = bin_file.readlines()

            assembly_output = []

            for line_no, line in enumerate(lines, start=1):
                line = line.strip()
                if not line:  # Ignorer les lignes vides
                    continue

                try:
                    byte1, byte2 = line.split()
                except ValueError:
                    raise ValueError(f"Format incorrect à la ligne {line_no}: {line} - Deux octets sont attendus.")

                binary_line = f"{byte1}{byte2}"

                # Extraction de l'opcode (les 4 premiers bits)
                opcode = binary_line[:4]
                operands = binary_line[4:]  # Les bits restants

                # Recherche du mnémonique correspondant à l'opcode
                mnemonic = next((key for key, value in instruction_set.items() if value == opcode), None)

                if mnemonic is None:
                    raise ValueError(f"Opcode inconnu à la ligne {line_no}: {opcode}")

                # Traitement des formats d'instruction différents
                try:
                    if mnemonic == "LDI":  # Format: LDI Reg Immediate
                        reg = self.binary_to_register(operands[:3])
                        immediate = int(operands[3:], 2)  # Convertir l'immédiat en entier
                        assembly_line = f"{mnemonic} {reg} {immediate}"

                    elif mnemonic in {"JMP", "BIF"}:  # Format: JMP Address
                        address = int(operands[3:], 2)  # Convertir l'adresse en entier
                        assembly_line = f"{mnemonic} {address}"

                    elif mnemonic in {"LOD", "STR"}:  # Format: LOD/STR Reg
                        reg = self.binary_to_register(operands[:3])
                        assembly_line = f"{mnemonic} {reg}"

                    elif mnemonic in {"HLT", "NOP"}:  # Instructions sans opérandes
                        assembly_line = mnemonic

                    else:  # Instructions avec registres: ADD, SUB, etc.
                        reg_dest = self.binary_to_register(operands[:3])
                        reg_a = self.binary_to_register(operands[3:6])
                        reg_b = self.binary_to_register(operands[6:])
                        assembly_line = f"{mnemonic} {reg_dest} {reg_a} {reg_b}"

                    assembly_output.append(assembly_line)

                except ValueError as e:
                    raise ValueError(f"Erreur de format pour l'instruction '{mnemonic}' à la ligne {line_no}: {e}")

            # Écriture du fichier texte avec les instructions décompilées
            with open(self.output_file, "w") as asm_file:
                asm_file.write("\n".join(assembly_output))
        
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la décompilation du fichier binaire '{self.input_file}': {str(e)}")