def fibonacci(n: int):
    if type(n) is not int:
        print(f'{int(n)} is used')
        n = int(n)
    if n < 0:
        raise ValueError('n < 0')
    if n < 2:
        return n
    prev = 0
    curr = 1
    for i in range(1, n):
        prev, curr = curr, prev+curr
    return curr
