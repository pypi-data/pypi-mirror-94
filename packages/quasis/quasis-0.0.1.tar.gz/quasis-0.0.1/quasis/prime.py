import math

def is_prime(n):
    for i in range(2, round(math.sqrt(n)) + 1):
        if n % i == 0:
            return False 
    return True

def get_primes(n):

    i = 0
    j = 2

    primes = list()

    while i != n:
        if is_prime(j):
            primes.append(j)
            i += 1
        j += 1
    
    return primes

def factors(n):
    facts = dict()
    i = 2
    while True:
        if n % i == 0:
            if i in facts:
                facts[i] += 1
            else:
                facts[i] = 1
            n /= i
            i = 2
        else:
            i += 1

        if n == 1:
            break 
        
    return facts