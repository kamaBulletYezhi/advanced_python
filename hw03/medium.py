from numpy.lib.mixins import NDArrayOperatorsMixin as NumpyMixin
import numpy as np
from hw03.pretty_matrix import matrix_pretty_print


class TrivialMatrixMixin:
    def __init__(self, data: np.ndarray):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class PrettyMatrixMixin:
    def __str__(self):
        return matrix_pretty_print(self.data)


class FileMatrixMixin:
    def write_to_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(str(self))


class Matrix(TrivialMatrixMixin, PrettyMatrixMixin, FileMatrixMixin, NumpyMixin):
    _HANDLED_TYPES = (np.ndarray,)

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):
        for x in args:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        return Matrix(getattr(ufunc, method)(
            *(x.__data for x in args),
            **kwargs
        ))


if __name__ == "__main__":
    np.random.seed(0)
    path = 'artifacts/medium/'
    file_name = 'matrix{0}.txt'
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    res_matrs: dict[str, Matrix] = {'+': a + b,
                                    '*': a * b,
                                    '@': a @ b}

    for op in res_matrs:
        res_matrs[op].write_to_file(path + file_name.format(op))

