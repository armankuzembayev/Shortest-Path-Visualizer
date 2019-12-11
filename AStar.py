import pygame
import heapq
vec = pygame.Vector2


def vec2tuple(node):
    return (int(node.x), int(node.y))

def heursitic(node1, node2):
    return 10*(abs(node1.x - node2.x) + abs(node1.y - node2.y))

class PriorityQueue(object):
    def __init__(self):
        self.node = []

    def push(self, node, cost):
        heapq.heappush(self.node, (cost, node))

    def pop(self):
        return heapq.heappop(self.node)[1]

    def isEmpty(self):
        return len(self.node) == 0


def AStar(graph, start, end):
    frontier = PriorityQueue()
    frontier.push(vec2tuple(end), 0)
    cost = {}
    path = {}
    cost[vec2tuple(end)] = 0
    path[vec2tuple(end)] = vec(0, 0)

    while not frontier.isEmpty():
        current = frontier.pop()
        if current == start:
            break
        for next in graph.findNeigbors(vec(current)):
            next_cost = cost[current] + graph.w(current, vec2tuple(next))
            if vec2tuple(next) not in cost or next_cost < cost[vec2tuple(next)]:
                cost[vec2tuple(next)] = next_cost
                frontier.push(vec2tuple(next), next_cost + heursitic(start, next))
                path[vec2tuple(next)] = vec(current) - next
    return path