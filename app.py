from flask import Flask, request, jsonify, render_template
from solver import solve_with_dfs, solve_with_bfs , solve_with_ucs
import random

app = Flask(__name__)

mazes = {
    "maze1": [
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
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

@app.route('/generate-maze', methods=['POST'])
def generate_maze():
    data = request.get_json()
    rows = data.get("rows", 5)
    cols = data.get("cols", 5)
    density = data.get("density", 0.3)  # percentage of walls (0.0–0.9)

    maze = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i == 0 and j == 0) or (i == rows - 1 and j == cols - 1):
                row.append(0)  # start and end should always be open
            else:
                row.append(1 if random.random() < density else 0)
        maze.append(row)

    return jsonify({'maze': maze})

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        maze = data.get('maze')
        algorithm = data.get('algorithm')

        if not maze or not algorithm:
            return jsonify({'error': 'Maze or algorithm not provided'}), 400

        start = (0, 0)
        end = (len(maze) - 1, len(maze[0]) - 1)

        if algorithm == 'dfs':
            path, explored_tiles = solve_with_dfs(maze, start, end)
            return jsonify({
                'path': path,
                'explored_tiles': explored_tiles
            })

        elif algorithm == 'bfs':
            path, explored_tiles = solve_with_bfs(maze, start, end)
            return jsonify({
                'path': path,
                'explored_tiles': explored_tiles
            })

        elif algorithm == 'ucs':
            path, explored_tiles, cost_map = solve_with_ucs(maze, start, end)
            cost_map_str_keys = {f"{x},{y}": cost for (x, y), cost in cost_map.items()}
            return jsonify({
                'path': path,
                'explored_tiles': explored_tiles,
                'cost_map': cost_map_str_keys
            })

        else:
            return jsonify({'error': 'Invalid algorithm selected'}), 400

    except Exception as e:
        print(f"Error in solve endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


    except Exception as e:
        print(f"Error in solve endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
