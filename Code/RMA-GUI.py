import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import string
import re

class MetadataMatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metadata Matcher")
        self.geometry("600x400")
        self.current_page = None
        self.lexicon_df = None
        self.metadata_df = None
        self.selected_category = tk.StringVar()
        self.create_main_page()

    def create_main_page(self):
        self.current_page = MainPage(self)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def load_lexicon(self, file_path):
        try:
            self.lexicon_df = pd.read_csv(file_path, encoding='latin1')
            self.current_page.destroy()
            self.create_metadata_page()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_metadata(self, file_path):
        try:
            self.metadata_df = pd.read_csv(file_path, encoding='latin1')
            self.current_page.destroy()
            # Create the page to select categories here if needed
            self.process_files()  # Directly process files after loading metadata
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_metadata_page(self):
        self.current_page = MetadataPage(self)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def process_files(self):
        output_file_path = self.current_page.output_entry.get()

        if self.lexicon_df is None or self.metadata_df is None:
            messagebox.showerror("Error", "Please load lexicon and metadata files.")
            return

        selected_category = self.selected_category.get()

        matches = self.find_matches(selected_category)
        if matches:
            self.save_matches(matches, output_file_path)

    def find_matches(self, selected_category):
        matches = []
        for index, row in self.metadata_df.iterrows():
            for col in ['Title', 'Description', 'Subject', 'Collection Name']:
                if isinstance(row[col], str):
                    for term, category in zip(self.lexicon_df['term'], self.lexicon_df['category']):
                        if category == selected_category or selected_category == "All Categories":
                            if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                                matches.append((row['Identifier'], term, category, col))
        return matches

    def save_matches(self, matches, output_file_path):
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        merged_df = pd.merge(self.metadata_df, matches_df, on="Identifier", how="left")
        merged_df = merged_df.dropna(subset=['Term'])
        merged_df.to_csv(output_file_path, index=False)
        messagebox.showinfo("Success", f"Merged data saved to: {output_file_path}")


class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))

        lexicon_label = ttk.Label(self, text="Lexicon File:")
        lexicon_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lexicon_entry = ttk.Entry(self, width=50)
        self.lexicon_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        lexicon_button = ttk.Button(self, text="Browse", command=self.browse_lexicon)
        lexicon_button.grid(row=0, column=2, padx=5, pady=5)

        metadata_label = ttk.Label(self, text="Metadata File:")
        metadata_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.metadata_entry = ttk.Entry(self, width=50)
        self.metadata_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        metadata_button = ttk.Button(self, text="Browse", command=self.browse_metadata)
        metadata_button.grid(row=1, column=2, padx=5, pady=5)

        output_label = ttk.Label(self, text="Output File:")
        output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.output_entry = ttk.Entry(self, width=50)
        self.output_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        output_button = ttk.Button(self, text="Browse", command=self.browse_output)
        output_button.grid(row=2, column=2, padx=5, pady=5)

        process_button = ttk.Button(self, text="Next", command=self.process_next)
        process_button.grid(row=3, column=1, padx=5, pady=5)

        self.columnconfigure(1, weight=1)  # Expand middle column

    def browse_lexicon(self):
        filename = filedialog.askopenfilename()
        self.lexicon_entry.delete(0, tk.END)
        self.lexicon_entry.insert(0, filename)

    def browse_metadata(self):
        filename = filedialog.askopenfilename()
        self.metadata_entry.delete(0, tk.END)
        self.metadata_entry.insert(0, filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, filename)

    def process_next(self):
        lexicon_file = self.lexicon_entry.get()
        metadata_file = self.metadata_entry.get()
        output_file = self.output_entry.get()

        if not all([lexicon_file, metadata_file, output_file]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.master.load_lexicon(lexicon_file)
        self.master.load_metadata(metadata_file)


class MetadataPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))

        lexicon_label = ttk.Label(self, text="Lexicon File:")
        lexicon_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lexicon_entry = ttk.Entry(self, width=50)
        self.lexicon_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        lexicon_button = ttk.Button(self, text="Browse", command=self.browse_lexicon)
        lexicon_button.grid(row=0, column=2, padx=5, pady=5)

        metadata_label = ttk.Label(self, text="Metadata File:")
        metadata_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.metadata_entry = ttk.Entry(self, width=50)
        self.metadata_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        metadata_button = ttk.Button(self, text="Browse", command=self.browse_metadata)
        metadata_button.grid(row=1, column=2, padx=5, pady=5)

        output_label = ttk.Label(self, text="Output File:")
        output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.output_entry = ttk.Entry(self, width=50)
        self.output_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        output_button = ttk.Button(self, text="Browse", command=self.browse_output)
        output_button.grid(row=2, column=2, padx=5, pady=5)

        process_button = ttk.Button(self, text="Process", command=self.process_files)
        process_button.grid(row=3, column=1, padx=5, pady=5)

        self.columnconfigure(1, weight=1)  # Expand middle column

    def browse_lexicon(self):
        filename = filedialog.askopenfilename()
        self.lexicon_entry.delete(0, tk.END)
        self.lexicon_entry.insert(0, filename)

    def browse_metadata(self):
        filename = filedialog.askopenfilename()
        self.metadata_entry.delete(0, tk.END)
        self.metadata_entry.insert(0, filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, filename)

    def process_files(self):
        lexicon_file = self.lexicon_entry.get()
        metadata_file = self.metadata_entry.get()
        output_file = self.output_entry.get()

        if not all([lexicon_file, metadata_file, output_file]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.master.load_lexicon(lexicon_file)
        self.master.load_metadata(metadata_file)


if __name__ == "__main__":
    app = MetadataMatcherApp()
    app.mainloop()
