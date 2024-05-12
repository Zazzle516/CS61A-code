# p * v = n * k* t 

from operator import add,sub
from operator import mul,truediv

# 定义了系统结构 
def make_converter(c,f):
    """
    Connect c to f with constraints to convert from Celsius to Fahrenheit
    """
    u,v,w,x,y = [make_connector() for i in range(5)]    # 批量赋值 
    # from the pipe perspective
    multiplier(c,w,u)
    multiplier(x,v,u)
    adder(v,y,f)
    constant(w,9)
    constant(x,5)
    constant(y,32)

def make_connector(name = None):
    """
    The pipe that convey message
    这个函数其实就是一个对象 函数式对象? 
    """
    informant = None    # 记录传递来源 
    constraints = []    # 与之连接的约束器 

    def set_value(source , value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name , '=' ,value)
            inform_all_expect(source, 'new_val' , constraints)
        else:
            if val != value:
                print('Contradiction detected:', val,'vs',value)

    def forget_value(source):
        nonlocal informant          # 判断是否是同一个用户操作 'user' 但是数据只能被一个用户记录 
        if informant == source:
            informant, connector['val'] = None , None
            if name is not None:
                print(name,'is forgotten')
            inform_all_expect(source,'forget',constraints)  # 有点像泛洪传播~ 
        else:
            print("不是同一个用户")

    connector = {'val': None,                   # 记录是否有传递过信息 
                 'set_val': set_value,          # 调用函数 
                 'forget': forget_value,
                 'has_value': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}
    
    return connector

# 三元组的函数约束 
def make_ternary_constraint(a,b,c,ab,ca,cb):
    """
    The abstrat constraint that ab(a,b) = c  ca(c,a) = b  cb(c,b) = a 
    a,b,c 参数是在 make_converter 中定义的 make_connector 函数 
    """
    def new_value():
        # 通过 connector 迭代器 返回 list 结果 av bv cv 是 bool 结果 
        av,bv,cv = [connector['has_value']() for connector in (a,b,c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))

    def forget_value():
        for connector in (a,b,c):
            connector['forget'](constraint)

    constraint = {'new_val': new_value,'forget': forget_value}  # 定义约束函数的两个功能 
    for connector in (a,b,c):
        connector['connect'](constraint)

    return constraint

def inform_all_expect(source,message,constraints):
    """
    inform other constraints 
    """
    for c in constraints:
        if c != source:
            c[message]()

def adder(a,b,c):
    """
    The constraint of add_function 
    """
    return make_ternary_constraint(a,b,c,add,sub,sub)

def multiplier(a,b,c):
    """
    The constraint of mul_function
    """
    return make_ternary_constraint(a,b,c,mul,truediv,truediv)

# 常数 直接通过 pipe 通知 
def constant(connector,value):
    """
    The constraint of connector = value
    """
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

celsius = make_connector('Celsius')
fahrenheit = make_connector('Fahrenheit')
make_converter(celsius,fahrenheit)

celsius['set_val']('user',25)

fahrenheit['set_val']('user',200)

celsius['forget']('user1')

fahrenheit['set_val']('user',212)
