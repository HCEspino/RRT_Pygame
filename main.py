import pygame
from rrt import RRT

WIDTH = 800
HEIGHT = 600

def drawRecursive(screen, node):
    drawCircle(screen, 'black', (node.x, node.y), 5)
    for child in node.children:
        drawLine(screen, 'black', (node.x, node.y), (child.x, child.y))
        drawRecursive(screen, child)

def drawCircle(screen, color, pos, radius):
    pygame.draw.circle(screen, color, pos, radius)

def drawLine(screen, color, pos1, pos2, width=1):
    pygame.draw.line(screen, color, pos1, pos2, width)

def drawGoal(screen, pos):
    drawCircle(screen, 'green', pos, 20)

def drawPath(screen, path):
    for i in range(len(path) - 1):
        drawCircle(screen, 'red', path[i], 6)
        drawLine(screen, 'red', path[i], path[i + 1], 3)

    drawCircle(screen, 'red', path[-1], 6)


def setup() -> tuple:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption('RRT Simulation')
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))

    screen.fill('white')

    pygame.display.flip()

    return screen, clock

def acceptingInput(mainrrt, done) -> bool:
    return not mainrrt and not done

def run() -> None:
    pygame.init()

    rewire = True
    screen, clock = setup()

    running = True
    done = False
    mainrrt = False

    down = False
    obstacles = []
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and acceptingInput(mainrrt, done):
                if not down:
                    down = True
                    startpos = pygame.mouse.get_pos()
                else:
                    endpose = pygame.mouse.get_pos()
                    screen.fill('white')
                    drawLine(screen, 'black', startpos, endpose, 3)
                    pygame.display.flip()


                print("HERE")
            if event.type == pygame.MOUSEBUTTONUP and acceptingInput(mainrrt, done) and down:
                down = False
                print("HERE")
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and acceptingInput(mainrrt, done) and not down:
                screen.fill('white')
                pos = pygame.mouse.get_pos()
                drawGoal(screen, pos)
                rrt = RRT(screen.get_width(), screen.get_height())
                rrt.goal = pos
                mainrrt = True

        if mainrrt:
            pos, parent, finished = rrt.step(rewire=True)

            if rewire:
                screen.fill('white')
                drawGoal(screen, rrt.goal)
                drawRecursive(screen, rrt.root)
            else:
                drawCircle(screen, 'black', pos, 5)
                if parent is not None:
                    drawLine(screen, 'black', pos, parent)

            pygame.display.flip()
            if finished:
                mainrrt = False
                done = True
                path = rrt.getPath()
                drawPath(screen, path)
                pygame.display.flip()
            



        

        


    pygame.quit()

if __name__ == '__main__':
    run()