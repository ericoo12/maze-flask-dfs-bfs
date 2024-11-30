def solve_with_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = set()
    parent_map = {}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        x, y = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent_map[(x, y)]
            path.append(start)
            return path[::-1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent_map[(nx, ny)] = (x, y)

    return None


def solve_with_bfs(maze, start, end):
    from collections import deque
    queue = deque([start])
    visited = set()
    parent_map = {}

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent_map.get(current)
            return path[::-1]

        neighbors = get_neighbors(maze, current)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                parent_map[neighbor] = current

    return None


def get_neighbors(maze, position):
    x, y = position
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            neighbors.append((nx, ny))

    return neighbors
