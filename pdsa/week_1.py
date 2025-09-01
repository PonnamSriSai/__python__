'''
week 1 of pdsa course
1. computing GCD or HCF
    a. naive method
    b. using - operator and division operator properties
    c. using euclid's algo(% modulo operator)
    
2. computing primes upto n in an efficient way

3. Exceptions, Classes and Objects
    - to create a Timer class to calculate the performance time of algorithms in future of this course.
    
'''

from math import isqrt
from time import perf_counter

def gcd_naive(a : int, 
              b : int) -> int:
    '''computes the gcd naively'''
    if a == 0 or b == 0:    # handles the 0 inputs 
        return max(abs(a), abs(b))
    gcd = 1
    for i in range(1, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            gcd = i
    return gcd

def gcd_subtraction(a : int,
                    b : int) -> int:
    '''computes the gcd using subtraction method'''
    if a == 0:
        return b
    if b == 0:
        return a
    
    while a != b: 
        if a > b:
            a -= b
        else:
            b -= a
    
    return a
        
def gcd_euclid(a : int,
               b : int) -> int:
    '''computes the gcd using euclid's algo'''
    while b:
        a, b = b, a % b
        
    return a

def primes_upto(n : int) -> list[int]:
    '''returns a list of primes upto n'''
    if n < 2:
        return []
    
    primes = []
    
    def is_prime(n : int) -> bool:
        '''checks a number is prime or not'''
        limit = isqrt(n)
        for prime in primes:    # only check with known primes upto n
            if prime > limit:  # stop at sqrt(n)
                break
                
            if n % prime == 0:  # if divisible by any known prime then it is not a prime
                return False

        return True
    
    for num in range(2, n + 1):
        if is_prime(num):
            primes.append(num)
            
    return primes


class TimerError(Exception):
    """A custom exception used to raise errors occured in Timer class"""
    pass

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None
    
    def start(self):
        '''starts the timer'''
        if self.start_time:
            raise TimerError('timer is alredy started...')
            
        self.start_time = perf_counter()
    
    def stop(self):
        '''stops the timer...'''
        if self.start_time is None:
            raise TimerError('timer is not yet started...')
            
        self.elapsed_time = perf_counter() - self.start_time
        self.start_time = None
    
    def elapsed(self):
        '''returns the elapsed time'''
        if self.elapsed_time is None:
            raise TimerError('timer is not yet started...')
            
        return self.elapsed_time
    
    def __str__(self):
        return f'{self.elapsed_time : 0.6f} sec'
    



if __name__ == "__main__":
    from math import gcd as math_gcd
    
    def test_gcd_functions():
        cases = [
            (0, 0),
            (0, 5),
            (5, 0),
            (1, 1),
            (18, 24),
            (100, 25),
            (17, 13),   # both primes
            (270, 192), # gcd = 6
        ]
        for a, b in cases:
            expected = math_gcd(a, b)
            assert gcd_naive(a, b) == expected, f"Failed gcd_naive({a}, {b})"
            assert gcd_subtraction(a, b) == expected, f"Failed gcd_subtraction({a}, {b})"
            assert gcd_euclid(a, b) == expected, f"Failed gcd_euclid({a}, {b})"
        print("GCD tests passed!")


    def test_primes():
        assert primes_upto(1) == []
        assert primes_upto(2) == [2]
        assert primes_upto(10) == [2, 3, 5, 7]
        assert primes_upto(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        primes_100 = primes_upto(100)
        assert len(primes_100) == 25
        assert primes_100[0] == 2
        assert primes_100[-1] == 97
        print("Prime tests passed!")


    def test_timer():
        t = Timer()
        t.start()
        x = sum(range(1000))  # some work
        t.stop()
        assert t.elapsed() >= 0
        print(f"Timer basic test passed! Elapsed = {t.elapsed():.6f} seconds")

        # Error cases
        t2 = Timer()
        try:
            t2.stop()
        except TimerError:
            print("TimerError correctly raised when stopping before start")

        try:
            t2.elapsed()
        except TimerError:
            print("TimerError correctly raised when elapsed before start")

        t2.start()
        try:
            t2.start()
        except TimerError:
            print("TimerError correctly raised when starting twice")
        t2.stop()

    test_gcd_functions()
    test_primes()
    test_timer()
    print("\nAll tests passed!")
    
    print('\ncomparing the performances of different gcd fun')
    a, b = 12345699, 987654321

    funcs = [("Naive", gcd_naive), ("Subtraction", gcd_subtraction), ("Euclid", gcd_euclid)]
    for name, func in funcs:
        t = Timer()
        t.start()
        result = func(a, b)
        t.stop()
        print(f"{name:<12}: gcd={result}, time={t.elapsed():.6f} seconds")
    
 
    
    


