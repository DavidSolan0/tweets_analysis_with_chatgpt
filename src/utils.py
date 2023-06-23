import os
import re
import glob
import json
import time
import gensim
import pickle
import pandas as pd

import openai

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from gensim.utils import simple_preprocess

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)


def read_social_listening_data(folder_name: str) -> pd.DataFrame:
    """
    Lee los archivos .csv resultado de la escucha social para un cliente
    en particular y los concatena en un único dataframe.

    Args:
        folder_name (str): Nombre del folder del cliente de interés.

    Returns:
        pd.DataFrame: El dataframe concatenado de unir la escucha social.
    """

    folder_path = os.path.join(
        "../data/", folder_name
    )  # Replace with the path to your folder containing the CSV files
    csv_files = glob.glob(
        f"{folder_path}/*.csv"
    )  # Get a list of all CSV file paths in the folder

    print(f"Ruta destino...{folder_path}")
    dfs = []  # List to store individual DataFrames

    # Iterate over each CSV file and read it into a DataFrame
    for file in csv_files:
        df = pd.read_csv(file, encoding="ISO-8859-1", on_bad_lines="skip")
        dfs.append(df)

    # Concatenate all the DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df


def tokenizador(text: str) -> str:
    """
    Elimina los carácteres especiales de los tweets

    Args:
        text (str): Tweet a limpiar.

    Returns:
        str: Texto limpiado.

    """
    return " ".join(tknzr.tokenize(text))


def remove_word_after_hashtag(string):
    # Use regular expression pattern to match the word after a hashtag
    pattern = r"#\w+\b"
    modified_string = re.sub(pattern, "", string)

    return modified_string


def remove_special_characters(string):
    # Remove special characters using regular expressions
    pattern = r"[^a-zA-Z0-9\s]"
    string = re.sub(pattern, "", string)

    return string


def clean_text(df: pd.DataFrame, variable: str = "text") -> pd.DataFrame:
    """
    Aplica la limpieza a cada instancia del dataframe.

    Args:
        df (pd.DataFrame): Data Frame con columna de texto objetivo a limpiar.
        variable (str): Nombre de la columna que contiene el texto a limpiar.

    Returns:
        pd.Series: pandas Series de la columna de texto limpia.
    """
    data_cleaned = (
        df[variable]
        .map(tokenizador)
        .map(remove_word_after_hashtag)
        .map(remove_special_characters)
        .map(lambda x: x.lower())
    )

    return data_cleaned


def save_pandas_object(
    df: pd.DataFrame, root_path: str, subfolder: str, name: str
) -> None:
    """
    Guardar los resultados de la escucha en la carpeta "data.
    Si la carpeta no existe primero la crea.

    Args:
        df (pd.DataFrame): Archivo a guardar.
        subfolder (str): Subfolder en data donde se guardarán los datos.
        name (str): Nombre que se quiere para los archivos.

    Returns:
        None.
    """
    folder_path = os.path.join(root_path, subfolder)
    # Check if the root directory exists
    if not os.path.exists(folder_path):
        # Create the root directory
        os.makedirs(folder_path)
        print(f"Root directory created at {folder_path}")
    else:
        print(f"Root directory already exists at {folder_path}")

    # Proceed with saving the file in the root directory
    file_path = os.path.join(folder_path, f"{name}")
    df.to_csv(file_path, index=False)


def save_pickle_object(obj, root_path: str, subfolder: str, name: str) -> None:
    """
    Save a file as a pickle file in the specified directory.

    Args:
        obj : Object to be saved.
        root_path (str): Root directory path where the file will be saved.
        subfolder (str): Subfolder in the root directory where the file will be saved.
        name (str): Name for the file.

    Returns:
        None.
    """
    folder_path = os.path.join(root_path, subfolder)

    # Check if the root directory exists
    if not os.path.exists(folder_path):
        # Create the root directory
        os.makedirs(folder_path)
        print(f"Root directory created at {folder_path}")
    else:
        print(f"Root directory already exists at {folder_path}")

    # Proceed with saving the file in the root directory
    file_path = os.path.join(folder_path, f"{name}.pkl")
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)
    print(f"File saved as pickle file: {file_path}")
