# Reparative Metadata Audit Tool

The Reparative Metadata Audit Tool is a graphical application built using Tkinter in Python. This tool allows users to match terms from a problematic terms lexicon file with text data from a collections metadata file, facilitating metadata cleanup and analysis.

## Overview

The application provides the following functionalities:

- Load CSV files for both lexicon and metadata.
- Select specific columns from the metadata for analysis.
- Choose an identifier column in the metadata to relate back to the original dataset.
- Select categories of terms from the lexicon for searching.
- Perform matching to find terms in selected metadata columns and export results to a CSV file.

## Features

- **User Interface**: Utilizes Tkinter for a GUI interface.
- **File Loading**: Supports loading CSV files for lexicon and metadata.
- **Column Selection**: Allows users to choose specific columns from metadata for term analysis.
- **Identifier Selection**: Enables selection of an identifier column for linking matched terms back to the original metadata.
- **Category Selection**: Provides options to select categories of terms from the lexicon for matching.
- **Matching Process**: Performs regex-based term matching across selected metadata columns and chosen lexicon categories.
- **Output**: Exports matched data to a CSV file for further analysis or use.

## Getting Started

To use the Reparative Metadata Audit Tool, follow these steps:

1. Download the [RMA-GUI-2.52.py](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-GUI-2.52.py) file.
2. Download one of our sample lexicons in the [Code](https://github.com/kayleealexander/RMA-Tool/tree/main/Code) folder, or create your own.
3. Download the metadata you want to audit as a CSV file.
4. Open the [RMA-GUI-2.52.py](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-GUI-2.52.py) file and follow the prompts.

## Using the Tool

**1. Load Lexicon and Metadata**:
   - Follow on-screen instructions to load your lexicon and metadata CSV files using the provided buttons.

**2. Perform Analysis**:
   - Select columns from your metadata for analysis.
   - Choose an identifier column for matching results back to the original dataset.
   - Select categories of terms from the lexicon for analysis.
   - Click "Perform Matching" to find matches and export the results as a CSV file.

## Additional Notes

**Dependencies**: Ensure you have Python 3.x and the `pandas` library installed as per the installation instructions.

## Contact

For any questions or support, please contact [Kaylee Alexander](mailto:kaylee.alexander@utah.edu).
