import pygame
import sys
import random

def win(pl, fld):
    if fld[0] == pl and fld[1] == pl and fld[2] == pl or \
            fld[3] == pl and fld[4] == pl and fld[5] == pl or \
            fld[6] == pl and fld[7] == pl and fld[8] == pl or \
            fld[0] == pl and fld[3] == pl and fld[6] == pl or \
            fld[1] == pl and fld[4] == pl and fld[7] == pl or \
            fld[2] == pl and fld[5] == pl and fld[8] == pl or \
            fld[0] == pl and fld[4] == pl and fld[8] == pl or \
            fld[2] == pl and fld[4] == pl and fld[6] == pl:
        return True
    return False

def game_over(fld):
    for i in range(9):
        if fld[i] == 0:
            return False
    return True

def free_cell(fld):
    ans = []
    for i in range(9):
        if fld[i] == 0:
            ans.append(i)
    return ans

def balanse(k, pl, fld):
    nfld = fld.copy()
    nfld[k] = pl
    if win(pl, nfld):
        return 1
    elif game_over(nfld):
        return 0
    fc = free_cell(nfld)
    b = []
    for i in range(len(fc)):
        nb = balanse(fc[i], 3 - pl, nfld)
        b.append(nb)
    m = -1
    for i in range(len(b)):
        if b[i] > m:
            m = b[i]
    m *= -1
    return m

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False


pygame.init()
size_block = 140
margin = 5
width = heigth = size_block * 3 + margin * 4

size_window = (width, heigth)

screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Tic-tac-toe")

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 128, 0)
teal = (0, 128, 128)
LightSeaGreen = (32, 178, 170)
PaleTurquoise =	(175, 238, 238)
field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
counter = 0
flag = True
play_with_clever = False
play_with_stupid = False
start_menu = True
cleverButton = button(teal, 70, 200, 300, 80, 'Play with clever!')
stupidButton = button(teal, 70, 320, 300, 80, 'Play with stupid!')
while True:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and flag:
            if cleverButton.isOver(pos):
                play_with_clever = True
                play_with_stupid = False
                flag = False
                start_menu = False
                counter = 0
                field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                screen.fill(black)
            if stupidButton.isOver(pos):
                play_with_stupid = True
                start_menu = False
                play_with_clever = False
                flag = False
                counter = 0
                field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                screen.fill(black)
        elif event.type == pygame.MOUSEBUTTONDOWN and not flag:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (size_block+margin)
            row = y_mouse // (size_block+margin)
            if (field[3* row + col] == 0 and counter % 2 == 0):
                field[3*row + col] = 1
                counter += 1
        elif event.type == pygame.MOUSEMOTION:
            if cleverButton.isOver(pos):
                cleverButton.color = PaleTurquoise
            else:
                cleverButton.color = teal
            if stupidButton.isOver(pos):
                stupidButton.color = PaleTurquoise
            else:
                stupidButton.color = teal

    if not flag:
        for row in range(3):
            for col in range(3):
                x = col * size_block + (col+1)*margin
                y = row * size_block + (row + 1)*margin
                pygame.draw.rect(screen, LightSeaGreen, (x, y, size_block, size_block))
                if field[3 * row + col] == 1:
                    pygame.draw.line(screen, black, (x, y), (x+size_block, y+size_block), 5)
                    pygame.draw.line(screen, black, (x+size_block, y), (x, y+size_block), 5)
                elif field[3 * row + col] == 2:
                    pygame.draw.circle(screen, black, (x+size_block//2, y+size_block//2), size_block//2, 5)
    if start_menu:
        screen.fill(LightSeaGreen)
        cleverButton.draw()
        stupidButton.draw()
    if win(1, field):
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render("YOU WIN!", True, green)
        text_rect = text.get_rect()
        text_x = screen.get_width()/2 - text_rect.width/2
        text_y = 70
        screen.blit(text, [text_x, text_y])
        flag = 1
        cleverButton.draw()
        stupidButton.draw()
    elif win(2, field):
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render("YOU LOSE!", True, red)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = 70
        screen.blit(text, [text_x, text_y])
        flag = 1
        cleverButton.draw()
        stupidButton.draw()
    elif game_over(field):
        font = pygame.font.SysFont('comicsans', 80)
        text = font.render("DRAW!", True, green)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = 70
        screen.blit(text, [text_x, text_y])
        flag = 1
        cleverButton.draw()
        stupidButton.draw()
    if not flag:
        if counter % 2:
            if play_with_clever:
                fc = free_cell(field)
                b = []
                for i in range(len(fc)):
                    nb = balanse(fc[i], 2, field)
                    b.append(nb)
                m = -5
                idd = 0
                for i in range(len(b)):
                    if b[i] > m:
                        m = b[i]
                        idd = fc[i]
                field[idd] = 2
                counter += 1
            if play_with_stupid:
                fc = free_cell(field)
                idd = random.randint(0, len(fc) - 1)
                field[fc[idd]] = 2
                counter += 1
    pygame.display.update()
