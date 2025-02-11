import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Combiner with Format Selection")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Store paths of selected files
        self.selected_files = []

        # Mapping of Combobox label -> file dialog filter
        # You can add/remove formats as you please.
        self.format_options = {
            "Python Files (*.py)": [("Python Files", "*.py")],
            "Text Files (*.txt)": [("Text Files", "*.txt")],
            "Markdown Files (*.md)": [("Markdown Files", "*.md")],
            "HTML Files (*.html)": [("HTML Files", "*.html")],
            "JavaScript Files (*.js)": [("JavaScript Files", "*.js")],
            "All Files (*.*)": [("All Files", "*.*")]
        }

        self.create_widgets()

    def create_widgets(self):
        # =========== Top Button Frame ===========
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame,
            text="Add Files",
            command=self.add_files,
            padx=10,
            pady=5,
            font=("Arial", 12)
        )
        add_button.grid(row=0, column=0, padx=5)

        remove_button = tk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_selected,
            padx=10,
            pady=5,
            font=("Arial", 12)
        )
        remove_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            padx=10,
            pady=5,
            font=("Arial", 12)
        )
        clear_button.grid(row=0, column=2, padx=5)

        # =========== Listbox for Selected Files ===========
        self.listbox = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=80, height=15, font=("Arial", 10))
        self.listbox.pack(pady=10)

        # =========== Bottom Frame for Format Selection and Combine Button ===========
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Label
        format_label = tk.Label(bottom_frame, text="Select file format:", font=("Arial", 10, "bold"))
        format_label.pack(side=tk.LEFT)

        # Combobox to select the file format
        self.format_combobox = ttk.Combobox(bottom_frame, state="readonly", width=25)
        # Set the dropdown options from self.format_options keys
        self.format_combobox["values"] = list(self.format_options.keys())
        self.format_combobox.set("Python Files (*.py)")  # default selection
        self.format_combobox.pack(side=tk.LEFT, padx=5)

        # Combine Files Button
        combine_button = tk.Button(
            bottom_frame,
            text="Combine Files",
            command=self.combine_files,
            padx=10,
            pady=5,
            font=("Arial", 12),
            bg="green",
            fg="white"
        )
        combine_button.pack(side=tk.RIGHT, padx=5)

    def add_files(self):
        """
        Open a file dialog using the selected format from the combobox.
        Only files of that format (or 'All Files') will be shown.
        """
        chosen_format = self.format_combobox.get()
        filetypes = self.format_options.get(chosen_format, [("All Files", "*.*")])

        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=filetypes
        )

        if file_paths:
            # Avoid adding duplicates
            new_files = [f for f in file_paths if f not in self.selected_files]
            self.selected_files.extend(new_files)
            for file in new_files:
                self.listbox.insert(tk.END, file)

    def remove_selected(self):
        """
        Remove highlighted files from the listbox and from the selected_files list.
        """
        selected_indices = list(self.listbox.curselection())
        selected_indices.reverse()
        for idx in selected_indices:
            file_path = self.listbox.get(idx)
            self.selected_files.remove(file_path)
            self.listbox.delete(idx)

    def clear_all(self):
        """
        Clear all selected files after a confirmation.
        """
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all selected files?"):
            self.selected_files.clear()
            self.listbox.delete(0, tk.END)

    def combine_files(self):
        """
        Combine the contents of all selected files into a single text file.
        """
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please add at least one file.")
            return

        # Prompt user for save location
        save_path = filedialog.asksaveasfilename(
            title="Save Combined File",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if not save_path:
            return  # User canceled the save dialog

        try:
            with open(save_path, "w", encoding="utf-8") as outfile:
                for file_path in self.selected_files:
                    outfile.write(f"# === {os.path.basename(file_path)} ===\n")
                    # Attempt to read file as text
                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            data = infile.read()
                            outfile.write(data)
                    except UnicodeDecodeError:
                        outfile.write(f"# [Skipped: Unable to read {file_path} as text.]\n")
                    outfile.write("\n\n")

            messagebox.showinfo("Success", f"Combined file saved at:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    root = tk.Tk()
    app = FileCombinerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
