from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count
import math
from datetime import datetime
import time
import random
cpu_count = cpu_count()

n_jobs = 2 * cpu_count
n_iter = 10**4


def log_and_run(args):
    x, i, f = args
    log_and_run.buffer += f'task number {i} out of {n_iter} was started at {datetime.now()} with {n_jobs} jobs\n'
    return f(x)


log_and_run.buffer = ''


def piece_integrate(f, a, b, *, n_jobs=1, n_iter=1000, Executor=ThreadPoolExecutor):
    step = (b - a) / n_iter
    args_list = ((a + i * step, i, f) for i in range(n_iter))
    with Executor(max_workers=n_jobs) as executor:
        result = step * sum(executor.map(log_and_run, args_list))
    with open('artifacts/medium_log.txt', 'a') as file:
        file.write(log_and_run.buffer)
    log_and_run.buffer = ''
    return result


for n_jobs in range(1, 2 * cpu_count + 1):
    start = time.time()
    piece_integrate(math.cos, 0, math.pi/2, n_jobs=n_jobs, n_iter=n_iter)
    stop = time.time()

    with open('artifacts/medium_compare.txt', 'a') as file:
        file.write(f'n_jobs = {n_jobs}, time = {stop-start}\n')


