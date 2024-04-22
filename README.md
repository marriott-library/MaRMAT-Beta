# Reparative Metadata Audit Tool

## Background

## Credits and Acknowledgments
This tool was inspired by the Duke University Libraries Description Audit Tool, developed by [Noah Huffman](https://github.com/noahgh221) at the Rubenstein Library, and expanded by [Miriam Shams-Rainey](https://github.com/mshamsrainey). See: [Description-Audit](https://github.com/duke-libraries/description-audit/tree/main). 

Code developed by [Kaylee Alexander](https://github.com/kayleealexander) in collaboration with ChatGPT 3.5, [Rachel Wittmann](https://github.com/RachelJaneWittmann), and [Anna Neatrour](https://github.com/aneatrour) at the University of Utah's J. Willard Marriot Library.

## About the Tool
At the most basic level, this Python script is designed to match terms from a lexicon with textual data and produce a CSV file containing the matched results. It utilizes the Pandas library for data manipulation and regular expressions for text processing. It was designed for librarians engaged in reparative metadata practices to assist them in idenfiying terms in their metadata that may be outdated, biased, or otherwise problematic. The code and lexicon for the tool can be accessed via the [Code](https://github.com/kayleealexander/RMA-Tool/tree/main/Code) folder of this repository; a GUI is currently under development.

An initial test case developed a tool for parsing, extracting, tokenizing, and preprocessing XML files containing Open Archives Initiative (OAI) feed metadata for library special collections that would then crosscheck tokens against Duke's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons) and append the corresponding lexicon categories (Aggrandizement, Race Euphemisms, Race Terms, Slavery Terms, Gender Terms, LGBTQ, Mental Illness, and Disability) to each row in the CSV output. This tool is accessible via the [XML Test Code](https://github.com/kayleealexander/RMA-Tool/tree/main/XML%20Test%20Code) folder of this repository, though may not work with all OAI feed formats. 

### Dependencies 
1. **Pandas**: A powerful data manipulation library for Python.
2. **String**: A standard Python library for string manipulation.
3. **Re**: A module providing support for regular expressions (regex) in Python.

### Functions 
1. **load_lexicon(file_path)**: Loads a lexicon CSV file into a Pandas DataFrame.
   - Parameters:
      - file_path: Path to the lexicon CSV file.
    - Returns:
      - lexicon_df: DataFrame containing the lexicon data.

2. **load_metadata(file_path)**: Loads a metadata CSV file into a Pandas DataFrame. Removes punctuation from specified columns in the metadata DataFrame.
   - Parameters:
     - file_path: Path to the metadata CSV file.
   - Returns:
     - metadata_df: DataFrame containing the metadata.

3. **find_matches(lexicon_df, metadata_df)**: Finds matches between terms in the lexicon and text in specified columns of the metadata.
   - Parameters:
     - lexicon_df: DataFrame containing the lexicon data.
     - metadata_df: DataFrame containing the metadata.
   - Returns:
     - matches: List of tuples (Identifier, Term, Category, Column) representing matches.

### Example Usage
1. Replace **lexicon_file_path**, **metadata_file_path**, and **output_file_path** with the paths to the locally saved [lexicon CSV file](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/reparative-metadata_lexicon.csv), your metadata CSV file, and your desired output CSV file, respectively.
2. Ensure that the specified columns in the metadata CSV file are present and accurately represent the textual data to be matched. Preformat your metadata file with the following column names:
   - **Title**
   - **Description**
   - **Subject**
   - **Collection Name**
4. Execute the script to generate the output CSV file containing the matched results.

*Note: Make sure the CSV files have the required format and structure for proper processing. Handle any exceptions related to file loading or data processing as needed.*

### The Lexicon

### Sample Data

### Using the GUI
