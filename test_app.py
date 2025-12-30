import pandas as pd
import os
import pytest
from app import load_data, save_data

def test_load_data(tmp_path):
    # Create a dummy CSV file
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    csv_file = tmp_path / "test.csv"
    df.to_csv(csv_file, index=False)

    # Test loading
    # Streamlit file uploader returns a file-like object, but pandas read_csv handles paths too.
    # However, our load_data expects an uploaded_file which might be an object.
    # We should simulate that or modify load_data to handle strings.
    # pd.read_csv handles both.

    loaded_df = load_data(str(csv_file))
    assert loaded_df is not None
    assert len(loaded_df) == 2
    assert 'col1' in loaded_df.columns

def test_save_data(tmp_path):
    d = {'col1': [1, 2], 'ERI_Score': [5, 6], 'Labeler': ['A', 'B']}
    df = pd.DataFrame(data=d)
    output_file = tmp_path / "output.csv"

    # We need to mock streamlit success/error or ignore them
    # But for this unit test, let's just see if file is created.
    # save_data calls st.success, which needs a running app context or mock.
    # We can mock st in the test.

    import unittest.mock as mock
    with mock.patch('app.st') as mock_st:
        save_data(df, str(output_file))
        assert output_file.exists()
        loaded = pd.read_csv(output_file)
        assert len(loaded) == 2
        assert 'ERI_Score' in loaded.columns

def test_dataframe_update():
    d = {'col1': [1, 2]}
    df = pd.DataFrame(data=d)
    df['ERI_Score'] = None

    # Update logic simulation
    df.at[0, "ERI_Score"] = 5
    assert df.at[0, "ERI_Score"] == 5
    assert pd.isna(df.at[1, "ERI_Score"])
