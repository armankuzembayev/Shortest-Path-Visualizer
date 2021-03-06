import pygame
from Dijkstra import *
from Grid import *
from AStar import *

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


def vec2tuple(node):
    return (int(node.x), int(node.y))

def main():
    arrows, end_img, home_img = loadFiles()
    running = True
    g = grid(WIDTH, HEIGHT)
    # g.walls.append(vec(5, 5))
    start = vec(3, 20)
    end = vec(30, 2)

    path = AStar(g, start, end)
    astar = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if astar:
                        astar = False
                    else:
                        astar = True


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
            if astar:
                path = AStar(g, start, end)
            else:
                path = Dijkstra(g, start, end)

        screen.fill((0, 0, 0))
        g.drawGrid(screen)
        g.drawWalls(screen)
        for node in path:
            x, y = node
            rect = pygame.Rect(x * GRIDWIDTH, y * GRIDHEIGHT, GRIDWIDTH, GRIDHEIGHT)
            pygame.draw.rect(screen, (30, 30, 30), rect)
        if vec2tuple(start) in path:
            current = start + path[vec2tuple(start)]
        while current != end:
            x = current.x * GRIDWIDTH + GRIDWIDTH / 2
            y = current.y * GRIDHEIGHT + GRIDHEIGHT / 2
            a = vec2tuple(path[(current.x, current.y)])
            img = arrows[a]
            screen.blit(img, img.get_rect(center=(x, y)))
            current = current + path[vec2tuple(current)]
        g.drawGrid(screen)
        g.draw_icons(screen, start, end, end_img, home_img)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
