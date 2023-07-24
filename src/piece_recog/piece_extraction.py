import cv2 as cv
import pyautogui as pg 

# constants

BOARD_SIZE = 600
DARK_SQUARE_THRESHOLD = 150
CELL_SIZE = int(BOARD_SIZE / 8)
BOARD_TOP_COORD = 146
BOARD_LEFT_COORD = 5

# map pieces

piece_names = {
    '0': 'black_king',
    '1': 'black_queen',
    '2': 'black_rook',
    '3': 'black_bishop',
    '4': 'black_knight',
    '5': 'black_pawn',
    '6': 'white_knight',
    '7': 'white_pawn',
    '8': 'white_king',
    '9': 'white_queen',
    '10': 'white_rook',
    '11': 'white_bishop'
}

y = BOARD_TOP_COORD
x = BOARD_LEFT_COORD

# take screenshot and store it locally
pg.screenshot('screenshot.png')

screenshot = cv.imread('screenshot.png')
screenshot_grayscale = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

piece_code = 0

# loop over board rows and columns
for row in range(8):
    for col in range(8):
        if row in [0, 1, 5, 6]:
            if screenshot_grayscale[y][x] > DARK_SQUARE_THRESHOLD:
                # skip empty cells
                if row == 1 and col < 4: continue
                if row == 5 and col < 4: continue

                # crop piece image
                piece_image = screenshot[y:y + CELL_SIZE, x: x + CELL_SIZE]

                # display extracted images (for verification)
                cv.imshow('scr', piece_image)
                cv.waitKey(0)

                # store extracted image
                cv.imwrite('./pieces/' + piece_names[str(piece_code)] + '.png', piece_image)

                piece_code += 1
            
            x += CELL_SIZE

        x = BOARD_LEFT_COORD
        y += CELL_SIZE

    cv.destroyAllWindows()