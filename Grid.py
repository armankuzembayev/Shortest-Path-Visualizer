import pygame
vec = pygame.Vector2
GRIDWIDTH = 32
GRIDHEIGHT = 32

class grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.directions = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1),
                           vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]
        self.weights = []

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

    def draw_icons(self, screen, start, end, x_img, home_img):
        end_center = (end.x * GRIDWIDTH + GRIDWIDTH / 2, end.y * GRIDHEIGHT + GRIDHEIGHT / 2)
        screen.blit(x_img, x_img.get_rect(center=end_center))
        start_center = (start.x * GRIDWIDTH + GRIDWIDTH / 2, start.y * GRIDHEIGHT + GRIDHEIGHT / 2)
        screen.blit(home_img, home_img.get_rect(center=start_center))

    def w(self, node1, node2):
        if abs(vec(node1).x - vec(node2).x) + abs(vec(node1).y - vec(node2).y) == 1:
            return 10
        else:
            return 14
