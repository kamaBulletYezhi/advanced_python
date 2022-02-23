from hw03.easy import Matrix
import numpy as np
np.random.seed(0)

class MatrixHashMixin:
    """
    Извините.
    """
    def __hash__(self):
        if not self.frozen:
            raise Exception('mutable object!!!')
        return hash(str(self))


class HashableMatrix(Matrix, MatrixHashMixin):
    pass


if __name__ == "__main__":
    """
    Я не смог найти коллизии :(
    """

