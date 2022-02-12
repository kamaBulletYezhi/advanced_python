def fibonacci(n: int):
    if type(n) is not int:
        print(f'{int(n)} is used')
        n = int(n)
    if n <= 0:
        raise ValueError('n <= 0')
    prev = 0
    curr = 1
    yield curr
    for i in range(1, n):
        prev, curr = curr, prev+curr
        yield curr

