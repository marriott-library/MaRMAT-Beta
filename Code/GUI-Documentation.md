# Reparative Metadata Audit Tool: GUI Documentation
The [Reparative Metadata Audit Tool GUI ](https://github.com/kayleealexander/RMA-Tool/blob/main/Code/RMA-GUI-2.5.py) was designed using the Tkinter library in Python. This application allows users to load a lexicon and metadata file, select relevant columns and categories, and perform a search to identify problematic terms from the lexicon in the metadata. Below is the detailed breakdown of the functionalities implemented in this tool:


### 1. Class Initialization
  - Class Definition: The ReparativeMetadataAuditTool class inherits from tk.Tk.
  - Initial Setup: The __init__ method initializes the main window, frames, and widgets.
  - Variables Initialization: Variables to hold dataframes, columns, categories, and UI elements are initialized.

### 2. Main Frame UI Elements
  - Explanation Label: Provides instructions to the user.
  - Buttons:
    - Load Lexicon: To load the lexicon file.
    - Load Metadata: To load the metadata file.
    - Reset: To reset the application.
    - Next: Initially hidden, appears after loading metadata to proceed to column selection.

### 3. Methods for Loading Files
  - load_lexicon: Opens a file dialog to select and load a lexicon file (CSV/TSV). Disables the button upon successful load.
  - load_metadata: Opens a file dialog to select and load a metadata file (CSV/TSV). Enables the Next button upon successful load.

### 4. Column Selection
  - show_column_selection: Displays UI to select columns from the metadata for analysis.
  - Column Listbox: Allows multiple selections of columns. Includes a checkbox to select all columns.

### 5. Identifier Selection
  - show_identifier_selection: Displays UI to select an identifier column.
  - Identifier Dropdown: Shows a dropdown list of metadata columns to select the identifier.

### 6. Category Selection
  - show_category_selection: Displays UI to select categories from the lexicon for analysis.
  - Category Listbox: Allows multiple selections of categories. Includes a checkbox to select all categories.

### 7. Perform Matching
  - perform_matching: Matches terms from the selected lexicon categories against the selected metadata columns.
  - Multithreading: Uses threading to perform matching without freezing the UI.

### 8. Export Results
  - export_results: Exports the matching results to a CSV file chosen by the user.

### 9. Helper Methods
  - get_selected_columns: Returns the list of selected columns.
  - get_selected_categories: Returns the list of selected categories.
  - toggle_columns and toggle_categories: Toggle all selections in the listboxes.

### 10. Main Execution
  - if __name__ == "__main__": Initializes and starts the main Tkinter event loop.
