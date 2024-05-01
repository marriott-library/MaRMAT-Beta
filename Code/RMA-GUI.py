import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import string

def load_lexicon(file_path):
    try:
        # Load the lexicon CSV file into a DataFrame
        lexicon_df = pd.read_csv(file_path, encoding='latin1')
        return lexicon_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))
        return None

def load_metadata(file_path):
    try:
        # Load the metadata CSV file into a DataFrame
        metadata_df = pd.read_csv(file_path, encoding='latin1')
        
        # Remove punctuation from specified columns
        punctuation_table = str.maketrans('', '', string.punctuation)
        metadata_df['Title'] = metadata_df['Title'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Description'] = metadata_df['Description'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Collection Name'] = metadata_df['Collection Name'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        
        return metadata_df
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))
        return None
    
def find_matches(lexicon_df, metadata_df, selected_categories):
    matches = []
    # Iterate over each row in the metadata DataFrame
    for index, row in metadata_df.iterrows():
        # Process the text in each specified column
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            # Check if the value is a string
            if isinstance(row[col], str):
                # Iterate over each term in the lexicon and check for matches
                for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                    # Check if the term exists in the text column and if it belongs to the selected categories
                    if term.lower() in row[col].lower() and (not selected_categories or category in selected_categories):
                        matches.append((row['Identifier'], term, category, col))
    return matches

def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def analyze():
    lexicon_file_path = lexicon_entry.get()
    metadata_file_path = metadata_entry.get()
    output_file_path = output_entry.get()

    selected_categories = [category_var.get() for category_var in category_vars if category_var.get()]
    
    lexicon = load_lexicon(lexicon_file_path)
    metadata = load_metadata(metadata_file_path)

    if lexicon is not None and metadata is not None:
        matches = find_matches(lexicon, metadata, selected_categories)
        # Create DataFrame from matches
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        # Merge matches with original metadata using left join on "Identifier"
        merged_df = pd.merge(metadata, matches_df, on="Identifier", how="left")
        # Filter out rows without matches
        merged_df = merged_df.dropna(subset=['Term'])
        # Save merged DataFrame to CSV
        merged_df.to_csv(output_file_path, index=False)

        messagebox.showinfo("Success", "Merged data saved to: " + output_file_path)

# Create main window
root = tk.Tk()
root.title("Lexicon Matcher")

# Lexicon file selection
lexicon_label = tk.Label(root, text="Lexicon CSV file:")
lexicon_label.grid(row=0, column=0, sticky=tk.W)
lexicon_entry = tk.Entry(root, width=50)
lexicon_entry.grid(row=0, column=1, padx=5, pady=5)
lexicon_button = tk.Button(root, text="Browse", command=lambda: browse_file(lexicon_entry))
lexicon_button.grid(row=0, column=2, padx=5, pady=5)

# Metadata file selection
metadata_label = tk.Label
