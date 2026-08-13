import copy
import random
from .solver import has_unique_solution
from .validator import is_safe, SIZE, EMPTY


def deep_copy(board):
    """Return a fully independent copy of the Sudoku board."""
    return copy.deepcopy(board)


def fill_board(board):
    """Fill the board using backtracking while keeping each move valid."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def remove_cells(board, clues):
    """Remove values until the puzzle has roughly the requested number of clues.

    Each removal is kept only if the board still has a unique solution; this
    preserves puzzle validity while making it playable.
    """
    attempts = SIZE * SIZE - clues
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    removed = 0

    for row, col in cells:
        if removed >= attempts:
            break
        if board[row][col] == EMPTY:
            continue

        previous = board[row][col]
        board[row][col] = EMPTY
        if has_unique_solution(copy.deepcopy(board)):
            removed += 1
        else:
            board[row][col] = previous


def generate_puzzle(clues=35):
    """Create a valid Sudoku puzzle and its solved board."""
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution


def create_empty_board():
    """Build a blank 9x9 board initialized with empty cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
