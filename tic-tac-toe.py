HUMAN = +1 # X player
BOT = -1 # O player

RANGE = 5

DEPTH = 5

board = None

# Evaluate the board: +1 if the human wins; -1 if the bot wins; 0 if it's a tie
def evaluate(board):
    # Check rows
    for i in range(RANGE):
        for j in range(RANGE - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                if board[i][j] == 'X':
                    return 1
                elif board[i][j] == 'O':
                    return -1

    # Check columns
    for i in range(RANGE - 3):
        for j in range(RANGE):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                if board[i][j] == 'X':
                    return 1
                elif board[i][j] == 'O':
                    return -1

    # Check diagonals
    for i in range(RANGE - 3):
        for j in range(RANGE - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                if board[i][j] == 'X':
                    return 1
                elif board[i][j] == 'O':
                    return -1
    
    for i in range(RANGE - 3):
        for j in range(3, RANGE):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3]:
                if board[i][j] == 'X':
                    return 1
                elif board[i][j] == 'O':
                    return -1
                
    # Check for a tie
    if all(cell != ' ' for row in board for cell in row):
        return 0

    # Count the number of X and O
    count_X = sum(row.count('X') for row in board)
    count_O = sum(row.count('O') for row in board)

    if count_X > count_O:
        return 0.5
    elif count_O > count_X:
        return -0.5
    return 0

def print_board(board):
    print("   " + "   ".join(str(i) for i in range(RANGE)))
    for i, row in enumerate(board):
        print(i, end="  ")
        print(" | ".join(cell for cell in row))
        if i < RANGE - 1:
            print("  " + "-" * (4 * RANGE - 1))

# Determine if a player has won
def is_game_over(board):
    if evaluate(board) == 1 or evaluate(board) == -1:
        return True
    return False


# Function to make a move
def make_move(board, row, col, player):
    board[row][col] = player

# Function to undo a move
def undo_move(board, row, col):
    board[row][col] = ' '

def is_move_valid(board, row, col):
    return 0 <= row < RANGE and 0 <= col < RANGE and board[row][col] == ' '

# Alpha-Beta Pruning algorithm
def minimax(board, depth, alpha, beta, maximizing_player):
    # Check if the game is over or the maximum depth has been reached
    if is_game_over(board) or depth == 0:
        return evaluate(board)

    if maximizing_player:
        max_score = float('-inf')
        for row in range(RANGE):
            for col in range(RANGE):
                if board[row][col] == ' ':
                    make_move(board, row, col, 'X')
                    score = minimax(board, depth - 1, alpha, beta, False)
                    undo_move(board, row, col)
                    max_score = max(max_score, score)
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                    break
        return max_score
    else:
        min_score = float('inf')
        for row in range(RANGE):
            for col in range(RANGE):
                if board[row][col] == ' ':
                    make_move(board, row, col, 'O')
                    score = minimax(board, depth - 1, alpha, beta, True)
                    undo_move(board, row, col)
                    min_score = min(min_score, score)
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
        return min_score

# Find the best move using the Alpha-Beta Pruning algorithm
# Bot is minimizing player
def find_best_move(board):
    best_eval = float('inf')
    best_move = None
    for row in range(RANGE):
        for col in range(RANGE):
            if board[row][col] == ' ':
                make_move(board, row, col, 'O')
                eval = minimax(board, DEPTH, float('-inf'), float('inf'), True)
                undo_move(board, row, col)
                if eval < best_eval:
                    best_eval = eval
                    best_move = (row, col)
    return best_move

def main():
    board = [[' ' for _ in range(RANGE)] for _ in range(RANGE)]
    print("Enter row and column (0-indexed) separated by space. Example: '0 1'")
    print_board(board)

    while not is_game_over(board):
        human_move = input("Enter your move (row col): ").split()
        if len(human_move) != 2:
            print("Invalid input! Please enter row and column separated by space.")
            continue
        try:
            row, col = map(int, human_move)
        except ValueError:
            print("Invalid input! Please enter valid integers.")
            continue

        if is_move_valid(board, row, col):
            make_move(board, row, col, 'X')
            print_board(board)
        else:
            print("Invalid move! Please select an empty cell.")
            continue

        if is_game_over(board):
            break

        print("Bot is thinking...")
        
        bot_row, bot_col = find_best_move(board)
        make_move(board, bot_row, bot_col, 'O')
        print_board(board)

    result = evaluate(board)
    print(result)
    if result == 1:
        print("Congratulations! You win!")
    elif result == -1:
        print("Bot wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()