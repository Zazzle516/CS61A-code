class Node:
    def __init__(self, name):
        self.name = name
        self.next = None    # 在应用时存储的应该是 Node Object 
    
    def __iter__(self):
        return NodeIter(self)   # 返回迭代器本身
    
class NodeIter:
    def __init__(self, node):
        self.curr_node = node
    def __next__(self):
        if self.curr_node is None:
            raise StopIteration
        node, self.curr_node = self.curr_node, self.curr_node.next
        return node
    # def __iter__(self):
        # return self

# node1 node2 node3 作为可迭代对象需要提供 __iter__() 方法
# 迭代器用来记录状态需要提供 __next__() 方法
# for node in node1:
#     print(node.name)

# Python 文档有写 Iterator 本身最好也有 __iter__() 方法，目的是让迭代器本身也变成可迭代的

# -------------------------------------- #

# class Node:
#     def __init__(self, name):
#         self.name = name
#         self.next = None
#     def __iter__(self):
#         node = self
#         while node is not None:
#             yield node
#             node = node.next

# node_1 = Node("node_1")
# node_2 = Node("node_2")
# node_3 = Node("node_3")

# node_1.next = node_2
# node_2.next = node_3

# for i in node_1:
#     print(i.name)

#############################################

# def gen(num):
#     while num > 0:
#         tmp = yield num     # tmp 是 send() 的接收者
#         if tmp is not None:
#             num = tmp
#         num -= 1

# g = gen(5)

# first = next(g)
# print(f"first: {first}")    # 5

# print(f"send: {g.send(10)}")

# for i in g:
#     print(i)
    
def repeated(k):
    count = 1
    index_slow = None
    s = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    while True:
        index_fast = next(s)
        if index_fast == index_slow:
            count += 1
        if index_slow != index_fast:
            index_slow = index_fast
            count = 1   # 记得更新
        if count == k:
            return index_slow

def merge(incr_a, incr_b):
    iter_a, iter_b = iter(incr_a), iter(incr_b)     # 记录状态
    next_a, next_b = next(iter_a, None), next(iter_b, None)     # 通过传递第二个参数 None 取消触发 StopIteration 异常 这里也是初始化获得第一个元素的地方
    "*** YOUR CODE HERE ***"
    # 通过 yield 返回 generator 类型 也能满足流式文件的读取
    while next_a is not None and next_b is not None:
        val_a, val_b = next_a, next_b   # 直接调用已经给出的 function handle
        if val_a < val_b:
            yield val_a
            next_a = next(iter_a, None)
        elif val_a == val_b:
            yield val_a
            next_a = next(iter_a, None)
            next_b = next(iter_b, None)
        else:
            yield val_b
            next_b = next(iter_b, None)
    while next_a is not None:
        yield val_a
        next_a = next(iter_a, None)
    while next_b is not None:
        yield val_b
        next_b = next(iter_b, None)


def make_withdraw(balance, password):
    error_count = 0
    error_list = []
    def try_withdraw(amount, type_password):
        nonlocal balance
        nonlocal error_count
        nonlocal error_list

        while error_count <= 2:
            if type_password != password:
                error_count += 1
                error_list.append(type_password)
                return 'Incorrect password'
            else:
                if balance >= amount:
                    balance -= amount
                    return balance
                else:
                    return 'Insufficient funds'
        return 'Too many incorrect attempts. Attempts: ' + str(error_list)
    return try_withdraw


def make_joint(withdraw, old_pass, new_pass):
    def joint_withdraw(amount, password):
        nonlocal old_pass, new_pass
        # 关键在这里
        # TMD 我其实最开始就是想要不要替换成 old_pass 去调用 
        # 但是仍然需要对 new_pass 进行判断 所以后面就放弃了这个想法 所以其实还是没想到要利用父函数的环境去替换密码
        return withdraw(amount, old_pass if password == new_pass else password) # 调用的都是 withdraw 函数 有关系吗 应该是有的 只调用了一次
    
    # 检查密码的思路倒是没问题
    check = withdraw(0, old_pass)
    if type(check) == str:
        return check
    return joint_withdraw


def naturals():
    i = 1
    while True:
        yield i
        i += 1
        
def remainders_generator(m):
    def remainder(n):
        while True:
            for natural in naturals():
                yield natural*m + n

    yield remainder(0)
    for i in range(-m+1,0):
        yield remainder(i)