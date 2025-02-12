import pytest
from pandas import read_csv
from marmat.audit import AuditTool


def test_init_attrs():
    tool = AuditTool()
    assert tool.lexicon_df is None
    assert tool.metadata_df is None
    assert tool.columns == []
    assert tool.categories == []
    assert tool.selected_columns == []
    assert tool.selected_categories == []
    assert tool.identifier_column is None


class TestMaRMAT:
    cols = [
        "id", "title", "description", "creator", "date",
        "collection name", "subjects", "spatial coverage"
    ]

    @pytest.fixture(scope="class")
    def tool(self):
        tool = AuditTool()
        tool.select_columns(["title"])  # Input the name(s) of the metadata column(s) you want to analyze.
        tool.select_identifier_column("id")
        tool.select_categories(["RaceTerms", "JapaneseincarcerationTerm"])
        tool.load_metadata("tests/example-input-metadata.csv")
        tool.load_lexicon("tests/example-lexicon-reparative-metadata.csv")
        return tool

    def test_attrs(self, tool):
        assert tool.columns == self.cols
        assert tool.identifier_column == "id"
        assert tool.categories == ["RaceTerms", "JapaneseincarcerationTerm"]
        assert tool.selected_columns == ["title"]
        assert tool.selected_categories == ["RaceTerms", "JapaneseincarcerationTerm"]

    def test_find_matches(self, tool, capsys):
        standard_cols = [tool.identifier_column, "Term", "Category", "Context", "Field", "Occurences"]

        one_cat_df = tool.find_matches(selected_columns=["title"], selected_categories=["RaceTerms"])
        captured = capsys.readouterr()
        assert captured.out == "Processing RaceTerms term 1 of 2\nProcessing RaceTerms term 2 of 2\n"
        assert one_cat_df.shape == (3, 6)
        assert one_cat_df["id"].to_list() == [337805, 1498946, 1302623]
        assert one_cat_df.loc[0, "Field"] == "title"
        assert one_cat_df.loc[0, "Context"] == "Aborigines of Taiwan [001]"
        assert one_cat_df.loc[1, "Context"] == "Spanish at Indian pueblo"
        assert one_cat_df.loc[2, "Context"] == "Basalt-capped mesa on Dolores (Triassic), 6± miles south of Beddehoche (Indian Wells), Ariz., 1909 (photo G-67)"
        assert one_cat_df.columns.to_list() == standard_cols

        two_cat_df = tool.find_matches(selected_columns=["title"], selected_categories=["RaceTerms", "JapaneseincarcerationTerm"])
        captured = capsys.readouterr()
        assert captured.out == "Processing RaceTerms term 1 of 2\nProcessing RaceTerms term 2 of 2\n" \
                               "Processing JapaneseincarcerationTerm term 1 of 2\n" \
                               "Processing JapaneseincarcerationTerm term 2 of 2\n"
        assert two_cat_df.shape == (6, 6)
        assert two_cat_df["id"].to_list() == [337805, 1498946, 1302623, 941713, 941496, 941536]
        assert two_cat_df.loc[0, "Context"] == "Aborigines of Taiwan [001]"
        assert two_cat_df.loc[4, "Context"] == "Evacuees cleaning vegetables in the packing shed."
        assert two_cat_df.loc[5, "Context"] == "Evacuees harvesting potatoes at Tule Lake. [5]"
        assert two_cat_df.columns.to_list() == standard_cols

        two_cat_two_col_df = tool.find_matches(selected_columns=["title", "description"], selected_categories=["RaceTerms", "JapaneseincarcerationTerm"])
        captured = capsys.readouterr()
        assert captured.out == "Processing RaceTerms term 1 of 2\nProcessing RaceTerms term 2 of 2\n" \
                               "Processing JapaneseincarcerationTerm term 1 of 2\n" \
                               "Processing JapaneseincarcerationTerm term 2 of 2\n"
        assert two_cat_two_col_df.shape == (17, 6)
        assert two_cat_two_col_df["id"].to_list() == [337805, 1498946, 1302623, 1533946, 962277, 1498946,
                                                      1302623,1396777, 941713, 941496, 941536, 941713, 941496,
                                                      941536, 941713, 941496, 941536]
        assert two_cat_two_col_df.loc[0, "Context"] == "Aborigines of Taiwan [001]"
        assert two_cat_two_col_df.loc[5, "Context"] == "Photograph of an illustration in an unidentified publication, artist's rendition of a party of Spanish horsemen at an Indian pueblo, perhaps in New Mexico."
        assert two_cat_two_col_df.loc[16, "Context"] == "Photo of evacuees harvesting potatoes at the Tule Lake Relocation Center in California during World War II"
        assert two_cat_two_col_df.columns.to_list() == standard_cols

    def test_perform_matching(self, tool, tmp_path):
        blank_tool = AuditTool()
        with pytest.raises(ValueError):  # neither metadata nor lexicon
            blank_tool.perform_matching(tmp_path)

        with pytest.raises(ValueError):  # lexicon but no metadata
            blank_tool.load_lexicon("tests/example-lexicon-reparative-metadata.csv")
            blank_tool.perform_matching(tmp_path)

        tool.perform_matching(tmp_path / "test_output.csv")
        check_df = read_csv(tmp_path / "test_output.csv")
        assert check_df.shape == (6, 6)
