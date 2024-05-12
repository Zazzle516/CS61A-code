"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    index_to_k = -1
    for sub_string in paragraphs:
        if select(sub_string):
            index_to_k += 1
            if index_to_k == k:
                return sub_string
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    import re
    def my_remove_punctuation(sentence):
        return re.sub(r'[^\w\s]', '', sentence)
    def is_contain(sentence):
        # replace all the punctuation to space
        sentence = my_remove_punctuation(sentence)
        # sentence to word 
        words = sentence.split(" ")     # ['word-0','word-1'...]
        # 去除特殊符号对单词的影响 并转变为小写进行判断 
        for word in words:
            # if word[0] == '"':
            #     word = word.join(i for i in word if i not in '"')
            word = word.lower()
            if word in topic:
                return True
        return False
    return is_contain
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if len(typed_words) == len(reference_words) == 0:
        return 100.0
    elif len(typed_words) == 0:
        return 0.0
    correct = 0
    for x, y in zip(typed_words, reference_words):
        if x == y:
            correct += 1
    return correct / len(typed_words) * 100.0
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    typical_word_length = 5
    char_number = len(typed)

    unit_word = char_number / typical_word_length
    time_num = 60.0 / elapsed
    total_word = time_num * unit_word
    return total_word
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word not in valid_words:
        min_limit = limit
        correct_word = user_word
        for valid_word in valid_words[::-1]:
            curr_diff = diff_function(user_word, valid_word, limit)
            print("DEBUG: " + "Compare " + user_word + " with " + valid_word + " and score: " + str(curr_diff))
            if curr_diff <= min_limit:
                min_limit = curr_diff
                correct_word = valid_word
        return correct_word
    return user_word
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def inner_score(start, goal, curr_limit,total_limit):
        if curr_limit > total_limit:
            # 提前结束判断 
            return total_limit + 1
        if len(start) == 0 or len(goal) == 0:
            # 到达递归终点 
            return abs(len(start) - len(goal))
        else:
            # print("DEBUG: " + start[0])
            curr_limit += (0 if start[0] == goal[0] else 1)
            # print("DEBUG: " + str(curr_limit))
            return (0 if start[0] == goal[0] else 1) + inner_score(start[1:], goal[1:], curr_limit, limit)
    return inner_score(start, goal, 0, limit)
    # END PROBLEM 6

def meowstake_matches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def inner_match(start, goal, curr_limit, limit):
        if curr_limit > limit:
            return limit + 1
        if len(start) <= 1 or len(goal) <= 1:
            # 可能余下最后一个字符判断 问题出在这里 or 的使用 spell speling 差异判断会提前结束 
            if len(start) != len(goal):
                return abs(len(start) - len(goal))
            else:
                if start == goal:
                    return 0
                return 1

        if start[0] != goal[0]:
            curr_limit += 1
            if start[0] == goal[1]:
                print("DEBUG: " + "head_insert " + goal[1])
                # 原单词缺少 goal[0] 字符 head_insert 
                # print("DEBUG: " + "head_insert " + goal[0])
                list_string_start = list(start)
                # print("DEBUG: " + str(list_string_start))
                list_string_goal = list(goal)
                list_string_start = list_string_start[::-1]
                # print("DEBUG: " + str(list_string_start))
                list_string_start.append(list_string_goal[0])
                print("DEBUG: " + str(list_string_start[::-1]))
                list_string_start = list_string_start[::-1]
                start = ''.join(list_string_start)
                return 1 + inner_match(start, goal, curr_limit, limit)
            if start[1] == goal[0]:
                # 原单词多出 goal[0] 字符 remove 
                print("DEBUG: " + "remove " + start[0])
                list_string_start = list(start)
                list_string_start = list_string_start[1:]
                start = ''.join(list_string_start)
                return 1 + inner_match(start, goal, curr_limit, limit)
            if start[1] == goal[1]:
                # 原单词替换 goal[0] 字符 replace 
                print("DEBUG: " + "replace " + goal[0])
                # start[0] = goal[0]
                # string in python can not be changed, so if you want to change that, better do that in list.
                list_string = list(start)
                list_string[0] = goal[0]
                start = ''.join(list_string)
                return 1 + inner_match(start, goal, curr_limit, limit)
            else:
                print("DEBUG: " + "other_cases ")
                # 剩余的任意情况 head_insert 
                list_string_start = list(start)
                list_string_goal = list(goal)
                list_string_start = list_string_start[::-1]
                list_string_start.append(list_string_goal[0])
                print("DEBUG: " + str(list_string_start[::-1]))
                start = ''.join(list_string_start[::-1])
                return 1 + inner_match(start, goal, curr_limit, limit)
        else:
            return inner_match(start[1:], goal[1:], curr_limit, limit)
    return inner_match(start, goal, 0, limit)
    # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    # 计算当前进度 
    total_count = len(prompt)   # 统计标准 
    curr_progress = 0
    for typed_word, prompt_word in zip(typed, prompt):
        if typed_word == prompt_word:
            curr_progress += 1
        else:
            break
    curr_score = curr_progress / total_count
    curr_dict = {}
    curr_dict['id'] = id
    curr_dict['progress'] = curr_score
    send(curr_dict)
    return curr_score
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    time_list_player_0 = []
    for word_time in range(0, len(times_per_player[0]) - 2):
        time_list_player_0.append( times_per_player[0][word_time + 1] - times_per_player[0][word_time] )
    
    time_list_player_1 = []
    for word_time in range(0, len(times_per_player[1]) - 2):
        time_list_player_1.append( times_per_player[1][word_time + 1] - times_per_player[1][word_time] )
    
    time_list = [time_list_player_0, time_list_player_1]
    
    return game(words, time_list)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player 玩家总数
    words = range(len(all_words(game)))    # An index for each word 单词总数 
    # # BEGIN PROBLEM 10
    # "*** YOUR CODE HERE ***"
    # player_id_list = list(players)[::-1]
    # print("DEBUG: " + "reversed_player_index: " + str(player_id_list))
    # # 多维列表按列的访问    两层循环实现 
    # single_word_min_time_player = -1
    # min_time_word_list = [[] for _ in players]
    # print("DEBUG: " + "resulr_list_init: " + str(min_time_word_list))
    
    # # 找到每个单词打印最短时间的玩家 id 
    # for single_word_index in words:
    #     single_word_min_time = float('inf')
    #     print("DEBUG: " + "outter_loop: " + str(single_word_index))
    #     for single_player_index in player_id_list:
    #         single_word_time = time(game, single_player_index, single_word_index)
    #         print("DEBUG: " + str(single_word_time))
    #         if single_word_time < single_word_min_time:
    #             single_word_min_time = single_word_time
    #             single_word_min_time_player = single_player_index
    #             print("DEBUG: " + "find player: " + str(single_player_index))
    #     # 离开内层循环 此时已经找到某一个单词的最小值的玩家 id 
    #     print("DEBUG: " + "sub_resulr_list: " + str(min_time_word_list[single_word_min_time_player]))
    #     min_time_word_list[single_word_min_time_player].append(word_at(game, single_word_index))
    #     print("DEBUG: " + "resulr_list: " + str(min_time_word_list))
    # return min_time_word_list

    fastest = [[] for _ in players]
    print("DEBUG: " + "init: " + str(fastest))  # 显示没有区别啊 
    for word_index in words:
        min_time = float('inf')
        player = 0
        for player_index in players:
            if time(game, player_index, word_index) < min_time:
                min_time = time(game, player_index, word_index)
                player = player_index
        fastest[player].append(word_at(game, word_index))
    return fastest

    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you

##########################
# Extra Credit #
##########################

key_distance = get_key_distances()  # 已经给出任意两个 key 之间的 distace 
def key_distance_diff(start, goal, limit):
    """ A diff function that takes into account the distances between keys when
    computing the difference score."""

    start = start.lower() #converts the string to lowercase
    goal = goal.lower() #converts the string to lowercase

    # BEGIN PROBLEM EC1
    "*** YOUR CODE HERE ***"
    # 发生在 replace 功能实现中 我先假设已经在 replace 了
    def inner_distance(start, goal, curr_limit, limit):
        if curr_limit > limit:
            return limit + 1
        if len(start) == 0 or len(goal) == 0:
            return 0
        if start[0] == goal[0]:
            return inner_distance(start[1:], goal[1:], curr_limit, limit)
        else:
            curr_limit += key_distance[start[0],goal[0]]
            return key_distance[start[0],goal[0]] + inner_distance(start[1:], goal[1:], curr_limit, limit)
    return inner_distance(start, goal, 0, limit)
    # END PROBLEM EC1

def memo(f):
    """A memoization function as seen in John Denero's lecture on Growth"""

    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized

key_distance_diff = count(key_distance_diff)


def faster_autocorrect(user_word, valid_words, diff_function, limit):
    """A memoized version of the autocorrect function implemented above."""

    # BEGIN PROBLEM EC2
    "*** YOUR CODE HERE ***"
    # END PROBLEM EC2


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)