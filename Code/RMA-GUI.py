import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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

def find_matches(lexicon_df, metadata_df, selected_category):
    matches = []
    for index, row in metadata_df.iterrows():
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            if isinstance(row[col], str):
                for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                    if category == selected_category or selected_category == "All Categories":
                        if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                            matches.append((row['Identifier'], term, category, col))
    return matches

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def process_files():
    lexicon_file_path = lexicon_entry.get()
    metadata_file_path = metadata_entry.get()
    output_file_path = output_entry.get()
    selected_category = category_combobox.get()

    lexicon = load_lexicon(lexicon_file_path)
    metadata = load_metadata(metadata_file_path)

    if lexicon is not None and metadata is not None:
        matches = find_matches(lexicon, metadata, selected_category)
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        merged_df = pd.merge(metadata, matches_df, on="Identifier", how="left")
        merged_df = merged_df.dropna(subset=['Term'])
        merged_df.to_csv(output_file_path, index=False)
        messagebox.showinfo("Success", f"Merged data saved to: {output_file_path}")

# GUI
root = tk.Tk()
root.title("Metadata Matcher")

# Lexicon File
lexicon_label = tk.Label(root, text="Lexicon File:")
lexicon_label.grid(row=0, column=0, padx=5, pady=5)
lexicon_entry = tk.Entry(root, width=50)
lexicon_entry.grid(row=0, column=1, padx=5, pady=5)
lexicon_button = tk.Button(root, text="Browse", command=lambda: browse_file(lexicon_entry))
lexicon_button.grid(row=0, column=2, padx=5, pady=5)

# Metadata File
metadata_label = tk.Label(root, text="Metadata File:")
metadata_label.grid(row=1, column=0, padx=5, pady=5)
metadata_entry = tk.Entry(root, width=50)
metadata_entry.grid(row=1, column=1, padx=5, pady=5)
metadata_button = tk.Button(root, text="Browse", command=lambda: browse_file(metadata_entry))
metadata_button.grid(row=1, column=2, padx=5, pady=5)

# Output File
output_label = tk.Label(root, text="Output File:")
output_label.grid(row=2, column=0, padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=5, pady=5)
output_button = tk.Button(root, text="Browse", command=lambda: browse_file(output_entry))
output_button.grid(row=2, column=2, padx=5, pady=5)

# Category Dropdown
category_label = tk.Label(root, text="Category:")
category_label.grid(row=3, column=0, padx=5, pady=5)
categories = ["All Categories"] + lexicon_df['category'].unique().tolist()
category_combobox = ttk.Combobox(root, values=categories, state="readonly")
category_combobox.current(0)
category_combobox.grid(row=3, column=1, padx=5, pady=5)

# Process Button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
