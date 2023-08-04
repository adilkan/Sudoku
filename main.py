import pygame
from sudoku import Sudoku

pygame.init()
weight = 40 * 9
height = 40 * 9

white = (255, 255, 255)
black = (0, 0, 0)
gray = (125, 125, 125)
red = (255, 5, 0)

tick = pygame.time.Clock()
display = pygame.display.set_mode([weight, height])


def set_up():
    display.fill(white)

    for i in range(10):
        if i % 3 == 0:
            continue
        pygame.draw.line(display, gray, (i * 40, 0), (i * 40, 40 * 9), 2)
        pygame.draw.line(display, gray, (0, i * 40), (40 * 9, i * 40), 2)
    for i in range(10):
        if i % 3:
            continue
        pygame.draw.line(display, black, (i * 40, 0), (i * 40, 40 * 9), 3)
        pygame.draw.line(display, black, (0, i * 40), (40 * 9, i * 40), 3)

    pygame.display.update()


set_up()
sudoku = Sudoku()
clicked = False
x, y = -1, -1
sudoku.start_player_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            set_up()
            x, y = pygame.mouse.get_pos()
            x //= 40
            y //= 40
            if x > 8 or y > 8 or sudoku.players_board[y][x] != '.':
                continue
            pygame.draw.rect(display, red, (x * 40, y * 40, 40, 40), 3)
            clicked = True
        elif event.type == pygame.KEYDOWN:
            input_ = chr(event.key)
            if clicked and input_.isdigit():
                sudoku.sudoku_click(y, x, input_)
            elif input_.lower() == 'f':
                sudoku.solve_sudoku(display)
            clicked = False
            set_up()
    sudoku.draw(display)
    tick.tick(20)

