"""Taller evaluable"""

import glob

import pandas as pd
from os import listdir
from os.path import join

def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    lines = list()
    for filename in listdir(input_directory):
        with open(join(input_directory, filename)) as file:
            for line in file.readlines():
                lines.append(line)

    return pd.DataFrame(lines, columns = ["text"])




def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    df_final = dataframe.copy()
    df_final["text"] = df_final["text"].str.lower()
    df_final.text = df_final.text.apply(lambda x: x.replace(",", "").replace(".", ""))
    return df_final


def count_words(dataframe):
    """Word count"""
    df = dataframe.copy()
    df.text = dataframe.text.apply(lambda x: x.split(" "))
    df = df.explode(("text")).reset_index(drop=True)
    df = df.rename(columns = {"text": "word"})
    df["count"] = 1
    df.to_csv()
    df = df.groupby("word", as_index= False).agg({"count": "sum"})
    return df


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, index=False, sep="\t", header=None)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    df = load_input(input_directory)
    df = clean_text(df)
    df = count_words(df)
    save_output(df, output_filename)



if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
