import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import re
import threading
import queue

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
        self.category_selection_page_active = False

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Explanation text
        explanation_text = (
            "Welcome to the Reparative Metadata Audit Tool!\n\n"
            "This tool allows you to match terms from a problematic terms lexicon file with text data from a collections metadata file.\n\n"
            "Please follow the steps below:\n\n"
            "1. Load your lexicon and metadata files using the provided buttons.\n"
            "2. Select the columns from your metadata file that you want to analyze.\n"
            "3. Choose the column in your metadata file that you want to use as the 'Identifier' column.\n"
            "4. Choose the categories of terms from the lexicon that you want to search for.\n"
            "5. Click 'Perform Matching' to find matches and export the results to a CSV file.\n\n"
            "Let's get started!"
        )

        self.explanation_label = ttk.Label(self.main_frame, text=explanation_text, justify='left')
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

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.main_frame, orient='horizontal', mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.progress_bar.grid_remove()

        # Queue for thread communication
        self.matching_queue = queue.Queue()
        self.matching_thread = None
        self.check_queue_job = None

    def load_lexicon(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV and TSV files", "*.csv *.tsv")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.lexicon_df = pd.read_csv(file_path, encoding='latin1')
                elif file_path.endswith('.tsv'):
                    self.lexicon_df = pd.read_csv(file_path, encoding='latin1', sep='\t')
                messagebox.showinfo("Success", "Lexicon loaded successfully.")
                self.load_lexicon_button.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading lexicon: {e}")

    def load_metadata(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV and TSV files", "*.csv *.tsv")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.metadata_df = pd.read_csv(file_path, encoding='latin1')
                elif file_path.endswith('.tsv'):
                    self.metadata_df = pd.read_csv(file_path, encoding='latin1', sep='\t')
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

        self.next_button_categories = ttk.Button(self.category_selection_frame, text="Perform Matching", command=self.start_matching_thread)
        self.next_button_categories.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    def start_matching_thread(self):
        self.progress_bar.grid()
        self.progress_bar.start()
        self.matching_thread = threading.Thread(target=self.perform_matching)
        self.matching_thread.start()
        self.check_queue()

    def perform_matching(self):
        selected_categories = self.get_selected_categories()
        if not selected_categories:
            messagebox.showwarning("Warning", "Please select at least one category.")
            self.matching_queue.put("done")
            return

        self.matched_results = []

        total_rows = len(self.metadata_df)
        for idx, row in self.metadata_df.iterrows():
            for col in self.selected_columns:
                cell_value = str(row[col])
                for _, lexicon_row in self.lexicon_df.iterrows():
                    term = lexicon_row['term']
                    category = lexicon_row['category']
                    if category in selected_categories:
                        if re.search(rf'\b{re.escape(term)}\b', cell_value, re.IGNORECASE):
                            match_info = {
                                'Identifier': row[self.identifier_column],
                                'Column': col,
                                'Term': term,
                                'Category': category,
                                'Original Text': cell_value
                            }
                            self.matched_results.append(match_info)
            self.matching_queue.put(idx)

        self.matching_queue.put("done")

    def check_queue(self):
        try:
            while True:
                message = self.matching_queue.get_nowait()
                if message == "done":
                    self.progress_bar.stop()
                    self.progress_bar.grid_remove()
                    if self.matched_results:
                        self.export_results()
                    else:
                        messagebox.showinfo("No Matches", "No matches found.")
                    return
                else:
                    self.progress_bar['value'] = (message + 1) / len(self.metadata_df) * 100
        except queue.Empty:
            self.after(100, self.check_queue)

    def export_results(self):
        results_df = pd.DataFrame(self.matched_results)
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            try:
                results_df.to_csv(save_path, index=False, encoding='utf-8')
                messagebox.showinfo("Success", "Results exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting results: {e}")

    def get_selected_columns(self):
        if self.all_columns_var.get():
            return self.columns
        selected_indices = self.column_listbox.curselection()
        return [self.columns[i] for i in selected_indices]

    def get_selected_categories(self):
        if self.all_categories_var.get():
            return self.categories
        selected_indices = self.category_listbox.curselection()
        return [self.categories[i] for i in selected_indices]

    def toggle_columns(self):
        if self.all_columns_var.get():
            self.column_listbox.selection_set(0, tk.END)
        else:
            self.column_listbox.selection_clear(0, tk.END)

    def toggle_categories(self):
        if self.all_categories_var.get():
            self.category_listbox.selection_set(0, tk.END)
        else:
            self.category_listbox.selection_clear(0, tk.END)

    def reset(self):
        self.destroy()
        self.__init__()
        self.mainloop()

if __name__ == "__main__":
    app = ReparativeMetadataAuditTool()
    app.mainloop()
