# ------------------------ #

# def make_pair(x,y):
#     def get_item(index):
#         if(index == 0):
#             return x
#         else:
#             return y
#     return get_item
# pair = make_pair(1,2)
# x = pair(0)
# y = pair(1)
# print(x)
# print(y)

# ------------------------ #

# empty_sequence = None
# def make_rlist(first,rest):
#     return (first,rest)

# def first_elem(seq):
#     return seq[0]

# def second_elem(seq):
#     return seq[1]

# def len_rlist(seq):
#     len = 0
#     while(seq != empty_sequence):
#         seq = second_elem(seq)
#         len += 1
#     return len

# # 指定下标取值 
# def getitem_rlist(seq,index):
#     while(index > 0):
#         seq = second_elem(seq)
#         index -= 1
#     return first_elem(seq)

# str = make_rlist(1,make_rlist(2,make_rlist(3,make_rlist(4,empty_sequence))))

# res1 = first_elem(str)
# print(res1)

# res2 = second_elem(str)
# print(res2)

# len = len_rlist(str)
# print(len)

# index_3 = getitem_rlist(str,3)
# print(index_3)

# ------------------------ #

# same_count = 0
# pair = ((1,2),(1,1),(3,4),(2,2))
# for x,y in pair:
#     if(x == y):
#         same_count += 1
# print(same_count)

# ------------------------ #

# def fib(n):
#     prev,next = 1,0
#     for i in range(n - 1):
#         prev,next = next,prev + next
#     return next

# def is_even(x):
#     if(x % 2 == 0):
#         return True
#     return False

# def pipeline(n):
#     return sum(filter(is_even,map(fib,range(1,n + 1))))

# print(pipeline(20))

# ------------------------ #

# def first(seq):
#     return seq[0]

# def is_cap(seq):
#     if(len(seq) > 0):
#         if(seq[0].isupper()):
#             return True
#     return False

# def acronym(name):
#     return tuple(map(first, filter(is_cap,name.split()) ))

# print(acronym('University of Cali Ber Under Graphic'))

# ------------------------ #

# 找出首字母大写的单词然后作为 tuple 输出 

# def is_cap(seq):
#     if(len(seq) > 0):
#         if(seq[0].isupper()):
#             return True
#     return False

# def acronym(name):
#     return tuple( seq[0] for seq in name.split() if is_cap(seq) )

# print(acronym('University of Cali Ber Under Graphic'))

def is_even(x):
    if(x % 2 == 0):
        return True
    return False

def fib(n):
    prev,next = 1,0
    for i in range(n - 1):
        prev,next = next,prev + next
    return next

# def sum_even_fib(n):
#     # return sum(fib(i) for i in range(1,n + 1) if is_even(i) )
#     return sum(fib(i) for i in range(1,n + 1) if is_even( fib(i) ))


# print(sum_even_fib(20))

# ------------------------ #
# from operator import mul
# from functools import reduce
# def product_even_fib(n):
#     return reduce(mul,filter(is_even,map(fib,range(2,n + 1))))

# a = product_even_fib(20)
# print(a)
# ------------------------ #

# def make_withdraw(balance):
#     def withdraw(amount):
#         nonlocal balance
#         if(amount > balance):
#             return 'Insufficient funds'
#         else:
#             balance = balance - amount
#             return balance
#     return withdraw
# withdraw = make_withdraw(100)
# a = withdraw(25)
# print(a)
# b = withdraw(25)
# print(b)
# c = withdraw(60)
# print(c)
# d = make_withdraw(120)(20)
# print(d)

# ------------------------ #

# test_list = [1,2]
# print("test_list 地址是 ",id(test_list))
# print("test_list第一个元素地址是 ",id(test_list[0]))
# print("test_list第二个元素地址是 ",id(test_list[1]))
# a = test_list
# print("address a",id(a))
# print(a)

class Account(object):
    interest = 0.02
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
    def deposit(self,amount):
        self.balance += amount
        return self.balance
    def withdraw(self,amount):
        rest = self.balance - amount
        if(rest < 0):
            return 'Not enough'
        else:
            self.balance -= amount
            return self.balance

# a = Account('Jim')

# print(id(a))

# b = Account('Jack')
# b.balance = 200

# print([acc.balance for acc in (a,b)])

# c = a
# print(id(c))

print(getattr(Account,'balance'))
