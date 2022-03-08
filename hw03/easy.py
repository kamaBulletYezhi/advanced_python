from typing import Iterable as t_Iterable
from collections.abc import Iterable
import numpy as np
from pretty_matrix import matrix_pretty_print
from operator import add, mul, eq


class Matrix:
    def __init__(self, obj: t_Iterable, *, dtype=None, frozen=False):
        def self_type(elem):
            return elem
        self.__dtype = self_type if dtype is None else dtype
        self.__frozen = frozen

        depth, self.__length = self._correct_shape_check(obj)

        container = tuple if frozen else list
        self.__shape = [0] * depth
        self.__data = self._build_matrix(obj, container)
        self.__shape = tuple(self.__shape)

    @property
    def dtype(self):
        return self.__dtype

    @property
    def frozen(self):
        return self.__frozen

    @property
    def length(self):
        return self.__length

    @property
    def shape(self):
        return self.__shape

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        """
        Увлекся, по хорошему надо реализовать get-/set-item
        """
        if not self.frozen:
            self.__data = value
        else:
            raise AttributeError("can't set attribute 'data'")

    def _correct_shape_check(self, obj: t_Iterable) -> tuple[int, int]:
        """

        :param obj:
            Подозреваемый
        :return depth, size:
            глубина (номер оси) и длина матрицы на этой глубине
        """

        if isinstance(obj, Iterable):
            size = None
            depth = None
            i = -1
            # Только цикл умеет работать с исключительно Iterable объектами.
            # Увы, len, getitem, slice, next -- не при делах.
            for i, sub_obj in enumerate(obj):
                d, s = self._correct_shape_check(sub_obj)
                if size is None:
                    size = s
                if depth is None:
                    depth = d

                if size != s or depth != d:
                    raise Exception("incorrect shape")
            if i == -1:
                raise Exception("empty cell")
            return depth+1, i+1
        else:
            return 0, 0

    def _build_matrix(self, obj: t_Iterable, container: type, depth: int = 0):
        if isinstance(obj, Iterable):
            data = container(self._build_matrix(sub_obj, container, depth + 1) for sub_obj in obj)
            self.shape[depth] = len(data)
        else:
            data = self.dtype(obj)
        return data

    def new_data(self, a, b, len_, bin_op, container, axis=0):
        if axis < len_:
            result = container(self.new_data(sub_a, sub_b, len_, bin_op, container, axis+1) for sub_a, sub_b in zip(a, b))
        else:
            result = bin_op(a, b)
        return result

    def bin_operate(self, other, bin_op):
        if self.shape != other.__shape:
            raise Exception('bad shapes')

        a, b = self.__data, other.__data
        len_ = len(self.shape)
        container = tuple if self.frozen else list
        res = self.new_data(a, b, len_, bin_op, container)
        return Matrix(res, dtype=self.dtype, frozen=self.frozen)

    def __add__(self, other):
        return self.bin_operate(other, add)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        if self.frozen:
            raise Exception('frozen matrix')
        new_self = self + other
        self.__data = new_self.__data
        return self

    def __mul__(self, other):
        return self.bin_operate(other, mul)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        if self.frozen:
            raise Exception('frozen matrix')
        temp = self * other
        self.__data = temp.__data
        return self

    def __matmul__(self, other):
        if len(self.shape) != 2 or len(other.__shape) != 2:  # тут я узнал, что матрица это не тензор
            raise Exception('only for 2d matrix')
        if self.shape[-1] != other.__shape[0]:
            raise Exception('bad shapes')

        a, b = self.__data, other.__data
        b_T = [[b[j][i] for j in range(other.__shape[0])] for i in range(other.__shape[-1])]
        res = [[sum(e1 * e2 for e1, e2 in zip(x, y)) for y in b_T] for x in a]
        return Matrix(res, dtype=self.dtype, frozen=self.frozen)

    def __rmatmul__(self, other):
        return self @ other

    def __imatmul__(self, other):
        if self.frozen:
            raise Exception('frozen matrix')
        temp = self @ other
        self.__data = temp.__data
        return self

    def __str__(self):
        return matrix_pretty_print(self.__data)

    def write_to_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(str(self))


if __name__ == "__main0__":
    np.random.seed(0)
    path = 'artifacts/easy/'
    file_name = 'matrix{0}.txt'
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    res_matrs: dict[str, Matrix] = {'+': a + b,
                                    '*': a * b,
                                    '@': a @ b}

    for op in res_matrs:
        res_matrs[op].write_to_file(path + file_name.format(op))


a = Matrix(np.random.randint(0, 10, (10, 10)))

a.data = [4]












