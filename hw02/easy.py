"""
Извините, но я не догадался,
как красивее на питоне сделать это задание в стиле ФП.
Надеюсь, map() и max() это не читерство.

"""
path = 'artifacts/easy/'
file_name = 'table01.tex'
hardcode_table = [
    ['1345', '2', '3444'],
    ['4', '5', '635534'],
    ['7', '8', '9']
]


def max_cell_len(table: list[list]) -> int:
    def max_len_in_line(line: list) -> int:
        return len(max(map(str, line), key=len))
    return max(map(max_len_in_line, table))


def f_elem(sz: int):
    def inner(elem):
        return f'{elem: ^{sz}}'
    return inner


def wrap_line(cell_len: int):
    def inner(line: list) -> str:
        return '&'.join(
            map(f_elem(cell_len), line)
        ) + r"\\ \hline" + '\n'
    return inner


def make_tex_table(table: list[list], align: str = 'c') -> str:
    """

    :param table:
    :param align: str
        Параметр выравнивания.
        Возможные значения: 'l', 'r', 'c'.
    :return: str
        LaTex таблица
    """
    return ''.join((
        '\\begin{table}\n\\begin{tabular}{|',
        (align + '|') * len(table[0]),
        '}\n\\hline\n',
        ''.join(map(wrap_line(max_cell_len(table)+2), table)),
        '\\end{tabular}\n\\end{table}\n'
    ))


with open(path + file_name, 'w') as tex_file:
    tex_file.write(make_tex_table(hardcode_table))
