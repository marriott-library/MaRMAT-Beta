# Marriott Reparative Metadata Assessment Tool (MaRMAT) - Beta
The Marriott Reparative Metadata Assessment Tool (MaRMAT) is a Python application designed for auditing collections metadata files against a lexicon of potentially problematic terms. The tool's design facilitates an easy-to-follow process for assessing metadata using a lexicon of terms. For PC user's, we provide a graphical interface for file loading, column selection, and term matching, making it user-friendly for those with limited programming experience. The tool can also be run in your command line. 

Note: Whether you are using the GUI for Windows or the command-line tool for MacOS, you will need to have [Python](https://docs.python.org/3/) and the `pandas` library for Python installed on your machine. Installation instructions for `pandas` are provided below in the respective **Dependencies** sections for the GUI and command-line tool.

We value your feedback! Please take [this survey](https://docs.google.com/forms/d/e/1FAIpQLSfaABD5qsU2trEjrDWs3MoytgiNCaD08GJvRWzqhgzv5GjoDg/viewform?usp=sf_link) to tell us about your experience using MaRMAT.

UPDATE: We are anticipating a MaRMAT upgrade in June 2025 which will expand GUI usablity to MacOS and PC users, in addition to many feature and functionality improvments. 

## **Table of Contents**
1. [Project Background](#1-project-background)

   1.1 [About the Tool](#11-about-the-tool)
   
   1.2 [The Lexicons](#12-the-lexicons)

   1.3 [Features](#13-features)

   1.4 [Example Outputs and Tutorial](#14-example-outputs-and-tutorial)

2. [The GUI for Windows Users](#2-the-gui-for-windows-users)

   2.1 [Usage](#21-usage)

   2.2 [Dependencies](#22-dependencies)

   2.3 [Installation](#23-installation)

   2.4 [Troubleshooting](#24-troubleshooting)

3. [The Command-Line Tool](#3-the-command-line-tool)

   3.1 [Usage](#31-usage)

   3.2 [Dependencies](#32-dependencies)

   3.3 [Notes](#33-notes)

4. [Credits and Acknowledgments](#4-credits-and-acknowledgments)
5. [User Feedback Survey](#5-user-feedback-survey)

## 1. Project Background
Identifying potentially harmful language, problematic and outdated Library of Congress Subject Headings, is one step towards reparative metadata practices. Deciding what and how to change this metadata, however, is up to metadata practitioners and involves awareness, education, and sensitivity for the communities and history reflected in digital collections. The [Digital Library Federation’s Inclusive Metadata Toolkit, created by the Digital Library Federation’s Cultural Assessment Working Group](https://osf.io/2nmpc/), provides resources to educate and assist in reparative metadata decision-making.  

The Marriot Reparative Metadata Assessment Tool (MaRMAT) is based [Duke University’s Description Audit Tool](https://github.com/duke-libraries/description-audit). It is intended to assist digital collections metadata practitioners in bulk analysis of metadata collections to identify potentially harmful language in description and facilitate repairing metadata to reflect current and preferred terminology. While Duke University's Description Audit Tool was created to analyze MARC XML and EAD finding aid metadata, MaRMAT was developed to analyze metadata in a spreadsheet format, allowing for assessment of Dublin Core metadata and other schemas due to only requiring key column-header names. In addition, the script has been altered to provide more custom querying capabilities.

## 1.1 About the Tool
At the most basic level, [MaRMAT](https://github.com/marriott-library/MaRMAT/blob/main/Code/MaRMAT-GUI-2.5.3.py) is designed to match terms from a lexicon with textual data and produce a CSV file containing the matched results. It utilizes the Pandas library for data manipulation and regular expressions for text processing. It was designed primarily with librarians in mind, specifically those engaged in reparative metadata practices, to assist in idenfiying terms in their metadata that may be outdated, biased, or otherwise problematic. The underlying code (including preliminary iterations) and sample lexicons for using the tool can be accessed via the [Code](https://github.com/marriott-library/MaRMAT/tree/main/Code) folder of this repository. For additional information about the GUI, see [GUI-Documentation](https://github.com/marriott-library/MaRMAT/blob/main/Code/GUI-Documentation.md). 

### 1.2 The Lexicons
There are two lexicons provided to help begin your reparative metadata assessment. Not all of the terms in these lexicons may need remediation, rather, they may signal areas of your collections that should be reiveiwed carefully. Users may download the provided lexicons to use in MaRMAT as is, remove terms that may not be problematic in your metadata, or add additional terms and categories based on specific project needs. The only requirements for a lexicon to work against another file are that there be two columns in the CSV file: "Term" and "Category" (case sensitive). Therefore, the tool's use is not limited to assessing metadata for problematic terms; it may also be loaded with a custom lexicon to perform matching against a variety of content types.

| Lexicon      | Description |
| :----------:| ---------- |
| Reparative Metadata Lexicon   | The [Reparative Metadata Lexicon](https://github.com/marriott-library/MaRMAT/blob/main/Code/lexicon-reparative-metadata.csv) includes potentially harmful terminology organized by category and is best suited for uncontrolled metadata fields (i.e. Title, Description). This lexicon has been adapted from Duke University's lexicons, which were created for similar use cases. For the Marriott Reparative Metadata Assessment Tool (MaRMAT),  Duke's [lexicons](https://github.com/duke-libraries/description-audit/tree/main/lexicons) were modified  by transposing across their category columns to create a single lexicon (term, category) that better accommodate users adding additional terms and categories without having to adjust the underlying code structure.  |
| Library of Congress Subject Heading (LCSH) Lexicon   | The [LCSH Lexicon](https://github.com/marriott-library/MaRMAT/blob/main/Code/lexicon-LCSH.csv) includes selected changed and canceled LCSH (mostly from 2023) and headings that have been identified as problematic. The LCSH Lexicon is best suited to run against the Subject metadata field, or other fields that contain LCSH terms

### 1.3 Features
- Load lexicon and metadata files in CSV format.
- Select columns from the metadata file for analysis.
- Choose the column in the metadata file to be rewritten as the "Identifier" column so that the output can be reconciled with the original metadata file.
- Select categories of terms from the lexicon for analysis.
- Perform matching to find matches between selected columns and categories.
- Export results to a CSV file.

### 1.4 Example Outputs and Tutorial

To provide users with a sense of what to expect from running MaRMAT against their own metadata collection, below includes example metadata to load and query against the provided lexicons, and outputs from the the provided lexicons: 
1. [Example Input: Potentially Problematic Metadata](https://github.com/marriott-library/MaRMAT/blob/main/Code/example-input-metadata.csv)
2. [Example Output: Reparative Metadata Lexicon](https://github.com/marriott-library/MaRMAT/blob/main/Code/example-output-reparative-metadata-lexicon.csv)
3. [Example Output: LCSH Lexicon](https://github.com/marriott-library/MaRMAT/blob/main/Code/example-output-lcsh-subject-lexicon.csv)

Please keep in mind these reports are just snippets of larger reports. Users should be aware that there may be false positives or results that may not need remediation. For example, the LCSH term "Race" is considered a problem heading but MaRMAT may flag other headings with "race," as in "Bonneville Salt Flats Race, Utah." Likewise, the gender term "wife" may not always signal an unnamed woman, and terms that may be harmful in some contexts may not be in others. Therefore, we stress the importance of human review and intervention prior to making broad conclusions or global changes based on MaRMAT outputs.

To assist in getting started with MaRMAT, there is also a [video tutorial](https://youtu.be/uspAoqfj99g?si=jQArVdlbGm_qN78l) that demonstrates the first steps in using the GUI for Windows (subtitles can be enabled in settings). The Mac OS demonstration is also available [on video](https://youtu.be/j_fFplU1W_o), please note audio for this demo will be coming soon.  

## 2. The GUI for Windows Users
To facilitate wider use, the [MaRMAT GUI](https://github.com/marriott-library/MaRMAT/blob/main/Code/MaRMAT-GUI-2.5.3.py) allows users to easily load a lexicon and a metadata file, select a key column (i.e., Identifier) to use in reconciling matches, and choose the columns and categories they'd like to perform matching on. 

*Note: The GUI is not compatible with MacOS. Additional information on the MaRMAT GUI is available [here](https://github.com/marriott-library/MaRMAT/blob/main/Code/GUI-Documentation.md).

### 2.1 Usage 
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
  
### 2.2 Dependencies
- **[Python 3.x](https://docs.python.org/3/)**: Python is a widely used high-level programming language for general-purpose programming.

- **[Tkinter](https://docs.python.org/3/library/tk.html)**: Tkinter is Python's standard GUI (Graphical User Interface) package. It is used to create desktop applications with a graphical interface. It is usually included with Python distributions, so no separate installation is required.

- **[re](https://docs.python.org/3/library/re.html)**: This module provides regular expression matching operations. It's a built-in module in Python and doesn't require separate installation.

- **[pandas](https://pandas.pydata.org/docs/)**: Pandas is a Python library that provides easy-to-use data structures and data analysis tools for manipulating and analyzing structured data, particularly tabular data. Pandas can be installed using pip in your command line interface: ``py -m pip install pandas``

*Note: These dependencies are essential for running MaRMAT. If you don't have Python installed, you can download it from the [official Python website](https://www.python.org/downloads).*

### 2.3 Installation 
No installation is required. Simply follow the steps below to download and run the Python script to start the application on your PC.

1. Download the Python Script:
   - Download the [MaRMAT-GUI-2.5.3.py](https://github.com/marriott-library/MaRMAT/blob/main/Code/MaRMAT-GUI-2.5.3.py) script to a location on your PC where you can easily find it, such as your Desktop or Downloads.

2. Ensure Python is Installed:
   - To make sure that Python is installed on your PC, search for "Python" in your Start Menu or look for the Python folder in your Program Files.
   - If Python is not installed, you can download and install it from the official [Python website](https://www.python.org/downloads).

3. Double-Click the Python Script:
   - Navigate to the location where you downloaded the script.
   - Double-click on the script file (i.e., MaRMAT-GUI-2.5.3.py).

4. Application Starts:
   - The application should start running automatically; the GUI will appear on your screen.
  
### 2.4 Troubleshooting
The GUI should automacially open when you open the Python code file. If you are having issues with the GUI opening, try opening the file in Python IDLE and running it. IDLE should give ou an error message with insights as to why it is not loading correctly. If you are receiving error messages pyrelated to ``pandas``, such as ``No module named 'pandas'``, follow these steps to install ``pandas``. 

1. Open your command line interface

2. Type the following into command line: ``py -m pip install pandas``

3. Press enter to run the command

If this process does not resolve your issue, follow these Getting Started tips to make sure python and the pip installer are running correctly on your PC: [https://pip.pypa.io/en/stable/getting-started](https://pip.pypa.io/en/stable/getting-started/)

## 3. The Command-Line Tool 
The [MaRMAT](https://github.com/marriott-library/MaRMAT/blob/main/Code/MaRMAT-CommandLine-2.6.py) can be run by any user from their command line.

### 3.1 Usage
1. Install Python if not already installed (Python 3.x recommended).
   
2. Clone or download the MaRMAT repository.

3. Use the command-line interface to navigate to the directory where you saved the files (e.g., `Downloads`, `Desktop`). For example, run `cd Downloads` to change your directory to your `Downloads` folder.

5. Run the tool in your command line using the following command: ```python3 MaRMAT-CommandLine-2.6.py```

6. Follow the prompts in your command line to provide the paths to the lexicon and metadata files.

7. Follow the prompts to input the names of the columns you want to analyze in the metadata file, the name of the column that should be used as the identifier or key column, and the categories of terms from the lexicon that you want to search for in your metadata file. Note: inputs are case sensitive.
   
8. Follow the prompt to provide the path you would like to save your output to. 

9. Review the matching results displayed on the console or in the generated CSV file.

*Note: Demonstration video coming soon*

### 3.2 Dependencies

- **[Python 3.x](https://docs.python.org/3/)**: Python is a widely used high-level programming language for general-purpose programming.

- **[pandas](https://pandas.pydata.org/docs/)**: Pandas is a Python library that provides easy-to-use data structures and data analysis tools for manipulating and analyzing structured data, particularly tabular data. Pandas can be installed using pip in Terminal: `pip install pandas`

- **[re](https://docs.python.org/3/library/re.html)**: This module provides regular expression matching operations. It's a built-in module in Python and doesn't require separate installation.

*Note: These dependencies are necessary to run the provided code successfully. Ensure that you have them installed before running the code.*

### 3.3 Notes
- Ensure that both the lexicon and metadata files are in CSV format.
- The lexicon file should contain columns for terms and their corresponding categories ("Terms","Category").
- The metadata file should contain the text data to be analyzed, with each row representing a separate entry.
- The metadata file should contain a column, such as a Record ID, that you can use as an "Identifier" to reconcile the tool's output with your original metadata. 
- The tool outputs matching results to a CSV file named "matching_results.csv" in the tool's directory.

## 4. Credits and Acknowledgments
Code developed by [Kaylee Alexander](https://github.com/kayleealexander) in collaboration with ChatGPT 3.5, [Rachel Wittmann](https://github.com/RachelJaneWittmann), and [Anna Neatrour](https://github.com/aneatrour) at the University of Utah's J. Willard Marriott Library. MaRMAT Beta was released in July, 2024.

This tool was inspired by the Duke University Libraries Description Audit Tool, developed by [Noah Huffman](https://github.com/noahgh221) at the Rubenstein Library, and expanded by [Miriam Shams-Rainey](https://github.com/mshamsrainey) (see [Description-Audit](https://github.com/duke-libraries/description-audit/tree/main)). 

## 5. User Feedback Survey
After using MaRMAT, please take [this suvery](https://docs.google.com/forms/d/e/1FAIpQLSfaABD5qsU2trEjrDWs3MoytgiNCaD08GJvRWzqhgzv5GjoDg/viewform?usp=sf_link) and tell us about your exeprience using MARMAT. We appreciate your feedback!
