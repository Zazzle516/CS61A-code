def make_instance(my_class):
    """
    Return a new Object instance (a dispatch dictionary) 
    """
    def get_value(name):
        if name in attributes:  # attributes: holder balance 直接调用的时候这个 attributes 哪来的 line_14 
            return attributes[name]
        else:
            value = my_class['get'](name)
            return bind_method(value, instance)
        
    def set_value(name , value):
        attributes[name] = value    # 在 __init__ 中声明 
    attributes = {} # 初始化 
    instance = {'get': get_value, 'set': set_value}
    return instance

def bind_method(value,instance):
    """
    If the value is a method then run it 
    """
    if callable(value):
        # 这里为什么要新写一个子函数 直接调用不行吗 
        def method(*args):
            return value(instance,*args)
        return method
    else:
        return value
    
def make_class(attributes, base_class = None):
    # attributes: __init__  deposit  withdraw  interest 
    def set_value(name,value):
        attributes[name] = value

    def get_value(name):
        if name in attributes:
            return attributes[name]     # init Q: 如何找到的 A: 在最开始声明 Account 的时候 传递了 attributes 
        elif base_class is not None:
            # 向上递归查找 
            return base_class['get'](name)
    
    def new(*args):
        return init_instance(my_class , *args)

    my_class = {'get': get_value, 'set': set_value , 'new': new}
    return my_class

def init_instance(my_class,*args):
    """
    Return a new Object with type my_class initialized with *args
    """
    # 在 init_instance 中调用 make_instance 初始化的两个步骤是分开的 
    instance = make_instance(my_class)  # 'get' 'set'
    init = my_class['get']('__init__')  # make_class().get_value 通过 my_class 回到 make_class() 找到对应的函数执行 

    if init:    # make_account_class().__init__() 
        init(instance,*args)
    return instance

def make_account_class():
    """
    Return Account class   method: deposit withdraw   var: balance holder
    """

    def __init__(self,account_holder):
        self['set']('holder', account_holder)
        self['set']('balance',0)

    def deposit(self, amount):
        new_balance = self['get']('balance') + amount
        self['set']('balance',new_balance)
        return self['get']('balance')
    
    def withdraw(self, amount):
        new_balance = self['get']('balance') - amount
        if(new_balance < 0):
            return 'Insufficient funds'
        else:
            self['set']('balance',new_balance)
        return self['get']('balance')
    
    return make_class({'__init__': __init__,
                       'deposit': deposit,
                       'withdraw': withdraw,
                       'interest': 0.02})

Account = make_account_class()  # 'get' 'set' 'new' make_class() 

jim_account = Account['new']('Jim') # make_class().new().init_instance(Account,'Jim').make_instance()... -> instance 

name_jim = jim_account['get']('holder')

jack_account = Account['new']('Jack')
name_jack = jack_account['get']('holder')

print("name_jim:",name_jim,"name_jack:",name_jack)

# 这个字典存储其实可以理解为 如果访问到这个字典值对应的函数 会直接跳转执行内部函数 不会通过外面的父函数调用 

# Q: 如何实现不同对象的数据分离 
# A: 两个不同的 attributes 分别是什么时候声明的? 
# A: 在 init() 调用 make_instance().set_value() 时的声明 添加了 attributes 