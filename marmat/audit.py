import re
import pandas as pd


class AuditTool:
    """A tool for assessing metadata and identifying matches based on a provided lexicon."""

    def __init__(self):
        """Initialize the assessment tool."""
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []  # List of all available columns in the metadata
        self.categories = []  # List of all available categories in the lexicon
        self.selected_columns = []  # List of columns selected for matching
        self.selected_categories = []  # List of categories selected for matching
        self.identifier_column = None  # Identifier column used to uniquely identify rows

    def load_lexicon(self, file_path):
        """Load the lexicon file.

        Parameters:
        file_path (str): Path to the lexicon CSV file.

        """
        try:
            self.lexicon_df = pd.read_csv(file_path, encoding='utf8')
            self.categories = self.lexicon_df["category"].unique().tolist()
            print("Lexicon loaded successfully.")
        except Exception as e:
            raise Exception(f"An error occurred while loading lexicon: {e}")

    def load_metadata(self, file_path):
        """Load the metadata file.

        Parameters:
        file_path (str): Path to the metadata CSV file.

        """
        try:
            self.metadata_df = pd.read_csv(file_path, encoding='utf8')
            self.columns = self.metadata_df.columns.to_list()
            print("Metadata loaded successfully.")
        except Exception as e:
            raise Exception(f"An error occurred while loading metadata: {e}")

    def select_columns(self, columns):
        """Select columns from the metadata for matching.

        Parameters:
        columns (list of str): List of column names in the metadata.

        """
        self.selected_columns = columns

    def select_identifier_column(self, column):
        """Select the identifier column used for uniquely identifying rows.

        Parameters:
        column (str): Name of the identifier column in the metadata.

        """
        self.identifier_column = column

    def select_categories(self, categories):
        """Select categories from the lexicon for matching.

        Parameters:
        categories (list of str): List of category names in the lexicon.

        """
        self.selected_categories = categories

    def perform_matching(self, output_file):
        """Perform matching between selected columns and categories and save results to a CSV file.

        Parameters:
        output_file (str): Path to the output CSV file to save matching results.

        """
        if not (self.metadata_df is not None and self.lexicon_df is not None):
            raise ValueError("Please load lexicon and metadata files first.")

        matches_df = self.find_matches(self.selected_columns, self.selected_categories)
        matches_df.sort_values(by=["Category", "Term"], inplace=True)

        """Write results to CSV"""
        try:
            matches_df.to_csv(output_file, index=False, encoding="utf8")
            print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"An error occurred while saving results: {e}")

    def find_matches(self, selected_columns, selected_categories):
        """Find matches between metadata and lexicon based on selected columns and categories.

        Parameters:
        selected_columns (list of str): List of column names from metadata for matching.
        selected_categories (list of str): List of category names from the lexicon for matching.

        Returns:
        list of tuple: List of tuples containing matched results (Identifier, Term, Category, Column).

        """
        lexicon_df = self.lexicon_df[self.lexicon_df['category'].isin(selected_categories)]

        count = lexicon_df.groupby(by="category", sort=False)["category"].count()
        cumsum = lexicon_df.groupby(by="category", sort=False)["category"].count().cumsum().shift(1)
        cumsum.iloc[0] = 0
        cumsum = cumsum.astype(int)

        combined_dfs = []
        for i, (term, category) in enumerate(zip(lexicon_df['term'], lexicon_df['category'])):
            print(f"Processing {category} term {i + 1 - cumsum.loc[category]} of {count.loc[category]}")
            term_col_dfs = []
            bounded_term = re.compile(rf"\b{term}\b", flags=re.IGNORECASE)  # make term a group for .split()
            for col in selected_columns:
                raw_matches = self.metadata_df[self.metadata_df[col].str.contains(term, regex=False, na=False, case=False)]
                matches = raw_matches[raw_matches[col].str.contains(bounded_term, regex=True, na=False)].copy()
                if len(matches) > 0:
                    matches.rename(columns={col: "Context"}, inplace=True)

                    # add all other cols
                    matches["Term"] = term
                    matches["Category"] = category
                    matches["Field"] = col
                    matches["Occurences"] = matches["Context"].str.count(bounded_term)

                    standard_cols = [self.identifier_column, 'Term', 'Category', 'Context', 'Field', 'Occurences']
                    term_col_dfs.append(matches.loc[:, standard_cols])

            if term_col_dfs:
                combined_dfs.append(pd.concat(term_col_dfs, axis=0))

        return pd.concat(combined_dfs, axis=0).reset_index(drop=True)
