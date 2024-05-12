"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# 本轮内扔指定次数的色子 返回结果 
# 在 phase3 中要用到 
def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    sum = 0
    is_dice1 = False

    # 扔足够的次数 
    for i in range(1,num_rolls + 1):
        temp_res = dice()
        if(temp_res == 1):
            is_dice1 = True
        else:
            sum += temp_res

    # 结果判断 
    if(is_dice1 == True):
        return 1
    return sum
    # END PROBLEM 1

# 本轮内一次不扔的
def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # 一次都不扔色子的玩家 固定获得的分数 
    ones_num = score % 10
    tens_num = score // 10
    return 10 - ones_num + tens_num
    # END PROBLEM 2

# 本轮的得分结果 
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if(num_rolls == 0):
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls,dice)
    # END PROBLEM 3

# 本轮结束后的分数判定 
def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    oppo_tens_num = (opponent_score // 10) % 10
    oppo_ones_num = opponent_score % 10
    player_ones_num = player_score % 10

    ones_num_gap = oppo_ones_num - player_ones_num
    if(abs(ones_num_gap) == oppo_tens_num):
        return True
    return False
    # END PROBLEM 4

# 返回对手玩家 id 
def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    # 通过标号让玩家轮流扔色子 
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence

# 实现之前：我应该是全局的视角还是其中一个玩家的视角 
# 从命名方式（01）来看应该是全局视角 

def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence, feral_hogs=True):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    feral_hogs: A boolean indicating whether the feral hogs rule should be active.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if(feral_hogs == False):
        while(score0 < goal and score1 < goal):
            # print("DEBUG:", strategy0(score0,score1))
            score0 += take_turn(strategy0(score0,score1),score1,dice)
            if(is_swap(score0,score1)):
                temp_score = score0
                score0 = score1
                score1 = temp_score
            say = say(score0,score1)
            if(score0 >= goal or score1 >= goal):
                break
            
            score1 += take_turn(strategy1(score1,score0),score0,dice)
            if(is_swap(score1,score0)):
                temp_score = score0
                score0 = score1
                score1 = temp_score
            say = say(score0,score1)
            if(score0 >= goal or score1 >= goal):
                break

    if(feral_hogs == True):
        last_score0 = 0
        last_score1 = 0

        while(score0 < goal and score1 < goal):

            play0_roll_time = strategy0(score0,score1)
            if(abs(play0_roll_time - last_score0) == 2):
                score0 += 3
            last_score0 = take_turn(play0_roll_time,score1,dice)

            score0 += last_score0
            if(is_swap(score0,score1)):
                temp_score = score0
                score0 = score1
                score1 = temp_score
            say = say(score0,score1)
            if(score0 >= goal or score1 >= goal):
                break

            play1_roll_time = strategy1(score1,score0)
            if(abs(play1_roll_time - last_score1) == 2):
                score1 += 3
            last_score1 = take_turn(play1_roll_time,score0,dice)

            score1 += last_score1
            if(is_swap(score1,score0)):
                temp_score = score0
                score0 = score1
                score1 = temp_score
            say = say(score0,score1)
            if(score0 >= goal or score1 >= goal):
                break    
    # END PROBLEM 5

    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)

    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # 就是插入 say function 即可 
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 17)
    Player 0 now has 6 and Player 1 now has 17
    Player 1 takes the lead by 11
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score = 0, running_high = 0):
# def announce_highest(who, last_score = 0, running_high = 0,para1 = 0 , para2 = 0):

    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20)
    >>> f5 = f4(20, 35)
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # 避免使用赋值语句 

# --------------------------------------------------------------------- #

    # def sub_func(not_impotant , current_score , last_current_score = last_score , max_score_gap = running_high):
    #     if( (current_score - last_current_score) > max_score_gap):
    #         max_score_gap = current_score - last_current_score
    #         print(max_score_gap,"point(s)! That's the biggest gain yet for Player",who)
        
    #     return announce_highest(who,current_score,max_score_gap)
    # return sub_func
    
# --------------------------------------------------------------------- #

    # def sub_func_both(current_score_0 , current_score_1):

    #     max_score_gap_0 = last_score
    #     max_score_gap_1 = running_high

    #     last_current_score_0 = para1
    #     last_current_score_1 = para2

    #     if(who == 0):
    #         if(current_score_0 - last_current_score_0 > max_score_gap_0):
    #             max_score_gap_0 = current_score_0 - last_current_score_0
    #             last_current_score_0 = current_score_0
    #             print(max_score_gap_0,"point(s)! That's the biggest gain yet for Player",who)
    #         last_current_score_0 = current_score_0
        
    #     else:
    #         if(current_score_1 - last_current_score_1 > max_score_gap_1):
    #             max_score_gap_1 = current_score_1 - last_current_score_1
    #             last_current_score_1 = current_score_1
    #             print(max_score_gap_1,"point(s)! That's the biggest gain yet for Player",who)
    #         # 没有超过最大 gap 的时候也要更新 last_current_score 
    #         last_current_score_1 = current_score_1

    #     return announce_highest(who,max_score_gap_0,max_score_gap_1,last_current_score_0,last_current_score_1)    
    # return sub_func_both

# --------------------------------------------------------------------- #

    def track_highest(score0, score1, highest=running_high):
        if who == 0:
            this_score = score0
        else:
            this_score = score1
        gain = this_score - last_score
        if gain > highest:
            print(gain, "point(s)! That's the biggest gain yet for Player", who)
            highest = gain
        return announce_highest(who, this_score, highest)
    return track_highest
    
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def returned_func(*args):
        res = 0
        for i in range(0,trials_count):
            res += original_function(*args)
        res /= trials_count
        return res
    return returned_func
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    roll_num = 0
    max_score = 0

    for i in range(1,11):
        max_score_temp = make_averaged(roll_dice,trials_count)(i,dice)
        if(max_score_temp > max_score):
            max_score = max_score_temp
            roll_num = i
    return roll_num

    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

# 可修改的执行代码 
def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"



def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    # cutoff: to decide whether 0 time is enough otherwise throw num_rolls times
    oppo_ones_num = opponent_score % 10
    oppo_tens_num = (opponent_score // 10 ) % 10
    free_score = 10 - oppo_ones_num + oppo_tens_num
    if(free_score >= cutoff):
        return 0    
    return num_rolls  # Replace this statement
    # END PROBLEM 10


def swap_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least CUTOFF points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    oppo_ones_num = opponent_score % 10
    oppo_tens_num = ( opponent_score // 10 ) % 10

    free_score = 10 - oppo_ones_num + oppo_tens_num
    player_current_score = score + free_score
    # print("DEBUG:", player_current_score,"玩家当前的分数")
    player_ones_num = player_current_score % 10

    if( abs(oppo_ones_num - player_ones_num) == oppo_tens_num):
        # 存在交换条件 
        if(opponent_score >= player_current_score):
            return 0
        else:
            return num_rolls
    else:
        if(free_score >= cutoff):
            # 额外进行交换判断
            return 0
    return num_rolls  # Replace this statement
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Replace this statement
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()