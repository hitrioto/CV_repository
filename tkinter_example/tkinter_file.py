import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading


class App:
    def __init__(self, root):
        self.root = root
        root.title("C++ Executable GUI")

        # Entry for Parameter1
        tk.Label(root, text="Parameter 1:").pack()
        self.param1 = tk.Entry(root)
        self.param1.pack()

        # Entry for Parameter2
        tk.Label(root, text="Parameter 2:").pack()
        self.param2 = tk.Entry(root)
        self.param2.pack()

        # File selection for text file
        tk.Label(root, text="Select a text file:").pack()
        self.text_file = tk.Entry(root)
        self.text_file.pack()
        tk.Button(root, text="Browse", command=self.browse_file).pack()

        # File selection for JSON file
        tk.Label(root, text="Select a JSON file:").pack()
        self.json_file = tk.Entry(root)
        self.json_file.pack()
        tk.Button(root, text="Browse", command=self.browse_json).pack()

        # Button to run the executable
        tk.Button(root, text="Run", command=self.run_executable).pack()

        # Text area for output
        self.output_area = scrolledtext.ScrolledText(root)
        self.output_area.pack()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        self.text_file.delete(0, tk.END)
        self.text_file.insert(0, filename)

    def browse_json(self):
        filename = filedialog.askopenfilename(
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        self.json_file.delete(0, tk.END)
        self.json_file.insert(0, filename)

    def run_executable(self):
        # Build the command
        import os

        exe_string = os.path.join("tkinter_example", "dist", "simulation.exe")
        cmd = [
            exe_string,
            #'-p1', self.param1.get(),
            #'-p2', self.param2.get(),
            #'-f', self.text_file.get(),
            #'-j', self.json_file.get()
        ]
        threading.Thread(target=self.execute_command, args=(cmd,)).start()

    def execute_command(self, cmd):
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            self.output_area.insert(tk.END, line)
            self.output_area.yview(tk.END)
        process.stdout.close()
        process.wait()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
