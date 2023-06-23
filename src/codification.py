import os
import json
import pickle
import time
import pandas as pd
import openai


class Codificacion:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def join_text_batch(self, text_batch: list, ids: list) -> str:
        """
        Crear un string con los textos de cada elemento de la lista
        que indique que cada elemento es una frase e indique el index
        del elemento en la lista.

        Args:
            text_bacth (list): Lista con las textos a concatenar.
            ids (list): Lista con los ids para identificar cada frase.

        Returns:
            str: String resultante.
        """
        result = "\n".join([f"Frase{i}: {elem}" for i, elem in zip(ids, text_batch)])
        return result

    def replace_keys_values(self, dictionary_keys: dict) -> list:
        """
        Reemplaza las claves de un diccionario eliminando la subcadena "Frase"
        y devuelve las claves modificadas como una lista.

        Args:
            dictionary_keys (dict): Diccionario con las claves a reemplazar.

        Returns:
            list: Lista de claves modificadas.
        """
        return list(map(lambda x: x.replace("Frase", ""), list(dictionary_keys)))

    def from_json_list_to_df(self, json_list: dict) -> pd.Series:
        """
        Convierte una lista de cadenas JSON en una serie de pandas.

        Args:
            json_list (dict): Lista de cadenas JSON.

        Returns:
            pd.Series: Serie de pandas que contiene los datos convertidos.
        """
        new_dict = {}

        for i in range(0, len(json_list)):
            dict_i = json.loads("".join(json_list[i].splitlines()))
            new_keys = self.replace_keys_values(dict_i.keys())

            new_dict_i = {}
            for i, (key, value) in enumerate(dict_i.items(), start=0):
                new_key = new_keys[i]
                new_dict_i[new_key] = value

            new_dict.update(new_dict_i)

        return pd.Series(new_dict)

    def get_completion(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Llama al modelo deseado e interactua con él dependiendo
        el prompt.

        Args:
            prompt (str): Instrucciones que se le dan al modelo.
            model (str): LLM a utilizar.

        Returns:
            str: Respuesta del modelo a la solicitud del usuario.
        """
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

    def get_topics(
        self,
        df: pd.DataFrame,
        batch_size: int,
        column_name: str,
        id_column: str,
        num_topicos: int,
    ) -> list:
        """
        Obtiene los tópicos para cada frase en un DataFrame, utilizando un modelo de generación de lenguaje.

        Args:
            df (pd.DataFrame): DataFrame que contiene las frases.
            batch_size (int): Tamaño del lote de frases a procesar en cada iteración.
            column_name (str): Nombre de la columna que contiene las frases.
            id_column (str): Nombre de la columna que contiene los identificadores de las frases.
            num_topicos (int): Número máximo de tópicos a determinar para cada frase.

        Returns:
            list: Lista de respuestas en formato JSON que contiene cada frase y su lista de tópicos.
        """
        response = []
        for i in range(0, len(df), batch_size):
            text_batch = df[i : (i + batch_size)][column_name].tolist()
            ids_batch = df[i : (i + batch_size)][id_column].tolist()
            str_text_batch = self.join_text_batch(text_batch, ids_batch)

            prompt = f"""
                Determine máximo {num_topicos} tópicos para \
                cada una de las frases a continuación: \

                {str_text_batch}

                Cada tópico debe ser de máximo tres palabras.
                El resultado debe ser un JSON con cada frase y su lista de tópicos.

                """

            response_i = self.get_completion(prompt)
            response.append(response_i)

            if i % 100 == 0:
                print("Iteración:", i)
                time.sleep(10)

        return response

    def get_sentiment(
        self, df: pd.DataFrame, batch_size: int, column_name: str, id_column: str
    ) -> list:
        """
        Obtiene el sentimiento para cada frase en un DataFrame, utilizando un modelo de generación de lenguaje.

        Args:
            df (pd.DataFrame): DataFrame que contiene las frases.
            batch_size (int): Tamaño del lote de frases a procesar en cada iteración.
            column_name (str): Nombre de la columna que contiene las frases.
            id_column (str): Nombre de la columna que contiene los identificadores de las frases.

        Returns:
            list: Lista de respuestas en formato JSON que contiene cada frase y su sentimiento.
        """
        response = []
        for i in range(0, len(df), batch_size):
            text_batch = df[i : (i + batch_size)][column_name].tolist()
            ids_batch = df[i : (i + batch_size)][id_column].tolist()
            str_text_batch = self.join_text_batch(text_batch, ids_batch)

            prompt = f"""
                Determine el sentimiento para \
                cada una de las frases a continuación: \

                {str_text_batch}

                El resultado debe ser una lista.

                """

            response_i = self.get_completion(prompt)
            response.append(response_i)

            if i % 100 == 0:
                print("Iteración:", i)
                time.sleep(15)

        return response

    def get_translation(
        self, df: pd.DataFrame, batch_size: int, column_name: str, id_column: str
    ) -> list:
        """
        Realiza la traducción al inglés de cada frase en un DataFrame, utilizando un modelo de generación de lenguaje.

        Args:
            df (pd.DataFrame): DataFrame que contiene las frases.
            batch_size (int): Tamaño del lote de frases a procesar en cada iteración.
            column_name (str): Nombre de la columna que contiene las frases.
            id_column (str): Nombre de la columna que contiene los identificadores de las frases.

        Returns:
            list: Lista de respuestas en formato JSON que contiene cada frase y su traducción al inglés.
        """
        response = []
        for i in range(0, len(df), batch_size):
            text_batch = df[i : (i + batch_size)][column_name].tolist()
            ids_batch = df[i : (i + batch_size)][id_column].tolist()
            str_text_batch = self.join_text_batch(text_batch, ids_batch)

            prompt = f"""
                Realice la traducción a inglés de \
                cada una de las frases a continuación: \

                {str_text_batch}

                El resultado debe ser un JSON con cada frase y su traducción.

                """

            response_i = self.get_completion(prompt)
            response.append(response_i)

            if i % 100 == 0:
                print("Iteración:", i)
                time.sleep(15)

        return response

    def get_spelling_correction(
        self, df: pd.DataFrame, batch_size: int, column_name: str, id_column: str
    ) -> list:
        """
        Realiza la corrección ortográfica de cada frase en un DataFrame, utilizando un modelo de generación de lenguaje.

        Args:
            df (pd.DataFrame): DataFrame que contiene las frases.
            batch_size (int): Tamaño del lote de frases a procesar en cada iteración.
            column_name (str): Nombre de la columna que contiene las frases.
            id_column (str): Nombre de la columna que contiene los identificadores de las frases.

        Returns:
            list: Lista de respuestas en formato JSON que contiene cada frase y su corrección ortográfica.
        """
        response = []
        for i in range(0, len(df), batch_size):
            text_batch = df[i : (i + batch_size)][column_name].tolist()
            ids_batch = df[i : (i + batch_size)][id_column].tolist()
            str_text_batch = self.join_text_batch(text_batch, ids_batch)

            prompt = f"""
                Realice la correción ortográfica de \
                cada una de las frases a continuación: \

                {str_text_batch}

                El resultado debe ser un JSON con cada frase y su corrección ortográfica.

                """

            response_i = self.get_completion(prompt)
            response.append(response_i)

            if i % 100 == 0:
                print("Iteración:", i)
                time.sleep(15)

        return response

    def save_pandas_object(
        self, df: pd.DataFrame, root_path: str, subfolder: str, name: str
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

    def save_pickle_object(
        self, obj, root_path: str, subfolder: str, name: str
    ) -> None:
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

    def load_pickle_object(self, file_path: str):
        """
        Load a pickle file.

        Args:
            file_path (str): Path to the pickle file.

        Returns:
            The loaded object.
        """
        with open(file_path, "rb") as f:
            obj = pickle.load(f)

        return obj
