from collections import defaultdict
import pygame
import random
from time import sleep

pygame.init()
f_sys = pygame.font.SysFont('arial', 20, 1)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (125, 125, 125)
red = (255, 5, 0)
green = (0, 255, 0)


class Sudoku:
    def __init__(self):
        self.board = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"]
        ]
        self.players_board = None
        self.row = defaultdict(set)
        self.col = defaultdict(set)
        self.squares = defaultdict(set)

    def change_in_one_chunk(self):

        x = random.randint(0, 2)
        first = random.randint(x * 3, (x + 1) * 3 - 1)
        second = random.randint(x * 3, (x + 1) * 3 - 1)
        while second == first:
            second = random.randint(x * 3, (x + 1) * 3 - 1)
        if random.randint(0, 1):
            self.board[first], self.board[second] = self.board[second], self.board[first]
        else:
            for i in range(9):
                self.board[i][first], self.board[i][second] = self.board[i][second], self.board[i][first]

    def change_chunk(self):
        first = random.randint(0, 2)
        second = random.randint(0, 2)
        while first == second:
            second = random.randint(0, 2)

        if random.randint(0, 1):
            self.board[first * 3: first * 3 + 3], self.board[second * 3:second * 3 + 3] = self.board[
                                                                                          second * 3:second * 3 + 3], self.board[
                                                                                                                      first * 3:first * 3 + 3]
        else:
            for i in range(9):
                for j in range(3):
                    self.board[i][first * 3 + j], self.board[i][second * 3 + j] = self.board[i][second * 3 + j], \
                                                                                  self.board[i][first * 3 + j]

    def shuffle_board(self):
        for i in range(100):
            num = random.randint(0, 3)
            if not num:
                self.change_chunk()
            else:
                self.change_in_one_chunk()

    def start_player_board(self):
        self.shuffle_board()
        self.players_board = [[i for i in j] for j in self.board]
        for i in range(50):
            y = random.randint(0, 8)
            x = random.randint(0, 8)

            while self.players_board[y][x] == '.':
                y = random.randint(0, 8)
                x = random.randint(0, 8)
            self.players_board[y][x] = '.'

    def draw(self, dis, x=1,y=1,check=False):
        if check:
            dis.fill(white)

            for i in range(10):
                if i % 3 == 0:
                    continue
                pygame.draw.line(dis, gray, (i * 40, 0), (i * 40, 40 * 9), 2)
                pygame.draw.line(dis, gray, (0, i * 40), (40 * 9, i * 40), 2)
            for i in range(10):
                if i % 3:
                    continue
                pygame.draw.line(dis, black, (i * 40, 0), (i * 40, 40 * 9), 3)
                pygame.draw.line(dis, black, (0, i * 40), (40 * 9, i * 40), 3)

            pygame.display.update()

        for row in range(9):
            for col in range(9):
                if self.players_board[row][col] == '.':
                    continue
                number = f_sys.render(self.players_board[row][col], True, black)
                dis.blit(number, (col * 40 + 17, row * 40 + 10))
        pygame.display.update()

    def sudoku_check(self, i, j, num):
        return str(num) != self.board[i][j]

    def sudoku_click(self, i, j, num):
        if self.sudoku_check(i, j, num):
            return
        self.players_board[i][j] = str(num)

    def solve_sudoku(self, dis):
        result = False
        row = defaultdict(set)
        col = defaultdict(set)
        squares = defaultdict(set)
        dots = []

        def check(i, j):
            return self.players_board[i][j] in row[i] or self.players_board[i][j] in col[j] or self.players_board[i][
                j] in squares[(i // 3, j // 3)]

        for i in range(9):
            for j in range(9):
                if self.players_board[i][j] == '.':
                    dots.append((i, j))
                    continue
                if check(i, j):
                    return False
                row[i].add(self.players_board[i][j])
                col[j].add(self.players_board[i][j])
                squares[(i // 3, j // 3)].add(self.players_board[i][j])

        def backtracking(idx):
            nonlocal result, row, col, squares
            if idx == len(dots):
                result = True
                return
            i, j = dots[idx]
            sleep(0.03)
            for num in range(1, 10):
                val = str(num)
                self.players_board[i][j] = val
                if check(i, j):
                    continue
                row[i].add(val)
                col[j].add(val)
                squares[(i // 3, j // 3)].add(val)
                self.draw(dis, True)
                backtracking(idx + 1)
                if result:
                    return
                self.players_board[i][j] = '.'
                pygame.draw.rect(dis,white,(j * 40 + 5, i * 40 + 5, 30, 30))
                pygame.display.update()
                row[i].remove(val)
                col[j].remove(val)
                squares[(i // 3, j // 3)].remove(val)
            if not result:
                self.players_board[i][j] = '.'

        backtracking(0)

