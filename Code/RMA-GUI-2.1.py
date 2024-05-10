import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import string
import re

class ReparativeMetadataAuditTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reparative Metadata Audit Tool")
        
        # Initialize variables
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []
        self.categories = []
        self.selected_columns = []  # Store selected columns as an attribute
        self.category_selection_page_active = False  # Track whether category selection page is active
        self.identifier_column = None  # Store selected identifier column
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        
        # Load lexicon button
        self.load_lexicon_button = ttk.Button(self.main_frame, text="Load Lexicon", command=self.load_lexicon)
        self.load_lexicon_button.pack(pady=10, padx=20, side="left")
        
        # Load metadata button
        self.load_metadata_button = ttk.Button(self.main_frame, text="Load Metadata", command=self.load_metadata)
        self.load_metadata_button.pack(pady=10, padx=20, side="left")
        
        # Reset button
        self.reset_button = ttk.Button(self.main_frame, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10, padx=20, side="left")
        
        # Next button
        self.next_button = ttk.Button(self.main_frame, text="Next", command=self.show_column_selection)
        self.next_button.pack(pady=10)
        
        # Hide next button initially
        self.next_button.pack_forget()
        
        # Second screen frame (Column selection)
        self.column_selection_frame = ttk.Frame(self)
        
        # Column selection label
        self.column_label = ttk.Label(self.column_selection_frame, text="Select Columns to Analyze:")
        self.column_label.pack(pady=5)
        
        # Columns listbox
        self.column_listbox = tk.Listbox(self.column_selection_frame, selectmode='multiple')
        self.column_listbox.pack(pady=5)
        
        # All columns checkbox
        self.all_columns_var = tk.BooleanVar(value=False)
        self.all_columns_checkbox = ttk.Checkbutton(self.column_selection_frame, text="All", variable=self.all_columns_var, command=self.toggle_columns)
        self.all_columns_checkbox.pack(pady=5)
        
        # Next button for column selection
        self.next_button_columns = ttk.Button(self.column_selection_frame, text="Next", command=self.show_category_selection)
        self.next_button_columns.pack(pady=10)
        
        # Back button for column selection
        self.back_button_columns = ttk.Button(self.column_selection_frame, text="Back", command=self.show_main_frame)
        self.back_button_columns.pack(pady=10)
        
        # Second screen frame (Category selection)
        self.category_selection_frame = ttk.Frame(self)
        
        # Initialize match button
        self.match_button = ttk.Button(self.category_selection_frame, text="Perform Matching", command=self.perform_matching)
        
        # Select identifier column label
        self.identifier_label = ttk.Label(self.category_selection_frame, text="Select Identifier Column:")
        self.identifier_label.pack(pady=5)
        
        # Identifier column dropdown
        self.identifier_var = tk.StringVar()
        self.identifier_dropdown = ttk.Combobox(self.category_selection_frame, textvariable=self.identifier_var, state='readonly')
        self.identifier_dropdown.pack(pady=5)
        
        # Hide match button and identifier selection initially
        self.match_button.pack_forget()
        self.identifier_label.pack_forget()
        self.identifier_dropdown.pack_forget()
        
        # Hide second screen frames initially
        self.column_selection_frame.pack_forget()
        self.category_selection_frame.pack_forget()
        
        # Explanation text
        self.explanation_text = """
        Welcome to the Reparative Metadata Audit Tool!
        
        This tool allows you to match terms from a lexicon file with text data from a metadata file.
        
        Please follow the steps below:
        
        1. Load your lexicon and metadata files using the provided buttons.
        
        2. On the next screen, select the columns from your metadata file that you want to analyze.
        
        3. After selecting columns, choose the categories of terms you want to match from the lexicon.
        
        4. Finally, select the column in your metadata file that you want to rewrite as the Identifier column.
        
        5. Click "Perform Matching" to find matches and save the results to a CSV file.
        
        Let's get started!
        """
        
        self.explanation_label = ttk.Label(self.main_frame, text=self.explanation_text, justify='left')
        self.explanation_label.pack(padx=20, pady=20)
    
    def load_lexicon(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.lexicon_df = pd.read_csv(file_path, encoding='latin1')
                messagebox.showinfo("Success", "Lexicon loaded successfully.")
                self.load_lexicon_button.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading lexicon: {e}")
    
    def load_metadata(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.metadata_df = pd.read_csv(file_path, encoding='latin1')
                messagebox.showinfo("Success", "Metadata loaded successfully.")
                self.load_metadata_button.config(state='disabled')
                self.next_button.pack()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading metadata: {e}")
    
    def show_column_selection(self):
        if self.lexicon_df is None or self.metadata_df is None:
            messagebox.showwarning("Warning", "Please load lexicon and metadata files first.")
            return
        
        # Populate columns listbox
        self.columns = self.metadata_df.columns.tolist()
        for column in self.columns:
            self.column_listbox.insert(tk.END, column)
        
        # Show column selection frame
        self.main_frame.pack_forget()
        self.column_selection_frame.pack(fill='both', expand=True)
    
    def show_category_selection(self):
        # Get selected columns
        self.selected_columns = self.get_selected_columns()  # Store selected columns
        if not self.selected_columns:
            messagebox.showwarning("Warning", "Please select at least one column.")
            return
        
        # Clear previous selections
        self.categories.clear()
        if hasattr(self, 'category_listbox'):
            self.category_listbox.destroy()  # Destroy previous listbox if exists
        self.category_listbox = tk.Listbox(self.category_selection_frame, selectmode='multiple')
        self.category_listbox.pack(pady=5)
        
        # Populate categories listbox
        self.categories = self.lexicon_df['category'].unique().tolist()
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)
        
        # Show category selection frame
        self.column_selection_frame.pack_forget()
        self.match_button.pack_forget()  # Hide matching button if it's already displayed
        self.identifier_label.pack(pady=5)
        self.identifier_dropdown['values'] = self.columns  # Update dropdown with all columns
        self.identifier_dropdown.current(0)  # Select first column by default
        self.identifier_dropdown.pack(pady=5)
        self.category_selection_frame.pack(fill='both', expand=True)
        self.category_selection_page_active = True  # Set category selection page as active
        self.match_button.pack(pady=10)  # Display matching button
    
    def perform_matching(self):
        # Hide back buttons
        self.back_button_columns.pack_forget()
        
        # Get selected identifier column
        self.identifier_column = self.identifier_var.get()
        
        if self.category_selection_page_active:  # Check if currently on category selection page
            # Get selected categories
            selected_categories = self.get_selected_categories()

            if not selected_categories:
                messagebox.showwarning("Warning", "Please select at least one category.")
                return

            # Proceed with matching
            matches = self.find_matches(self.selected_columns, selected_categories)
        else:
            # Get selected columns
            selected_columns = self.get_selected_columns()

            if not selected_columns:
                messagebox.showwarning("Warning", "Please select at least one column.")
                return

            # Get selected categories
            selected_categories = self.get_selected_categories()

            if not selected_categories:
                messagebox.showwarning("Warning", "Please select at least one category.")
                return

            # Proceed with matching
            matches = self.find_matches(selected_columns, selected_categories)

        # Filter matches to include only selected columns
        matches_filtered = [(identifier, term, category, col) for identifier, term, category, col in matches if col in self.selected_columns]

        # Save to CSV
        output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_file_path:
            try:
                matches_df = pd.DataFrame(matches_filtered, columns=['Identifier', 'Term', 'Category', 'Column'])
                matches_df.to_csv(output_file_path, index=False)
                messagebox.showinfo("Success", f"Merged data saved to: {output_file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving file: {e}")
    
    def toggle_columns(self):
        if self.all_columns_var.get():
            self.column_listbox.selection_set(0, tk.END)
            self.column_listbox.config(state='disabled')
        else:
            self.column_listbox.selection_clear(0, tk.END)
            self.column_listbox.config(state='normal')
    
    def get_selected_columns(self):
        if self.all_columns_var.get():
            return self.columns
        else:
            return [self.columns[i] for i in self.column_listbox.curselection()]
    
    def get_selected_categories(self):
        return [self.categories[i] for i in self.category_listbox.curselection()]
    
    def find_matches(self, selected_columns, selected_categories):
        matches = []
        # Filter lexicon based on selected categories
        lexicon_df = self.lexicon_df[self.lexicon_df['category'].isin(selected_categories)]
        # Iterate over each row in the metadata DataFrame
        for index, row in self.metadata_df.iterrows():
            # Process the text in each specified column
            for col in selected_columns:
                # Check if the value in the column is a string
                if isinstance(row[col], str):
                    # Iterate over each term in the lexicon and check for matches
                    for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                        # Check if the whole term exists in the text column
                        if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                            matches.append((row[self.identifier_column], term, category, col))
                            break  # Break out of the inner loop once a match is found in this column
        return matches
    
    def show_main_frame(self):
        if self.category_selection_page_active:
            self.category_selection_page_active = False
            self.category_selection_frame.pack_forget()
            self.column_selection_frame.pack(fill='both', expand=True)
            self.back_button_columns.pack_forget()
        else:
            self.column_selection_frame.pack_forget()
            self.main_frame.pack(fill='both', expand=True)
    
    def reset(self):
        self.load_lexicon_button.config(state='normal')
        self.load_metadata_button.config(state='normal')
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []
        self.categories = []
        self.selected_columns = []
        self.identifier_column = None
        self.next_button.pack_forget()
        self.explanation_label.pack_forget()
        self.main_frame.pack()
        self.explanation_label.pack(padx=20, pady=20)

# Create and run the application
app = ReparativeMetadataAuditTool()
app.mainloop()
