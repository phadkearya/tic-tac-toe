
# Importing the necessary libraries.
from math import inf
from os import system
from time import sleep

#  Declaring the gameboard and the numbers representing the cells globally so that it becomes more convenient to use.

BOARD = [
    [0, 0 ,0],
    [0, 0, 0],
    [0, 0, 0]
]

# Actions is used to represent the cells of the gmeboard.

ACTIONS = {
    0: [0, 0], 1: [0, 1], 2: [0, 2],
    3: [1, 0], 4: [1, 1], 5: [1, 2],
    6: [2, 0], 7: [2, 1], 8: [2, 2],
}

# Setting variables called human and agent(for computer)

HUMAN = -1
AGENT = +1
NONE = 0

BLANK = ' '
LINE = '\n----------------'

# eval function whihc decides if the Computer wins, or the user wins, or it is a draw.

def eval(state):
    # Return +1 if the Computer wins
    if winner(state, AGENT):
        return +1
    # Return -1 if the user wins
    elif winner(state, HUMAN):
        return -1
    # Return 0 if it is a draw
    else:
        return 0

# Function to check if a winning combination is present on the board in the current stage of the game.

def winner(state, player):
    # Returns true if the player has won or else returns false
    win_state = [
        [state[0][0], state[0][1], state[0][2]], # Row 1
        [state[1][0], state[1][1], state[1][2]], # Row 2
        [state[2][0], state[2][1], state[2][2]], # Row 3
        [state[0][0], state[1][0], state[2][0]], # Col 1
        [state[0][1], state[1][1], state[2][1]], # Col 2
        [state[0][2], state[1][2], state[2][2]], # Col 3
        [state[0][0], state[1][1], state[2][2]], # Diag 1
        [state[2][0], state[1][1], state[0][2]], # Diag 2
    ]
    return True if [player, player, player] in win_state else False

# Checks if the game is over means if any player has already won at the current stage.
# Just involves calling the winner function for Computer and user,

def game_over(state):
    return winner(state, AGENT) or winner(state, HUMAN)

# Blank_tiles function to check if there are any blank cells available in the board or if the board is completely filled.

def blank_tiles(state):
    # Returns a list of available blank cells.
    blanks = list()
    for i, row in enumerate(state):
        for j, tile in enumerate(row):
            if not tile:
                blanks.append([i, j])

    return blanks

# valid_action fucntion to check if the inout given by the user is correct. Basically checks if the cell given by the user is empty or not.

def valid_action(i, j):
    return True if [i, j] in blank_tiles(BOARD) else False

# apply_action function to apply the action mentioned to the gamboard if it is valid and returns true. If it is invalid it simply returns false.

def apply_action(i, j, player):
    if valid_action(i, j):
        BOARD[i][j] = player
        return True
    else:
        False

# Implementation of minimax algorithm

def minimax(state, depth, player):
    """
    Minimax implementation.
    Returns: Max or Min for (row, col, score)
    """
    if player == AGENT:
        maximise = [-1, -1, -inf]
    else:
        maximise = [-1, -1, +inf]

    if depth == 0 or game_over(state):
        score = eval(state)
        return [-1, -1, score]

    for tile in blank_tiles(state):
        i, j = tile[0], tile[1]
        state[i][j] = player
        score = minimax(state, depth - 1, -player)
        state[i][j] = 0
        score[0], score[1] = i, j

        if player == AGENT:
            """
            Max Value
            """
            if score[2] > maximise[2]:
                maximise = score
        else:
            """
            Min Value
            """
            if score[2] < maximise[2]:
                maximise = score

    return maximise

# print_board  function just prints the gameboard at its current state.

def print_board(state, agent_piece, human_piece):
    pieces = {
    HUMAN: human_piece,
    AGENT: agent_piece,
    NONE: BLANK
    }
    print(LINE)
    for row in state:
        for tile in row:
            print(f" {pieces[tile]} |", end='')
        print(LINE)

# agent function to call minimax. This is usd when it is the computer's chance to make a move.

def agent(agent_piece, human_piece):
    """
    Agent function to call minimax.
    No depth limit mwuahahaha (going to regret this)
    Returns: None, just applies a move.
    """
    depth = len(blank_tiles(BOARD))
    if depth == 0 or game_over(BOARD):
        # The game has ended when the board is full.
        return None

    # Printing the board.

    print_board(BOARD, agent_piece, human_piece)
    print(f"Computer's Turn (Piece: {agent_piece})")

    # Applying minimax algorithm.

    """
    Recall that input is: state, depth, player
    """
    move = minimax(BOARD, depth, AGENT)
    apply_action(move[0], move[1], AGENT)

    sleep(0.5)

# Function for the turn if the user.

def human(agent_piece, human_piece):
    depth = len(blank_tiles(BOARD))

    # Checking if the game is over.

    if depth == 0 or game_over(BOARD):
        return None

    # If the game is not over prints the board.

    print_board(BOARD, agent_piece, human_piece)
    print(f"Your Turn (Piece: {human_piece})")

    # Takes input from the user about which cell to fill. If the user gives an already occupied cell or number which is not between 0-8 it will give error message and ask for input again

    while True:
        action = input("Enter your action (0 - 8): ")
        if action.isdigit() and int(action) in range(9):
            action = int(action)
            try:
                coord = ACTIONS[action]
                if apply_action(coord[0], coord[1], HUMAN):
                    break
                else:
                    print("Invalid Action. Try Again")
            except:
                print("Invalid Action. Try Again")
        else:
            print("Invalid Action. Try Again")

# Main function.

def main():

    # Letting the user choose X or O. The player who has X will always play first.

    human_piece = False
    while not human_piece: # Originally defined as '' so it should be None
        print("ORDER: X goes first, and O goes second.")
        choice = input("Choose X or O: ").upper()
        if choice == 'X' or choice == 'O':
            human_piece = choice
            # Computer is O and human is X
            if choice == 'X':
                agent_piece = 'O'
            else:
                # Compiuter is X and human is O
                agent_piece = 'X'
            print("Successful. Let's start the game!")
        else:
            # If the user enters anything other than X or O then it will give error and ask for input again.
            print("Invalid Entry. Try Again.")

    # If the Computerhas to play first go to the agent function.

    if choice == 'O':
        agent(agent_piece, human_piece)

    # We are writing the below lines to let the game continue. This will happen as long as there are blank tiles left on the board or there is no winning combinationon the board.
    # Alternate turns of the user and Computer till gameboard gets filled or there is a winner.

    while len(blank_tiles(BOARD)) > 0 and not game_over(BOARD):
        human(agent_piece, human_piece)
        agent(agent_piece, human_piece)

    # Printing the board after the game has ended.

    print_board(BOARD, agent_piece, human_piece)

    # If the user is the winner it prints a corresponding statement.

    if winner(BOARD, HUMAN):
        print("YOU WIN!")
        # If the Computer wins, prints the corresponding statement.
    elif winner(BOARD, AGENT):
        print("YOU LOSE! BETTER LUCK NEXT TIME!")
        # If it is a draw, prints the corresponding statement.
    else:
        print("DRAW!")

    exit()

if __name__ == '__main__':
    main()
