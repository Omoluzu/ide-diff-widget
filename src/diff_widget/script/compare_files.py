from difflib import SequenceMatcher
from typing import Callable


def compare_files(
        lines1: list[str],
        lines2: list[str],
        func_equals: Callable[[int, int, str], None],
        func_modified: Callable[[int, int, str, str], None],
        func_remove: Callable[[int, str], None],
        func_added: Callable[[int, str], None],
        sequence_percent: float = .8,
) -> None:
    """Compares two files and outputs the differences in git diff format.

    The matches found are passed to the corresponding passed functions

    :param lines1: Contents of the list with file lines
    :param lines2: Contents of the list with file lines
    :param func_equals: Function if equality is found
    :param func_modified: Function if the percentage of changes specified in
        sequence_percent is found
    :param func_remove: Function if delete row
    :param func_added: Function if added row
    :param sequence_percent: Finding the percentage of matches where 1 is 100%
    """
    index1 = index2 = 0

    while True:
        try:
            line1 = lines1[index1]
        except IndexError:
            if index2 >= len(lines2):
                break

            func_added(index2 + 1, lines2[index2])
            index2 = index2 + 1
            continue

        try:
            line2 = lines2[index2]
        except IndexError:
            func_remove(index1 + 1, line1)
            if index1 + 1 != len(lines1):
                index1 = index1 + 1
                continue
            break

        if line1 == line2:
            func_equals(index1, index2, line1)
            index1, index2 = index1 + 1, index2 + 1
            continue

        percentage_match = SequenceMatcher(None, line1, line2).ratio()
        if percentage_match >= sequence_percent:
            func_modified(index1, index2, line1, line2)
            index1, index2 = index1 + 1, index2 + 1
            continue

        index = 1
        try:
            while True:
                for ii2 in range(index + 1):
                    for ii1 in range(index + 1):
                        percentage_match = SequenceMatcher(None, lines1[index1 + ii1], lines2[index2 + ii2]).ratio()
                        if percentage_match >= sequence_percent:
                            for iii2 in range(ii2):
                                func_added(index2 + iii2, lines2[index2 + iii2])
                            for iii1 in range(ii1):
                                func_remove(index1 + iii1, lines1[index1 + iii1])
                            index1, index2 = index1 + ii1, index2 + ii2
                            raise StopIteration

                index = index + 1
        except StopIteration:
            continue
