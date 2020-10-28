"""

file: read_file.py
language: python3.7
author: Shantanav Saurav << ss9415@g.rit.edu >>
purpose: Read File function

"""
import sys


def read_file(filename: str) -> dict:
    """
    Read URLs file into memory as dictionary
    ----Pre Conditions:
    filename -> str: String of filename
    ----Post Conditions:
    return -> dict: Dictionary of patch_number : URL
    """
    dct = dict()
    with open(filename) as f:
        for line in f:
            line = line.strip().split(": ")
            dct[line[0].lower()] = line[1]
    return dct


if __name__ == "__main__":
    dct = read_file(sys.argv[1])
    for key in dct:
        print(key + ": " + dct[key])
