import pandas as pd
import numpy as np
from typing import List


def remove_colums(df: pd.DataFrame, columns_to_remove: List[str]) -> pd.DataFrame:
    """
    Remove specified columns from a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns_to_remove (List[str]): List of column names to remove.
    
    Returns:
        pd.DataFrame: DataFrame with specified columns removed.
    """
    columns_list = list(df.columns)
    for column in columns_to_remove:
        columns_to_iterate_through.remove(column)
    return columns_list


def get_prime_columns(df: pd.DataFrame) -> List[str]:
    """
    Get the list of column names containing 'prime' in a DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        List[str]: List of column names containing 'prime'.
    """
    prime_columns = [column for column in list(df.columns) if "prime" in column]
    return prime_columns


def adding_prime_columns(
    df: pd.DataFrame, mo_column: str, list_of_columns: List[str]
) -> pd.DataFrame:
    """
    Add prime columns to a DataFrame based on specific conditions.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        mo_column (str): Name of the column representing 'MO'.
        list_of_columns (List[str]): List of column names to add prime columns.
    
    Returns:
        pd.DataFrame: DataFrame with prime columns added.
    """
    for column in list_of_columns:
        new_column_name = f"{column}_prime"
        condition = np.logical_or(
            df[column] > 1.2 * df[mo_column], df[column] < 0.8 * df[mo_column]
        )
        df[new_column_name] = np.where(condition, np.nan, df[column])
        return df


def adding_pm_pr(df: pd.DataFrame, prime_columns: List[str]) -> pd.DataFrame:
    """
    Add 'PM' and 'PR' columns to a DataFrame based on prime column values.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        prime_columns (List[str]): List of prime column names.
    
    Returns:
        pd.DataFrame: DataFrame with 'PM' and 'PR' columns added.
    """
    df["PM"] = df[prime_columns].mean(axis=1, skipna=True)
    df["PR"] = df[["MO", "PM"]].mean(axis=1, skipna=True)
    return df
