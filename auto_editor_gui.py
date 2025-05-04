import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os

class AutoEditorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Silence Cutter")

        # Variables to store file paths and settings
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.threshold_value = tk.StringVar(value="4%") # Default threshold
        self.margin_value = tk.StringVar(value="0.2sec") # Default margin
        self.status_text = tk.StringVar(value="Ready")

        # --- GUI Elements ---

        # Input File Selection
        tk.Label(root, text="Input Video File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.input_file_path, state='readonly', width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Select Input File", command=self.select_input_file).grid(row=0, column=2, padx=5, pady=5)
    
        # Silence Threshold
        tk.Label(root, text="Silence Threshold:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.threshold_value, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Margin
        tk.Label(root, text="Margin:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.margin_value, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Output File Selection
        tk.Label(root, text="Output MP4 File:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.output_file_path, state='readonly', width=50).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(root, text="Set Output File", command=self.set_output_file).grid(row=3, column=2, padx=5, pady=5)

        # Start Button
        tk.Button(root, text="Start Cutting Silence", command=self.start_processing).grid(row=4, column=0, columnspan=3, pady=10)

        # Status Bar
        tk.Label(root, textvariable=self.status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W).grid(row=5, column=0, columnspan=3, sticky="ew")

    def select_input_file(self):
        filetypes = [("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="Select Input Video File", filetypes=filetypes)
        if filepath:
            self.input_file_path.set(filepath)
            # Suggest an output filename based on the input
            input_dir, input_filename = os.path.split(filepath)
            name, ext = os.path.splitext(input_filename)
            suggested_output = os.path.join(input_dir, f"{name}_edited.mp4")
            self.output_file_path.set(suggested_output)


    def set_output_file(self):
        filetypes = [("MP4 files", "*.mp4")]
        filepath = filedialog.asksaveasfilename(title="Set Output MP4 File", defaultextension=".mp4", filetypes=filetypes)
        if filepath:
            # Ensure the extension is .mp4
            if not filepath.lower().endswith(".mp4"):
                filepath += ".mp4"
            self.output_file_path.set(filepath)

    def start_processing(self):
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()
        threshold = self.threshold_value.get()
        margin = self.margin_value.get()

        if not input_file:
            messagebox.showwarning("Input Missing", "Please select an input video file.")
            return
        if not output_file:
            messagebox.showwarning("Output Missing", "Please set the output MP4 file.")
            return

        # Construct the auto-editor command
        command = [
            "auto-editor",
            input_file,
            "-o", output_file,
            "--edit", f"audio:threshold={threshold}",
            "--margin", margin
        ]

        self.status_text.set("Processing...")
        # Run the command in a separate thread to keep the GUI responsive
        threading.Thread(target=self.run_auto_editor, args=(command,)).start()

    def run_auto_editor(self, command):
        try:
            # Use shell=True on Windows to handle paths with spaces correctly
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.status_text.set("Finished!")
                messagebox.showinfo("Success", "Auto-editor finished successfully!")
            else:
                self.status_text.set("Error occurred")
                error_message = stderr.decode('utf-8')
                messagebox.showerror("Error", f"Auto-editor failed:\n{error_message}")

        except FileNotFoundError:
            self.status_text.set("Error: auto-editor not found")
            messagebox.showerror("Error", "The 'auto-editor' command was not found. Please ensure it is installed and in your system's PATH.")
        except Exception as e:
            self.status_text.set(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoEditorGUI(root)
    root.mainloop()