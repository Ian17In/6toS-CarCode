import heapq
import numpy as np


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Costo desde el inicio hasta este nodo
        self.h = 0  # Heurística (distancia estimada hasta el final)
        self.f = 0  # f = g + h (costo total)

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position

    def __lt__(self, other):
        return self.f < other.f  # Necesario para usar heapq

def expand_obstacles(maze, expansion_size=2):
    """Expande los obstáculos en la matriz para mejorar la evasión"""
    new_maze = np.array(maze)
    rows, cols = new_maze.shape

    for x in range(rows):
        for y in range(cols):
            if maze[x][y] == 1:
                for dx in range(-expansion_size, expansion_size + 1):
                    for dy in range(-expansion_size, expansion_size + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            new_maze[nx][ny]=max(new_maze[nx][ny], 1)  # Celda expandida

    return new_maze.tolist()

# Redefinir A* con penalización más fuerte para obstáculos cercanos
def heuristic_improved(a, b, maze):
    """Heurística que penaliza más la proximidad a obstáculos."""
    manhattan_dist = abs(a[0] - b[0]) + abs(a[1] - b[1])
    penalty = 0

    # Aumentar la penalización en un radio mayor
    for dx in range(-6, 6):
        for dy in range(-4, 4):
            nx, ny = a[0] + dx, a[1] + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1:
                penalty += 8 # Penalización mayor por proximidad

    return manhattan_dist + penalty

# Redefinir A* con la nueva heurística
def adastra(maze1, start, end):
    """A* con mayor penalización para obstáculos cercanos."""

    maze = expand_obstacles(maze1,5)

    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = set()
    open_dict = {}

    heapq.heappush(open_list, (start_node.f, start_node))
    open_dict[start_node.position] = start_node.g

    moves = [(0, -1), (0, 1), (-1, 0), (1, 0),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while open_list:
        current_node = heapq.heappop(open_list)[1]

        if current_node.position == end_node.position:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
                returnedPath = path[::-1]
                correctPath = []
                for i in range(len(returnedPath)):
                    if i%15 == 0:
                        correctPath.append(returnedPath[i])
                        del correctPath[0]
                        

            return correctPath,maze

        closed_list.add(current_node.position)

        for move in moves:
            node_position = (current_node.position[0] + move[0], 
                             current_node.position[1] + move[1])

            if not (0 <= node_position[0] < len(maze) and 0 <= node_position[1] < len(maze[0])):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            if move in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                if maze[current_node.position[0] + move[0]][current_node.position[1]] == 1 or \
                   maze[current_node.position[0]][current_node.position[1] + move[1]] == 1:
                    continue

            new_node = Node(current_node, node_position)
            new_node.g = current_node.g + (1.41 if move in [(-1, -1), (-1, 1), (1, -1), (1, 1)] else 1)
            new_node.h = heuristic_improved(new_node.position, end_node.position, maze)
            new_node.f = new_node.g + new_node.h

            if new_node.position in closed_list:
                continue

            if node_position in open_dict and new_node.g >= open_dict[node_position]:
                continue

            heapq.heappush(open_list, (new_node.f, new_node))
            open_dict[node_position] = new_node.g

    return None  # No se encontró ruta



def print_maze_with_path(maze, path):
    """Imprime el laberinto con la ruta encontrada."""
    maze_copy = [row[:] for row in maze]
    for x, y in path:
        maze_copy[x][y] = "+"  

    for row in maze_copy:
        print(" ".join(str(cell) for cell in row))


def main():
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    end = (7, 6)

    path = adastra(maze, start, end)

    if path:
        print("Camino encontrado:", path)
        print_maze_with_path(maze, path)
    else:
        print("No se encontró un camino.")


if __name__ == '__main__':
    main()
