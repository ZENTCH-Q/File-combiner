import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Files Combiner")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # List to store selected file paths
        self.selected_files = []

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Add Files Button
        add_button = tk.Button(
            button_frame, 
            text="Add Python Files", 
            command=self.add_files, 
            padx=10, 
            pady=5,
            font=("Arial", 12)
        )
        add_button.grid(row=0, column=0, padx=5)

        # Remove Selected Button
        remove_button = tk.Button(
            button_frame, 
            text="Remove Selected", 
            command=self.remove_selected, 
            padx=10, 
            pady=5,
            font=("Arial", 12)
        )
        remove_button.grid(row=0, column=1, padx=5)

        # Clear All Button
        clear_button = tk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all, 
            padx=10, 
            pady=5,
            font=("Arial", 12)
        )
        clear_button.grid(row=0, column=2, padx=5)

        # Listbox to display selected files
        self.listbox = tk.Listbox(
            self.root, 
            selectmode=tk.EXTENDED, 
            width=80, 
            height=15,
            font=("Arial", 10)
        )
        self.listbox.pack(pady=10)

        # Combine Files Button
        combine_button = tk.Button(
            self.root, 
            text="Combine Files", 
            command=self.combine_files, 
            padx=10, 
            pady=5,
            font=("Arial", 12),
            bg="green",
            fg="white"
        )
        combine_button.pack(pady=10)

    def add_files(self):
        """
        Opens a file dialog for the user to select multiple Python (.py) files from any directory.
        """
        file_paths = filedialog.askopenfilenames(
            title="Select Python Files",
            filetypes=[("Python Files", "*.py")]
        )
        if file_paths:
            # Avoid adding duplicates
            new_files = [f for f in file_paths if f not in self.selected_files]
            self.selected_files.extend(new_files)
            for file in new_files:
                self.listbox.insert(tk.END, file)

    def remove_selected(self):
        """
        Removes the selected files from the list.
        """
        selected_indices = list(self.listbox.curselection())
        selected_indices.reverse()  # Remove from the end to avoid index shifting
        for index in selected_indices:
            file_path = self.listbox.get(index)
            self.selected_files.remove(file_path)
            self.listbox.delete(index)

    def clear_all(self):
        """
        Clears all selected files from the list.
        """
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all selected files?"):
            self.selected_files.clear()
            self.listbox.delete(0, tk.END)

    def combine_files(self):
        """
        Combines the contents of the selected Python files into a single text file.
        """
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please add at least one Python file to combine.")
            return

        try:
            # Prompt user to choose the save location for the combined file
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Combined File As"
            )
            if not save_path:
                return  # User cancelled the save dialog

            with open(save_path, 'w', encoding='utf-8') as outfile:
                for file_path in self.selected_files:
                    outfile.write(f"# ===== {os.path.basename(file_path)} =====\n")
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n\n")  # Add spacing between files
            messagebox.showinfo("Success", f"Combined file saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    """
    Sets up the main application window and starts the Tkinter event loop.
    """
    root = tk.Tk()
    app = FileCombinerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
