from math import sqrt
import pygame
import time

def a_star(start, goal):
    closedset = set()
    openset = set([start])
    came_from = {}

    # came_from = { (2,1): (0,1) }

    #cost form start along best known path
    g_score = { start: 0 }
    #estimated total cost form start to goal through y
    f_score = { start: g_score[start] + heuristic_cost_estimate(start, goal)}

    while openset:
        # current is the node with the lowest f_score
        current = sorted(openset, key=lambda item: f_score[item])[0]
        if current == goal:
            return reconstruct_path(came_from, goal)

        openset.remove(current)
        closedset.add(current)

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + graph[current[1]][current[0]]
            if neighbor in closedset and tentative_g_score >= g_score.get(neighbor, float("inf")):
                continue    

            if neighbor not in openset or tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                if neighbor not in openset:
                    openset.add(neighbor)

    return None

def heuristic_cost_estimate(start, goal):
    return sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)


def get_neighbors(current):
    neighbors = []
    x, y = current
    height = len(graph)
    width = len(graph[0])
    for y_ in range(max(0, y-1), min(height, y+2)):
        for x_ in range(max(0, x-1), min(width, x+2)):
            if current == (x_, y_):
                continue
            else:
                neighbors.append((x_, y_))
    return neighbors

def reconstruct_path(came_from, current_node):
    if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        p.append(current_node)
        return p
    return [current_node]

def get_position():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                row = pos[0] // (width + margin)
                column = pos[1] // (height + margin)
                position = (row, column)
                return position

def draw_circle(point, color):
    pygame.draw.circle(screen, color, (point[0]*width + width/2, point[1]*height+ height/2), 10)
    pygame.display.flip()


pygame.init()


graph = [[1, 1, 2, 1, 3],
         [3, 1, 2, 1, 2],
         [3, 1, 3, 3, 3],
         [1, 2, 2, 2, 1],
         [3, 1, 3, 2, 1]]

size = [255, 255]

black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
blue     = (   0,   0, 255)
red      = ( 255,   0,   0)
yellow   = ( 255, 255,   0)

screen=pygame.display.set_mode(size)

margin = 0
height = size[1]/len(graph)
width = size[0]/len(graph[0])

for row in range(len(graph)):
    for column in range(len(graph[0])):
        color = white
        if graph[row][column] == 2:
            color = green
        if graph[row][column] == 3:
            color = blue
        if graph[row][column] == 1:
            color = white
        pygame.draw.rect(screen,
                         color,
                         [(margin+width)*column+margin,
                          (margin+height)*row+margin,
                          width,
                          height])
pygame.display.flip()

start = get_position()
draw_circle(start, red)

goal = get_position()
draw_circle(goal, red)
    
path = a_star(start, goal)

for position in path:
    draw_circle(position, yellow)
    time.sleep(0.5)

time.sleep(10)
