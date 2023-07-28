import cv2 as cv
import numpy as np
import pyautogui as pg
import chess 
import chess.engine
import sys
import time
from stockfish import Stockfish
from waiting import wait

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

player = 0

# read argv 
try:
    if sys.argv[1] == 'black': stm = BLACK
except:
    print('usage: "chessbot.py white" or "chessbot.py black"')
    sys.exit(0)

square_to_coords = []

# array to convert board square indices to coordinates (black)
get_square = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
];

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


def search(fen):
    print("Searching for best move in this position...")
    print(fen)
    board = chess.Board(fen)
    print(board)

    # load Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("./Stockfish/stockfish/stockfish")

    # load BBC engine
    # engine = chess.engine.SimpleEngine.popen_uci("./bbc/bbc")

    # get best move
    best_move = str(engine.play(board, chess.engine.Limit(time=0.1)).move)
    engine.quit()

    return best_move


def my_turn(curr_fen):
    screenshot, piece_locs = find_pos()  
    fen = loc_to_fen(piece_locs)

    if curr_fen != fen:
        return True
    return False


# ------ INIT COORDS --------
x = BOARD_LEFT_COORD
y = BOARD_TOP_COORD

for row in range(8):
    for col in range(8):
        square = row * 8 + col
        square_to_coords.append((int(x + CELL_SIZE / 2), int(y + CELL_SIZE / 2)))

        x += CELL_SIZE
        
    x = BOARD_LEFT_COORD
    y += CELL_SIZE


# ------------ MAIN --------------

curr_fen = ''

while True:
    try:
        # locate pieces
        screenshot, piece_locs = find_pos()
        
        # convert piece image coords to FEN string
        fen = loc_to_fen(piece_locs)

        # find best move
        best_move = search(fen)
        print("Best Move: ", best_move)

        # extract source and destination square coords
        from_sq = square_to_coords[get_square.index(best_move[0] + best_move[1])]
        to_sq = square_to_coords[get_square.index(best_move[2] + best_move[3])]

        # make move
        pg.moveTo(from_sq)
        pg.click()
        pg.moveTo(to_sq)
        pg.click()

        # wait for opponent to move

        screenshot, piece_locs = find_pos()
        curr_fen = loc_to_fen(piece_locs)

        # when FEN changes it means opponent has made a move
        wait(lambda: my_turn(curr_fen), timeout_seconds=600, waiting_for='Waiting for opponent...')

    except:
        print("gg easy.")
        sys.exit(0)