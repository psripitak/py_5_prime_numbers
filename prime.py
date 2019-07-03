import time
import multiprocessing as mp
from sys import argv
from math import sqrt, floor, ceil

# File: prime.py
# Author: Pete Sripitak
# This program computes the number of prime numbers between
#   specified low and high values, inclusive.
#   It divides the range of work as evenly as possible among the
#   worker processes.

def worker_bee(low, high, q):
    list_primes = []
    if (low % 2) == 0:
        low -= 1
    for i in range(low, high, 2):
        not_prime = False
        eratosthenes = ceil(sqrt(i)) + 1
        for j in range(2, eratosthenes):
            if (i % j) == 0:
                not_prime = True
                break
        if not not_prime:
            list_primes.append(i)
    num_prime = len(list_primes)
    #print(mp.current_process().name, low, high, num_prime)
    q.put(num_prime)
#    s = 0
#    for n in range(a, b):
#        s += n
#    print(mp.current_process().name, a, b-1, s)
#    q.put(s)

#print("cpu_count: ",mp.cpu_count())  ## just for demo

procs = []
q = mp.Queue()
low = int(argv[1])
high = int(argv[2]) + 1
n = int(argv[3])

if (low % 2) == 0:
    low += 1

#big_number = int(argv[2])
#chunk = int(big_number / n)
mid = high - low
chunk = ceil(mid / n)
#print(mid, chunk)
lo = low
hi = high
#print(lo,hi)
for i in range(n):
    if i == 0:
        lo = low
        hi = low + chunk - 1
        if n == 1:
            hi = high
        #print(lo,hi, 'first')
        p = mp.Process(target=worker_bee, args=(lo,hi,q))
        procs.append(p)
    if i > 0:
        lo = hi + 1
        hi = lo + chunk - 1
        if hi > (high - 2):
            hi = high
        #print(lo,hi)
        p = mp.Process(target=worker_bee, args=(lo,hi,q))
        procs.append(p)


startTime = time.time()
for p in procs:
    p.start()

for p in procs:
    p.join()

print()
print( "Time: %0.4f" % (time.time() - startTime) )

s = 0
for p in procs:
    s += q.get()

print('Total number of prime: ', s)
print()
