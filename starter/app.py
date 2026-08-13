from flask import Flask, render_template, jsonify, request
from sudoku import generate_puzzle, SIZE

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}


def json_error(message, status_code=400):
    """Return a JSON error payload with the requested HTTP status."""
    return jsonify({'error': message}), status_code


def parse_clues(raw_value):
    """Validate a clue count from request arguments and return it as an int."""
    if raw_value is None:
        raise ValueError('Missing clue/difficulty value.')

    try:
        clues = int(raw_value)
    except (TypeError, ValueError):
        raise ValueError('Clue/difficulty value must be an integer.')

    if clues < 17 or clues > 81:
        raise ValueError('Clue/difficulty value must be between 17 and 81.')

    return clues


def validate_board(board):
    """Ensure the submitted board is a 9x9 grid of integer cell values in range 0-9."""
    if not isinstance(board, list) or len(board) != SIZE:
        raise ValueError('Board must be a 9x9 grid.')

    for row in board:
        if not isinstance(row, list) or len(row) != SIZE:
            raise ValueError('Board must be a 9x9 grid.')
        for value in row:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError('Board contains invalid cell values.')
            if value < 0 or value > 9:
                raise ValueError('Board contains invalid cell values.')


@app.route('/')
def index():
    """Render the browser UI for the Sudoku game."""
    return render_template('index.html')


@app.route('/new')
def new_game():
    """Generate a fresh puzzle and save the matching solution for validation."""
    if 'clues' in request.args:
        raw_clues = request.args.get('clues')
    elif 'difficulty' in request.args:
        raw_clues = request.args.get('difficulty')
    else:
        raw_clues = 35

    try:
        clues = parse_clues(raw_clues)
    except ValueError as exc:
        return json_error(str(exc))

    puzzle, solution = generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle, 'solution': solution})



@app.route('/check', methods=['POST'])
def check_solution():
    """Compare the player's board against the solved answer and report mistakes."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return json_error('Request body must be valid JSON.')

    board = data.get('board')
    if board is None:
        return json_error('Missing board data.')

    try:
        validate_board(board)
    except ValueError as exc:
        return json_error(str(exc))

    solution = CURRENT.get('solution')
    if solution is None:
        return json_error('No game in progress.', 400)

    incorrect = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


if __name__ == '__main__':
    app.run(debug=True)