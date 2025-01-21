import tkinter as tk
from compilator.Assembler import Assembler # Importer la classe Assembler
from compilator.UnAssembler import UnAssembler # Importer la classe UnAssembler

class CompilerInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Assembler et Décompiler")
        self.root.configure(bg="#2b2b2b")

        # Centrer l'interface
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (1300 / 2)
        y = (screen_height / 2) - (800 / 2)
        self.root.geometry(f'1300x800+{int(x)}+{int(y)}')

        # Cadre principal
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Titre
        title_label = tk.Label(
            main_frame, text="Assembler et Décompiler", font=("Arial", 16, "bold"),
            bg="#2b2b2b", fg="#ffffff"
        )
        title_label.pack(side=tk.TOP, pady=10)

        # Boutons en haut
        button_frame = tk.Frame(main_frame, bg="#2b2b2b")
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.assembler_button = tk.Button(
            button_frame, text="Compiler", bg="#4CAF50", fg="white", font=("Arial", 10),
            command=self.compile_code
        )
        self.assembler_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.unassembler_button = tk.Button(
            button_frame, text="Décompiler", bg="#2196F3", fg="white", font=("Arial", 10),
            command=self.uncompile_code
        )
        self.unassembler_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.open_file_button = tk.Button(
            button_frame, text="Ouvrir Fichier", bg="#FFC107", fg="black", font=("Arial", 10),
            command=self.open_file
        )
        self.open_file_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.save_button = tk.Button(
            button_frame, text="Sauvegarder", bg="#FF5722", fg="white", font=("Arial", 10),
            command=self.save_file
        )
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Cadre de gauche pour assembler et décompiler
        left_frame = tk.Frame(main_frame, bg="#3c3f41", bd=2, relief=tk.RIDGE, padx=5, pady=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Champ pour assembler
        assembler_label = tk.Label(
            left_frame, text="Assembler", font=("Arial", 12), bg="#3c3f41", fg="#ffffff", anchor="w"
        )
        assembler_label.pack(fill=tk.X)

        self.assembler_entry = tk.Text(
            left_frame, height=15, font=("consolas", 12), wrap=tk.WORD,
            bg="#2b2b2b", fg="#ffffff", insertbackground="#ffffff"
        )
        self.assembler_entry.pack(fill=tk.BOTH, expand=True, pady=5)

        # Champ pour décompiler
        unassembler_label = tk.Label(
            left_frame, text="Décompiler", font=("Arial", 12), bg="#3c3f41", fg="#ffffff", anchor="w"
        )
        unassembler_label.pack(fill=tk.X)

        self.unassembler_entry = tk.Text(
            left_frame, height=15, font=("consolas", 12), wrap=tk.WORD,
            bg="#2b2b2b", fg="#ffffff", insertbackground="#ffffff"
        )
        self.unassembler_entry.pack(fill=tk.BOTH, expand=True, pady=5)

        # Cadre droit pour le jeu d'instructions
        right_frame = tk.Frame(main_frame, bg="#3c3f41", bd=2, relief=tk.RIDGE)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_label = tk.Label(
            right_frame, text="Instruction Set", font=("Arial", 16, "bold"),
            bg="#3c3f41", fg="#ffffff"
        )
        right_label.pack(pady=10)

        self.instructions_text = tk.Text(
            right_frame, width=40, height=15, bg="#2b2b2b", font=("Courier", 10),
            fg="#ffffff", state=tk.DISABLED, insertbackground="#ffffff"
        )
        self.instructions_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Charger le jeu d'instructions
        self.load_instruction_set()

        # Cadre d'aide en bas
        self.help_label = tk.Label(
            right_frame, text="Aide: Sélectionner une instruction pour plus d'infos", font=("Arial", 10, "italic"),
            bg="#3c3f41", fg="#ffffff"
        )
        self.help_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.help_text = tk.Text(
            right_frame, height=5, bg="#2b2b2b", font=("Courier", 10),
            fg="#ffffff", wrap=tk.WORD, insertbackground="#ffffff", state=tk.DISABLED
        )
        self.help_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Cadre pour les erreurs de compilation en bas
        self.error_label = tk.Label(
            right_frame, text="Erreurs de Compilation", font=("Arial", 12, "bold"),
            bg="#3c3f41", fg="#ffffff"
        )
        self.error_label.pack(pady=10)

        self.error_text = tk.Text(
            right_frame, height=5, bg="#2b2b2b", font=("Courier", 10),
            fg="#ffffff", wrap=tk.WORD, insertbackground="#ffffff", state=tk.DISABLED
        )
        self.error_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_instruction_set(self):
        """Charge l'instruction set dans la section droite."""
        instruction_set = {
            "NOP": "0000 - No Operation",
            "HLT": "0001 - Halt the program",
            "ADD": "0010 - Add two registers",
            "SUB": "0011 - Subtract two registers",
            "ORR": "0100 - Logical OR",
            "NOR": "0101 - Logical NOR",
            "AND": "0110 - Logical AND",
            "XOR": "0111 - Logical XOR",
            "INC": "1000 - Increment a register",
            "DEC": "1001 - Decrement a register",
            "RSH": "1010 - Right shift",
            "LDI": "1011 - Load immediate",
            "LOD": "1100 - Load from memory",
            "STR": "1101 - Store to memory",
            "JMP": "1110 - Jump to address",
            "BIF": "1111 - Branch if condition is met",
        }

        self.instructions_text.config(state=tk.NORMAL)
        for mnemonic, description in instruction_set.items():
            self.instructions_text.insert(tk.END, f"{mnemonic}: {description}\n")
        self.instructions_text.config(state=tk.DISABLED)

    def update_help_text(self, instruction):
        """Mise à jour du texte d'aide pour l'instruction sélectionnée."""
        help_texts = {
            "NOP": "No Operation: Does nothing, typically used for padding.",
            "HLT": "Halt: Stops the program execution.",
            "ADD": "Add: Adds two registers.",
            "SUB": "Subtract: Subtracts one register from another.",
            "ORR": "Logical OR: Performs a logical OR operation.",
            "NOR": "Logical NOR: Performs a logical NOR operation.",
            "AND": "Logical AND: Performs a logical AND operation.",
            "XOR": "Logical XOR: Performs a logical XOR operation.",
            "INC": "Increment: Increments the value in a register by one.",
            "DEC": "Decrement: Decrements the value in a register by one.",
            "RSH": "Right Shift: Shifts bits in a register to the right.",
            "LDI": "Load Immediate: Loads an immediate value into a register.",
            "LOD": "Load from Memory: Loads a value from memory into a register.",
            "STR": "Store to Memory: Stores a register value into memory.",
            "JMP": "Jump: Jumps to a specific memory address.",
            "BIF": "Branch If: Branches if a condition is met.",
        }
        self.help_text.config(state=tk.NORMAL)
        self.help_text.delete("1.0", tk.END)
        self.help_text.insert("1.0", help_texts.get(instruction, "Sélectionner une instruction pour plus d'infos."))
        self.help_text.config(state=tk.DISABLED)

    def compile_code(self):
        """Compile the assembler code."""
        code = self.assembler_entry.get("1.0", tk.END).strip()
        try:
            # Crée le fichier .asm à partir du code entré
            with open("code/input.asm", "w") as file:
                file.write(code)

            # Crée l'objet Assembler et compile le code
            assembler = Assembler("code/input.asm", "compile/output.bin")
            assembler.compile_assembly()

            # Ouvrir le fichier binaire compilé et afficher le contenu binaire
            with open("compile/output.bin", "rb") as bin_file:
                binary_code = bin_file.read()

            # Afficher le code binaire dans le champ de texte
            self.unassembler_entry.insert("1.0", binary_code)

            # Réinitialiser le champ d'erreur
            self.error_text.config(state=tk.NORMAL)
            self.error_text.delete("1.0", tk.END)
            self.error_text.config(state=tk.DISABLED)

        except Exception as e:
            # Afficher l'erreur dans le champ d'erreur
            self.error_text.config(state=tk.NORMAL)
            self.error_text.delete("1.0", tk.END)
            self.error_text.insert("1.0", f"Erreur de compilation : {str(e)}")
            self.error_text.config(state=tk.DISABLED)

    def uncompile_code(self):
        """Uncompile the binary code."""
        try:
            # Crée l'objet UnAssembler et décompile le fichier binaire
            unassembler = UnAssembler("compile/output.bin", "code/decompiled.asm")
            unassembler.decompile_binary()

            with open("code/decompiled.asm", "r") as file:
                decompiled_code = file.read()

            # Affiche le code décompilé dans le champ unassembler_entry
            self.assembler_entry.insert("1.0", decompiled_code)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la décompilation : {str(e)}")

    def open_file(self):
        """Open a file and load its content into the assembler field."""
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, "r") as file:
                    code = file.read()
                    self.assembler_entry.delete("1.0", tk.END)
                    self.assembler_entry.insert("1.0", code)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du fichier : {str(e)}")

    def save_file(self):
        """Save the compiled or decompiled code to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".asm", filetypes=[("Assembly Files", "*.asm"), ("All Files", "*.*")])
        if file_path:
            try:
                # Récupère le code dans l'un des champs de texte
                code = self.assembler_entry.get("1.0", tk.END).strip() or self.unassembler_entry.get("1.0", tk.END).strip()
                with open(file_path, "w") as file:
                    file.write(code)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde du fichier : {str(e)}")
