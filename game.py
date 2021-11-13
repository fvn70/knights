import re

def clear_board():
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            v = get(x, y)
            if v == -1:
                set(x, y, -2)
            elif v >= 0:
                set(x, y, -9)

def calc_land(x0, y0):
    cnt = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get(x, y) != -2:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    cnt += 1
    return cnt

def set_land(x0, y0):
    cnt = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get(x, y) != -2:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    set(x, y, calc_land(x, y) - 1)
                    cnt += 1
    return cnt

# '*' if -2, 'X' if -1, '_' if 0 else n
def draw_board():
    cell_size = len(str(xmax * ymax))
    lpad = len(str(ymax))
    w = xmax * (cell_size + 1) + 3
    head = ' ' * lpad + '-' * w
    cell = f" {'_' * cell_size}"
    bottom = [str(i+1).rjust(cell_size) for i in range(xmax)]
    knight = ' ' * cell_size + 'X'
    star = ' ' * cell_size + '*'
    # print("\nHere are the possible moves:")
    print(head)
    for r in range(ymax):
        row = f"{ymax - r}|".rjust(lpad + 1)
        print(row, end="")
        for c in range(xmax):
            if board[r][c] == -9:
                row = cell
            elif board[r][c] == -1:
                row = knight
            elif board[r][c] == -2:
                row = star
            else:
                row = ' ' * cell_size + str(board[r][c])
            print(row, end="")
        print(" |")
    print(head)
    print(' ' * (lpad + 2) + ' '.join(bottom))

def set(x, y, val):
    board[ymax - y][x - 1] = val

def get(x, y):
    return board[ymax - y][x - 1]

def matched(template, string):
    return re.match(template, string) is not None

def read_pos(msg):
    is_move = 'move' in msg
    while True:
        cmd = input(msg)
        if cmd and matched(rexp, cmd):
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

def read_dim():
    while True:
        cmd = input("Enter your board dimensions: ")
        if cmd and matched(rexp, cmd):
            break
        print("Invalid dimensions!")
    return map(int, cmd.split())

def make_move():
    set(x0, y0, -1)
    n = set_land(x0, y0)
    draw_board()
    if n == 0:
        print("\nNo more possible moves!")
        print(f"Your knight visited {cnt} squares!")
        return False
    return True

rexp = r"[1-9][0-9]? [1-9][0-9]?\Z"
xmax, ymax = read_dim()
board = [[-9 for c in range(xmax)] for r in range(ymax)]
x0, y0 = 0, 0
x0, y0 = read_pos("Enter the knight's starting position: ")
is_game = make_move()
cnt = 1

while is_game:
    print()
    x0, y0 = read_pos("Enter your next move: ")
    clear_board()
    cnt += 1
    is_game = make_move()

if cnt == xmax * ymax:
    print("What a great tour! Congratulations!")
