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
            else:
                row = cell
            print(row, end="")
        print(" |")
    print(head)
    print(' ' * (lpad + 2) + ' '.join(bottom))


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


rexp = r"[1-9][0-9]? [1-9][0-9]?\Z"
xmax, ymax = read_dim()
board = [['_' for c in range(xmax)] for r in range(ymax)]
x0, y0 = 0, 0
x0, y0 = read_pos("Enter the knight's starting position: ")
board[ymax - y0][x0 - 1] = 'X'
draw_board()
