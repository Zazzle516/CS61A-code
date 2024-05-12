HW_SOURCE_FILE=__file__


def composer(func=lambda x: x):
    """
    Returns two functions -
    one holding the composed function so far, and another
    that can create further composed problems.
    >>> add_one = lambda x: x + 1
    >>> mul_two = lambda x: x * 2

    >>> f, func_adder = composer()
    >>> f1, func_adder = func_adder(add_one)
    >>> f1(3)
    4
    >>> f2, func_adder = func_adder(mul_two)
    >>> f2(3) # should be 1 + (2*3) = 7
    7
    >>> f3, func_adder = func_adder(add_one)
    >>> f3(3) # should be 1 + (2 * (3 + 1)) = 9
    9
    """
    # composer 传递的参数默认最底层是 f(x) = x 
    # 实际要保存的只有 func_addr() 这个问题的层数应该是体现在了复合函数 
    def func_adder(g):
        "*** YOUR CODE HERE ***"
        def composed_func(x): return func(g(x))
        return composer(composed_func)
    return func, func_adder


def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'g', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if(n <= 3):
        return n
    else:
        return g(n - 1) + 2 * g(n - 2) + 3 * g(n - 3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.

    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    >>> from construct_check import check
    >>> # ban recursion
    >>> check(HW_SOURCE_FILE, 'g_iter', ['Recursion'])
    True
    """
    "*** YOUR CODE HERE ***"
    if(n <= 3):
        return n
    
    start = 1
    third = start
    second = 2
    first = 3

    new = 0
    count = 3
    while(count < n):
        new = 1 * first + 2 * second + 3 * third
        third = second
        second = first
        first = new
        count += 1
    return new




def missing_digits(n):
    """Given a number a that is in sorted, increasing order,
    return the number of missing digits in n. A missing digit is
    a number between the first and last digit of a that is not in n.
    >>> missing_digits(1248) # 3, 5, 6, 7
    4
    >>> missing_digits(1122) # No missing numbers
    0
    >>> missing_digits(123456) # No missing numbers
    0
    >>> missing_digits(3558) # 4, 6, 7
    3
    >>> missing_digits(35578) # 4, 6
    2
    >>> missing_digits(12456) # 3
    1
    >>> missing_digits(16789) # 2, 3, 4, 5
    4
    >>> missing_digits(19) # 2, 3, 4, 5, 6, 7, 8
    7
    >>> missing_digits(4) # No missing numbers between 4 and 4
    0
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'missing_digits', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    # 因为不知道数字的大小 只能反向求 
    last_num = n % 10
    n = n // 10
    def sub_fun():
        if(n == 0 or last_num == 0):
            return 0
        if(last_num -1 > n % 10):
            return (last_num - n % 10 - 1) + missing_digits(n)
        return missing_digits(n)
    return sub_fun()


def count_change(total):
    """Return the number of ways to make change for total.

    >>> count_change(7)
    6
    >>> count_change(10)
    14
    >>> count_change(20)
    60
    >>> count_change(100)
    9828
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_change', ['While', 'For'])
    True
    """
    # ----------------------------------------------- #

    if(total >= 16):
        return count_single(16,total)
    if(total >= 8):
        return count_single(8,total)
    if(total >= 4):
        return count_single(4,total)
    if(total >= 2):
        return count_single(2,total)
    else:
        return 1

    # import math
    # return count_single(pow(2, round(math.log2(total))),total)

def count_single(start_unit , total):
    # 必须包含对应的 start_unit 
    if(start_unit == 1 or total == 0):
        return 1
    if(total < 0):
        return 0
    return count_single(start_unit // 2 ,total) + count_single(start_unit,total - start_unit)
    

def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"
    # 前 (n - 1) 个圆盘移动到 temp 第 n 个移动到 end 
    
    temp = 0
    if((start == 1 and end == 2) or (start == 2 and end == 1)):
        temp = 3
    if((start == 3 and end == 2) or (start == 2 and end == 3)):
        temp = 1
    if((start == 3 and end == 1) or (start == 1 and end == 3)):
        temp = 2

    # 把前 n - 1 个圆盘移动到 temp 
    if(n > 1):
        move_stack(n - 1 , start,temp)
        print_move(start,end)
        move_stack(n - 1 , temp,end)
    if(n == 1):
        print_move(start,end)
    else:
        return 

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    # return (lambda f:lambda x: f(f,x))(lambda f,x:1 if x == 1 else x * f(f,(x - 1)))

    # 这个更好懂 
    return lambda n : (lambda x, function : 1 if x == 1 else x * function(x - 1, function))(n, lambda x, function : 1 if x == 1 else x * function(x - 1, function))

    # def inner_func_name(x, inner_func_name):
    #     # 本质上还是通过 HOF 给了一个名字进行调用 因为有 def statement 无法通过 ok 测试 
    #     if(x == 1):
    #         return 1
    #     else:
    #         return inner_func_name(x - 1, inner_func_name) * x
    # return lambda n : inner_func_name(n, inner_func_name)
