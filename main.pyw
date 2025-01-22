import tkinter as tk
from compilator.Interface import CompilerInterface

if __name__ == "__main__":
    root = tk.Tk()
    interface = CompilerInterface(root)
    root.mainloop()