from hw01.easy import f
import threading
import multiprocessing
import time
N = 15 * 10 ** 4


def timer(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    stop = time.time()
    return stop-start


def fib_10(n):
    for _ in range(10):
        f(n)


def fib_tread_or_proc(n, Executor: type):
    threads = tuple(Executor(target=f, args=(n,)) for _ in range(10))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    usual = timer(fib_10, N)
    threaded = timer(fib_tread_or_proc, N, threading.Thread)
    multiproc = timer(fib_tread_or_proc, N, multiprocessing.Process)
    with open('artifacts/easy.txt', 'w') as file:
        file.write(f'usual: {usual}\n')
        file.write(f'with threading: {threaded}\n')
        file.write(f'with multiprocessing: {multiproc}\n')


main()
