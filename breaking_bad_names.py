# Script to do Breaking Bad credits with names,
# replacing letters with periodic table elements
# Gets total possibilities, gets replaces, and elements name contains
import re
import time

import pandas as pd

beginTime = time.perf_counter()
name = "Joseph Palombo"

periodicTable = pd.read_csv("data/periodic_table.csv")
symbolMap = dict(zip(periodicTable["Symbol"].str.lower(), periodicTable["Element"]))
possibleSymbols = set()
possibleNames = 0
# One letter at a time
for letter in name:
    if letter.lower() in symbolMap:
        possibleSymbols.add(letter.lower())

# 2 letter elements
for letters in zip(name, name[1:]):
    bothLetters = letters[0].lower() + letters[1].lower()
    if bothLetters in symbolMap:
        possibleSymbols.add(bothLetters)

print(f"{'Symbol':<6} | {'Element':<12} | {'# Of Occur':<10} | {'Modified Name':<20}")
fullName = name.lower()
for symbol in possibleSymbols:
    occurIndices = [i.start() for i in re.finditer(symbol, fullName)]
    for occurance, index in enumerate(occurIndices):
        creditName = fullName[:index] + symbol.upper() + fullName[index + len(symbol) :]
        possibleNames += 1
        print(
            f"{symbol.capitalize():<6} | {symbolMap[symbol]:<12} | {occurance:<10} | {creditName:<20}"
        )

print(
    f"{name} has {possibleNames} possible modified names with elements:\n{[symbolMap[symbol] for symbol in set(possibleSymbols)]}"
)
performTime = time.perf_counter() - beginTime
print("Took", performTime, "seconds")
