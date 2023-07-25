import cv2 as cv
import numpy as np
import pyautogui as pg
import chess 
import chess.engine
import sys

# constants

BOARD_SIZE = 610
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 215
BOARD_LEFT_COORD = 4
CONFIDENCE = 0.73
DETECTION_NOISE_THRESHOLD = 15
PIECES_PATH = './piece_recog/pieces/'

# players
WHITE = 0
BLACK = 1

# side to move
stm = 0

# read argv 
try:
    if sys.argv[1] == 'black': stm = BLACK
except:
    print('usage: "chessbot.py white" or "chessbot.py black"')
    sys.exit(0)

piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}

# locate piece on given image

def locate_piece(screenshot, piece_loc):
    # loop over pieces
    for index in range(len(piece_loc)):
        piece = piece_loc[index]
        # draw rectangle around piece
        cv.rectangle(
            screenshot,
            (piece.left, piece.top),
            (piece.left + piece.width, piece.top + piece.height),
            (0, 0, 255),
            2
        )

    cv.imshow('Screenshot', screenshot)
    cv.waitKey(0)

def find_pos():
    piece_locs = {
        'black_king': [],
        'black_queen': [],
        'black_rook': [],
        'black_bishop': [],
        'black_knight': [],
        'black_pawn': [],
        'white_knight': [],
        'white_pawn': [],
        'white_king': [],
        'white_queen': [],
        'white_rook': [],
        'white_bishop': []
    }

    # take a board snapshot
    screenshot = cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR)

    for piece in piece_names.keys():
        for location in pg.locateAllOnScreen(PIECES_PATH + piece + '.png', confidence=CONFIDENCE):
            # Noise detection 
            noise = False

            for pos in piece_locs[piece]:
                if abs(pos.left - location.left) < DETECTION_NOISE_THRESHOLD and \
                    abs(pos.top - location.top) < DETECTION_NOISE_THRESHOLD:
                        noise = True
                        break
            if noise: continue

            piece_locs[piece].append(location)

    return screenshot, piece_locs


def loc_to_fen(piece_locs):
    # FEN string
    fen = ""

    x = BOARD_LEFT_COORD
    y = BOARD_TOP_COORD

    for row in range(8):
        # empty square counter
        empty = 0
        for col in range(8):
            # intit square
            square = row * 8 + col
            # piece detection
            is_piece = ()

            for piece_type in piece_locs.keys():
                for piece in piece_locs[piece_type]:
                    if abs(piece.left - x) < DETECTION_NOISE_THRESHOLD and \
                    abs(piece.top - y) < DETECTION_NOISE_THRESHOLD:
                        if empty:
                            fen += str(empty)
                            empty = 0

                        fen += piece_names[piece_type]
                        is_piece = (square, piece_names[piece_type])

            if not len(is_piece):
                empty += 1

            # increment x coord by cell size
            x += CELL_SIZE
        
        if empty: fen += str(empty)
        if row < 7: fen += '/'

        x = BOARD_LEFT_COORD
        y += CELL_SIZE
    
    # add side to move to FEN
    fen += ' b' if stm else ' w'
    
    # add placeholders (no 'en passant' and castling)
    fen += ' KQkq - 0 1'

    return fen




# Main


screenshot, piece_locs = find_pos()

for piece in piece_names.keys():
    locate_piece(screenshot, piece_locs[piece])

fen = loc_to_fen(piece_locs)
print('FEN: ', fen)
