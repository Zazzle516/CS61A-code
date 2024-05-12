"""A Scheme interpreter and its read-eval-print loop."""
from __future__ import print_function  # Python 2 compatibility

import sys

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):        # scheme_buildins   line_175
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    
    # 原子操作结束 判断合法性结束   只剩下 procedure 和 special forms 的可能性
    first, rest = expr.first, expr.rest

    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        # 判断特殊形式的处理
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        # 参数 expr Pair 本身就是有层级关系的
        operator = scheme_eval(first, env)
        validate_procedure(operator)    # 事实上是 operator 不能进行百分百的判断 所以需要 validate_procedure 额外判断

        if isinstance(operator, MacroProcedure):
            # 根据 do_define_macro() 中 env.define 的绑定进行判断

            # 对比下面非 macro 的情况 其实原理是一样的 通过 operator 得到 lambda-expr 计算 operand 后返回结果
            # marco 特殊在第一层调用必然是尾调用(rest is nil) 实际上结果返回在 line_749
            return scheme_eval(operator.apply_macro(rest, env), env)

        args = rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(operator, args, env)
        # END PROBLEM 4

def self_evaluating(expr):
    """Return whether EXPR evaluates to itself."""
    # boolean number null string => themselves  | symbol -> number/...
    # 这里要排除变量有自己对应的值的情况 这种情况下变量并不能等于它自己
    return (scheme_atomp(expr) and not scheme_symbolp(expr)) or expr is None

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        # phase-2 调用途径
        return procedure.apply(args, env)
    else:
        # user-defined function
        new_env = procedure.make_call_frame(args, env)
        return eval_all(procedure.body, new_env)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    environment ENV and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 7
    if expressions is nil:
        return None
    
    # first = expressions.first
    # rest = expressions.rest
    
    # while rest is not nil:
    #     scheme_eval(rest.first, env)
    #     rest = rest.rest
    # return scheme_eval(first, env, True)

    ptr = expressions # Pair(Pair('car', Pair('x', nil)), nil)
    while ptr.rest is not nil:
        scheme_eval(ptr.first, env)
        ptr = ptr.rest
    return scheme_eval(ptr.first, env, True)
    
    # END PROBLEM 7

################
# Environments #
################

class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        self.bindings[symbol] = value
        # END PROBLEM 2

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        if symbol in self.bindings:
            return self.bindings[symbol]
        if self.parent is not None:
            return self.parent.lookup(symbol)
        # END PROBLEM 2
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Raise an error if too many or too few
        vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        child_Frame = Frame(parent=self)
        def set_child_frame(sub_frame, symbol, val):
            if symbol is nil and val is not nil:
                raise SchemeError
            
            elif symbol is not nil and val is nil:
                raise SchemeError
            
            elif symbol is not nil and val is not nil:
                sub_frame.define(symbol.first, val.first)
                set_child_frame(sub_frame, symbol.rest, val.rest)
            else:
                return
        
        set_child_frame(child_Frame, formals, vals)
        return child_Frame
        # END PROBLEM 10

##############
# Procedures #
##############

class Procedure(object):
    """The supertype of all Scheme procedures."""

def scheme_procedurep(x):
    return isinstance(x, Procedure)

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list (a Pair instance).

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        if not scheme_listp(args):
            raise SchemeError('arguments are not in a list: {0}'.format(args))
        # Convert a Scheme list to a Python list
        python_args = []
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        def transfer_list(scheme_args):
            nonlocal python_args
            if scheme_args is nil:
                return
            python_args.append(scheme_args.first)
            return transfer_list(scheme_args.rest)
        
        transfer_list(args)
        if self.use_env is True:
            python_args.append(env)

        try:
            return self.fn(*python_args)
        except TypeError:
            raise SchemeError    # scheme_buildins.py line_12
        # END PROBLEM 3

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env): 
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def make_call_frame(self, args, env):
        """Make a frame that binds my formal parameters to ARGS, a Scheme list
        of values, for a lexically-scoped call evaluated in my parent environment."""
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # child_frame_instance = env.make_child_frame(self.formals, args)
        child_frame_instance = self.env.make_child_frame(self.formals, args)
        return child_frame_instance
        # END PROBLEM 11

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MacroProcedure(LambdaProcedure):
    """A macro: a special form that operates on its unevaluated operands to
    create an expression that is evaluated in place of a call."""

    def apply_macro(self, operands, env):
        """Apply this macro to the operand expressions."""
        return complete_apply(self, operands, env)

def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form.

    >>> # Problem 5
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env)
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # Problem 9
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env)
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2
    target = expressions.first
    if scheme_symbolp(target):
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 5
        "*** YOUR CODE HERE ***"
        value = None
        if self_evaluating(expressions.rest.first):
            # atom expr
            value = expressions.rest.first
        else:
            value = scheme_eval(expressions.rest.first, env)
        env.define(target, value)
        return target
        # END PROBLEM 5
    elif isinstance(target, Pair) and scheme_symbolp(target.first):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        func_name = target.first

        lambda_expr = Pair(target.rest, expressions.rest)
        lambda_instance = do_lambda_form(lambda_expr, env)

        env.define(func_name, lambda_instance)
        return func_name
        # END PROBLEM 9
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))

def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env)
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    return expressions.first
    # END PROBLEM 6

def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env)
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    body = expressions.rest
    lambda_instance = LambdaProcedure(formals, body, env)
    return lambda_instance
    # END PROBLEM 8

def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env)
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env)
    3
    """
    validate_form(expressions, 2, 3)
    if is_true_primitive(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env, True)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env, True)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env)
    False
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    result = True
    while expressions is not nil:
        result = scheme_eval(expressions.first, env, True if expressions.rest is nil else False)
        if result is not False:
            expressions = expressions.rest
        else:
            return False
    return result
    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env)
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env)
    2
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    while expressions is not nil:
        result = scheme_eval(expressions.first, env, True if expressions.rest is nil else False)
        if result is not False:
            return result
        expressions = expressions.rest
    return False
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)        # 参与 branch 判断的只有一个参数
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            # get branch result
            test = scheme_eval(clause.first, env)
        if is_true_primitive(test):
            # BEGIN PROBLEM 13
            "*** YOUR CODE HERE ***"
            # 进入 true-branch 分支
            if clause.rest is nil:
                return test
            test = eval_all(clause.rest, env)
            return test
            # END PROBLEM 13
        expressions = expressions.rest
        # 只在 true-branch 和 else-branch 返回 不需要处理 false-branch

def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names, values = nil, nil # Pair(Pair('a', Pair(1, nil)), Pair(Pair('b', Pair(2, nil)), Pair(Pair('c', Pair(3, nil)), nil)))
    # BEGIN PROBLEM 14
    "*** YOUR CODE HERE ***"
    def create_name_binding(expr):
        nonlocal names
        if names is nil:
            return Pair(expr, nil)
        return Pair(expr, names)
        
    def create_value_binding(expr):
        nonlocal values
        value = scheme_eval(expr, env)
        if values is nil:
            return Pair(value, nil)
        return Pair(value, values)
    
    while bindings is not nil:
        current_binding = bindings.first
        validate_form(current_binding, 2, 2)
        names = create_name_binding(current_binding.first)
        values = create_value_binding(current_binding.rest.first)
        bindings = bindings.rest

    validate_formals(names)
    # END PROBLEM 14
    return env.make_child_frame(names, values)

def do_define_macro(expressions, env):
    """Evaluate a define-macro form.

    >>> env = create_global_frame()
    >>> do_define_macro(read_line("((f x) (car x))"), env)
    'f'
    >>> scheme_eval(read_line("(f (1 2))"), env)
    1
    """
    # BEGIN Problem 20
    "*** YOUR CODE HERE ***"
    validate_form(expressions, 2)

    target = expressions.first
    # 相比于 de_define_form() 排除了 scheme_symbolp(target) 的分支
    if isinstance(target, Pair) and scheme_symbolp(target.first):
        func_name = target.first
        formals = target.rest
        body = expressions.rest

        # 注意 MacroProcedure 继承了 LambdaProcedure
        # Q: 对 body 没有什么特殊处理吗
        # A: 和 do_define_form () 没有什么不同 毕竟是用户定义顺序 语法执行上没有变化
        # 这道题的关键还是 scheme_eval() 中对 tail recursion 的处理(complete apply)
        macroInstance = MacroProcedure(formals, body, env)

        env.define(func_name, macroInstance)

        return func_name
    else:
        bad_target = target.first if isinstance(target, Pair) else target
        raise SchemeError('non-symbol: {0}'.format(bad_target))
    # END Problem 20

def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    environment ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in environment ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form, # here
    'or': do_or_form,
    'quote': do_quote_form,
    'define-macro': do_define_macro,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
}

# Utility methods for checking the structure of Scheme programs

def validate_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()
    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest


def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

#################
# Dynamic Scope #
#################

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    # BEGIN PROBLEM 15
    "*** YOUR CODE HERE ***"
    def make_call_frame(self, args, env):

        def bind_in_same_env(symbol, value):
            if value is nil and symbol is nil:
                return
            elif value is nil and symbol is not nil:
                raise SchemeError
            elif value is not nil and symbol is nil:
                raise SchemeError
            else:
                env.define(symbol.first, value.first)
                bind_in_same_env(symbol.rest, value.rest)
        
        bind_in_same_env(self.formals, args)
        return env        
    # END PROBLEM 15

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 15
    "*** YOUR CODE HERE ***"
    body = expressions.rest
    mu_procedure_instance = MuProcedure(formals, body)
    return mu_procedure_instance
    # END PROBLEM 15

SPECIAL_FORMS['mu'] = do_mu_form

###########
# Streams #
###########

class Promise(object):
    """A promise."""
    def __init__(self, expression, env):
        self.expression = expression
        self.env = env

    def evaluate(self):
        if self.expression is not None:
            value = scheme_eval(self.expression, self.env)
            if not (value is nil or isinstance(value, Pair)):
                raise SchemeError("result of forcing a promise should be a pair or nil, but was %s" % value)
            self.value = value
            self.expression = None
        return self.value

    def __str__(self):
        return '#[promise ({0}forced)]'.format(
                'not ' if self.expression is not None else '')

def do_delay_form(expressions, env):
    """Evaluates a delay form."""
    validate_form(expressions, 1, 1)
    return Promise(expressions.first, env)

def do_cons_stream_form(expressions, env):
    """Evaluate a cons-stream form."""
    validate_form(expressions, 2, 2)
    return Pair(scheme_eval(expressions.first, env),
                do_delay_form(expressions.rest, env))

SPECIAL_FORMS['cons-stream'] = do_cons_stream_form
SPECIAL_FORMS['delay'] = do_delay_form

##################
# Tail Recursion #
##################

class Thunk(object):
    """An expression EXPR to be evaluated in environment ENV."""
    # 用来保证原函数 scheme_eval 执行而暂存变量的工具
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env      # 在 caller frame 中执行 callee func

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)    # line_773  如果是 marco 的情况第一层必然会得到 Thunk
    if isinstance(val, Thunk):
        # 此时是在 new_env 中执行 procedure_body 后续和 lambda_func 执行没有区别
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(prior_eval_function):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in environment ENV. If TAIL,
        return a Thunk containing an expression for further evaluation.
        """
        # 尾递归情况
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            # tail: support tail optimized or not
            # scheme_symbolp(): 针对完整的 expr 所以只是判断变量的情况    正常的函数表达式的话是 Pair 结构 not instance of str
            # self_evaluating(): atmoic expr
            # 之所以要额外判断一次 scheme_symbolp() 是因为 self_evaluating() 未包含该情况

            # 对比下面递归调用 prior_eval_function(scheme_eval) 增加递归深度 体现了尾递归的意义
            # Q: 然后呢 Thunk 下一步怎么作用
            # A: 通常是直接返回到 "上一层" 的 result(line_783) 虽然中间经过 scheme_eval()->scheme_apply()->eval_all() 这样的计算
            # A: 利用在 eval_all() 中对 rest = nil 情况尾调用的修改 进入这里 然后直接返回(或者是其他支持尾调用的函数)

            # 变量的修改会在其他执行语句中正常计算(line_54) 但是这里保持了 env 不变
            # 对比在 scheme_apply() 会调用 make_call_frame() 得到 new_env 计算
            return Thunk(expr, env)

        # 非尾递归情况
        result = Thunk(expr, env)
        # BEGIN
        "*** YOUR CODE HERE ***"
        while isinstance(result, Thunk):
            # Q: 这里是怎么和 scheme_eval() 联系起来的
            # Q: 返回结果是怎么被转换到 Thunk 的
            # A: 因为表达式存在嵌套的情况 仍然会调用 scheme_eval() 此时转向到 optimize_tail_calls() 从而得到 Thunk
            result = prior_eval_function(result.expr, result.env)

        # 非尾递归情况返回最终结果
        return result
        # END
    return optimized_eval






################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
# 该行其实是重定向了该 scheme_eval 函数名
# 通过一个 HOF 保留了原 scheme_eval() 的地址
# 好巧妙 我这辈子也写不出来这种代码 :)
# 经过长达两个小时的 debug 我现在话都快说不出来了呜呜呜呜呜
scheme_eval = optimize_tail_calls(scheme_eval)






####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))

def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head

def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=(), report_errors=False):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if report_errors:
                if isinstance(err, SyntaxError):
                    err = SchemeError(err)
                    raise err
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet, report_errors=True)

def scheme_load_all(directory, env):
    """
    Loads all .scm files in the given directory, alphabetically. Used only
        in tests/ code.
    """
    assert scheme_stringp(directory)
    directory = eval(directory)
    import os
    for x in sorted(os.listdir(".")):
        if not x.endswith(".scm"):
            continue
        scheme_load(x, env)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    # define build-in functions
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('load-all',
               BuiltinProcedure(scheme_load_all, True, 'load-all'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env

@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('--pillow-turtle', action='store_true',
                        help='run with pillow-based turtle. This is much faster for rendering but there is no GUI')
    parser.add_argument('--turtle-save-path', default=None,
                        help='save the image to this location when done')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    import builtins
    builtins.TK_TURTLE = not args.pillow_turtle
    builtins.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, '')

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()