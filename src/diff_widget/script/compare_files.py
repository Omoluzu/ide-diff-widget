from difflib import SequenceMatcher


def compare_files(lines1, lines2, sequence_percent: int = 80):
    """Сравнивает два файла и выводит различия в формате git diff."""
    index1 = index2 = 0

    while True:
        try:
            line1 = lines1[index1]
        except IndexError:
            if index2 <= len(lines2):
                break

            line2 = lines2[index2]
            print(index2 + 1, '-', '-', line2, end='')
            index2 = index2 + 1
            continue

        try:
            line2 = lines2[index2]
        except IndexError:
            print(index1 + 1, '-', '-', line1, end='')
            if index1 + 1 != len(lines1):
                index1 = index1 + 1
                continue
            break

        if line1 == line2:
            print(index1 + 1, index2 + 1, line1, end='')
            index1, index2 = index1 + 1, index2 + 1
            continue

        percentage_match = SequenceMatcher(None, line1, line2).ratio() * 100
        if percentage_match > sequence_percent:
            print(index1 + 1, index2 + 1, '+/-', line1.replace('\n', ''), line2.replace('\n', ''))
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
                                print('-', index2 + iii2, '+', lines2[index2 + iii2].replace('\n', ''))
                            for iii1 in range(ii1):
                                print(index1 + iii1, '-', '-', lines1[index1 + iii1].replace('\n', ''))
                            index1, index2 = index1 + ii1, index2 + ii2
                            raise StopIteration

                index = index + 1
        except StopIteration:
            continue
