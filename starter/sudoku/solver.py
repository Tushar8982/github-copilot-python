from .validator import SIZE, EMPTY, is_safe, has_conflicts


def find_empty_cell(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def solve_board(board):
    if has_conflicts(board):
        return False

    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, SIZE + 1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_board(board):
                return True
            board[row][col] = EMPTY
    return False


def count_solutions(board, limit=2):
    if has_conflicts(board):
        return 0

    empty = find_empty_cell(board)
    if not empty:
        return 1
    row, col = empty
    total = 0

    for num in range(1, SIZE + 1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            total += count_solutions(board, limit)
            board[row][col] = EMPTY
            if total >= limit:
                return total
    return total


def has_unique_solution(board):
    return count_solutions(board, limit=2) == 1
