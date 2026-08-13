SIZE = 9
EMPTY = 0


def is_safe(board, row, col, num):
    """Check whether placing num at row, col would violate Sudoku rules."""
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def has_conflicts(board):
    """Return True if the board already violates any row, column, or 3x3 rule."""
    for i in range(SIZE):
        seen = set()
        for j in range(SIZE):
            value = board[i][j]
            if value == EMPTY:
                continue
            if value in seen:
                return True
            seen.add(value)

    for j in range(SIZE):
        seen = set()
        for i in range(SIZE):
            value = board[i][j]
            if value == EMPTY:
                continue
            if value in seen:
                return True
            seen.add(value)

    for block_row in range(0, SIZE, 3):
        for block_col in range(0, SIZE, 3):
            seen = set()
            for i in range(block_row, block_row + 3):
                for j in range(block_col, block_col + 3):
                    value = board[i][j]
                    if value == EMPTY:
                        continue
                    if value in seen:
                        return True
                    seen.add(value)
    return False
