import pandas as pd
import string
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def load_lexicon(file_path):
    try:
        # Load the lexicon CSV file into a DataFrame
        lexicon_df = pd.read_csv(file_path)
        return lexicon_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def load_metadata(file_path):
    try:
        # Load the metadata CSV file into a DataFrame
        metadata_df = pd.read_csv(file_path)
        
        # Remove punctuation from specified columns
        punctuation_table = str.maketrans('', '', string.punctuation)
        metadata_df['Title'] = metadata_df['Title'].apply(lambda x: x.translate(punctuation_table))
        metadata_df['Description'] = metadata_df['Description'].apply(lambda x: x.translate(punctuation_table))
        metadata_df['Collection Name'] = metadata_df['Collection Name'].apply(lambda x: x.translate(punctuation_table))
        
        return metadata_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def find_matches(lexicon_df, metadata_df, search_terms=None):
    matches = []
    # If no search terms provided, use all terms in the lexicon
    if not search_terms:
        search_terms = lexicon_df['term']
    # Iterate over each row in the metadata DataFrame
    for index, row in metadata_df.iterrows():
        # Process the text in each specified column
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            # Iterate over each term in the lexicon and check for matches
            for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                if term in search_terms:
                    # Check if the whole term exists in the text column
                    if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                        matches.append((row['Identifier'], term, category, col))
    return matches

def search():
    lexicon_file_path = lexicon_path_entry.get()
    metadata_file_path = metadata_path_entry.get()
    category = category_entry.get()
    
    lexicon = load_lexicon(lexicon_file_path)
    metadata = load_metadata(metadata_file_path)
    
    if lexicon is not None and metadata is not None:
        search_terms = None
        if category:
            # Filter lexicon terms based on category
            search_terms = lexicon[lexicon['category'] == category]['term']
        matches = find_matches(lexicon, metadata, search_terms)
        # Create DataFrame from matches
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        # Merge matches with original metadata using left join on "Identifier"
        merged_df = pd.merge(metadata, matches_df, on="Identifier", how="left")
        # Filter out rows without matches
        merged_df = merged_df.dropna(subset=['Term'])
        # Save merged DataFrame to CSV
        output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if output_file_path:
            merged_df.to_csv(output_file_path, index=False)
            messagebox.showinfo("Success", "Merged data saved successfully.")
    else:
        messagebox.showerror("Error", "Failed to load lexicon or metadata.")

# Create the main window
root = tk.Tk()
root.title("Lexicon Matcher")

# Lexicon file path entry
lexicon_path_label = tk.Label(root, text="Lexicon File Path:")
lexicon_path_label.grid(row=0, column=0, sticky="e")
lexicon_path_entry = tk.Entry(root, width=50)
lexicon_path_entry.grid(row=0, column=1, padx=5, pady=5)
lexicon_browse_button = tk.Button(root, text="Browse", command=lambda: lexicon_path_entry.insert(tk.END, filedialog.askopenfilename()))
lexicon_browse_button.grid(row=0, column=2, padx=5, pady=5)

# Metadata file path entry
metadata_path_label = tk.Label(root, text="Metadata File Path:")
metadata_path_label.grid(row=1, column=0, sticky="e")
metadata_path_entry = tk.Entry(root, width=50)
metadata_path_entry.grid(row=1, column=1, padx=5, pady=5)
metadata_browse_button = tk.Button(root, text="Browse", command=lambda: metadata_path_entry.insert(tk.END, filedialog.askopenfilename()))
metadata_browse_button.grid(row=1, column=2, padx=5, pady=5)

# Category entry
category_label = tk.Label(root, text="Category (optional):")
category_label.grid(row=2, column=0, sticky="e")
category_entry = tk.Entry(root, width=50)
category_entry.grid(row=2, column=1, padx=5, pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=3, column=1, pady=10)

root.mainloop()
