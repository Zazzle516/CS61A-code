from operator import add, sub

def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    >>> # a check that you didn't change the return statement!
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_plus_abs_b), re.M)
    ['return h(a, b)']
    """
    if b >= 0:
        h = add
    else:
        h = sub
    return h(a, b)


def two_of_three(x, y, z):
    """Return a*a + b*b, where a and b are the two smallest members of the
    positive numbers x, y, and z.

    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    >>> # check that your code consists of nothing but an expression (this docstring)
    >>> # a return statement
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    # list = [x,y,z]
    # a = min(x,y,z)
    # b = max(x,y,z)
    # c = a
    # for i in range(len(list)):
    #     if a == list[i] or b == list[i]:
    #         continue
    #     c = list[i]

    # a = min([x, y], [x, z], [y, z])
    # return add(a[0]*a[0],a[1]*a[1])

    return add(min([x, y], [x, z], [y, z])[0]*min([x, y], [x, z], [y, z])[0],min([x, y], [x, z], [y, z])[1]*min([x, y], [x, z], [y, z])[1])
    # 目前没想到更好的

def largest_factor(x):
    """Return the largest factor of x that is smaller than x.
    返回最大的（不包括自己）的因数
    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    "*** YOUR CODE HERE ***"
    factors = []
    for index in range(1,x):
        if(x % index == 0):
            factors.append(index)

    return factors[-1]


def if_function(condition, true_result, false_result):
    """Return true_result if condition is a true value, and
    false_result otherwise.

    >>> if_function(True, 2, 3)
    2
    >>> if_function(False, 2, 3)
    3
    >>> if_function(3==2, 3+2, 3-2)
    1
    >>> if_function(3>2, 3+2, 3-2)
    5
    """
    if condition:
        return true_result
    else:
        return false_result


def with_if_statement():
    """
    >>> result = with_if_statement()
    47
    >>> print(result)
    None
    """
    if cond():
        return true_func()
    else:
        return false_func()

def with_if_function():
    """
    >>> result = with_if_function()
    42
    47
    >>> print(result)
    None
    """
    return if_function(cond(), true_func(), false_func())

# 证明 if_statement 没有完全实现 if 的功能性 构思一个反例
# 1.可能是嵌套调用的影响吗 类似于 print() 返回值是 None
# tip: None和任何对象比较返回值都是False，除了自己   None 在 bool 判断中认为是 false

# cond() 在 if_function() 中是以 true / false 的形式传参的
def cond():
    "*** YOUR CODE HERE ***"
    return None

def true_func():
    "*** YOUR CODE HERE ***"
    return print(42)

def false_func():
    "*** YOUR CODE HERE ***"
    return print(47)




def hailstone(x):
    """Print the hailstone sequence starting at x and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    list = []
    list.append(x)
    print(x)
    while(x != 1):
        if(x % 2 == 0):
            x = x / 2
            print('%d' %x)
        else:
            x = x * 3 + 1
            print('%d' %x)
        list.append(x)
    return len(list)