from sudoku import create_empty_board, generate_puzzle, is_safe, solve_board, count_solutions, has_unique_solution, SIZE, EMPTY


def test_create_empty_board_returns_nine_by_nine_grid():
    board = create_empty_board()
    assert len(board) == SIZE
    assert all(len(row) == SIZE for row in board)
    assert all(cell == EMPTY for row in board for cell in row)


def test_is_safe_rejects_duplicates_in_row_column_and_box():
    board = create_empty_board()
    board[0][0] = 5

    assert not is_safe(board, 0, 1, 5)
    assert not is_safe(board, 1, 0, 5)
    assert not is_safe(board, 1, 1, 5)
    assert is_safe(board, 0, 1, 4)


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = generate_puzzle(clues=35)

    assert len(puzzle) == SIZE
    assert len(solution) == SIZE
    assert all(len(row) == SIZE for row in puzzle)
    assert all(len(row) == SIZE for row in solution)
    assert any(cell == EMPTY for row in puzzle for cell in row)
    assert all(cell != EMPTY for row in solution for cell in row)

    for i in range(SIZE):
        for j in range(SIZE):
            assert puzzle[i][j] == EMPTY or puzzle[i][j] == solution[i][j]


def test_count_solutions_and_uniqueness():
    puzzle, solution = generate_puzzle(clues=35)
    board_copy = [row[:] for row in puzzle]

    count = count_solutions(board_copy)
    assert count >= 1
    assert has_unique_solution(puzzle)


def test_solve_board_can_complete_a_puzzle_from_generate_puzzle():
    puzzle, solution = generate_puzzle(clues=35)
    board_to_solve = [row[:] for row in puzzle]

    solved = solve_board(board_to_solve)
    assert solved is True
    assert all(cell != EMPTY for row in board_to_solve for cell in row)

    expected_numbers = set(range(1, SIZE + 1))
    for row in board_to_solve:
        assert set(row) == expected_numbers

    for col in range(SIZE):
        assert {board_to_solve[row][col] for row in range(SIZE)} == expected_numbers

    for block_row in range(0, SIZE, 3):
        for block_col in range(0, SIZE, 3):
            block = {
                board_to_solve[r][c]
                for r in range(block_row, block_row + 3)
                for c in range(block_col, block_col + 3)
            }
            assert block == expected_numbers

    for i in range(SIZE):
        for j in range(SIZE):
            if puzzle[i][j] != EMPTY:
                assert board_to_solve[i][j] == puzzle[i][j]


def test_solver_returns_false_for_invalid_board():
    board = create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert solve_board(board) is False
