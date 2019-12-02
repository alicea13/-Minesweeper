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
        self.color = ["blue", "yellow", "green", "white", "pink", "gray"]
        self.list_mines = []
        for _ in range(self.c_min):
            cell = (random.randint(0, self.height - 1),
                    random.randint(0, self.width - 1))
            if cell not in self.list_mines:
                self.list_mines.append(cell)
        print('\n'.join(str(i) for i in self.list_mines))
        self.board = [[0] * width for _ in range(self.height)]
        for j in range(self.width):
            for i in range(self.height):
                if (i, j) not in self.list_mines:
                    self.board[i][j] = - 1
                else:
                    self.board[i][j] = 10
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
            board.open_cell()


class Minesweeper(Board):
    def __init__(self, width, height, mines, left=10, top=10, cell_size=520):
        super().__init__(width, height, mines, left, top, cell_size)

    def open_cell(self):
        temp = copy.deepcopy(self.board)  # сохраняем поле для дальнейшего изменения текущего
        for x in range(self.width):
            l = 0
            for y in range(self.height):
                count2 = 0
                count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if (x + dx < 0 or y + dy < 0
                                or x + dx >= self.width or y + dy >= self.height):
                            continue
                        else:
                            count += self.board[y + dy][x + dx]
            count -= self.board[y][x]
            l += count
            temp[y][x] = count2
        self.board = copy.deepcopy(temp)
        print(l)
        print('\n'.join(str(i) for i in self.board))


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