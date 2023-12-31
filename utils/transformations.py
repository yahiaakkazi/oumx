from typing import List
import pandas as pd
import numpy as np


def get_list_with_removed_colums(
    df: pd.DataFrame, columns_to_remove: List[str]
) -> List[str]:
    """
    Remove specified columns from a DataFrame column list.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns_to_remove (List[str]): List of column names to remove.

    Returns:
        List[str]: List of column names with remvoved specified columns
    """
    columns_list = list(df.columns)
    for column in columns_to_remove:
        columns_list.remove(column)
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


def adding_distance_columns(df: pd.DataFrame, prime_columns: List[str]) -> pd.DataFrame:
    """
    Adds columns where, if prime is null, the new columns stays null, and if it's not, the distance between prime & PR gets computed there.

    Args:
        df (pd.DataFrame): The input DataFrame.
        prime_columns (List[str]): List of prime column names.

    Returns:
        pd.DataFrame: DataFrame with 'Prime_distance' columns added.
    """
    for column in prime_columns:
        new_column_name = f"{column}_distance_to_PR"
        condition = np.isnan(df[column])
        df[new_column_name] = np.where(
            condition, float("inf"), np.abs(df[column] - df["PR"])
        )
    return df


def format_column(column_name: str) -> str:
    """
    Removes a certain value from the column names.

    Args:
        column_name: the name of the column

    Returns:
        str : the formatted column name
    """
    processed_name = column_name.replace("_prime_distance_to_PR", "")
    return processed_name


def order_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orders the items in an ascending order

    Args:
        df:pd.DataFrame: the dataframe to be ordered

    Returns:
        pd.DataFrame : the ordered dataframe
    """
    df_dict = df.to_dict()
    for item in df_dict.keys():
        df_dict[item] = sorted(df_dict[item].items(), key=lambda x: x[1])
    return pd.DataFrame.from_dict(df_dict).astype(str)
