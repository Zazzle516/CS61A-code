from operator import add, mul, sub

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


HW_SOURCE_FILE=__file__


def product(n, term):
    """Return the product of the first n terms in a sequence.
    n -- a positive integer
    term -- a function that takes one argument to produce the term

    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    "*** YOUR CODE HERE ***"
    res = 1
    for i in range(1,n + 1):
        res *= term(i)
    return res



def accumulate(combiner, base, n, term):
    """Return the result of combining the first n terms in a sequence and base.
    The terms to be combined are term(1), term(2), ..., term(n).  combiner is a
    two-argument commutative function.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    >>> accumulate(lambda x, y: 2 * (x + y), 2, 3, square)      # 只有这个出错 我自己手动算也是 80... 为什么是 58
    58
    >>> accumulate(lambda x, y: (x + y) % 17, 19, 20, square)
    16
    """
    "*** YOUR CODE HERE ***"
    # lambda 给 combiner 一个函数指针 让 combiner 以这种方式运算 每次接受两个参数
    # res_start = term(1)
    # if(n == 0):
    #     res_start = term(0)
    # for i in range(2,n + 1):
    #     res_start = combiner(res_start,term(i))
    #
    # return combiner(base,res_start)

    # 这样写就没有 58 的报错
    # 原因在运算顺序 优先从 base 开始计算 而不是最后加上去
    res = base
    for i in range(1,n + 1):
        res = combiner(res,term(i))
    return res


def summation_using_accumulate(n, term):
    """Returns the sum of term(1) + ... + term(n). The implementation
    uses accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'summation_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    return accumulate(add,0,n,term)

def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    >>> from construct_check import check
    >>> # ban iteration and recursion
    >>> check(HW_SOURCE_FILE, 'product_using_accumulate',
    ...       ['Recursion', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    return accumulate(mul,1,n,term)


def compose1(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f
def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    "*** YOUR CODE HERE ***"

# ----------- my code ------------- #
    # 用一个嵌套函数来接收 func 的参数 循环的写法 这个相对好想
    # def sub_func(x):
    #     count = n
    #     while count >= 0:
    #         if(count == 0):
    #             return x
    #         count = count - 1
    #         x = func(x)
    # return sub_func
# ---------------------------------- #

# ----------- my code ------------- #
    # 递归的写法
    def sub_func(x):
        if n == 0:
            return x
        else:
            # 里面的嵌套不能修改 n 的值
            # return make_repeater(func,n - 1)(func(x))
            # 有点复杂.. 真的想不到
            return func(make_repeater(func,n - 1)(x))
    return sub_func

# 就一般而言 递归的方式是 fun(){ return fun() } 这样自己调用自己的过程 伴随着一个出递归的标志
# 这个递归复杂在嵌套函数的调用过程 不能显示的传递 (n - 1) 的过程 因为 n 在外层 要通过外层的调用表示 n 的变化

# ---------------------------------- #

# ------------------------------------ #
#     def sub_func(x):
#         for i in range(n):
#             x = func(x)
#         return x
#     return sub_func
# ------------------------------------ #


# if we have functions, we do not need to assume that numbers exist, but instead we can invent them.

def zero(f):
    # 无论传入什么参数 返回的都是 x lambda 是定义在 zero 内部的子函数 也就是第二层函数
    # 需要给 zero() 一个指针之后传值或者用两个括号 类似于上面的 repeater()()
    return lambda x: x

def successor(n):
    # 这个函数的功能是 + 1
    # 从语法解释一下这个奇怪的表达 f(n(f)(x)) successor 接受的参数 n 是 one two 类似的 eg. 后面的 successor(two)
    # 代入一下就是 f(one(f)(x)) 所以 后面的 (f) 是和前面的函数名绑定 更后面的 x 是 lambda 的参数传递
    # 当时这个 f 函数很困惑 但实际上这个 successor 只表示一种抽象的逻辑过程 不涉及具体计算
    # 真正的 + 1 操作 也就是函数转变为实数 要在后面的调用过程中传递

    # 从执行的角度上 successor 的两个 lambda 函数 只有给 zero 传参的意义
    # 又因为 zero 本身没有任何意义 zero(f)(x) == x => successor(zero) = return f(x)
    # 所以 到现在只能看到逻辑层面的相加 zero -> x  one -> f(x)  two -> f(f(x)) 缩写 zero(x) one(x) two(x) 外面的 n 表示层数
    return lambda f: lambda x: f(n(f)(x))

# 模仿 zero 去写 具体的执行只要一层就够了
def one(f):
    """Church numeral 1: same as successor(zero)"""
    "*** YOUR CODE HERE ***"
    # return lambda f: lambda x: f(x)
    return lambda x: f(x)


# -------------------------------------------------------- #
# def two(f):
#     """Church numeral 2: same as successor(successor(zero))"""
#     "*** YOUR CODE HERE ***"
#     # return lambda f: lambda x: f(f(x))
#     return lambda x: f(f(x))
# -------------------------------------------------------- #

two = successor(one)    # 都是 OK 的

three = successor(two)

def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    "*** YOUR CODE HERE ***"
    # 通过 zero 给定 baseline 然后通过 successor 求值
    # 之前的理解有问题 本质不是通过 successor 求值的 successor 本质上只是一个计数器 通过 f 记录相对 zero 来说 多了几次嵌套

    # 不能针对每个数字函数都写一个具体实现 如何判断调用 f 的层数
    # 错误！在本程序中 必须对每个数字函数有定义才可以运行 因为传递的是一个函数

    # 如何计算 successor 调用的层数 自然是之前一直没有实际意义的 f 参数
    # 这里 f 的功能是 + 1 也是因为数学规律(从 0 开始 如果改成 + 2 就是乘 2 倍的关系
    f = lambda x: x + 1
    return n(f)(0)



def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    "*** YOUR CODE HERE ***"
    # --------------------------------------------------------- #
    # 注意这里的函数调用是嵌套了 church_to_int 不能像上面一样直接返回
    # # 功能: 转换成一个和 zero 同性质的单函数名 能过但是很丑陋 呜呜呜
    # four = successor(three)
    # five = successor(four)
    # return five
    # --------------------------------------------------------- #

    # 在上层 return add_church(two,three)(f)(0)
    # 目标是 m( (f)( n(f)(0) ) )  把内部的计算结果作为新的 zero 在上面累加

    # 看了答案 m(f)( n(f)(x) ) (f)(0) 等效替换会产生个问题 也是我没想出来的原因 church_to_int 的 (f)(0) 要怎么办
    # 它们没有运算意义 只有传递参数的意义 
    return lambda f: lambda x: m(f)(n(f)(x))


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    # return [ mul_church(m)(n) ](f)(0) x 是用来接收参数 0 的 
    "*** YOUR CODE HERE ***"
    # return lambda f: m(n(f)) 实际上不给这个参数 作为父函书调用 zero 也可以知道 x = 0 
    return lambda f: lambda x: m(n(f))(x)   # 实际上是拆成了两个子函数 lambda2 嵌套在 lambda1 里面 

def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))   # return f(f(f(f(f(f..)))))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    "*** YOUR CODE HERE ***"

    # -------------------------- #
    # count = church_to_int(n)
    # res = m
    # while(count > 1):
    #     m = mul_church(res,m)
    #     count -= 1
    # return m
    # -------------------------- #

    # return lambda f: n(m)(f)
    # return [ pow_church(m)(n) ](f)(0) 
    # return [ lambda f: n(m)(f) ](f)(0) 通过 lambda1 接收了 f 参数 

    return n(m)