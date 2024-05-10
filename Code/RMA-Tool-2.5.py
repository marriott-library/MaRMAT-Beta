import pandas as pd
import re

class ReparativeMetadataAuditToolCLI:
    def __init__(self):
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []
        self.categories = []
        self.selected_columns = []
        self.identifier_column = None

    def load_lexicon(self, file_path):
        try:
            self.lexicon_df = pd.read_csv(file_path, encoding='latin1')
            print("Lexicon loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading lexicon: {e}")

    def load_metadata(self, file_path):
        try:
            self.metadata_df = pd.read_csv(file_path, encoding='latin1')
            print("Metadata loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading metadata: {e}")

    def select_columns(self, columns):
        self.selected_columns = columns

    def select_identifier_column(self, column):
        self.identifier_column = column

    def select_categories(self, categories):
        self.categories = categories

    def perform_matching(self):
        if self.lexicon_df is None or self.metadata_df is None:
            print("Please load lexicon and metadata files first.")
            return

        matches = self.find_matches(self.selected_columns, self.categories)
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        print(matches_df)

    def find_matches(self, selected_columns, selected_categories):
        matches = []
        lexicon_df = self.lexicon_df[self.lexicon_df['category'].isin(selected_categories)]
        for index, row in self.metadata_df.iterrows():
            for col in selected_columns:
                if isinstance(row[col], str):
                    for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                        if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                            matches.append((row[self.identifier_column], term, category, col))
                            break
        return matches

# Example usage:
tool = ReparativeMetadataAuditToolCLI()
tool.load_lexicon("lexicon.csv")
tool.load_metadata("metadata.csv")
tool.select_columns(["column1", "column2"])
tool.select_identifier_column("ID")
tool.select_categories(["Category1", "Category2"])
tool.perform_matching()
