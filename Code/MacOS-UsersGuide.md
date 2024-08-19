## Comprehensive Guide for Running MaRMAT in Terminal on a Mac

### Prerequisites

1. **Python Installation**: Ensure Python is installed by running the following in Terminal:
   ```bash
   python3 --version
   ```
   If Python is not installed, download it from the [official Python website](https://www.python.org/downloads/).

2. **Library Requirements**:
   - **Pandas**: Install the `pandas` library:
     ```bash
     pip3 install pandas
     ```
   - **Regular Expression (`re`) Module**: This module is part of Python’s standard library. Confirm its availability:
     ```bash
     python3 -c "import re; print('re module is available')"
     ```

### Step-by-Step Instructions

#### 1. **Save the Script**
   - Ensure the [MaRMAT-CommandLine-2.5.py](https://github.com/marriott-library/MaRMAT/blob/main/Code/MaRMAT-CommandLine-2.5.py) script is saved on your Mac.
   - Add the lexicon (e.g., [Reparative Metadata](https://github.com/marriott-library/MaRMAT/blob/main/Code/reparative-metadata-lexicon.csv), [LCSH](https://github.com/marriott-library/MaRMAT/blob/main/Code/LCSH-lexicon.csv)) you'd like to use as well as the metadata file you want to analyze to the same folder. 

#### 2. **Opening the Script for Editing with TextEdit**

   1. **Locate the Script**:
      - Open Finder and navigate to the directory where the script is saved (e.g., `Documents`, `Downloads`.

   2. **Open with TextEdit**:
      - Right-click on the script file (`MaRMAT-CommandLine-2.5.py`) and select **Open With > TextEdit**.
      - If you don’t see TextEdit, choose **Other...** and select TextEdit (or another text editor) from the list.

   3. **Edit the Script**:
      - In TextEdit, find and modify the following sections (at the very end of the script under "Example usage") according to your specific file paths and requirements:

        - **Load Lexicon**:
          ```python
          tool.load_lexicon("/path/to/your/lexicon.csv")  # Replace with the path to your lexicon CSV file.
          ```

        - **Load Metadata**:
          ```python
          tool.load_metadata("/path/to/your/metadata.csv")  # Replace with the path to your metadata CSV file.
          ```

        - **Select Columns for Matching**:
          ```python
          tool.select_columns(["Column1", "Column2"])  # Replace with the metadata column names you want to analyze.
          ```

        - **Select Identifier Column**:
          ```python
          tool.select_identifier_column("Identifier")  # Replace with the name of your identifier column (e.g., a record ID number).
          ```

        - **Select Categories for Matching**:
          ```python
          tool.select_categories(["RaceTerms"])  # Replace with the categories from the lexicon that you want to search for.
          ```

        - **Perform Matching and View Results**:
          ```python
          tool.perform_matching("/path/to/your/output.csv")  # Replace with the path to your output file.
          ```

      - Save your changes by clicking **File > Save** or pressing `Command + S`.

   4. **Ensure Proper TextEdit Settings**:
      - If TextEdit opens the file in **Rich Text Format (RTF)**, change it to **Plain Text** by selecting **Format > Make Plain Text** from the menu. This ensures the script runs correctly.

#### 3. **Running the Script**

   1. **Open Terminal**:
   
   2. **Navigate to the Script’s Directory**:
      - Use the `cd` command to go to the directory where your script is located, for example:
        ```bash
        cd ~/Documents
        ```
   
   3. **Execute the Script**:
      - Run the script using the following command:
        ```bash
        python3 MaRMAT-CommandLine-2.5.py
        ```

### Additional Considerations

- **Full Paths**: Always use the full path for files if they are not in the same directory as the script.
- **Output Files**: Ensure the output directory specified in the script has the appropriate permissions to save the results.
