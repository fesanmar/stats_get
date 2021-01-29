from os.path import exists
import numpy as np
import pandas as ps
import json
from statistics import mean, mode
from typing import Optional, Dict, List, Union

from stats_gen import ask_for_file_name

Number = Union[int, float]

def read_file(filename:str) -> Optional[Dict[str, int]]:
    """Reads the file with name `filename` if exists. Else returns null"""

    if exists(filename):
        with open(filename, "r") as json_file:
            json_text = json_file.read()
            return json.loads(json_text)

def get_stats_from_data(data:List[Number]) -> List[Number]:
    """Returns a list with the mean, mode, max and min functions applied to the `data`"""

    data_mean = mean(data)
    data_mode = mode(data)
    max_data = max(data)
    min_data = min(data)
    return [data_mean, data_mode, max_data, min_data]

def get_stats_for_categorys(data:Dict[str, int]) -> Dict[str, int]:
    """Returns a `dict` for each category containing: mean, mode, max and min"""

    stats_for_category = {}
    for category, category_data in data.items():
        stats_for_category[category] = get_stats_from_data(category_data)
    return stats_for_category

if __name__ == "__main__":
    filename = ask_for_file_name()
    data = read_file(filename)
    if data is None:
        print(f"El archivo <{filename}> no existe o no se encuentra en la ruta a actual.")
    else:
        stats_for_category = get_stats_for_categorys(data)
        print(ps.DataFrame.from_dict(stats_for_category, orient="index", columns=["Media", "Moda", "Máximo", "Mínimo"]))
        
