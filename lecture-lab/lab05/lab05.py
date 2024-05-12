def coords(fn, seq, lower, upper):
    """
    >>> seq = [-4, -2, 0, 1, 3]
    >>> fn = lambda x: x**2
    >>> coords(fn, seq, 1, 9)
    [[-2, 4], [1, 1], [3, 9]]
    """
    "*** YOUR CODE HERE ***"
    # lower upper 作用在结果上的界限 
    return [[x,fn(x)] for x in seq if (fn(x) <= upper and fn(x) >= lower)]


def riffle(deck):
    """Produces a single, perfect riffle shuffle of DECK, consisting of
    DECK[0], DECK[M], DECK[1], DECK[M+1], ... where M is position of the
    second half of the deck.  Assume that len(DECK) is even.
    >>> riffle([3, 4, 5, 6])
    [3, 5, 4, 6]
    >>> riffle(range(20))
    [0, 10, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
    """
    "*** YOUR CODE HERE ***"
    # start_index = 0
    # middle_index = len(deck) // 2
    # uncheck_list_len = len(deck)
    # index_k = 0

    # riffle_list = [0]*uncheck_list_len

    # while(uncheck_list_len > 0):
    #     if uncheck_list_len % 2 == 0:
    #         # 正常顺序
    #         riffle_list[index_k] = deck[start_index]
    #         index_k += 1
    #         start_index += 1
    #     else:
    #         # 从中间位置取元素 
    #         riffle_list[index_k] = deck[middle_index]
    #         index_k += 1
    #         middle_index += 1
    #     uncheck_list_len -= 1
    # return riffle_list
    
    start_index = 0
    middle_index = len(deck) // 2
    uncheck_list_len = len(deck)
    riffle_list = []
    while(uncheck_list_len > 0):
        if uncheck_list_len % 2 == 0:
            # 正常顺序
            riffle_list.append(deck[start_index])
            start_index += 1
        else:
            # 从中间位置取元素 
            riffle_list.append(deck[middle_index])
            middle_index += 1
        uncheck_list_len -= 1
    return riffle_list


def berry_finder(t):
    """Returns True if t contains a node with the value 'berry' and 
    False otherwise.
    >>> scrat = tree('berry')
    >>> berry_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('berry')]), tree('branch2')])
    >>> berry_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> berry_finder(numbers)
    False
    >>> t = tree(1, [tree('berry',[tree('not berry')])])
    >>> berry_finder(t)
    True
    """
    "*** YOUR CODE HERE ***"
    if label(t) == 'berry':
        return True
    for sub_tree in branches(t):
        if berry_finder(sub_tree):
          return True
    return False


def sprout_leaves(t, leaves):
    """Sprout new leaves containing the data in leaves at each leaf in
    the original tree t and return the resulting tree.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    "*** YOUR CODE HERE ***"
    # for sub_tree in branches(t):
    #     if is_leaf(sub_tree) is False:
    #         # 非空子树
    #         return sprout_leaves(sub_tree,leaves)
    #     else:
    #         # 叶结点 添加子树 
    #         sub_tree = tree(label(sub_tree), leaves)
    # return t

    # for sub_tree in branches(t):
    #     if is_leaf(sub_tree) is False:
    #         # 非空子树
    #         return sprout_leaves(sub_tree,leaves)
    #     else:
    #         # 叶结点 添加子树
    #         for leaf in leaves:
    #             tree(leaf)      后来想了这种解决方式 但是没办法把 sub_tree 和 leaf 绑在一起即使把 sub_tree 写到循环里也没办法覆盖到所有的 leaf 
    #         sub_tree = tree(label(sub_tree), leaves)
    # return t

    if is_leaf(t):
        # 在 branches 中建立循环 就可以规避我上面的问题
        return tree(label(t), [tree(l) for l in leaves])
    else:
        # 这里我当时面临的问题是：即使我成功挂上了 leaves_tree 在递归中怎么把新树传参传出去
        # 当时想构建新树 先把 root_label 提取出来 但是考虑后面递归会覆盖 不知道怎么传参
        # 这里也是在 branches 内部非空子树进行递归来保证最后的新树是完整的 
        return tree(label(t), [sprout_leaves(t, leaves) for t in branches(t)])

# Abstraction tests for sprout_leaves and berry_finder
def check_abstraction():
    """
    There's nothing for you to do for this function, it's just here for the extra doctest
    >>> change_abstraction(True)
    >>> scrat = tree('berry')
    >>> berry_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('berry')]), tree('branch2')])
    >>> berry_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> berry_finder(numbers)
    False
    >>> t = tree(1, [tree('berry',[tree('not berry')])])
    >>> berry_finder(t)
    True
    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    >>> change_abstraction(False)
    """


def add_trees(t1, t2):
    """
    >>> numbers = tree(1,
    ...                [tree(2,
    ...                      [tree(3),
    ...                       tree(4)]),
    ...                 tree(5,
    ...                      [tree(6,
    ...                            [tree(7)]),
    ...                       tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(tree(2), tree(3, [tree(4), tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(tree(2, [tree(3)]), tree(2, [tree(3), tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(tree(2, [tree(3, [tree(4), tree(5)])]), \
    tree(2, [tree(3, [tree(4)]), tree(5)])))
    4
      6
        8
        5
      5
    """
    "*** YOUR CODE HERE ***"
    # 把子树作为列表去处理 在递归中体现树的结构 
    # they might have branches, but they both must have label
    res_label = label(t1) + label(t2)   # 递归终点 进行真正的相加 
    # for each corresponding branch, add them together
    res_branch = []
    i = 0  # index to chase which branch I am in
    while i < len(branches(t1)) and i < len(branches(t2)):  # 通过使用同一个下标 i 保证递归的相同进度 
        # 也可以通过 zip() 来简化这个步骤
        b1, b2 = branches(t1)[i], branches(t2)[i]
        new_branch = add_trees(b1, b2)
        res_branch += [new_branch]  # remember to add []
        i += 1
    # where t1 or t2 is empty: no need to add, just need to include
    res_branch += branches(t1)[i:]
    res_branch += branches(t2)[i:]
    # return the new tree
    return tree(res_label, res_branch)


def build_successors_table(tokens):
    """Return a dictionary: keys are words; values are lists of successors.

    >>> text = ['We', 'came', 'to', 'investigate', ',', 'catch', 'bad', 'guys', 'and', 'to', 'eat', 'pie', '.']
    >>> table = build_successors_table(text)
    >>> sorted(table)
    [',', '.', 'We', 'and', 'bad', 'came', 'catch', 'eat', 'guys', 'investigate', 'pie', 'to']
    >>> table['to']
    ['investigate', 'eat']
    >>> table['pie']
    ['.']
    >>> table['.']
    ['We']
    """
    table = {}
    prev = '.'  # 方便后面循环的初始化 
    for word in tokens:
        if prev not in table:
            table[prev] = []  # key-values 
        table[prev].append(word)
        prev = word
    return table

def construct_sent(word, table):
    """Prints a random sentence starting with word, sampling from
    table.

    >>> table = {'Wow': ['!'], 'Sentences': ['are'], 'are': ['cool'], 'cool': ['.']}
    >>> construct_sent('Wow', table)
    'Wow!'
    >>> construct_sent('Sentences', table)
    'Sentences are cool.'
    """
    import random
    result = ''
    while word not in ['.', '!', '?']:
        "*** YOUR CODE HERE ***"
        result += word
        # 随机生成一个在 [0,len(table[key]) - 1] 的整数 
        random_index = random.randint(0,len(table[word]) - 1)
        result += " "
        word = table[word][random_index]
    return result.strip() + word

def shakespeare_tokens(path='shakespeare.txt', url='http://composingprograms.com/shakespeare.txt'):
    """Return the words of Shakespeare's plays as a list."""
    import os
    from urllib.request import urlopen
    if os.path.exists(path):
        return open('shakespeare.txt', encoding='ascii').read().split()
    else:
        shakespeare = urlopen(url)
        return shakespeare.read().decode(encoding='ascii').split()

# Uncomment the following two lines
tokens = shakespeare_tokens()
table = build_successors_table(tokens)

def random_sent():
    import random
    return construct_sent(random.choice(table['.']), table)

# for shakespeare_test
def sent():
    return construct_sent('The', table)

sent()

# Tree ADT

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    if change_abstraction.changed:
        for branch in branches:
            assert is_tree(branch), 'branches must be trees'
        return {'label': label, 'branches': list(branches)}
    else:
        for branch in branches:
            assert is_tree(branch), 'branches must be trees'
        return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    if change_abstraction.changed:
        return tree['label']
    else:
        return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    if change_abstraction.changed:
        return tree['branches']
    else:
        return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if change_abstraction.changed:
        if type(tree) != dict or len(tree) != 2:
            return False
        for branch in branches(tree):
            if not is_tree(branch):
                return False
        return True
    else:
        if type(tree) != list or len(tree) < 1:
            return False
        for branch in branches(tree):
            if not is_tree(branch):
                return False
        return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def change_abstraction(change):
    change_abstraction.changed = change

change_abstraction.changed = False


def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

