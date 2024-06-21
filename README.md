# Reparative Metadata Audit (RMA) Tool
The Reparative Metadata Audit (RMA) Tool is a Python application designed for auditing collections metadata files against a lexicon of potentially problematic terms. The tool's design facilitates an easy-to-follow process for auditing metadata using a lexicon of problematic terms. For PC user's, we provide a graphical interface for file loading, column selection, and term matching, making it user-friendly for those with limited programming experience. The tool can also be run in your command line. 

Code developed by [Kaylee Alexander](https://github.com/kayleealexander) in collaboration with ChatGPT 3.5, [Rachel Wittmann](https://github.com/RachelJaneWittmann), and [Anna Neatrour](https://github.com/aneatrour) at the University of Utah's J. Willard Marriot Library.

## **Table of Contents**
1. [Project Background](#1-project-background)

   1.1 [About the Tool](#11-about-the-tool)
   
   1.2 [The Lexicons](#12-the-lexicons)

   1.3 [Features](#13-features)

   1.4 [Sample Data](#14-sample-data)

2. [The Command-Line Tool](#2-the-command-line-tool)

   2.1 [Usage](#21-usage)

   2.2 [Dependencies](#22-dependencies)

   2.3 [Notes](#23-notes)

3. [The GUI for PC Users](#3-the-gui-for-pc-users)

   3.1 [Usage](#31-usage)

   3.2 [Dependencies](#32-dependencies)

   3.3 [Installation](#33-installation)

4. [Credits and Acknowledgments](#4-credits-and-acknowledgments)

## 1. Project Background
*Coming soon*

## 1.1 About the Tool
At the most basic level, the [RMA Tool](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-GUI-2.52.py) is designed to match terms from a lexicon with textual data and produce a CSV file containing the matched results. It utilizes the Pandas library for data manipulation and regular expressions for text processing. It was designed primarily with librarians in mind, specifically those engaged in reparative metadata practices, to assist in idenfiying terms in their metadata that may be outdated, biased, or otherwise problematic. The underlying code (including preliminary iterations) and sample lexicons for using the tool can be accessed via the [Code](https://github.com/kayleealexander/RMA-Tool/tree/main/Code) folder of this repository. For additional information about the GUI, see [GUI-Documentation](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/GUI-Documentation.md). 

An initial test case developed a tool for parsing, extracting, tokenizing, and preprocessing XML files containing Open Archives Initiative (OAI) feed metadata for library special collections that would then crosscheck tokens against Duke University's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons) and append the corresponding lexicon categories (Aggrandizement, Race Euphemisms, Race Terms, Slavery Terms, Gender Terms, LGBTQ, Mental Illness, and Disability) to each row in the CSV output. This tool is accessible via the [XML Test Code](https://github.com/kayleealexander/RMA-Tool/tree/main/XML%20Test%20Code) folder of this repository, please note that this may not work with all OAI feed formats or take into account resumption tokens.

### 1.2 The Lexicons
There are a few lexicons provided to help begin your reparative metadata assessment. Not all of the terms in these lexicons may need remediation, rather, they may signal areas of your collections that should be reiveiwed carefully. Users may download the provided lexicons to use in the MRMAT tool as is, remove terms that may not be problematic in your metadata, or add additional terms and categories based on specific project needs. The only requirements for a lexicon to work against another file are that there be two columns in the CSV file: "Term" and "Category" (case sensitive). Therefore, the tool's use is not limited to auditing metadata for problematic terms; it may also be loaded with a custom lexicon to perform matching against a variety of content types.

| Lexicon      | Description |
| :----------:| ---------- |
| Reparative Metadata Lexicon   | The [Reparative Metadata Lexicon](https://github.com/kayleealexander/RMA-Tool/tree/main/Code/reparative-metadata_lexicon.csv) includes potentially harmful terminology organized by category and is best suited for uncontrolled metadata fields (i.e. Title, Description). This lexicon has been adapted from Duke University's lexicons, which were created for similar use cases. For the Marriott Reparative Metadata Assessment Tool,  Duke's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons) were modified  by transposing across their category columns to create a single lexicon (term, category) that better accommodate users adding additional terms and categories without having to adjust the underlying code structure.  |
| Library of Congress Subject Heading Lexicon   | The [Library of Congress Subject Heading Lexicon](https://github.com/kayleealexander/RMA-Tool/tree/main/Code/LCSH-lexicon.csv) includes changed and canceled Library of Congress Subject Headings (mostly from 2023) and headings that have been identified as problematic. The LCSH-lexicon is best suited to run against the Subject field, or other fields that contain LCSH terms  |

### 1.3 Features
- Load lexicon and metadata files in CSV format.
- Select columns from the metadata file for analysis.
- Choose the column in the metadata file to be rewritten as the "Identifier" column so that the output can be reconciled with the original metadata file.
- Select categories of terms from the lexicon for analysis.
- Perform matching to find matches between selected columns and categories.
- Export results to a CSV file.

### 1.4 Sample Data
*Coming soon*

## 2. The Command-Line Tool 
The [RMA Tool](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-Tool-2.5.py) can be run by any user from their command line. Where indicated in the script, provide the paths to each file, specify the columns you wish to analyze, designate your "Identifier" column, and input the categories of terms you want to match. Then, run the Python file from your command line. 

### 2.1 Usage
1. Install Python if not already installed (Python 3.x recommended).
   
2. Clone or download the Reparative Metadata Audit Tool repository.

3. Navigate to the tool's directory in the command-line interface.
   
4. Update the paths to your lexicon and metadata files in the reparative_metadata_audit.py script. 

6. Run the tool using the following command: ```python RMA-Tool-2.5.py```

8. Follow the on-screen prompts to input the columns and categories:
   - Enter the names of the columns you want to analyze, separated by commas (e.g., "column1,column2").
   - Enter the name of the identifier column (e.g., the name of a column used as a record ID)
   - Enter the categories of terms you want to search for, separated by commas (e.g., "Category1,Category2").

9. Review the matching results displayed on the console or in the generated CSV file.

### 2.2 Dependencies

- **[Python 3.x](https://docs.python.org/3/)**: Python is a widely used high-level programming language for general-purpose programming.
- **[pandas](https://pandas.pydata.org/docs/)**: Pandas is a Python library that provides easy-to-use data structures and data analysis tools for manipulating and analyzing structured data, particularly tabular data. Pandas can be installed via pip:
     ``pip install pandas``
- **[re](https://docs.python.org/3/library/re.html)**: This module provides regular expression matching operations. It's a built-in module in Python and doesn't require separate installation.

*Note: These dependencies are necessary to run the provided code successfully. Ensure that you have them installed before running the code.*

### 2.3 Notes
- Ensure that both the lexicon and metadata files are in CSV format.
- The lexicon file should contain columns for terms and their corresponding categories ("Terms","Category").
- The metadata file should contain the text data to be analyzed, with each row representing a separate entry.
- The metadata file should contain a column, such as a Record ID, that you can use as an "Identifier" to reconcile the tool's output with your original metadata. 
- The tool outputs matching results to a CSV file named "matching_results.csv" in the tool's directory.

## 3. The GUI for PC Users
To facilitate wider use, our [Reparative Metadata Audit GUI](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-GUI-2.5.py) allows users to easily load a lexicon and a metadata file, select a key column (i.e., Identifier) to use in reconciling matches, and choose the columns and categories they'd like to perform matching on. 

*Note: The GUI is not compatible with MacOS. Additional information on the RMA GUI is available [here](https://github.com/kayleealexander/RMA-Tool/blob/main/GUI-Documentation.md).

### 3.1 Usage 
1. Loading Files:
   - Click on the "Load Lexicon" button to load the lexicon file.
   - Click on the "Load Metadata" button to load the metadata file.
     
2. Selecting Columns:
   - After loading files, click "Next" to proceed to column selection.
   - Select the columns from the metadata file that you want to analyze.
     
3. Selecting Identifier Column:
   - After selecting columns, choose the column in the metadata file that will serve as the key column or "Identifier" column, such as a record ID. 

4. Selecting Categories:
   - Next, choose the categories of terms from the lexicon that you want to search for.

5. Performing Matching:
   - Click "Perform Matching" to find matches between selected columns and categories.
   - The results will be exported to a CSV file.
  
### 3.2 Dependencies
- **[Python 3.x](https://docs.python.org/3/)**: Python is a widely used high-level programming language for general-purpose programming.

- **[Tkinter](https://docs.python.org/3/library/tk.html)**: Tkinter is Python's standard GUI (Graphical User Interface) package. It is used to create desktop applications with a graphical interface.

*Note: These dependencies are essential for running the Reparative Metadata Audit Tool. If you don't have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/). Tkinter is usually included with Python distributions, so no separate installation is required.*

### 3.3 Installation 
No installation is required. Simply download and run the Python script to start the application on your PC.

## 4. Credits and Acknowledgments
This tool was inspired by the Duke University Libraries Description Audit Tool, developed by [Noah Huffman](https://github.com/noahgh221) at the Rubenstein Library, and expanded by [Miriam Shams-Rainey](https://github.com/mshamsrainey) (see [Description-Audit](https://github.com/duke-libraries/description-audit/tree/main)). 
