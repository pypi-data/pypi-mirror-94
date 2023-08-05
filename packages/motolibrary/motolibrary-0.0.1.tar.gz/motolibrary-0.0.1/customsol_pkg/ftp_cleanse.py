# ftp_cleanse.py
# Dependencies: pandas

import pandas as pd

def ftp_cleanse_file(ftp_df):

    dummy_fill_val = "AAAAAAAAAAAAAAAAA"

    # Create a copy of the downloaded dataframe
    dummy_df = ftp_df.copy()

    # Remove all but the first row in downloaded dataframe
    dummy_df = dummy_df.iloc[:1]

    # Find which columns are filled and which are not
    filled_cols = []
    for col in dummy_df.columns:
        isFilled = not dummy_df[col].isna().any()
        filled_cols.append(isFilled)

    # Replace all filled columns with dummy value
    index_counter = 0

    for isFilled in filled_cols:
        if isFilled:
            dummy_df[dummy_df.columns[index_counter]] = [dummy_fill_val]
        index_counter += 1

    # Upload the dummy value, returning the result of upload
    return dummy_df
