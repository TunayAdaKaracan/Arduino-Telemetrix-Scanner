import time
from telemetrix import telemetrix
import pygame
import math
import threading


pygame.init()

SCREEN = pygame.display.set_mode((600, 600))

angle = 0
points = {}
changes = []
for i in range(0, 181):
    points[i] = []
    points[i].append(0)
    points[i].append((300, 300))


def the_callback(data):
    points[angle][0] = data[2]
    changes.append(angle)
    print(data[2])


def watchForServo():
    global angle

    board = telemetrix.Telemetrix(com_port="COM3")
    board.set_pin_mode_sonar(8, 9, the_callback)
    board.set_pin_mode_servo(5)
    board.servo_write(5, angle)

    while True:
        for i in range(0, 181):
            board.servo_write(5, i)
            angle = i
            time.sleep(75 / 1000)
        for n in range(180, 0, -1):
            board.servo_write(5, n)
            angle = n
            time.sleep(75 / 1000)


def fixLines():
    if angle == 0 or angle == 180:
        copy = points.copy()
        for i in range(0, 181):
            if i not in changes:
                if i == 0:
                    first = copy[i+1][0]
                else:
                    first = copy[i-1][0]

                if i == 180:
                    second = copy[i-1][0]
                else:
                    second = copy[i+1][0]

                points[i][0] = (first + second) / 2
        changes.clear()


def drawPoints():
    for i in range(0, 181):
        point = points[i][0] * 4

        radian = math.radians(i)

        dx = math.cos(radian) * point + 300
        dy = -math.sin(radian) * point + 300

        points[i][1] = (dx, dy)

        pygame.draw.circle(SCREEN, (0, 127, 127), (dx, dy), 4)


def drawLines():
    for i in range(0, 180):
        first_loc = points[i][1]
        second_loc = points[i+1][1]

        pygame.draw.line(SCREEN, (0, 65, 65), first_loc, second_loc)


def main():
    threading.Thread(daemon=True, target=watchForServo).start()
    while True:
        SCREEN.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        drawPoints()
        drawLines()

        pygame.draw.circle(SCREEN, (0, 255, 0), center=(300, 300), radius=10)
        pygame.draw.line(SCREEN, (255, 0, 0), (300, 300), points[angle][1], width=4)

        fixLines()

        pygame.display.update()


if __name__ == "__main__":
    main()