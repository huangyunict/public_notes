def naive_pow(a, n, m):
    result = 1
    for i in range(0, n):
        result = result * a % m
    return result


def recursive_pow(a, n, m):
    if n == 0:
        return 1
    r = recursive_pow(a, n // 2, m)
    r = r * r % m
    return r if n % 2 == 0 else r * a % m


def iterative_pow(a, n, m):
    b = a % m
    result = 1
    while n > 0:
        if n & 1 == 1:
            result = result * b % m
        b = b * b % m
        n = n >> 1
    return result


def prime_pow(a, n, m):
    if a % m == 0:
        return 0
    return iterative_pow(a, n % (m - 1), m)


def test_one(method, a, n, m, expected):
    tested = method(a, n, m)
    result = 'Passed' if tested == expected else 'Failed'
    n_str = str(n) if n < pow(2, 64) else '...'
    print('{}: {}({},{},{})={}, expected={}'.format(result, method.__name__, a, n_str, m, tested, expected))


if __name__ == '__main__':
    # Case 1.
    test_one(pow, 3, 4, 11, 4)
    test_one(naive_pow, 3, 4, 11, 4)
    test_one(recursive_pow, 3, 4, 11, 4)
    test_one(iterative_pow, 3, 4, 11, 4)
    test_one(prime_pow, 3, 4, 11, 4)
    # Case 2.
    test_one(pow, 3, 100, 11, 1)
    test_one(naive_pow, 3, 100, 11, 1)
    test_one(recursive_pow, 3, 100, 11, 1)
    test_one(iterative_pow, 3, 100, 11, 1)
    test_one(prime_pow, 3, 100, 11, 1)
    # Case 3.
    big_n = pow(7, 2000)
    test_one(pow, 3, big_n, 19, 14)
    test_one(iterative_pow, 3, big_n, 19, 14)
    test_one(prime_pow, 3, big_n, 19, 14)
    # Case 4.
    big_n = pow(2, pow(2, 20))
    test_one(pow, 3, big_n, 19, 17)
    test_one(prime_pow, 3, big_n, 19, 17)
    test_one(iterative_pow, 3, big_n, 19, 17)
