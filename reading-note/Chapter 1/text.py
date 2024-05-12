result = max(min(1, -2), min(pow(3, 5), -4))
print(result)

from math import sqrt, exp

print(sqrt(256))
print(exp(1))

from operator import *

print(add(1, 2))

print(print(1), print(2))  # 这个比较有意思欸

def square(x):
    return mul(x,x)
a = square(3)
print(a)

user_func = square
print(square)
print(user_func)

print(7 % 6)