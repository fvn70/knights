import re


def draw_board():
    cell_size = len(str(xmax * ymax))
    lpad = len(str(ymax))
    w = xmax * (cell_size + 1) + 3
    head = ' ' * lpad + '-' * w
    cell = f" {'_' * cell_size}"
    bottom = [str(i+1).rjust(cell_size) for i in range(xmax)]
    knight = ' ' * cell_size + 'X'
    print(head)
    for r in range(ymax):
        row = f"{ymax - r}|".rjust(lpad + 1)
        print(row, end="")
        for c in range(xmax):
            if board[r][c] == 'X':
                row = knight
            elif board[r][c] != '_':
                row = ' ' * cell_size + board[r][c]
            else:
                row = cell
            print(row, end="")
        print(" |")
    print(head)
    print(' ' * (lpad + 2) + ' '.join(bottom))


def set(x, y, val):
    board[ymax - y][x - 1] = val


def get(x, y):
    return board[ymax - y][x - 1]


def clear_board():
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            v = get(x, y)
            if v == 'X':
                set(x, y, '*')
            elif v != '*':
                set(x, y, '_')


def calc_moves(x0, y0):
    cnt = -1
    for move in moves:
        x = x0 + move[0]
        y = y0 + move[1]
        if x in range(1, xmax + 1) and y in range(1, ymax + 1):
            if get(x, y) != '*':
                cnt += 1
    return cnt


def find_moves():
    cnt = 0
    for move in moves:
        x = x0 + move[0]
        y = y0 + move[1]
        if x in range(1, xmax + 1) and y in range(1, ymax + 1):
            if get(x, y) != '*':
                num = calc_moves(x, y)
                set(x, y, str(num))
                cnt += 1
    return cnt

def read_dim():
    while True:
        cmd = input("Enter your board dimensions: ")
        if cmd and re.match(rexp, cmd) is not None:
            break
        print("Invalid dimensions!")
    return map(int, cmd.split())


def read_pos(msg):
    is_move = 'move' in msg
    while True:
        cmd = input(msg)
        if cmd and re.match(rexp, cmd) is not None:
            x, y = map(int, cmd.split())
            if x in range(1, xmax + 1) and y in range(1, ymax + 1) \
                    and (x, y) != (x0, y0):
                if not is_move or abs(x - x0) + abs(y - y0) == 3:
                    break
        if is_move:
            print("Invalid move! ", end="")
        else:
            print("Invalid position!")
    return x, y


def make_move():
    set(x0, y0, 'X')
    n = find_moves()
    draw_board()
    if n == 0:
        print("\nNo more possible moves!")
        print(f"Your knight visited {cnt_pos} squares!")
        return False
    return True


moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
rexp = r"[1-9][0-9]? [1-9][0-9]?\Z"
xmax, ymax = read_dim()
board = [['_' for c in range(xmax)] for r in range(ymax)]
x0, y0 = 0, 0
x0, y0 = read_pos("Enter the knight's starting position: ")
cnt_pos = 1
is_game = make_move()

while is_game:
    x0, y0 = read_pos("\nEnter your next move: ")
    clear_board()
    cnt_pos += 1
    is_game = make_move()

if cnt_pos == xmax * ymax:
    print("What a great tour! Congratulations!")
