from quasis.prime import factors

def proper_factors(n):
    facts = list()
    for i in range(1, n + 1):
        if n % i == 0:
            facts.append(i)
    return facts

def sigma(n):
    s = 0
    for i in proper_factors(n):
        s += i
    return s

def h(n):
  return sigma(n)/n

def mu(n):
    facts = factors(n)
    for p in facts:
        if facts[p] > 1:
            return 0
    if len(facts) % 2 == 0:
        return 1
    else:
        return -1
