def matrix_pretty_print(matr):
    """
    Писал для какой-то старой домашки (не судите строго),
    почему бы не преиспользовать код.
    """
    result = ''
    n = len(matr)
    m = len(matr[0])
    size = 0
    for row in matr:
        for el in row:
            size = max(size, len(str(el)))
    size += 1
    result += '  {} \n'.format(' '.join([str(num).center(size) for num in range(m)]))
    result += ' ┌{}┐\n'.format('┬'.join(['─'*size]*m))
    for i, row in enumerate(matr[:-1]):
        result += '{}│{}│\n'.format(i, '│'.join([str(num).center(size) for num in row]))
        result += ' ├{}┤\n'.format('┼'.join(['─'*size]*m))
    result += '{}│{}│\n'.format(i + 1, '│'.join([str(num).center(size) for num in matr[-1]]))
    result += ' └{}┘'.format('┴'.join(['─'*size]*m))
    return result
