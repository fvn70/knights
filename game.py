import re

def calc_land(x0, y0):
    cnt = 0
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                cnt += 1
    return cnt

def set_land(x0, y0):
    for x in range(1, xmax + 1):
        for y in range(1, ymax + 1):
            if x != x0 and y != y0 and abs(x - x0) + abs(y - y0) == 3:
                set(x, y, calc_land(x, y) - 1)

def draw_board():
    cell_size = len(str(xmax * ymax))
    lpad = len(str(ymax))
    w = xmax * (cell_size + 1) + 3
    head = ' ' * lpad + '-' * w
    cell = f" {'_' * cell_size}"
    bottom = [str(i+1).rjust(cell_size) for i in range(xmax)]
    knight = ' ' * cell_size + 'X'
    land = ' ' * cell_size + 'O'
    print("\nHere are the possible moves:")
    print(head)
    for r in range(ymax):
        row = f"{ymax - r}|".rjust(lpad + 1)
        print(row, end="")
        for c in range(xmax):
            if board[r][c] == 0:
                row = cell
            elif board[r][c] == -1:
                row = knight
            else:
                row = ' ' * cell_size + str(board[r][c])
            print(row, end="")
        print(" |")
    print(head)
    print(' ' * (lpad + 2) + ' '.join(bottom))

def set(x, y, val):
    board[ymax - y][x - 1] = val

def matched(template, string):
    return re.match(template, string) is not None

rexp = r"[0-9]+ [0-9]+\Z"
while True:
    cmd = input("Enter your board dimensions: ")
    if cmd and matched(rexp, cmd):
        break
    print("Invalid dimensions!")

xmax, ymax = map(int, cmd.split())
board = [[0 for c in range(xmax)] for r in range(ymax)]

while True:
    cmd = input("Enter the knight's starting position: ")
    if cmd and matched(rexp, cmd):
        x, y = map(int, cmd.split())
        if x in range(1, xmax + 1) and y in range(1, ymax + 1):
            break
    print("Invalid position!")

set(x, y, -1)
set_land(x, y)
draw_board()
