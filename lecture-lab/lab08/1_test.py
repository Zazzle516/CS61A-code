def make_generators_generator(g):
    def gen_helper(num):
            gen=g()    # 这里并不是在传递函数 如果不是惰性计算的特性 应该会执行到 line_14 generator 
            for i in range(num):
                yield(next(gen))       # next() 获取 yield 返回值
    temp = list(g())
    count=len(temp)
    for i in range(count):
        yield(gen_helper(i+1))  # creat new generator

def every_m_ints_to(n, m):
    i = 0
    while (i <= n):
        yield i     # 通过 next(gen) 获取 yield 返回值
        i += m

def every_3_ints_to_10():
    for item in every_m_ints_to(10, 3):
        yield item

# main
# for gen in make_generators_generator(every_3_ints_to_10):   # gen 遇到 line_9 yield 停止 gen_helper(num)
#     print("Next Generator:")
#     for item in gen:
#         print(item)
        
# --------------------------- #