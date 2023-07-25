import cv2 as cv
import numpy as np
import pyautogui as pg
import chess 

# constants

BOARD_SIZE = 610
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 215
BOARD_LEFT_COORD = 4
CONFIDENCE = 0.7
DETECTION_NOISE_THRESHOLD = 12
PIECES_PATH = './piece_recog/pieces/'

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
                if abs(pos.left - location.left) < DETECTION_NOISE_THRESHOLD and abs(pos.top - location.top) < DETECTION_NOISE_THRESHOLD:
                    noise = True
                    break
            if noise: continue

            piece_locs[piece].append(location)

    return screenshot, piece_locs


screenshot, piece_locs = find_pos()

for piece in piece_names.keys():
    locate_piece(screenshot, piece_locs[piece])