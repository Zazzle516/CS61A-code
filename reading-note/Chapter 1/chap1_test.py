# def a_new_decorator(a_func):
#     def wrapTheFunction():
#
#         print("I am doing some boring work before executing a_func()")
#
#         a_func()
#
#         print("I am doing some boring work after executing a_func()")
#
#     return wrapTheFunction
#
#
# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to remove my foul smell")
#
# a_function_requiring_decoration()
#
# @a_new_decorator
# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to "
#           "remove my foul smell")
#
# a_function_requiring_decoration()

def pow_church(m, n):
    return lambda f: n(m)(f)

def church_to_int(n):
    f = lambda x: x + 1
    return n(f)(0)
def successor(n):
    return lambda f: lambda x: f(n(f)(x))
def zero(f):
    return lambda x: x
def one(f):
    return lambda x: f(x)


two = successor(one)    # 都是 OK 的

three = successor(two)

church_to_int(pow_church(two, three))

print(church_to_int(pow_church(two, three)))