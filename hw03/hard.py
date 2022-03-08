from hw03.easy import Matrix
import numpy as np


class MatrixHashMixin:
    def __hash__(self):
        def mul(rows):
            res = 1
            for x in rows:
               res *= x
            return res

        if not self.frozen:
            raise Exception('mutable object!!!')

        return mul(sum(row) for row in self.data)


class HashableMatrix(Matrix, MatrixHashMixin):
    cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key not in self.cache:
            self.cache[key] = super().__matmul__(other)
        return self.cache[key]


if __name__ == "__main__":
    file_name = 'artifacts/hard/{0}.txt'
    a_ = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [3, 2, 1]
    ])
    b_ = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 1]
    ])
    c_ = np.array([
        [4, 5, 6],
        [1, 2, 3],
        [3, 2, 1]
    ])
    a = HashableMatrix(a_, dtype=int, frozen=True)
    b = HashableMatrix(b_, dtype=int, frozen=True)
    c = HashableMatrix(c_, dtype=int, frozen=True)
    d = HashableMatrix(b_, dtype=int, frozen=True)

    a.write_to_file(file_name.format('A'))
    b.write_to_file(file_name.format('B'))
    c.write_to_file(file_name.format('C'))
    d.write_to_file(file_name.format('D'))
    (a @ b).write_to_file(file_name.format('AB'))
    (c @ d).write_to_file(file_name.format('CD'))
    with open(file_name.format('hash'), 'w') as file:
        file.write(f'hash(AB) = {hash(a @ b)}\nhash(CD) = {hash(c @ d)}')