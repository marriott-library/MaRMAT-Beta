import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import re
import threading

class ReparativeMetadataAuditTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reparative Metadata Audit Tool")
        
        # Initialize variables
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []
        self.categories = []
        self.selected_columns = []
        self.identifier_column = None
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Explanation text
        self.explanation_text = """
        Welcome to the Reparative Metadata Audit Tool!
        
        This tool allows you to match terms from a problematic terms lexicon file with text data from a collections metadata file.
        
        Please follow the steps below:
        
        1. Load your lexicon and metadata files using the provided buttons.
        
        2. On the next screen, select the columns from your metadata file that you want to analyze.
        
        3. After selecting columns, choose the column in your metadata file that you want to rewrite as the "Identifier" column that relates back to your original metadata (e.g., a collection ID).
        
        4. Then, choose the categories of terms from the lexicon that you want to search for.
        
        5. Click "Perform Matching" to find matches and export the results to a CSV file.
        
        Let's get started!
        """
        
        self.explanation_label = ttk.Label(self.main_frame, text=self.explanation_text, justify='left', wraplength=600)
        self.explanation_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        
        # Load lexicon button
        self.load_lexicon_button = ttk.Button(self.main_frame, text="Load Lexicon", command=self.load_lexicon)
        self.load_lexicon_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        # Load metadata button
        self.load_metadata_button = ttk.Button(self.main_frame, text="Load Metadata", command=self.load_metadata)
        self.load_metadata_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Reset button
        self.reset_button = ttk.Button(self.main_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        
        # Next button
        self.next_button = ttk.Button(self.main_frame, text="Next", command=self.show_column_selection)
        self.next_button.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        self.next_button.grid_remove()  # Hide next button initially

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
                self.next_button.grid()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading metadata: {e}")
    
    def show_column_selection(self):
        if self.lexicon_df is None or self.metadata_df is None:
            messagebox.showwarning("Warning", "Please load lexicon and metadata files first.")
            return
        
        # Populate columns listbox
        self.columns = self.metadata_df.columns.tolist()
        self.column_selection_frame = ttk.Frame(self)
        self.column_selection_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.column_label = ttk.Label(self.column_selection_frame, text="Select Columns to Analyze:")
        self.column_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.column_listbox = tk.Listbox(self.column_selection_frame, selectmode='multiple')
        self.column_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        for column in self.columns:
            self.column_listbox.insert(tk.END, column)
        
        self.all_columns_var = tk.BooleanVar(value=False)
        self.all_columns_checkbox = ttk.Checkbutton(self.column_selection_frame, text="All", variable=self.all_columns_var, command=self.toggle_columns)
        self.all_columns_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.next_button_columns = ttk.Button(self.column_selection_frame, text="Next", command=self.show_identifier_selection)
        self.next_button_columns.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.back_button_columns = ttk.Button(self.column_selection_frame, text="Back", command=self.back_to_main_frame)
        self.back_button_columns.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    
    def show_identifier_selection(self):
        self.selected_columns = self.get_selected_columns()  # Store selected columns
        if not self.selected_columns:
            messagebox.showwarning("Warning", "Please select at least one column.")
            return
        
        self.column_selection_frame.grid_remove()
        
        self.identifier_selection_frame = ttk.Frame(self)
        self.identifier_selection_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.identifier_label = ttk.Label(self.identifier_selection_frame, text="Select Identifier Column:")
        self.identifier_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.identifier_var = tk.StringVar()
        self.identifier_dropdown = ttk.Combobox(self.identifier_selection_frame, textvariable=self.identifier_var, state='readonly')
        self.identifier_dropdown.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.identifier_dropdown['values'] = self.metadata_df.columns.tolist()  # Show all columns as options
        self.identifier_dropdown.current(0)  # Select first column by default
        
        self.next_button_identifier = ttk.Button(self.identifier_selection_frame, text="Next", command=self.show_category_selection)
        self.next_button_identifier.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.back_button_identifier = ttk.Button(self.identifier_selection_frame, text="Back", command=self.back_to_column_selection)
        self.back_button_identifier.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
    
    def show_category_selection(self):
        self.identifier_column = self.identifier_var.get()
        
        self.identifier_selection_frame.grid_remove()
        
        self.category_selection_frame = ttk.Frame(self)
        self.category_selection_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.category_label = ttk.Label(self.category_selection_frame, text="Select Categories to Analyze:")
        self.category_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.category_listbox = tk.Listbox(self.category_selection_frame, selectmode='multiple')
        self.category_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.categories = self.lexicon_df['category'].unique().tolist()
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)
        
        self.all_categories_var = tk.BooleanVar(value=False)
        self.all_categories_checkbox = ttk.Checkbutton(self.category_selection_frame, text="All", variable=self.all_categories_var, command=self.toggle_categories)
        self.all_categories_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.next_button_categories = ttk.Button(self.category_selection_frame, text="Perform Matching", command=self.perform_matching)
        self.next_button_categories.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.back_button_categories = ttk.Button(self.category_selection_frame, text="Back", command=self.back_to_identifier_selection)
        self.back_button_categories.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    
    def perform_matching(self):
        selected_categories = self.get_selected_categories()
        if not selected_categories:
            messagebox.showwarning("Warning", "Please select at least one category.")
            return
        
        matches = self.find_matches(self.selected_columns, selected_categories)
        matches_filtered = [(identifier, term, category, col, text) for identifier, term, category, col, text in matches if col in self.selected_columns]
        output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_file_path:
            try:
                matches_df = pd.DataFrame(matches_filtered, columns=['Identifier', 'Term', 'Category', 'Column', 'Original Text'])
                matches_df.to_csv(output_file_path, index=False)
                messagebox.showinfo("Success", f"Merged data saved to: {output_file_path}")
                self.reset()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving file: {e}")
    
    def toggle_columns(self):
        if self.all_columns_var.get():
            self.column_listbox.selection_set(0, tk.END)
            self.column_listbox.config(state='disabled')
        else:
            self.column_listbox.selection_clear(0, tk.END)
            self.column_listbox.config(state='normal')
    
    def toggle_categories(self):
        if self.all_categories_var.get():
            self.category_listbox.selection_set(0, tk.END)
            self.category_listbox.config(state='disabled')
        else:
            self.category_listbox.selection_clear(0, tk.END)
            self.category_listbox.config(state='normal')
    
    def get_selected_columns(self):
        if self.all_columns_var.get():
            return self.columns
        else:
            return [self.columns[i] for i in self.column_listbox.curselection()]
    
    def get_selected_categories(self):
        return [self.categories[i] for i in self.category_listbox.curselection()]
    
    def find_matches(self, selected_columns, selected_categories):
        matches = []
        lexicon_df = self.lexicon_df[self.lexicon_df['category'].isin(selected_categories)]
        for index, row in self.metadata_df.iterrows():
            for col in selected_columns:
                if isinstance(row[col], str):
                    for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                        if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                            matches.append((row[self.identifier_column], term, category, col, row[col]))
                            break
        return matches
    
    def back_to_main_frame(self):
        self.column_selection_frame.grid_remove()
        self.main_frame.grid()
    
    def back_to_column_selection(self):
        self.identifier_selection_frame.grid_remove()
        self.column_selection_frame.grid()
    
    def back_to_identifier_selection(self):
        self.category_selection_frame.grid_remove()
        self.identifier_selection_frame.grid()
    
    def reset(self):
        self.load_lexicon_button.config(state='normal')
        self.load_metadata_button.config(state='normal')
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []
        self.categories = []
        self.selected_columns = []
        self.identifier_column = None
        self.next_button.grid_remove()
        self.explanation_label.grid()

# Create and run the application
app = ReparativeMetadataAuditTool()
app.mainloop()
