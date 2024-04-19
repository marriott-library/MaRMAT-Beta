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

def analyze_csv(csv_file, output_csv):
    """
    Analyzes a CSV file containing text data, tokenizes the text, and writes the results to another CSV file.

    Parameters:
    - csv_file (str): File path of the input CSV file.
    - output_csv (str): File path of the output CSV file.
    """

    # Load stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)

    # Open CSV file for reading and output CSV file for writing
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as output_csvfile:
        
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Token']
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Analyze each row in the input CSV file
        for row in reader:
            text = row['Text']
            tokens = [word for word in word_tokenize(text.lower()) if word not in stop_words and word not in punctuation and not word.isdigit() and word != '--']
            
            # Write each token as a separate row with other columns filled down
            for token in tokens:
                row['Token'] = token
                writer.writerow(row)

def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, filename)

def browse_output():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def process_files():
    csv_file = csv_entry.get()
    output_file = output_entry.get()

    if not csv_file or not output_file:
        messagebox.showerror("Error", "Please select CSV file and output file.")
        return
    
    try:
        analyze_csv(csv_file, output_file)
        messagebox.showinfo("Success", "Analysis completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create GUI
root = tk.Tk()
root.title("CSV Analysis")

# CSV File
csv_label = tk.Label(root, text="Please select the CSV file you want to analyze:")
csv_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
csv_entry = tk.Entry(root, width=50)
csv_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
csv_button = tk.Button(root, text="Browse", command=browse_csv)
csv_button.grid(row=0, column=3, padx=5, pady=5)

# Output File
output_label = tk.Label(root, text="Choose where you would like the analysis file to be saved:")
output_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
output_button = tk.Button(root, text="Browse", command=browse_output)
output_button.grid(row=1, column=3, padx=5, pady=5)

# Process Button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
