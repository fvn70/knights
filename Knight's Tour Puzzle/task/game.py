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
            v = str(board[r][c])
            if v == 'X':
                row = knight
            elif v != '_':
                row = v.rjust(cell_size + 1)
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

def set_m(x, y, val):
    matrix[ymax - y][x - 1] = val

def get_m(x, y):
    return matrix[ymax - y][x - 1]


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
    for k in range(8):
        x = x0 + dx[k]
        y = y0 + dy[k]
        if x in range(1, xmax + 1) and y in range(1, ymax + 1):
            if get(x, y) != '*':
                cnt += 1
    return cnt


def find_moves():
    cnt = 0
    for k in range(8):
        x = x0 + dx[k]
        y = y0 + dy[k]
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
        print(f"Your knight visited {cnt_moves} squares!")
        return False
    return True

def read_try():
    while True:
        cmd = input("Do you want to try the puzzle? (y/n): ")
        if cmd in ('yn'):
            break
        print("Invalid input!")
    return cmd == 'y'


def set_number(c, r, i):
    matrix[r][c] = i
    done = try_next(c, r, i)
    if not done:
        matrix[r][c] = 0
    return done


def try_next(x, y, i):

    # eos - shows whether we have considered all the options for possible 8 moves
    # done - shows whether this branch of the solution is successful
    # k - the ordinal number of the considered attempt out of 8 allowed
    env = {'done': False, 'eos': False, 'r': y, 'c': x, 'r0': y, 'c0': x, 'k': -1}

    def next():
        x = env['c']
        y = env['r']
        if x != env['c0']:
            x = env['c0']
            y = env['r0']

        while env['k'] < 8:
            env['k'] += 1
            if env['k'] < 8:
                env['c'] = x + dx[env['k']]
                env['r'] = y + dy[env['k']]
            if (env['r'] >= 0 and env['r'] < ymax) \
                    and (env['c'] >= 0 and env['c'] < xmax) \
                    and matrix[env['r']][env['c']] == 0:
                break
        env['eos'] = (env['k'] == 8)

    if i < xmax * ymax:
        next()
        while not env['eos'] and not set_number(env['c'], env['r'], i + 1):
            next()
        done = not env['eos']
    else:
        done = True
    return done


# Possible moves
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

rexp = r"[1-9][0-9]? [1-9][0-9]?\Z"

xmax, ymax = read_dim()
n_max = xmax * ymax

board = [['_' for c in range(xmax)] for r in range(ymax)]
matrix = [[0 for c in range(xmax)] for r in range(ymax)]
x0, y0 = 0, 0

x0, y0 = read_pos("Enter the knight's starting position: ")
set_m(x0, y0, 1)

is_found = try_next(x0 - 1, ymax - y0, 1)
is_game = False

if read_try():
    if is_found:
        cnt_moves = 1
        is_game = make_move()

        while is_game:
            print()
            x0, y0 = read_pos("Enter your next move: ")
            clear_board()
            cnt_moves += 1
            is_game = make_move()

        if cnt_moves == n_max:
            print("What a great tour! Congratulations!")
    else:
        print("No solution exists!")
elif not is_found:
    print("No solution exists!")
else:
    print("\nHere's the solution!")
    board = matrix
    draw_board()
