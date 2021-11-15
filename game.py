import re
import numpy as np

def get_xy(m):
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get_m(x, y) == m:
                return x, y
    return 0, 0

def best_move(x0, y0, v0):
    nmax, xm, ym = 0, 0, 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            v = get_m(x, y)
            if v == 0 or v > v0 + 1:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    num = calc_move(x, y)
                    if num > nmax:
                        nmax = num
                        xm = x
                        ym = y
    return nmax, xm, ym

def clear_board():
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            v = get(x, y)
            if v == -1:
                set(x, y, -2)
            elif v >= 0:
                set(x, y, -9)

# num moves from (x0, y0)
def calc_land(x0, y0):
    num = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get(x, y) != -2:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    num += 1
    return num

# num moves from (x0, y0)
def calc_move(x0, y0):
    num = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get_m(x, y) == 0:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    num += 1
    return num

def set_land(x0, y0):
    cnt = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if get(x, y) != -2:
                if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                    set(x, y, calc_land(x, y) - 1)
                    cnt += 1
    return cnt

def draw_board():
    cell_size = len(str(n_max))
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
            if bo[r][c] == -9:
                row = cell          # '_'
            elif bo[r][c] == -1:
                row = knight        # 'X'
            elif bo[r][c] == -2:
                row = star          # '*'
            else:
                row = str(bo[r][c]).rjust(cell_size + 1)
            print(row, end="")
        print(" |")
    print(head)
    print(' ' * (lpad + 2) + ' '.join(bottom))

def set(x, y, val):
    bo[ymax - y][x - 1] = val

def get(x, y):
    return bo[ymax - y][x - 1]

def set_m(x, y, val):
    mo[ymax - y][x - 1] = val

def get_m(x, y):
    return mo[ymax - y][x - 1]

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

def read_try():
    while True:
        cmd = input("Do you want to try the puzzle? (y/n): ")
        if cmd in ('yn'):
            break
        print("Invalid input!")
    return cmd == 'y'

def make_move():
    set(x0, y0, -1)
    n = set_land(x0, y0)
    draw_board()
    if n == 0:
        print("\nNo more possible moves!")
        print(f"Your knight visited {cnt_moves} squares!")
        return False
    return True

def solve_game(x0, y0, n):
    if n == n_max or n == 0:
        return n
    set_m(x0, y0, n)
    num, x1, y1 = best_move(x0, y0, n)
    if num == 0:
        # set_m(x0, y0, -1)
        n -= 1
        x1, y1 = get_xy(n)
        n -= 1
        if x1 == 0 or y1 == 0:
            return n
    return solve_game(x1, y1, n + 1)

def set_number(c, r, i):
    mo[r][c] = i
    done = try_next(c, r, i)
    if not done:
        mo[r][c] = 0
    return done

def try_next(x, y, i):

    #eos - показывает все ли варианты возможных 8ми ходов мы рассмотрели
    #done - показывает удачна ли данная ветка решения
    #k - порядковый номер рассмотренной попытки из 8 допустимых
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
                    and mo[env['r']][env['c']] == 0:
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


rexp = r"[1-9][0-9]? [1-9][0-9]?\Z"
xmax, ymax = read_dim()
n_max = xmax * ymax
bo = [[-9 for c in range(xmax)] for r in range(ymax)]
mo = [[0 for c in range(xmax)] for r in range(ymax)]
x0, y0 = 0, 0

# Возможные ходы
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

x0, y0 = read_pos("Enter the knight's starting position: ")
mo[ymax - y0][x0 - 1] = 1
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
    bo = mo
    draw_board()

