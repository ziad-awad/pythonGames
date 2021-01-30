"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the 
    next player to move. 
    
    The function plays a game starting with the 
    given player by making random moves, alternating 
    between players. 
    
    The modified board will contain the state of the game.
    """
    while board.check_win() == None:
        # we select a board with empty squares
        board_empty_squares = board.get_empty_squares()
        # we select a random square in order to move there
        random_square = random.choice(board_empty_squares)
        #we make the move
        board.move(random_square[0], random_square[1], player)
        # we switch the player
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores with the same 
    dimensions as the Tic-Tac-Toe board, a board from 
    a completed game, and which player the machine
    player is.
    
    The function scores the completed board and updates 
    the scores grid. 
    """
    # we get the board dimension in order to iterate through it
    board_dimension = range(board.get_dim())
    # we get the winner
    winner = board.check_win() 
    # we do the iteration and add or substract the scores for win and looses 
    # based on a comparison between the winner and the current player
    for row in board_dimension:
        for col in board_dimension:
            current_player = board.square(row, col)
            if current_player == provided.PLAYERX and winner == provided.PLAYERX:
                scores[row][col] += SCORE_CURRENT
            elif current_player == provided.PLAYERX and winner == provided.PLAYERO:
                scores[row][col] += (-1)*SCORE_OTHER
            elif current_player == provided.PLAYERO and winner == provided.PLAYERX:
                scores[row][col] += (-1)*SCORE_OTHER
            elif current_player == provided.PLAYERO and winner == provided.PLAYERO:
                scores[row][col] += SCORE_CURRENT
        
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of 
    scores. The function finds all of the empty squares 
    with the maximum score and randomly return one of 
    them as a (row, column) tuple.
    """
    # we initialize the compare variables
    max_score_list = list()
    max_comparison = None
    # we get the board dimension in order to iterate through it
    board_dimension = range(board.get_dim())
    # we get the board with empty squares
    board_empty_squares = board.get_empty_squares()
    
    # we iterate through the board to get the empty squares 
    # that has max values
    for row in board_dimension:
        for col in board_dimension:
            current_position = (row, col)
            if max_comparison == None and current_position in board_empty_squares:
                max_comparison = scores[row][col]
                max_score_list = list([current_position])
            elif scores[row][col] > max_comparison and current_position in board_empty_squares:
                max_comparison = scores[row][col]
                max_score_list = list([current_position])
            elif scores[row][col] == max_comparison and current_position in board_empty_squares:
                max_score_list.append(current_position)
    
    random_max_move = random.choice(max_score_list)
    
    return random_max_move

def mc_move(board, player, trials):
    """
    This function takes a current board, which player 
    the machine player is, and the number of trials
    to run. This function uses the Monte Carlo simulation 
    to return a move for the machine player in the form 
    of a (row, column) tuple. 
    """
    #we populate the scores list with 0's
    scores = [[0 for _ in range(board.get_dim())] 
                          for _ in range(board.get_dim())]
    # given the number of trials we simulate and get the best move
    for _ in range(trials):
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(scores, cloned_board, player)
    
    best_move = get_best_move(board, scores)
    
    return best_move
        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
