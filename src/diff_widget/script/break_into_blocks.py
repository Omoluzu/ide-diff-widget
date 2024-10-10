def accumulate_result():
    old_info = None

    new_result = {
        'block_id': {}
    }
    block_id = 0

    while True:
        info = yield
        if info is None:
            return new_result

        if not old_info:
            new_result['block_id'][0] = info

        if old_info and (info - old_info) != 1:
            block_id += 1
            new_result['block_id'][block_id] = info

        new_result[info] = {'block_id': block_id}
        old_info = info


def gather_result(tallies):
    while 1:
        tally = yield from accumulate_result()
        tallies.update(tally)


def break_into_blocks(blocks: list[int]):
    results = {}
    acc = gather_result(results)
    next(acc)

    for i in blocks:
        acc.send(i)

    acc.send(None)

    return results