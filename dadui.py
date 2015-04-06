import pygame
import sys
from AICore import MoreSmartAI
from three import *
import random

slide_start = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1) }

def true_random(max):
    return random.randrange(max)

def true_shuffle(lst):
    copy = list(lst)
    random.shuffle(copy)
    return copy

dirs = [UP, RIGHT, DOWN, LEFT]
dir_pos = [(.5, 0), (1, .5), (.5, 1), (0, .5)]

def score_degrees(cells):
    count = 0
    for d in dirs:
        if Board(cells).shift(d).cells != cells:
            count += 1
        else:
            count += 0
    return count * 25

class Analysis:
    def __init__(self):
        self.remaining = [0, 0, 0]  # Threes, twos, ones
        self.max_extra_pkg = 0      # Max value of extra item (btwn 6 and that item)
        self.board = [0] * 16
        self.next_dir = 0           # What direction to try next
        self.depth = 0              # How much depth
        self.probability = 0.0      # Accum probability on this branch

def score_direction(cells, dir, depth):
    pass


def run_game():
    # Game parameters
    CELL_WIDTH = 100
    CELL_HEIGHT = 100
    BORDER = 5
    TOP_START = 100
    GUTTER_SIZE = 100
    SCREEN_WIDTH, SCREEN_HEIGHT = (5 * BORDER + 4*CELL_WIDTH + 2*GUTTER_SIZE, 5*BORDER + 4*CELL_HEIGHT + TOP_START + 2*GUTTER_SIZE)
    PEEK_WIDTH = 30
    PEEK_HEIGHT = 45

    BG_COLOR = 0x46,0xF0,0xE4
    RECT_COLOR = 0x3C,0xC7,0xBD
    FPS = 50
    MOVE_SPEED = 0.25 # seconds
    ONEBG = 0, 128, 0
    TWOBG = 128, 0, 0
    THREEBG = 255,255,255

    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    fonts = [pygame.font.Font(None, x) for x in [144, 120, 60, 50, 40]]
    peek_font = pygame.font.Font(None, 20)

    def piece_colors(v):
        fg = 255,255,255
        if v == 0:
            bg = RECT_COLOR
        elif v == 1:
            bg = ONEBG
        elif v == 2:
            bg = TWOBG
        else:
            bg = THREEBG
            fg = 0,0,0
        return fg, bg

    def draw_score(dir, txt):
        xm, ym = dir_pos[dir]
        rect = pygame.Rect( GUTTER_SIZE *xm + 4 * xm  * (CELL_WIDTH + BORDER) + BORDER, TOP_START + GUTTER_SIZE*ym + 4 * ym * (CELL_HEIGHT + BORDER) + BORDER, CELL_WIDTH, CELL_HEIGHT)
        text = fonts[len(txt)-1].render(txt, 1, (255,255,255))
        textpos = text.get_rect()
        textpos.center = rect.center
        screen.blit(text, textpos)

    def draw_peek(piece):
        for i in piece:
            fg, bg = piece_colors(i)
        rect = [0, 0, 0]
        rect[0] = pygame.Rect( ((SCREEN_WIDTH - PEEK_WIDTH) / 2)-PEEK_WIDTH-10, (TOP_START - PEEK_HEIGHT) / 2, PEEK_WIDTH, PEEK_HEIGHT)
        rect[1] = pygame.Rect( (SCREEN_WIDTH - PEEK_WIDTH) / 2, (TOP_START - PEEK_HEIGHT) / 2, PEEK_WIDTH, PEEK_HEIGHT)
        rect[2] = pygame.Rect( ((SCREEN_WIDTH - PEEK_WIDTH) / 2)+PEEK_WIDTH+10, (TOP_START - PEEK_HEIGHT) / 2, PEEK_WIDTH, PEEK_HEIGHT)
        if piece[0] <= 3:
            pygame.draw.rect(screen, bg, rect[1])
        if piece[0] > 3 and len(piece) == 3:
            for i in range(len(piece)):
                txt = str(piece[i])
                text = peek_font.render(txt, 1, fg)
                textpos = text.get_rect()
                textpos.center = rect[i].center
                pygame.draw.rect(screen, (255, 255, 255), rect[i])
                screen.blit(text, textpos)

    def draw_board(board, x, y):
        for row in range(4):
           for col in range(4):
               v = board[row][col]
               if v != -1:
                   fg, bg = piece_colors(v)
                   rect = pygame.Rect( x + col * (CELL_WIDTH + BORDER) + BORDER, y + row * (CELL_HEIGHT + BORDER) + BORDER, CELL_WIDTH, CELL_HEIGHT)
                   pygame.draw.rect(screen, bg, rect)
                   if v > 0:
                       txt = "%d" % v
                       text = fonts[len(txt)-1].render(txt, 1, fg)
                       textpos = text.get_rect()
                       textpos.center = rect.center
                       screen.blit(text, textpos)


    game = ThreeGame(true_random, true_shuffle)
    ai = MoreSmartAI()

    baseboard = None
    movingboard = None
    x, y, vx, vy = 0,0,0,0

    while True:
        # Limit frame speed to 50 FPS
        #
        time_passed = clock.tick(FPS)
        shift = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                print game.peek(), game.peek()
                if event.key == pygame.K_LEFT:
                    shift = LEFT
                elif event.key == pygame.K_RIGHT:
                    shift = RIGHT
                elif event.key == pygame.K_UP:
                    shift = UP
                elif event.key == pygame.K_DOWN:
                    shift = DOWN

                if shift is not None:
                    baseboard = game.board
                    if game.shift is not None:
                        game = game.shift(shift)
                    # x, y = slide_start[shift]
                    # x *= CELL_WIDTH
                    # y *= CELL_HEIGHT
                    # # Take 0.5 seconds to slide. Want pixels per frame
                    # vx = -x / (FPS * MOVE_SPEED)
                    # vy = -y / (FPS * MOVE_SPEED)

        # Redraw the background
        screen.fill(BG_COLOR)

        draw_board(game.board, GUTTER_SIZE, GUTTER_SIZE+TOP_START)
        draw_peek(game.peek())
        for d in dirs:
            score = ai.evaluateMoveValue(game.board, game.peek()[0], d)
            txt = "%.0f" % score
            draw_score(d, txt)


        # if baseboard is not None:
        #     draw_board(baseboard, 0, TOP_START)
        #     overlap = diff_board(baseboard, game.board)
        #     draw_board(overlap, x, TOP_START + y)
        #     if (int(x) == 0 or (x+vx < 0) != (x < 0)) and (int(y) == 0 or (y+vy < 0) != (y < 0)):
        #         baseboard = None
        #     x += vx
        #     y += vy
        # else:
        #     draw_board(game.board, 0, TOP_START)
        # draw_peek(game.peek())

        pygame.display.flip()
        if game.isEnded() is True:
            file = 'some.mp3'
            pygame.mixer.init()
            pygame.mixer.music.load('Price-is-right-losing-horn.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            sys.exit()


def exit_game():
    sys.exit()


run_game()
