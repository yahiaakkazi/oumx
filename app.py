import pandas as pd
import streamlit as st
from utils.transformations import (
    get_list_with_removed_colums,
    adding_prime_columns,
    get_prime_columns,
    adding_pm_pr,
    adding_distance_columns,
    format_column,
    order_items,
)


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
                st.dataframe(df[["Articles", "MO", "PM", "PR"]], height=150)
                st.markdown("Calculating distances...")
                df = adding_distance_columns(df, prime_columns)
                st.dataframe(
                    df.drop(columns=prime_columns + prices_columns + ["PM", "MO"]),
                    height=150,
                )
                st.markdown("Ordering prices and providing the last result:")
                df_dropped = df.drop(
                    columns=["MO", "PM", "PR"] + prime_columns + prices_columns
                )
                processed_column_names = [
                    format_column(column) for column in df_dropped.columns
                ]
                df_dropped.columns = processed_column_names
                transposed_df = df_dropped.set_index("Articles").T
                transposed_df = order_items(transposed_df)
                st.dataframe(transposed_df, height=150)
                transposed_df.to_excel("output.xlsx", index=False, sheet_name="Sheet")
                with open("output.xlsx", "rb") as file:
                    contents = file.read()
                st.download_button(
                    "Download as Excel",
                    data=contents,
                    file_name="output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            except Exception as e:
                st.error("Error reading the file: " + str(e))


if __name__ == "__main__":
    main()
