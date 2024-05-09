import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import string
import re

def load_lexicon(file_path):
    try:
        lexicon_df = pd.read_csv(file_path, encoding='latin1')
        return lexicon_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def load_metadata(file_path):
    try:
        metadata_df = pd.read_csv(file_path, encoding='latin1')
        punctuation_table = str.maketrans('', '', string.punctuation)
        metadata_df['Title'] = metadata_df['Title'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Description'] = metadata_df['Description'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Collection Name'] = metadata_df['Collection Name'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        return metadata_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
    
def find_matches(lexicon_df, metadata_df):
    matches = []
    for index, row in metadata_df.iterrows():
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            if isinstance(row[col], str):
                for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                    if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                        matches.append((row['Identifier'], term, category, col))
    return matches

def execute_matching():
    lexicon_file_path = lexicon_entry.get()
    metadata_file_path = metadata_entry.get()
    output_file_path = output_entry.get()
    
    lexicon = load_lexicon(lexicon_file_path)
    metadata = load_metadata(metadata_file_path)

    if lexicon is not None and metadata is not None:
        matches = find_matches(lexicon, metadata)
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        merged_df = pd.merge(metadata, matches_df, on="Identifier", how="left")
        merged_df = merged_df.dropna(subset=['Term'])
        merged_df.to_csv(output_file_path, index=False)
        messagebox.showinfo("Success", "Matching process completed. Output saved successfully.")

# GUI
root = tk.Tk()
root.title("Lexicon Matcher")

# Lexicon file path entry
lexicon_label = tk.Label(root, text="Lexicon File Path:")
lexicon_label.grid(row=0, column=0, padx=5, pady=5)
lexicon_entry = tk.Entry(root, width=50)
lexicon_entry.grid(row=0, column=1, padx=5, pady=5)
lexicon_button = tk.Button(root, text="Browse", command=lambda: lexicon_entry.insert(tk.END, filedialog.askopenfilename()))
lexicon_button.grid(row=0, column=2, padx=5, pady=5)

# Metadata file path entry
metadata_label = tk.Label(root, text="Metadata File Path:")
metadata_label.grid(row=1, column=0, padx=5, pady=5)
metadata_entry = tk.Entry(root, width=50)
metadata_entry.grid(row=1, column=1, padx=5, pady=5)
metadata_button = tk.Button(root, text="Browse", command=lambda: metadata_entry.insert(tk.END, filedialog.askopenfilename()))
metadata_button.grid(row=1, column=2, padx=5, pady=5)

# Output file path entry
output_label = tk.Label(root, text="Output File Path:")
output_label.grid(row=2, column=0, padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=5, pady=5)
output_button = tk.Button(root, text="Browse", command=lambda: output_entry.insert(tk.END, filedialog.asksaveasfilename(defaultextension=".csv")))
output_button.grid(row=2, column=2, padx=5, pady=5)

# Execute button
execute_button = tk.Button(root, text="Execute Matching", command=execute_matching)
execute_button.grid(row=3, column=1, padx=5, pady=5)

root.mainloop()
