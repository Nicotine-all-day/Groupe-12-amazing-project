# Tic-Tac-Toe game

# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Function to check if there is a winner
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if all(spot == player for spot in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all(spot != " " for row in board for spot in row)

# Function to handle player moves
def player_move(board, player):
    while True:
        move = input(f"Player {player}, enter your move (row and column as 'row,col'): ")
        try:
            row, col = map(int, move.split(","))
            if board[row][col] == " ":
                board[row][col] = player
                break
            else:
                print("This spot is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as 'row,col'.")

# Main game function
def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]  # Create a 3x3 board
    current_player = "X"
    
    while True:
        print_board(board)
        
        # Player makes a move
        player_move(board, current_player)
        
        # Check if there's a winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        # Check if it's a tie
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        # Switch players
        current_player = "O" if current_player == "X" else "X"

# Run the game
if __name__ == "__main__":
    tic_tac_toe()
