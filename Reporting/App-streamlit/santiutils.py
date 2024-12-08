import pandas as pd
import numpy as np

def singleitemdelist( df_cell ):
    if isinstance(df_cell, list):
        return df_cell[0]
    else:
        return df_cell


def emotoquadrant(emotion): 

    if emotion in ("exited", "delighted", "happy"):
        return "Q1" 
    elif emotion in ("tense", "angry", "frustrated"):
        return "Q2"    
    elif emotion in ("depressed", "bored", "tired"):
        return "Q3"
    elif emotion in ("calm", "relaxed", "content"):
        return "Q4"
    elif emotion in "neutral":
        return "NEUTRAL"

    else: 
        return "Not VA Emotion"



# def label_to_VAQuadrant_convert ( cell ) :
#     registros['Quadrant'] = registros.apply(lambda row: emotoquadrant(row['emotion']), axis=1)

#     return registros



def heavy_harcode_limiting_mega_function ( dfconlistas: pd.DataFrame) -> pd.DataFrame :

    # Define a function to get the first element of a list
    def get_first_element(lst):
        return lst[0] if isinstance(lst, list) and len(lst) > 0 else None

    # Apply the function to the 'values' column
    dfsinlistas = dfconlistas.map(get_first_element)

    return dfsinlistas


def talktime( dataframe_input_series , FPS_seteados ): 
    """_Esta funcion lo que hace es contar la cantidad de veces que se detecto un icono en un frame teniendo en cuenta los FPS seteados

    Args:
        ID (_type_): _description_
    """
    cantidad_iconos = dataframe_input_series.value_counts().get('icon',0)
    time_llamada = cantidad_iconos * (1/FPS_seteados)

    return time_llamada

def callresult( quadrant_series: pd.DataFrame ):

    if quadrant_series.value_counts().index[0] == ('Q1' or 'Q4'):
        return "Mostly positive"
    elif quadrant_series.value_counts().index[0] == ('Q2' or 'Q3'):
        return "Mostly Negative"
    elif quadrant_series.value_counts().index[0]  == 'NEUTRAL':
        return "Mostly Neutral"
    else:
        return "ERROR NO DETECTION"
    