import csv
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

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
            for category, terms in lexicon.items():
                terms.extend(row)  # Assuming each row contains terms for each lexicon category
    
    return lexicon

def search_and_append_lexicon_category(lexicon, input_csv_file, output_csv_file):
    """
    Searches for lexicon term matches in specified columns of an input CSV file,
    appends lexicon categories to each row, and writes the modified data into an output CSV file.

    Parameters:
    - lexicon (dict): Dictionary containing lexicon categories as keys and lists of terms as values.
    - input_csv_file (str): File path of the input CSV file.
    - output_csv_file (str): File path of the output CSV file.

    Note:
    - Specified columns for lexicon analysis: "Title", "Subject", "Description", "Collection Name"
    - The output CSV file will have additional columns for each lexicon category, indicating the matched terms.
    """

    # Load lexicon
    lexicon = load_lexicon_from_csv(lexicon)

    # Open input CSV file for reading and output CSV file for writing
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as input_csv, \
         open(output_csv_file, 'w', newline='', encoding='utf-8') as output_csv:
        
        reader = csv.DictReader(input_csv)
        fieldnames = reader.fieldnames + list(lexicon.keys())  # Add lexicon category names as additional columns
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        
        # Iterate over rows in the input CSV file
        for row in reader:
            # Tokenize and preprocess text from specified columns
            for column in ["Title", "Subject", "Description", "Collection Name"]:
                text = row[column]
                if text:
                    tokens = word_tokenize(text.lower())
                    filtered_tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation and not word.isdigit() and word != '--']
                    # Search for matches between tokens and terms in the lexicon
                    for category, terms in lexicon.items():
                        matches = [term for term in filtered_tokens if term in terms]
                        # Append lexicon matches to the row
                        row[category] = ', '.join(matches)
            # Write the modified row to the output CSV file
            writer.writerow(row)

# File paths
lexicon_file_path = "PATH_TO_LEXICON_CSV_FILE"  # Insert path to your lexicon CSV file
input_csv_file_path = "PATH_TO_INPUT_CSV_FILE"  # Insert path to your input CSV file
output_csv_file_path = "PATH_TO_OUTPUT_CSV_FILE"  # Insert path to desired output CSV file

# Search for matches, append lexicon categories, and write to output CSV
search_and_append_lexicon_category(lexicon_file_path, input_csv_file_path, output_csv_file_path)

print("Lexicon matching and appending completed.")
