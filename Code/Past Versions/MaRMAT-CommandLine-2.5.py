from MaRMAT import MaRMAT

# Define output file path
output_file = "matches.csv" # Input the file path where you want to save your matches here.

# Example usage:
print("1. Initialize the tool:")
tool = MaRMAT()

print("\n2. Load lexicon and metadata files:")
tool.load_lexicon("lexicon.csv")  # Input the path to your lexicon CSV file.
tool.load_metadata("metadata.csv")  # Input the path to your metadata CSV file.

print("\n3. Select columns for matching:")
tool.select_columns(["Column1", "Column2"])  # Input the name(s) of the metadata column(s) you want to analyze.

print("\n4. Select the identifier column:")
tool.select_identifier_column("Identifier")  # Input the name of your identifier column (e.g., a record ID number).

print("\n5. Select categories for matching:")
tool.select_categories(["RaceTerms"])  # Input the categories from the lexicon that you want to search for.

print("\n6. Perform matching and view results:")
tool.perform_matching(output_file) 
