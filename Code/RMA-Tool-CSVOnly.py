import csv
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog, messagebox

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

def load_lexicon_from_csv(file_path):
    """
    Loads lexicon categories and terms from a CSV file into a dictionary.

    Parameters:
    - file_path (str): File path of the CSV input file.

    Returns:
    - lexicon (dict): Dictionary containing lexicon categories as keys and lists of terms as values.

    Note:
    - The CSV file should have lexicon categories as column headers and terms listed under each category.
    """

    lexicon = {
        "Aggrandizement": [],
        "RaceEuphemisms": [],
        "RaceTerms": [],
        "SlaveryTerms": [],
        "GenderTerms": [],
        "LGBTQ": [],
        "MentalIllness": [],
        "Disability": []
    }
    
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            if len(row) == 8:
                lexicon["Aggrandizement"].append(row[0])
                lexicon["RaceEuphemisms"].append(row[1])
                lexicon["RaceTerms"].append(row[2])
                lexicon["SlaveryTerms"].append(row[3])
                lexicon["GenderTerms"].append(row[4])
                lexicon["LGBTQ"].append(row[5])
                lexicon["MentalIllness"].append(row[6])
                lexicon["Disability"].append(row[7])
            else:
                print("Invalid row format. Skipping...")
    
    return lexicon

def analyze_csv(csv_file, output_csv, lexicon_file):
    """
    Analyzes a CSV file containing text data, tokenizes the text, identifies lexicon matches, and writes the results to another CSV file.

    Parameters:
    - csv_file (str): File path of the input CSV file.
    - output_csv (str): File path of the output CSV file.
    - lexicon_file (str): File path of the lexicon CSV file.
    """

    # Load stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    # Load lexicon
    lexicon = load_lexicon_from_csv(lexicon_file)

    # Open CSV file for reading and output CSV file for writing
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as output_csvfile:
        
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Token', 'LexiconCategory']
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Analyze each row in the input CSV file
        for row in reader:
            text = row['Text']
            tokens = [word for word in word_tokenize(text.lower()) if word not in stop_words and word not in punctuation and not word.isdigit() and word != '--']
            
            # Identify lexicon matches for each token
            matching_categories = set()
            for token in tokens:
                for category, terms in lexicon.items():
                    if token in terms:
                        matching_categories.add(category)
            
            # Write each token with lexicon categories to the output CSV file
            for token in tokens:
                row['Token'] = token
                row['LexiconCategory'] = ', '.join(matching_categories)
                writer.writerow(row)

def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, filename)

def browse_lexicon():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    lexicon_entry.delete(0, tk.END)
    lexicon_entry.insert(0, filename)

def browse_output():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def process_files():
    csv_file = csv_entry.get()
    lexicon_file = lexicon_entry.get()
    output_file = output_entry.get()

    if not csv_file or not lexicon_file or not output_file:
        messagebox.showerror("Error", "Please select CSV file, lexicon file, and output file.")
        return
    
    try:
        analyze_csv(csv_file, output_file, lexicon_file)
        messagebox.showinfo("Success", "Analysis completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create GUI
root = tk.Tk()
root.title("CSV Analysis with Lexicon")

# CSV File
csv_label = tk.Label(root, text="Please select the CSV file you want to analyze:")
csv_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
csv_entry = tk.Entry(root, width=50)
csv_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
csv_button = tk.Button(root, text="Browse", command=browse_csv)
csv_button.grid(row=0, column=3, padx=5, pady=5)

# Lexicon File
lexicon_label = tk.Label(root, text="Please select the lexicon CSV file:")
lexicon_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
lexicon_entry = tk.Entry(root, width=50)
lexicon_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
lexicon_button = tk.Button(root, text="Browse", command=browse_lexicon)
lexicon_button.grid(row=1, column=3, padx=5, pady=5)

# Output File
output_label = tk.Label(root, text="Choose where you would like the analysis file to be saved:")
output_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
output_button = tk.Button(root, text="Browse", command=browse_output)
output_button.grid(row=2, column=3, padx=5, pady=5)

# Process Button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
