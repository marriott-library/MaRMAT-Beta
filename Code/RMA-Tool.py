import pandas as pd
import string
import re

def load_lexicon(file_path):
    try:
        # Load the lexicon CSV file into a DataFrame
        lexicon_df = pd.read_csv(file_path)
        return lexicon_df
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print("An error occurred:", e)
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
        print("File not found. Please provide a valid file path.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def find_matches(lexicon_df, metadata_df):
    matches = []
    # Iterate over each row in the metadata DataFrame
    for index, row in metadata_df.iterrows():
        # Process the text in each specified column
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            # Iterate over each term in the lexicon and check for matches
            for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                # Check if the term exists in the text column
