# from operator import add, sub
# def a_plus_abs_b(a,b):
#     if b >= 0:
#         h = add
#     else:
#         h = sub
#     # 返回函数的这个思路我真的没见过 太厉害了
#     return h(a,b)
#
# if __name__ == '__main__':
#     a = 3
#     b = -4
#     result = a_plus_abs_b(a,b)
#     print(result)

# python 的 input() 会把接受的数据视为字符串 在 line_4 (b >= 0) 会显示类型不同无法比较
# 至于怎么才能改，还没有想到

# print(bool(None))
# 0 1 1 2 3 5 8 13 ...

# -------------------------------- #
# a = 8
# k = 2   # the start pos of Fib
# pred = 0
# curr = 1
# while(k < a):
#     k += 1
#     new_value = pred + curr
#     pred = curr
#     curr = new_value
# print(curr)
# -------------------------------- #
# pred, curr = 0, 1
# k = 2
# n = 8
# while k < n:
#     pred, curr = curr, pred + curr
#     k = k + 1
# print(curr)
# -------------------------------- #

"""
This is the "example" module.

The example module supplies one function, factorial().  For example,

>>> factorial(5)
120
"""

def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    If the result is small enough to fit in an int, return an int.
    Else return a long.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n too large
    """

#     import math
#     if not n >= 0:
#         raise ValueError("n must be >= 0")
#     if math.floor(n) != n:
#         raise ValueError("n must be exact integer")
#     if n+1 == n:  # catch a value like 1e300
#         raise OverflowError("n too large")
#     result = 1
#     factor = 2
#     while factor <= n:
#         result *= factor
#         factor += 1
#     return result
#
#
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()

# def how_big(x):
#     if x > 10:
#         print('huge')
#     elif x > 5:
#         return 'big'
#         # return "big"
#     elif x > 0:
#         print('small')
#     else:
#         print("nothin'")
#
# if __name__ == "__main__":
#     print(how_big(7))

# print(True and 13)

# def double_eights(n):
#     if(n < 10):
#         return False
#     list = []
#     while(n > 0):
#         list.append(n % 10)
#         n = n // 10
#     for i in range(len(list)):
#         if(list[i] == 8):
#             if(list[i+1] == 8):
#                 return True
#             i += 1
#     return False
#
# if __name__ == "__main__":
#     print(double_eights(88))

f = abs
g = min
x = [1,2,-1,-2]
res1 = f(g(x))
print("res1:",res1)

# res2 等效于一个函数指针
fun2 = lambda f,g: lambda x: print("fun2:",f(g(x)))
res2 = fun2(f,g)
print("res2:",res2)
print("res2_x:",res2(x))

fun4 = lambda f,g: lambda x: f(g(x))
res4 = fun4(f,g)
print("res4:",res4)
print("res4_x:",res4(x))

# 显示传参出错 传递顺 序不能改变 只能由外往里面传递
# fun5 = lambda f,g: lambda x: f(g(x))
# res5 = fun5(f,g)(x)
# print("res5:",res5)
# print("res5_x:",res5(f,g))

fun3 = lambda f,g: print("fun3:",f(g(1,2,-1,-2)))
res3 = fun3(f,g)
print("res3:",res3)

