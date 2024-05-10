# Reparative Metadata Audit Tool
The Reparative Metadata Audit Tool is a Python application designed for auditing collections metadata files against a lexicon of potentially problematic terms. A graphical user interface (GUI), built using the Tkinter library, is available for PC users. 

Code developed by [Kaylee Alexander](https://github.com/kayleealexander) in collaboration with ChatGPT 3.5, [Rachel Wittmann](https://github.com/RachelJaneWittmann), and [Anna Neatrour](https://github.com/aneatrour) at the University of Utah's J. Willard Marriot Library.

## Project Background

## About the Tool
At the most basic level, the underlying Python code is designed to match terms from a lexicon with textual data and produce a CSV file containing the matched results. It utilizes the Pandas library for data manipulation and regular expressions for text processing. It was designed primarily with librarians in mind, specifically those engaged in reparative metadata practices, to assist in idenfiying terms in their metadata that may be outdated, biased, or otherwise problematic. The underlying code (including preliminary iterations) and a recommended lexicon for using the tool can be accessed via the [Code](https://github.com/kayleealexander/RMA-Tool/tree/main/Code) folder of this repository. 

An initial test case developed a tool for parsing, extracting, tokenizing, and preprocessing XML files containing Open Archives Initiative (OAI) feed metadata for library special collections that would then crosscheck tokens against Duke University's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons) and append the corresponding lexicon categories (Aggrandizement, Race Euphemisms, Race Terms, Slavery Terms, Gender Terms, LGBTQ, Mental Illness, and Disability) to each row in the CSV output. This tool is accessible via the [XML Test Code](https://github.com/kayleealexander/RMA-Tool/tree/main/XML%20Test%20Code) folder of this repository, though may not work with all OAI feed formats. 

### About the Lexicon
The lexicon provided [here](https://github.com/kayleealexander/RMA-Tool/tree/main/Code/reparative-metadata_lexicon.csv) has been adapted from Duke University's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons), which were created for similar use cases. We modified Duke's lexicons by transposing across their category columns to create a single lexcon (term, category) that better accomodate users adding additional terms and categories without having to adjust the underlying code structure. Our lexicon additionally provides a set of outdated Library of Congress Subject Headings (categorized as "Problematic LCSH") to assist in updating metadata subject headings. 

Users may download our lexicon to use in the tool as is or add additional terms and categories based on specific project needs. The only requirements for a lexicon to work against another file are that there be two columns in the CSV file: "Term" and "Category" (case sensitive). Therefore, the tool's use is not limited to auditing metadata for problematic terms; it may also be loaded with a custom lexicon to perform matching against a variety of content types.

### Sample Data
*Coming soon*

# Reparative Metadata Audit Tool GUI for PC

## GUI Features
- Load lexicon and metadata files in CSV format.
- Select columns from the metadata file for analysis.
- Choose the column in the metadata file to be rewritten as the "Identifier" column so that the output can be reconciled with the original metadata file.
- Select categories of terms from the lexicon for analysis.
- Perform matching to find matches between selected columns and categories.
- Export results to a CSV file.

*Note: This GUI is not compatible with MacOS*

## Usage 
1. Loading Files:
   - Click on the "Load Lexicon" button to load the lexicon file.
   - Click on the "Load Metadata" button to load the metadata file.
     
2. Selecting Columns:
   - After loading files, click "Next" to proceed to column selection.
   - Select the columns from the metadata file that you want to analyze.
     
3. Selecting Identifier Column:
   - After selecting columns, choose the column in the metadata file that will serve as the "Identifier" column.

4. Selecting Categories:
   - Next, choose the categories of terms from the lexicon that you want to search for.

5. Performing Matching:
   - Click "Perform Matching" to find matches between selected columns and categories.
   - The results will be exported to a CSV file.

6. Resetting:
   - Use the "Reset" button to clear file selections and start over.
  
## Dependencies
- Python 3.x: Python is a widely used high-level programming language for general-purpose programming. Documentation

- Tkinter: Tkinter is Python's standard GUI (Graphical User Interface) package. It is used to create desktop applications with a graphical interface. Documentation

*Note: These dependencies are essential for running the Reparative Metadata Audit Tool. If you don't have Python installed, you can download it from the official Python website. Tkinter is usually included with Python distributions, so no separate installation is required.*

## Installation 
No installation is required. Simply run the Python script reparative_metadata_audit_tool.py to start the application on your PC.

# Credits and Acknowledgments
This tool was inspired by the Duke University Libraries Description Audit Tool, developed by [Noah Huffman](https://github.com/noahgh221) at the Rubenstein Library, and expanded by [Miriam Shams-Rainey](https://github.com/mshamsrainey). See: [Description-Audit](https://github.com/duke-libraries/description-audit/tree/main). 
