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
        # Apply the regex pattern to each text column in metadata_df
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            # Concatenate all text columns into a single string
            text = metadata_df[col].astype(str).str.cat(sep=' ')
            # Remove punctuation
            text = remove_punctuation(text)
            # Find matches
            matches.extend([(term, category, col, identifier) for identifier in metadata_df.loc[metadata_df[col].str.contains(pattern, flags=re.IGNORECASE), 'Identifier']])
    return matches

# Example usage
lexicon_file_path = "lexicon.csv"  # Replace with the path to your lexicon file
metadata_file_path = "metadata.csv"  # Replace with the path to your metadata file

lexicon = load_lexicon(lexicon_file_path)
metadata = load_metadata(metadata_file_path)

if lexicon is not None and metadata is not None:
    print("Lexicon loaded successfully:")
    print(lexicon.head())  # Display the first few rows of the loaded lexicon
    print("Metadata loaded successfully:")
    print(metadata.head())  # Display the first few rows of the loaded metadata
    
    matches = find_matches(lexicon, metadata)
    if matches:
        print("Matches found:")
        matched_data = pd.DataFrame(matches, columns=['Matched Term', 'Category', 'Metadata Column', 'Identifier'])
        updated_metadata = pd.concat([matched_data, metadata], axis=1)
        updated_metadata.to_csv("updated_metadata.csv", index=False)
        print("Updated metadata saved to 'updated_metadata.csv'")
    else:
        print("No matches found.")
