# solver.py (original)
def solve_with_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = set()
    parent_map = {}
    explored_tiles = []  # Track all explored tiles

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        explored_tiles.append((x, y))  # Record explored tile

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent_map[(x, y)]
            path.append(start)
            return path[::-1], explored_tiles

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent_map[(nx, ny)] = (x, y)

    return None, explored_tiles


def solve_with_bfs(maze, start, end):
    from collections import deque
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set()
    parent_map = {}
    explored_tiles = []  # Track all explored tiles

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        explored_tiles.append((x, y))  # Record explored tile

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent_map[(x, y)]
            path.append(start)
            return path[::-1], explored_tiles

        # Explore neighbors
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and
                maze[nx][ny] == 0 and
                (nx, ny) not in visited):
                queue.append((nx, ny))
                if (nx, ny) not in parent_map:  # Only set parent if not already set
                    parent_map[(nx, ny)] = (x, y)

    return None, explored_tiles


def get_neighbors(maze, position):
    x, y = position
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors