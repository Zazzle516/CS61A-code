def make_generators_generator(g):
    """Generates all the "sub"-generators of the generator returned by
    the generator function g.

    >>> def every_m_ints_to(n, m):
    ...     i = 0
    ...     while (i <= n):
    ...         yield i
    ...         i += m
    ...
    >>> def every_3_ints_to_10():
    ...     for item in every_m_ints_to(10, 3):
    ...         yield item
    ...
    >>> for gen in make_generators_generator(every_3_ints_to_10):
    ...     print("Next Generator:")
    ...     for item in gen:
    ...         print(item)
    ...
    Next Generator:
    0
    Next Generator:
    0
    3
    Next Generator:
    0
    3
    6
    Next Generator:
    0
    3
    6
    9
    """
    "*** YOUR CODE HERE ***"
    # 主函数每次都要返回一个新的生成器 更新自己的状态 每次叠加一次 next()
    # def gen_helper(lst):
    #     yield from lst
    # yield_sofar = []
    # gg = g()
    # for x in gg:
    #     yield_sofar.append(x)
    #     yield gen_helper(yield_sofar.copy())

    def gen_helper(num):
            gen=g() #then gen is a generator
            for i in range(num):
                yield(next(gen))
    count=len(list(g()))
    for i in range(count):
        yield(gen_helper(i+1))