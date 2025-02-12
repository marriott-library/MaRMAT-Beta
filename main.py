import os
from marmat.audit import AuditTool

LEXICON_PATH = "data\\external\\bl_lexicon_plural.csv"
INTERIM_PATH = "data\\interim\\"
PROCESSED_PATH = "data\\processed\\restructure_test\\"

ALEPH = True
IAMS = False

if __name__ == "__main__":

    record_files = {
        "aleph": [
            "epBooksPre1700", "epBooks1700s", "epBooks1800s_1", "epBooks1800s_2", "epBooks1800s_3",
            "epBooks1800s_4", "Maps", "Music"
        ],
        "iams": [
            "India Office_v2", "Map Collections_v2", "Music Collections_v2", "Oriental Manuscripts_v2",
            "Philatelic Collections_v2", "Printed Collections_v2", "Qatar_v2", "Sound Archive_v2",
            "Visual Arts_v2", "Western Manuscripts_v2"
        ]
    }

    print("Initialize the tool:")
    tool = AuditTool()

    print("\nLoad lexicon and metadata files")
    tool.load_lexicon(LEXICON_PATH)  # Input the path to your lexicon CSV file.

    # Aleph
    if ALEPH:
        print(f"\nSetting metadata and ID columns, and lexicon categories")
        tool.select_columns(["Title [245]"])  # Input the name(s) of the metadata column(s) you want to analyze.
        tool.select_identifier_column("System No [001]")
        tool.select_categories(["Race", "Enslavement"])
        tool.select_export_cols(["Personal Name [100]", "Corp Name [110]", "Date Pub [260 and 264$c]", "Shelfmark [852]"])

        for f in record_files["aleph"][:-2]:
            print(f"\nLoading {f}")
            if "Maps" in f or "Music" in f:
                tool.select_export_cols(["Personal Name [100]", "Corp Name [110]", "Date Pub [264$c]", "Shelfmark [852]"])
            tool.load_metadata(os.path.join(INTERIM_PATH, f"{f}.csv"))  # Input the path to your metadata CSV file

            print("\nPerform matching and exporting results")
            output_file = os.path.join(PROCESSED_PATH, f"{f}_matches.csv")  # Input the file path where you want to save your matches here.
            tool.perform_matching()
            tool.export_matches(output_file)

    #IAMS
    if IAMS:
        print(f"\nSetting metadata and ID columns, and lexicon categories")
        tool.select_columns(["Title", "Scope and content"])  # Input the name(s) of the metadata column(s) you want to analyze.
        tool.select_identifier_column("Reference")
        tool.select_categories(["Race", "Enslavement", "Aggrandizement"])
        tool.select_export_cols(["Date range"])

        for f in record_files["iams"]:

            print(f"\nLoading {f}")
            tool.load_metadata(os.path.join(INTERIM_PATH, f"{f}.csv"))  # Input the path to your metadata CSV file

            print("\nPerform matching and exporting results")
            output_file = os.path.join(PROCESSED_PATH, f"{f}_matches.csv")  # Input the file path where you want to save your matches here.
            tool.perform_matching()
            tool.export_matches(output_file)
