# Script to do Breaking Bad credits with names,
# replacing letters with periodic table elements
# Gets total possibilities, gets replaces, and elements name contains
import re
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd  # type: ignore


def n_letter_substrings(
    n: int,
    name: str,
    symbols: List[str],
) -> set[str]:
    """Get n-letter consecutive substrings from word ,or ngrams, then return ngrams that occur in list of symbols.
    e.g. name = "joey", n=1 ngrams=[j,o,e,y], n=2 ngrams=[jo,oe,ey], n=3 [joe,oey] n=4 [joey]

    Args:
        n (int) : Length of substrings or ngrams to compose and test.
        name (str): name to test
        symbols (List[str]): List of symbols to see if substrings occur in list.

    Returns:
        set[str]: Unique list of substrings from name in symbols
    """
    return set(
        name[idx : idx + n]
        for idx in range(0, len(name) + 1 - n)
        if name[idx : idx + n] in symbols
    )


def get_elements(name: str, symbols: List[str]) -> set[str]:
    """
    Get all periodic table elements in name. Do this by getting 1 letter periodic table unique elements in name,
    then two letter unique elements in name.

    Args:
        name (str): Name to test which periodic elements occur in it.
        symbols (List[str]): List of periodic table symbols to check if name contains any of them.

    Returns:
        set[str]: Unique list of substrings from name in symbols
    """
    name = name.lower()
    one_letter_occur = n_letter_substrings(n=1, name=name, symbols=symbols)
    two_letter_occur = n_letter_substrings(n=2, name=name, symbols=symbols)
    return one_letter_occur.union(two_letter_occur)


def output_names(
    name: str, possible_symbols: set[str], symbol_map: Dict[str, str]
) -> None:
    """Output all possible name variations using the possible positions and one or more positions in name where symbol occurs.
    Iterate through all indices where symbol begins in name, at each occurance chop up name string by prefix capitalized symbol and suffix.

    e.g. name joseph palos, for possible symbol Os (Osmium), find start indices which are [1 for group [1-2] and 10 for group [10-11]]
    then for each occurance construct name with name[:1] + symbol.upper() + name[1+2:] which is j + OS + eph palos = jOSeph palos
    and name[:10] + symbol.upper() + name[10+2:] which is joseph pal + OS  = joseph palOS

    Args:
        name (str): name to test
        possible_symbols (set[str]): _description_
        symbol_map (Dict[str, str]): _description_
    """
    full_name = name.lower()
    print(
        f"{'Symbol':<6} | {'Element':<12} | {'# Of Occur':<10} | {'Modified Name':<20}"
    )
    possible_names = 0
    for symbol in possible_symbols:
        occur_indices = [i.start() for i in re.finditer(symbol, full_name)]
        for occurance, index in enumerate(occur_indices):
            credit_name = (
                full_name[:index] + symbol.upper() + full_name[index + len(symbol) :]
            )
            possible_names += 1
            print(
                f"{symbol.capitalize():<6} | {symbol_map[symbol]:<12} | {occurance:<10} | {credit_name:<20}"
            )

    print(
        f"{name} has {possible_names} possible modified names with elements:\n{[symbol_map[symbol] for symbol in possible_symbols]}"
    )


def main():
    """Main function."""
    NAME = "Joseph Palombo"
    CSV_PATH = Path("data") / "periodic_table.csv"

    periodic_table = pd.read_csv(CSV_PATH)
    symbols = periodic_table["Symbol"].str.lower().tolist()
    symbol_map: Dict[str, str] = dict(zip(symbols, periodic_table["Element"]))

    possible_symbols = get_elements(name=NAME, symbols=symbols)
    output_names(name=NAME, possible_symbols=possible_symbols, symbol_map=symbol_map)


if __name__ == "__main__":
    begin_time = time.perf_counter()
    main()
    perform_time = time.perf_counter() - begin_time
    print(f"Took {perform_time} seconds")
