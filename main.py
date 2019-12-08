import pygame
from collections import deque

pygame.init()
vec = pygame.Vector2
GRIDWIDTH = 32
GRIDHEIGHT = 32
WIDTH = GRIDWIDTH**2
HEIGHT = GRIDHEIGHT**2 - GRIDHEIGHT*10
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def loadFiles():
    x_img = pygame.transform.scale(pygame.image.load('x.png').convert_alpha(), (25, 25))
    x_img.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
    home_img = pygame.transform.scale(pygame.image.load('home.png').convert_alpha(), (30, 30))
    home_img.fill((0, 255, 0, 255), special_flags = pygame.BLEND_RGBA_MULT)
    arrows = {}
    arrow_img = pygame.transform.scale(pygame.image.load('arrow.png').convert_alpha(), (30, 30))
    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        arrows[direction] = pygame.transform.rotate(arrow_img, vec(direction).angle_to(vec(1, 0)))
    return arrows, x_img, home_img


class grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.directions = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1),
                           vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def drawGrid(self, screen):
        for x in range(0, self.width, GRIDWIDTH):
            pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, self.height))
        for y in range(0, self.height, GRIDHEIGHT):
            pygame.draw.line(screen, (100, 100, 100), (0, y), (self.width, y))

    def drawWalls(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (200, 0, 0), (wall.x * GRIDWIDTH, wall.y * GRIDHEIGHT, GRIDWIDTH, GRIDHEIGHT))

    def constraintsForWalls(self, node):
        return 0 <= node.x < self.width // GRIDWIDTH and 0 <= node.y < self.height // GRIDHEIGHT and node not in self.walls

    def findNeigbors(self, node):
        neighbors = [node + neighbor for neighbor in self.directions]
        neighbors = filter(self.constraintsForWalls, neighbors)
        return neighbors

    def draw_icons(self, start, end, x_img, home_img):
        end_center = (end.x * GRIDWIDTH + GRIDWIDTH / 2, end.y * GRIDHEIGHT + GRIDHEIGHT / 2)
        screen.blit(x_img, x_img.get_rect(center=end_center))
        start_center = (start.x * GRIDWIDTH + GRIDWIDTH / 2, start.y * GRIDHEIGHT + GRIDHEIGHT / 2)
        screen.blit(home_img, home_img.get_rect(center=start_center))


def vec2tuple(node):
    return (int(node.x), int(node.y))

def bfs(graph, start, end):
    path = {}
    visited = []
    visited.append(end)
    path[vec2tuple(end)] = None
    frontier = deque()
    frontier.append(end)
    while len(frontier) > 0:
        n = frontier.popleft()
        if n == start:
            break
        for node in graph.findNeigbors(n):
            if vec2tuple(node) not in path:
                visited.append(node)
                frontier.append(node)
                path[vec2tuple(node)] = n - node
    return path, visited


def main():
    arrows, end_img, home_img = loadFiles()
    running = True
    g = grid(WIDTH, HEIGHT)
    # g.walls.append(vec(5, 5))
    start = vec(3, 20)
    end = vec(30, 2)

    path, visited = bfs(g, start, end)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = vec(pygame.mouse.get_pos()) // GRIDHEIGHT
                if event.button == 1:
                    if pos not in g.walls:
                        g.walls.append(pos)
                    else:
                        g.walls.remove(pos)
                elif event.button == 3:
                    end = pos
                elif event.button == 2:
                    start = pos
                path, visited = bfs(g, start, end)
        screen.fill((0, 0, 0))
        g.drawGrid(screen)
        g.drawWalls(screen)
        for node in path:
            x, y = node
            rect = pygame.Rect(x * GRIDWIDTH, y * GRIDHEIGHT, GRIDWIDTH, GRIDHEIGHT)
            pygame.draw.rect(screen, (30, 30, 30), rect)
        current = start + path[vec2tuple(start)]
        while current != end:
            x = current.x * GRIDWIDTH + GRIDWIDTH / 2
            y = current.y * GRIDHEIGHT + GRIDHEIGHT / 2
            img = arrows[vec2tuple(path[(current.x, current.y)])]
            screen.blit(img, img.get_rect(center=(x, y)))
            current = current + path[vec2tuple(current)]
        g.drawGrid(screen)
        g.draw_icons(start, end, end_img, home_img)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

