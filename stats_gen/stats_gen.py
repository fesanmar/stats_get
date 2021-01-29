from os import getcwd
from io import open
from typing import Union, Literal, NoReturn
import random
import json

Number = Union[int, float]
Bound = Literal["superior", "inferior"]
BoundedMap = {str: (Number, Number)}

def is_forbidden_char(char: chr) -> bool:
    """Returns `True` if `char` isn't valid for filename."""

    forbidden_chars = ["[", "\\", "/", ":", "\"", "*", "?", "<", ">", "|", "]", "+"]
    return char in forbidden_chars


def ask_for_file_name() -> str:
    """Ask user to insert a valid filename and returns it, adding `.json` extension."""
    
    doc_name = ""
    while True:
        doc_name = input("Introduce el nombre del archivo: ").strip()
        if len(doc_name) > 0 and len(list(filter(is_forbidden_char, doc_name))) == 0:
            return doc_name + ".json"
        else:
            print("El nombre introducido no es válido.\n")

def ask_for_category(num: int) -> str:
    """Ask user to enter a valid category name for the category number `num` and returns it"""

    while True:
        category = input(f"Introduce la categoría número {num}: ").strip()
        if (len(category) > 0):
            return category
        else:
            print("La categoría introducida no es válida.\n")

def ask_5_categorys() -> [str]:
    """Ask  user to enter 5 categorys and returns a list with the 5 names"""

    categorys = []
    for i in range(1, 6):
        categorys.append(ask_for_category(i))
    return categorys

def get_bound(category: str, bound: Bound) -> Number:
    """Ask user to enter a numberic bound for a category and returns it casted to `int` or `float`"""

    while True:
        num_bound = input(f"Introduce el límite {bound} para la categoría {category}: ").strip()
        if num_bound.isdigit():
            return int(num_bound)
        elif num_bound.isdecimal():
            return float(num_bound)
        else:
            print(f"El valor introducido no es un límite válido para {category}")

def get_bounds(category: str) -> (Number, Number):
    """Get lower and upper bounds for a category and returns it as a `tuple`"""

    while True:
        lower_bound = get_bound(category, "inferior")
        upper_bound = get_bound(category, "superior")
        if lower_bound < upper_bound:
            break
        else:
            print("El límite inferior debe ser más pequeño que el superior.")
    return (lower_bound, upper_bound)

def get_categorys_bounded_map(categorys: [str]) -> BoundedMap:
    """Creates a `map` where the key is the category `str` and the value is a `tuple` with the lower and upper bound"""

    ranged_categorys = {}
    for cat in categorys:
        ranged_categorys[cat] = get_bounds(cat)
    return ranged_categorys

def get_1000_regs_betwen_range(lower_bound: Number, upper_bound: Number) -> [Number]:
    """Creates 1000 numbers between `lower_boun` and `upper_bound` and returns them as a list"""

    data = []
    for i in range(0, 1000):
        data.append(random.randrange(lower_bound, upper_bound + 1))
    return data

def generate_data_map(bounded_map: BoundedMap) -> {str: [Number]}:
    """Returns a `dict` of whatever keys are in `bounded_map` and 1000 random `Number` list as value.

    Generate a `dict` with a key for every key in the `bounded_map` and 1000 long list of `Number`
    as the value of each of them
    """

    data_map = {}
    for category, range_tuple in bounded_map.items():
        data_map[category] = get_1000_regs_betwen_range(*range_tuple)
    return data_map

def save_as_json(filename:str, data: {str: [Number]}) -> NoReturn:
    """Creates an object by name = `filename` and sotres `data` in it as a json"""

    with open(filename, "w") as json_file:
        json_file.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    file_name = ask_for_file_name()
    print(f"Se creará el fichero: {file_name}")
    categorys = ask_5_categorys()
    bounded_categorys_map = get_categorys_bounded_map(categorys)
    data_map = generate_data_map(bounded_categorys_map)
    print(f"Se crearon 1000 registros para cada categoría y se guardarán en <{getcwd()}/{file_name}> ")
    save_as_json(file_name, data_map)