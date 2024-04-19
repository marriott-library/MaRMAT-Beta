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
    for index, row in metadata_df.iterrows():
        for col in ['Title', 'Description', 'Subject', 'Collection Name']:
            text = remove_punctuation(row[col])
            for term in lexicon_df['term']:
                pattern = r'\b' + re.escape(term) + r'\b'  # Match the whole word
                if re.search(pattern, text, flags=re.IGNORECASE):
                    matches.append((term, lexicon_df[lexicon_df['term'] == term]['category'].iloc[0], col, row['Identifier']))
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
        updated_metadata = pd.concat([metadata] * len(matched_data), ignore_index=True)
        updated_metadata[['Matched Term', 'Category', 'Metadata Column', 'Identifier']] = matched_data
        updated_metadata.to_csv("updated_metadata.csv", index=False)
        print("Updated metadata saved to 'updated_metadata.csv'")
    else:
        print("No matches found.")
