from marmat.audit import AuditTool

# Main program for command line interaction
if __name__ == "__main__":
    print("1. Initialize the tool:")
    tool = AuditTool()

    print("\n2. Load lexicon and metadata files:")
    lexicon_path = input("Enter the path to the lexicon CSV file: ")
    tool.load_lexicon(lexicon_path)
    
    metadata_path = input("Enter the path to the metadata CSV file: ")
    tool.load_metadata(metadata_path)

    print("\n3. Select columns for matching:")
    columns = input("Enter the column names for matching, separated by commas: ").split(",")
    tool.select_columns([col.strip() for col in columns])  # Strip whitespace

    print("\n4. Select the identifier column:")
    identifier = input("Enter the name of the identifier column: ")
    tool.select_identifier_column(identifier)

    print("\n5. Select categories for matching:")
    categories = input("Enter the categories from the lexicon for matching, separated by commas: ").split(",")
    tool.select_categories([cat.strip() for cat in categories])  # Strip whitespace

    print("\n6. Perform matching and view results:")
    output_file = input("Enter the path to save the output CSV file: ")
    tool.perform_matching(output_file)
