import pandas as pd
import streamlit as st
from utils.transformations import (
    get_list_with_removed_colums,
    adding_prime_columns,
    get_prime_columns,
    adding_pm_pr,
    adding_distance_columns,
)

df = pd.read_excel("input_test.xlsx")
c = get_list_with_removed_colums(df, ["Articles", "MO"])
df = adding_prime_columns(df, "MO", c)
cc = get_prime_columns(df)
df = adding_pm_pr(df, cc)


def main():
    """Function that runs upon doing a streamlit run"""
    st.set_page_config(layout="wide")
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader(
            "Choose your xlsx file, it must contain at least 'Articles' & 'MO' columns",
            type="xlsx",
        )
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.dataframe(df)
                st.markdown("Creating prime columns")
                prices_columns = get_list_with_removed_colums(df, ["Articles", "MO"])
                df = adding_prime_columns(df, "MO", prices_columns)
                st.dataframe(df)
            except Exception as e:
                st.error("Error reading the file: " + str(e))
    with col2:
        if uploaded_file is not None:
            try:
                st.markdown("Adding PM & PR columns")
                prime_columns = get_prime_columns(df)
                df = adding_pm_pr(df, prime_columns)
                st.dataframe(df[["Articles", "MO", "PM", "PR"]])
                st.markdown("Calculating distances...")
                df = adding_distance_columns(df, prime_columns)
                st.dataframe(
                    df.drop(columns=prime_columns + prices_columns + ["PM", "MO"])
                )
            except Exception as e:
                st.error("Error reading the file: " + str(e))


if __name__ == "__main__":
    main()
