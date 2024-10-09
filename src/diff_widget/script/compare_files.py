from difflib import SequenceMatcher


def compare_files(
        lines1,
        lines2,
        func_equals,
        func_modified,
        func_remove,
        func_added,
        sequence_percent: int = 80,
):
    """Сравнивает два файла и выводит различия в формате git diff."""
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

        percentage_match = SequenceMatcher(None, line1, line2).ratio() * 100
        if percentage_match > sequence_percent:
            func_modified(index1, index2, line1, line2)
            index1, index2 = index1 + 1, index2 + 1
            continue

        index = 1
        try:
            while True:
                for ii2 in range(index + 1):
                    for ii1 in range(index + 1):
                        percentage_match = SequenceMatcher(None, lines1[index1 + ii1], lines2[index2 + ii2]).ratio() * 100
                        if percentage_match > sequence_percent:
                            for iii2 in range(ii2):
                                func_added(index2 + iii2, lines2[index2 + iii2])
                            for iii1 in range(ii1):
                                func_remove(index1 + iii1, lines1[index1 + iii1])
                            index1, index2 = index1 + ii1, index2 + ii2
                            raise StopIteration

                index = index + 1
        except StopIteration:
            continue
