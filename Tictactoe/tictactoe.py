"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xcalc = 0
    Ocalc = 0

    for row in board:
        Xcalc += row.count(X)
        Ocalc += row.count(O)

    if Xcalc <= Ocalc:
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_possible = set()

    for row_indx, row in enumerate(board):
        for column_indx, item in enumerate(row):
            if item == None:
                actions_possible.add((row_indx, column_indx))
    
    return actions_possible
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_movement = player(board)

    new_board = deepcopy(board)
    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player_movement

    return new_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):
        # vertical check
            for row in board:
                if row == [player] * 3:
                    return player

        # horizontal check
            for i in range(3):
                column = [board[x][i] for x in range(3)]
                if column == [player] * 3:
                    return player
        
        # diagonal check
            if [board[i][i] for i in range(0, 3)] == [player] * 3:
                return player

            elif [board[i][~i] for i in range(0, 3)] == [player] * 3:
                return player
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # a player wins
    if winner(board) != None:
        return True

    # there are still movements
    for row in board:
        if EMPTY in row:
            return False

    # there are no more movements
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player= winner(board)

    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        i = "i"
        j = "j"
        optim_move = (i, j)
        if terminal(board):
            return utility(board), optim_move
        else:
            val = -5
            for action in actions(board):
                minval = min_value(result(board, action))[0]
                if minval > val:
                    val = minval
                    optim_move = action
            return val, optim_move

    def min_value(board):
        optim_move = ()
        if terminal(board):
            return utility(board), optim_move
        else:
            val = 5
            for action in actions(board):
                maxval = max_value(result(board, action))[0]
                if maxval < val:
                    val = maxval
                    optim_move = action
            return val, optim_move

    current_player = player(board)

    if terminal(board):
        return None

    if current_player == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]

    raise NotImplementedError
