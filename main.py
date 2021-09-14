# pip install numpy
# pip install pygame

from pygame.locals import *
import pygame
import numpy as np
import sys
import time

pygame.init()
width, height = 960, 960
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("Game of Life")

# Background color
background = 15, 157, 88 # 66, 133, 244
screen.fill(background)

nxC, nyC = 64, 64

dimCW = width / nxC
dimCH = height / nyC

# Draw the window onto the screen
# pygame.display.update()

matrix = np.zeros((nxC, nyC))
""" matrix[21, 21] = 1
matrix[22, 22] = 1
matrix[22, 23] = 1
matrix[21, 23] = 1
matrix[20, 23] = 1

matrix[5, 3] = 1
matrix[5, 4] = 1
matrix[5, 5] = 1 """

for k in range(2**10):
    x = np.random.randint(nxC)
    y = np.random.randint(nyC)
    matrix[x, y] = 1

pause = False

while True:
    matrix_copy = np.copy(matrix)
    screen.fill(background)
    time.sleep(0.01)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pause = not pause
        elif sum(pygame.mouse.get_pressed()) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            matrix_copy[celX, celY] = int(not int(matrix_copy[celX, celY]))

    for y in range(nxC):
        for x in range(nyC):
            if not pause:
                # Neighbor near
                neighbor_num = matrix[(x - 1) % nxC, (y - 1) % nyC] + \
                            matrix[(x) % nxC, (y - 1) % nyC] + \
                            matrix[(x + 1) % nxC, (y - 1) % nyC] + \
                            matrix[(x - 1) % nxC, (y) % nyC] + \
                            matrix[(x + 1) % nxC, (y) % nyC] + \
                            matrix[(x - 1) % nxC, (y + 1) % nyC] + \
                            matrix[(x) % nxC, (y + 1) % nyC] + \
                            matrix[(x + 1) % nxC, (y + 1) % nyC]
                
                # Rules
                # 0: kill, 1: life
                if matrix[x, y] == 0 and neighbor_num == 3:
                    matrix_copy[x, y] = 1
                elif matrix[x, y] == 1 and (neighbor_num < 2 or neighbor_num > 3):
                    matrix_copy[x, y] = 0

            # Draw polygon for each cell
            poly = [
                (x * dimCW, y * dimCW),
                ((x + 1) * dimCW, y * dimCW),
                ((x + 1) * dimCW, (y + 1) * dimCW),
                (x * dimCW, (y + 1) * dimCW)
            ]
            
            if matrix_copy[x, y] == 0:
                pygame.draw.polygon(screen, (219, 68, 55), poly, width=1)
            else:
                pygame.draw.polygon(screen, (244, 180, 0), poly, width=0)
   
    # Update matrix
    matrix = np.copy(matrix_copy)
    pygame.display.flip()