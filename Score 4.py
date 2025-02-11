import csv

# Load or create new board
new_game = input('Do you want to play a new game or continue? (press c to load saved game): ')
if new_game == 'c':
    with open("ng.csv", "r") as file:
        csv_reader = csv.reader(file)
        board = [row for row in csv_reader]
    size = len(board)
    # Replace "0" with space
    for x in range(size):
        for y in range(size):
            if board[x][y] == '0':
                board[x][y] = ' '
    with open("bottom.csv", "r") as b:
        csv_reader_2 = csv.reader(b)
        bottom_copy = [row for row in csv_reader_2]
    bottom = [int(x) for x in bottom_copy[0]]
else:
    size = 0
    while size < 5 or size > 10:
        size = int(input('What size do you want the board to be? (pick a number between 5 and 10):\n'))
        if size < 5 or size > 10:
            print('The size you gave is out of range')
    board = [[' ' for _ in range(size)] for _ in range(size)]
    bottom = [size - 1 for _ in range(size)]

grammata = ['A','B','C','D','E','F','G','H','I','J'][:size]
arithmoi = list(range(1, size+1))

def print_board():
    print('\n')
    for x in arithmoi:
        print('   ', x, end='   ')
    print('\n')
    print('  ' + '--------' * size)
    for x in range(size):
        print(grammata[x], '|', end='')
        for y in board[x]:
            print('  ', y, end='   |')
        print('')

print_board()

def get_neighbors(p):
    neighbors = []
    for x in range(p[0]-1, p[0]+2):
        for y in range(p[1]-1, p[1]+2):
            if [x, y] != p and x >= 0 and x < size and y >= 0 and y < size:
                neighbors.append([x, y])
    return neighbors

# Revised fix_board logic: remove winning pieces and simulate gravity.
def fix_board(coordinates):
    global board, bottom, points_O, points_X, size
    removed_count = 0
    # Remove winning pieces based on coordinates (assumes coordinates[1:] holds [row, col] positions)
    for coord in coordinates[1:]:
        r, c = coord
        if board[r][c] != ' ':
            board[r][c] = ' '
            removed_count += 1

    # Optionally update points (if you want to add removed_count to the score)
    if coordinates[0] == 'O':
        points_O += removed_count
    elif coordinates[0] == 'X':
        points_X += removed_count

    # Gravity: For each column, let pieces fall down
    for col in range(size):
        for row in range(size-1, -1, -1):
            if board[row][col] == ' ':
                for r in range(row-1, -1, -1):
                    if board[r][col] != ' ':
                        board[row][col] = board[r][col]
                        board[r][col] = ' '
                        break

    # Update bottom array: bottom[col] is the index of the first empty cell from the top
    for col in range(size):
        found = False
        for row in range(size):
            if board[row][col] != ' ':
                bottom[col] = row - 1
                found = True
                break
        if not found:
            bottom[col] = size - 1

def win_horizontal(board_n, size_n):
    global coordinates
    for x in range(size_n):
        count = 1
        for y in range(1, size_n):
            if board_n[x][y] == board_n[x][y-1] and board_n[x][y] != ' ':
                count += 1
                if count == 4:
                    symbol = board_n[x][y]
                    coordinates = [symbol] + [[x, y-3], [x, y-2], [x, y-1], [x, y]]
                    return True
            else:
                count = 1
    return False

def win_vertical(board_n, size_n):
    global coordinates
    for y in range(size_n):
        count = 1
        for x in range(1, size_n):
            if board_n[x][y] == board_n[x-1][y] and board_n[x][y] != ' ':
                count += 1
                if count == 4:
                    symbol = board_n[x][y]
                    coordinates = [symbol] + [[x-3, y], [x-2, y], [x-1, y], [x, y]]
                    return True
            else:
                count = 1
    return False

def win_diagonal_main(board_n, size_n):
    global coordinates
    for x in range(size_n - 3):
        for y in range(size_n - 3):
            symbol = board_n[x][y]
            if symbol != ' ':
                if board_n[x+1][y+1] == symbol and board_n[x+2][y+2] == symbol and board_n[x+3][y+3] == symbol:
                    coordinates = [symbol] + [[x, y], [x+1, y+1], [x+2, y+2], [x+3, y+3]]
                    return True
    return False

def win_diagonal_anti(board_n, size_n):
    global coordinates
    for x in range(size_n - 3):
        for y in range(3, size_n):
            symbol = board_n[x][y]
            if symbol != ' ':
                if board_n[x+1][y-1] == symbol and board_n[x+2][y-2] == symbol and board_n[x+3][y-3] == symbol:
                    coordinates = [symbol] + [[x, y], [x+1, y-1], [x+2, y-2], [x+3, y-3]]
                    return True
    return False

def winning(board_n, size_n):
    return (win_horizontal(board_n, size_n) or 
            win_vertical(board_n, size_n) or 
            win_diagonal_main(board_n, size_n) or 
            win_diagonal_anti(board_n, size_n))

player_1 = input('What is your name Player 1? (You have the O symbol): ')
player_2 = input('What is your name Player 2? (You have the X symbol): ')
winner = ''

def bottom_ok(x):
    return bottom[x] != -1

def board_full(bottom):
    count = 0
    for x in bottom:
        if x == -1:
            count += 1
    return count == len(bottom)

rounds = 0
while rounds <= 0:
    rounds = int(input('How many rounds do you want to play?\n'))
    if rounds <= 0:
        print('Invalid number. Please pick a number above 0')

round = 0
points_O = 0
points_X = 0

while round < rounds:
    coordinates = []  # Will be set by winning functions
    # Player 1's turn (O)
    if not winning(board, size):
        O = -1
        print(player_1, 'it is your turn. (O)')
        while O <= 0 or O > size:
            O = int(input('Which line do you choose? '))
            if O <= 0 or O > size:
                print('Error, the line you chose does not exist. Please try again.')
            elif bottom[O-1] == -1:
                O = -1
                print('The line is full, please pick another line.')
        O = O - 1
        board[bottom[O]][O] = 'O'
        bottom[O] = bottom[O] - 1
        print_board()
    else:
        coordinates = []
    if winning(board, size):
        for coord in coordinates[1:]:
            board[coord[0]][coord[1]] = '*'
        print_board()
        winner = player_1
        points_O += 4  # Award exactly 4 points
        fix_board(coordinates)
        print("This round's winner is", winner, ". You got 4 points")
        print_board()
        coordinates = []
        round += 1
        if round == rounds:
            break
    elif board_full(bottom):
        print('The board is full. The round has ended and the board will be reset.')
        round += 1
        board = [[' ' for _ in range(size)] for _ in range(size)]
        bottom = [size - 1 for _ in range(size)]
        print_board()
        if round == rounds:
            break

    # Player 2's turn (X)
    if not winning(board, size):
        X = -1
        print(player_2, 'it is your turn. (X)')
        while X <= 0 or X > size:
            X = int(input('Which line do you choose? '))
            if X <= 0 or X > size:
                print('Error, the line you chose does not exist. Please try again.')
            elif bottom[X-1] == -1:
                X = -1
                print('The line is full, please pick another line.')
        X = X - 1
        board[bottom[X]][X] = 'X'
        bottom[X] = bottom[X] - 1
        print_board()
    else:
        coordinates = []
    if winning(board, size):
        for coord in coordinates[1:]:
            board[coord[0]][coord[1]] = '*'
        print_board()
        winner = player_2
        points_X += 4  # Award exactly 4 points
        fix_board(coordinates)
        print("This round's winner is", winner, ". You got 4 points")
        coordinates = []
        round += 1
        print_board()
    elif board_full(bottom):
        print('The board is full. The round has ended and the board will be reset.')
        round += 1
        board = [[' ' for _ in range(size)] for _ in range(size)]
        bottom = [size - 1 for _ in range(size)]
        print_board()

    # Save game prompt (for board and bottom) regardless of rounds
    answer = input('Do you want to save? (press s to save or any button to continue): ')
    if answer == 's':
        # Replace empty spaces with '0' for saving
        for x in range(size):
            for y in range(size):
                if board[x][y] == ' ':
                    board[x][y] = '0'
        with open('ng.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(board)
        with open('bottom.csv', 'w', newline='') as b:
            writer = csv.writer(b)
            writer.writerow(bottom)
        # Restore board: replace '0' back to space
        for x in range(size):
            for y in range(size):
                if board[x][y] == '0':
                    board[x][y] = ' '

if points_O > points_X:
    print(player_1, 'is the Final Winner with', points_O, 'points over', player_2, "'s", points_X, 'points')
elif points_O == points_X:
    print('It is a Tie. Nobody Won')
else:
    print(player_2, 'is the Final Winner with', points_X, 'points over', player_1, "'s", points_O, 'points')
