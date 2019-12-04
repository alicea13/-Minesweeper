import pygame
import random
import copy


class Board:
    # создание поля
    def __init__(self, width, height, mines, left=10, top=10, cell_size=50):
        self.width = width
        self.height = height
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.c_min = mines
        self.set_view(left, top, cell_size)
        self.list_mines = []
        while len(self.list_mines) != self.c_min:
            cell = (random.randint(0, self.height - 1),
                    random.randint(0, self.width - 1))
            if cell not in self.list_mines:
                self.list_mines.append(cell)
        print('\n'.join(str(i) for i in self.list_mines))
        self.board = [[0] * width for _ in range(self.height)]
        for y in range(self.width):
            for x in range(self.height):
                if (x, y) not in self.list_mines:
                    self.board[x][y] = - 1
                else:
                    self.board[x][y] = 10
        print('\n'.join(str(i) for i in self.board))

    # настройка внешнего вида

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 ((self.left + self.cell_size * i, self.top + self.cell_size * j),
                                 (self.cell_size, self.cell_size)), 1)
                if self.board[j][i] == 10:
                    pygame.draw.rect(screen2, pygame.Color("red"),
                                     ((self.left + self.cell_size * i,
                                       self.top + self.cell_size * j),
                                      (self.cell_size, self.cell_size)))
                elif self.board[j][i] == -1:
                    pygame.draw.rect(screen2, pygame.Color("black"),
                                     ((self.left + self.cell_size * i,
                                       self.top + self.cell_size * j),
                                      (self.cell_size, self.cell_size)))

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[
            0] <= self.left + self.cell_size * self.width and
                self.top <= mouse_pos[
                    1] <= self.top + self.cell_size * self.height):
            y = (mouse_pos[0] - self.left) // self.cell_size
            x = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        else:
            return None

    def on_click(self, cell_pos):
        pass  # заглушка для других полей

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            if self.board[cell[0]][cell[1]] != 10:
                board.open_cell(cell[0], cell[1])
        return cell[0], cell[1]


class Minesweeper(Board):
    def __init__(self, width, height, mines, left=10, top=10, cell_size=520):
        super().__init__(width, height, mines, left, top, cell_size)

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 ((self.left + self.cell_size * i, self.top + self.cell_size * j),
                                 (self.cell_size, self.cell_size)), 1)
                if self.board[j][i] == 10:
                    pygame.draw.rect(screen2, pygame.Color("red"),
                                     ((self.left + self.cell_size * i,
                                       self.top + self.cell_size * j),
                                      (self.cell_size, self.cell_size)))
                elif self.board[j][i] == -1:
                    pygame.draw.rect(screen2, pygame.Color("black"),
                                     ((self.left + self.cell_size * i,
                                       self.top + self.cell_size * j),
                                      (self.cell_size, self.cell_size)))

                # выводить число мин вокруг выбранной клетки
                #elif self.board[j][i] != 10 and self.board[j][i] != -1:
                    #screen.blit(self.bombs, (y0 * self.width, x0 * self.height))

    def open_cell(self, x0, y0):
        print(f"cell {x0, y0}")
        temp = copy.deepcopy(self.board)  # сохраняем поле для дальнейшего изменения текущего
        self.count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (x0 + dx < 0 or y0 + dy < 0
                        or y0 + dy >= self.width or x0 + dx >= self.height):
                    continue
                else:
                    print(x0 + dx, y0 + dy)
                    if self.board[x0 + dx][y0 + dy] == 10:
                        self.count += 1
                        print(f"bomb {x0 + dx, y0 + dy}")
        temp[x0][y0] = self.count
        self.board = copy.deepcopy(temp)
        print('\n'.join(str(i) for i in self.board))

        # создаем объект-шрифт, который будем рендерить и накладывать на screen
        fon = pygame.font.Font(None, 100)
        self.bombs = fon.render(str(self.count), 1,
                           pygame.Color("green"))
        # screen.blit(self.bombs, (y0 * self.width, x0 * self.height))


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())

# поле 5 на 7
board = Minesweeper(5, 7, 7, 10, 10, 10)
board.set_view(20, 20, 20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    screen.blit(screen2, (0, 0))
    board.render()
    pygame.display.flip()