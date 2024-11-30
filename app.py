from flask import Flask, request, jsonify, render_template
from solver import solve_with_dfs, solve_with_bfs

app = Flask(__name__)

mazes = {
    "maze1": [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ],
    "maze2": [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0]
    ],
    "maze3": [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ],
    "maze4": [
        [0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ],
    "maze5": [
        [0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
}

@app.route('/')
def index():
    return render_template('index.html', mazes=list(mazes.keys()))

@app.route('/get-maze', methods=['POST'])
def get_maze():
    data = request.json
    selected_maze = data.get("maze")

    if selected_maze not in mazes:
        return jsonify({'error': 'Invalid maze selected'}), 400

    return jsonify({'maze': mazes[selected_maze]})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    maze = data.get('maze')
    algorithm = data.get('algorithm')

    if not maze or not algorithm:
        return jsonify({'error': 'Maze or algorithm not provided'}), 400

    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    if algorithm == 'dfs':
        solution = solve_with_dfs(maze, start, end)
    elif algorithm == 'bfs':
        solution = solve_with_bfs(maze, start, end)
    else:
        return jsonify({'error': 'Invalid algorithm selected'}), 400

    if solution is None:
        return jsonify({'message': 'No solution found'})

    return jsonify({'solution': solution})


if __name__ == '__main__':
    app.run(debug=True)
