import pygame
import heapq
from collections import deque
vec = pygame.Vector2


class PriorityQueue(object):
    def __init__(self):
        self.node = []

    def push(self, node, cost):
        heapq.heappush(self.node, (cost, node))

    def pop(self):
        return heapq.heappop(self.node)[1]

    def isEmpty(self):
        return len(self.node) == 0


def vec2tuple(node):
    return (int(node.x), int(node.y))


def bfs(graph, start, end):
    path = {}
    visited = []
    visited.append(end)
    path[vec2tuple(end)] = vec(0, 0)
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

def Dijkstra(graph, start, end):
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
                path[vec2tuple(next)] = vec(current) - next
                frontier.push(vec2tuple(next), next_cost)
    return path, cost

