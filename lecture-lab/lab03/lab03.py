HW_SOURCE_FILE=__file__


def pascal(row, column):
    """Returns a number corresponding to the value at that location
    in Pascal's Triangle.
    >>> pascal(0, 0)
    1
    >>> pascal(0, 5)	# Empty entry; outside of Pascal's Triangle
    0
    >>> pascal(3, 2)	# Row 4 (1 3 3 1), 3rd entry
    3
    """
    "*** YOUR CODE HERE ***"
    if (row < column):
        return 0
    if(row == 0 and column == 0):
        return 1
    # 递归终点 在后面 [column - 1] = -1 的时候 怎么处理 
    if(row == 1 and column == 0):
        return 1
    if(row == 1 and column == 1):
        return 1
    
    def Triangle():
        res = pascal(row - 1 , column - 1) + pascal(row - 1 , column)
        return res
    return Triangle()
        
        


def compose1(f, g):
    """"Return a function h, such that h(x) = f(g(x))."""
    def h(x):
        return f(g(x))
    return h

def repeated(f, n):
    """Return the function that computes the nth application of func (recursively!).

    >>> add_three = repeated(lambda x: x + 1, 3)
    >>> add_three(5)
    8
    >>> square = lambda x: x ** 2
    >>> repeated(square, 2)(5) # square(square(5))
    625
    >>> repeated(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> repeated(square, 0)(5)
    5
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'repeated',
    ...       ['For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    def count_repeat(x):
        if(n == 0):
            return x
        else:
            return repeated(f,n - 1)(f(x))
    return count_repeat


def num_eights(n):
    """Returns the number of times 8 appears as a digit of x.

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AugAssign'])
    True
    """
    "*** YOUR CODE HERE ***"
    # 统计 8 出现的次数 
    # 如果不能赋值 那么怎么表示统计次数 
    # def single_num():
    #     if(x == 0):
    #         return count
    #     if(x % 10 == 8):
    #         # 次数计数 
    #         count += 1

    #     return num_eights(x / 10)()
    # return single_num

    if n % 10 == 8:
        return 1 + num_eights(n // 10)
    elif n < 10:
        return 0
    else:
        return num_eights(n // 10)
    
def contain_eight(x):
    # 判断 8 是不是因数 
    if(x % 8 == 0):
        return True
    return False

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(8)     # 6
    8
    >>> pingpong(10)    # 8
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    -2
    >>> pingpong(30)
    -2
    >>> pingpong(68)
    0
    >>> pingpong(69)
    -1
    >>> pingpong(80)
    0
    >>> pingpong(81)
    1
    >>> pingpong(82)
    0
    >>> pingpong(100)
    -6
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    "*** YOUR CODE HERE ***"
    # 遇到的数字里包含 8 或 8 可以作为因数的时候 就改变方向 
    # 可以调用刚刚实现的 num_eights() 
    # 和刚刚的函数不同的是 num_eights() 从末尾开始判断 但是 pinpang 要从开头开始
    # 和题目要求不同 反着去递归的时候 要反向运算 
    # 从 1 开始 默认up 

    # if(n == 1):
    #     return 1
    
    # if((contain_eight(n)) or (num_eights(n) > 0)):
    #     return pingpong(n - 1) - 1
    # else:
    #     return pingpong(n - 1) + 1
    
    # 这样编写会有一个问题 就是反向方向改变和原方式差了一步 导致结果会差 2 

    # answer
    # 从底层开始找数 
    def ping(index, value, upordown):
        if index == n:
            return value
        if upordown:
            return pong(index + 1, value + 1, upordown)
        else:
            return pong(index + 1, value - 1, upordown)

    def pong(index, value, upordown):
        if index % 8 == 0 or num_eights(index):
            return ping(index, value, not upordown)
        return ping(index, value, upordown)

    return ping(1, 1, True)

