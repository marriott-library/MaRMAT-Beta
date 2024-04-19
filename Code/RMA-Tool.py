import pandas as pd
import re
import string

def load_lexicon(file_path):
    try:
        # Load the lexicon CSV file into a DataFrame
        lexicon_df = pd.read_csv(file_path)
        
        # Ensure the DataFrame has two columns
        if len(lexicon_df.columns) != 2:
            raise ValueError("The lexicon file must have exactly two columns.")
        
        # Rename the columns to 'term' and 'category'
        lexicon_df.columns = ['term', 'category']
        
        return lexicon_df
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print("An error occurred:", str(e))

def load_metadata(file_path):
    try:
        # Load the metadata CSV file into a DataFrame
        metadata_df = pd.read_csv(file_path)
        return metadata_df
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print("An error occurred:", str(e))

def remove_punctuation(text):
    # Remove punctuation from the text
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def find_matches(lexicon_df, metadata_df):
    matches = []
    # Iterate over the terms in the lexicon
    for term, category in zip(lexicon_df['term'], lexicon_df['category']):
        # Create a regex pattern for the term
        pattern = r'\b' + re.escape(term) + r'\b'
