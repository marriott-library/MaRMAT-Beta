import pandas as pd
import string
import re

def load_lexicon(file_path):
    try:
        # Load the lexicon CSV file into a DataFrame
        lexicon_df = pd.read_csv(file_path, encoding='latin1')
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
        metadata_df = pd.read_csv(file_path, encoding='latin1')
        
        # Remove punctuation from specified columns
        punctuation_table = str.maketrans('', '', string.punctuation)
        metadata_df['Title'] = metadata_df['Title'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Description'] = metadata_df['Description'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        metadata_df['Collection Name'] = metadata_df['Collection Name'].apply(lambda x: x.translate(punctuation_table) if isinstance(x, str) else x)
        
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
            # Check if the value in the column is a string
            if isinstance(row[col], str):
                # Iterate over each term in the lexicon and check for matches
                for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                    # Check if the whole term exists in the text column
                    if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                        matches.append((row['Identifier'], term, category, col))
    return matches

# Example usage
lexicon_file_path = "C:/Users/u6045253/Desktop/reparative-metadata_lexicon.csv"  # Replace with the path to your lexicon CSV file
metadata_file_path = "C:/Users/u6045253/Desktop/ehc_sample.csv"  # Replace with the path to your metadata CSV file
output_file_path = "C:/Users/u6045253/Desktop/test.csv"  # Path to the output CSV

lexicon = load_lexicon(lexicon_file_path)
metadata = load_metadata(metadata_file_path)

# Perform matching
if lexicon is not None and metadata is not None:
    matches = find_matches(lexicon, metadata)
    # Create DataFrame from matches
    matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
    # Merge matches with original metadata using left join on "Identifier"
    merged_df = pd.merge(metadata, matches_df, on="Identifier", how="left")
    # Filter out rows without matches
    merged_df = merged_df.dropna(subset=['Term'])
    # Save merged DataFrame to CSV
    merged_df.to_csv(output_file_path, index=False)

    print("Merged data saved to:", output_file_path)
