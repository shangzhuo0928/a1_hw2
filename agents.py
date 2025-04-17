import numpy as np
import random
import game
import datetime
import copy
import sys

today = datetime.date.today()
today = today.strftime("%Y/%m/%d")
def print_INFO():
    """
    Prints your homework submission details.
    Please replace the placeholders (date, name, student ID) with valid information
    before submitting.
    """
    print(
        f"""========================================
        DATE: {today}
        STUDENT NAME: 何嘉婗
        STUDENT ID: 109550072
        ========================================
        """)


#
# Basic search functions: Minimax and Alpha‑Beta
#

def minimax(grid, depth, maximizingPlayer, dep=4):
    """
    TODO (Part 1): Implement recursive Minimax search for Connect Four.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
    """
    set_of_col = set()
    if depth == dep or grid.terminate():
        score = get_heuristic(grid)
        return (score, set_of_col)
    if maximizingPlayer:
        score = -sys.maxsize
    else:
        score = sys.maxsize
    for col in range(7):
        if grid.table[0][col] == 0:
          newgrid = game.drop_piece(grid, col)
          Tuple = minimax(newgrid, depth+1, not maximizingPlayer, dep)
          if not maximizingPlayer :
            if score > Tuple[0]:
              score  = Tuple[0]
              set_of_col = {col}
            elif score == Tuple[0]:
              set_of_col.add(col)
          else:
            if score < Tuple[0]:
              score = Tuple[0]
              set_of_col = {col}
            elif score == Tuple[0]:
              set_of_col.add(col)

    # Placeholder return to keep function structure intact
    return (score, set_of_col)

def alphabeta(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    TODO (Part 2): Implement Alpha-Beta pruning as an optimization to Minimax.

    Return:
      (boardValue, {setOfCandidateMoves})

    Where:
      - boardValue is the evaluated utility of the board state
      - {setOfCandidateMoves} is a set of columns that achieve this boardValue
      - Prune branches when alpha >= beta
    """
    set_of_col = set()
    if depth == dep or grid.terminate():
      score = get_heuristic(grid)
      return (score, set_of_col)
    if maximizingPlayer:
      score = -sys.maxsize
    else:
      score = sys.maxsize
    for col in range(7):
      if grid.table[0][col] == 0:
        newgrid = game.drop_piece(grid, col)
        Tuple = alphabeta(newgrid, depth+1,not maximizingPlayer, alpha, beta,  dep)
        if not maximizingPlayer : #min
          if score > Tuple[0]:
            score = Tuple[0]
            set_of_col = {col}
          elif score == Tuple[0]:
            set_of_col.add(col)
          if score <= alpha :
            return (score, set_of_col)
          else:
            beta = min(beta, score)
        else:                  #max
          if score < Tuple[0]:
            score = Tuple[0]
            set_of_col = {col}         
          elif score == Tuple[0]:
            set_of_col.add(col)
          if score >= beta :
            return (score, set_of_col)
          else:
            alpha = max(alpha, score)

    # Placeholder return to keep function structure intact
    return (score, set_of_col)


#
# Basic agents
#

def agent_minimax(grid):
    """
    Agent that uses the minimax() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(minimax(grid, 0, True)[1]))


def agent_alphabeta(grid):
    """
    Agent that uses the alphabeta() function with a default search depth (e.g., 4).
    Must return a single column (integer) where the piece is dropped.
    """
    return random.choice(list(alphabeta(grid, 0, True, -np.inf, np.inf)[1]))


def agent_reflex(grid):
    """
    A simple reflex agent provided as a baseline:
      - Checks if there's an immediate winning move.
      - Otherwise picks a random valid column.
    """
    wins = [c for c in grid.valid if game.check_winning_move(grid, c, grid.mark)]
    if wins:
        return random.choice(wins)
    return random.choice(grid.valid)


def agent_strong(grid):
    """
    TODO (Part 3): Design your own agent (depth = 4) to consistently beat the Alpha-Beta agent (depth = 4).
    This agent will typically act as Player 2.
    """
    # Placeholder logic that calls your_function().
    return random.choice(list(your_function(grid, 0, False, -np.inf, np.inf)[1]))


#
# Heuristic functions
#

def get_heuristic(board):
    """
    Evaluates the board from Player 1's perspective using a basic heuristic.

    Returns:
      - Large positive value if Player 1 is winning
      - Large negative value if Player 2 is winning
      - Intermediate scores based on partial connect patterns
    """
    num_twos       = game.count_windows(board, 2, 1)
    num_threes     = game.count_windows(board, 3, 1)
    num_twos_opp   = game.count_windows(board, 2, 2)
    num_threes_opp = game.count_windows(board, 3, 2)

    score = (
          1e10 * board.win(1)
        + 1e6  * num_threes
        + 10   * num_twos
        - 10   * num_twos_opp
        - 1e6  * num_threes_opp
        - 1e10 * board.win(2)
    )
    return score


def get_heuristic_strong(board):
    """
    TODO (Part 3): Implement a more advanced board evaluation for agent_strong.
    Currently a placeholder that returns 0.
    """
    num_twos_1, num_twos_2             = count_windows_strong(board, 2, 1)
    num_threes_1, num_threes_2         = count_windows_strong(board, 3, 1)
    num_twos_opp_1, num_twos_opp_2     = count_windows_strong(board, 2, 2)
    num_threes_opp_1, num_threes_opp_2 = count_windows_strong(board, 3, 2)

    score = (
          1e10 * board.win(1) 
        + 1e8  * num_threes_2 
        + 1e5  * num_threes_1
        + 1e3  * num_twos_2
        + 10   * num_twos_1
        - 10   * num_twos_opp_1
        - 1e3  * num_twos_opp_2
        - 1e5  * num_threes_opp_1
        - 1e8  * num_threes_opp_2
        - 1e10 * board.win(2) 
    )
    return score

c = [3, 2, 4, 1, 5, 0, 6]
def your_function(grid, depth, maximizingPlayer, alpha, beta, dep=4):
    """
    A stronger search function that uses get_heuristic_strong() instead of get_heuristic().
    You can employ advanced features (e.g., improved move ordering, deeper lookahead).

    Return:
      (boardValue, {setOfCandidateMoves})

    Currently a placeholder returning (0, {0}).
    """
    set_of_col = set()
    if depth == dep or grid.terminate():
      score = get_heuristic_strong(grid)
      return (score, set_of_col)
    if maximizingPlayer:
      score = -sys.maxsize
    else:
      score = sys.maxsize
    for col in c:
        if grid.table[0][col] == 0:
          newgrid = game.drop_piece(grid, col)
          Tuple = your_function(newgrid, depth+1,not maximizingPlayer, alpha, beta,  dep)
          if not maximizingPlayer :
            if score > Tuple[0]:
              score = Tuple[0]
              set_of_col = {col}
            elif score == Tuple[0]:
              set_of_col.add(col)
            if score < alpha :
              break
            else:
              beta = min(beta, score)
          else:
            if score < Tuple[0]:
              score = Tuple[0]
              set_of_col = {col}
            elif score == Tuple[0]:
              set_of_col.add(col)
            if score > beta :
              break
            else:
              alpha = max(alpha, score)
    return (score, set_of_col)

def count_windows_strong(board, num_discs, piece):
    """Count the number of contiguous segments ('windows') of length board.connect with 'num_discs' of 'piece'."""
    num_windows_e1 = 0
    num_windows_e2 = 0
    # Horizontal windows.
    for r in range(board.row):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[r, c:c + board.connect])
            if game.check_window(board, window, num_discs, piece):
              if (c-1 >= 0 and board.table[r][c-1] == 0) and (c+num_discs+1 < 7 and board.table[r][c+num_discs+1] == 0):
                num_windows_e2 += 1
              elif (c-1 >= 0 and board.table[r][c-1] == 0) or (c+num_discs+1 < 7 and board.table[r][c+num_discs+1] == 0):
                num_windows_e1 += 1 
    # Vertical windows.
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column):
            window = list(board.table[r:r + board.connect, c])
            if game.check_window(board, window, num_discs, piece):
              if (r-1 >= 0 and board.table[r-1][c] == 0) and (r+num_discs+1 < 6 and board.table[r+num_discs+1][c] == 0):
                num_windows_e2 += 1
              elif (r-1 >= 0 and board.table[r-1][c] == 0) or (r+num_discs+1 < 6 and board.table[r+num_discs+1][c] == 0):
                num_windows_e1 += 1 
    # Positive diagonal windows.
    for r in range(board.row - (board.connect - 1)):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[range(r, r + board.connect), range(c, c + board.connect)])
            if game.check_window(board, window, num_discs, piece):
              if (r-1 >= 0 and c-1 >=0 and board.table[r-1][c-1] == 0) and (r+num_discs+1 < 6 and c+num_discs+1 < 7 and board.table[r+num_discs+1][c+num_discs+1] == 0):
                num_windows_e2 += 1
              elif (r-1 >= 0 and c-1 >=0 and board.table[r-1][c-1] == 0) or (r+num_discs+1 < 6 and c+num_discs+1 < 7 and board.table[r+num_discs+1][c+num_discs+1] == 0):
                num_windows_e1 += 1 
    # Negative diagonal windows.
    for r in range(board.connect - 1, board.row):
        for c in range(board.column - (board.connect - 1)):
            window = list(board.table[range(r, r - board.connect, -1), range(c, c + board.connect)])
            if game.check_window(board, window, num_discs, piece):
              if (r+num_discs+1 < 6 and c-1 >=0 and board.table[r+num_discs+1][c-1] == 0) and (r-1 >= 0 and c+num_discs+1 < 7 and board.table[r-1][c+num_discs+1] == 0):
                num_windows_e2 += 1
              elif (r+num_discs+1 < 6 and c-1 >=0 and board.table[r+num_discs+1][c-1] == 0) or (r-1 >= 0 and c+num_discs+1 < 7 and board.table[r-1][c+num_discs+1] == 0):
                num_windows_e1 += 1
    return (num_windows_e1, num_windows_e2)
