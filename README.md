# OpenCV Chess Bot

This project showcases the development of an advanced chess bot that can autonomously engage users in live chess matches online. It leverages the power of Python's OpenCV and PyAutoGUI libraries to fully analyze the state of a current chess game and make the best move on the board.

## How It Works

The OpenCV Chess Bot works by capturing screenshots of the user's current game and processes the image to identify and extract the positions of each piece on the board to generate an FEN string (a string used to denote the state of a chess board at any given time). Then using this string as input, the bot finds the best move in the current position using an imported chess engine (Stockfish). Finally, the PyAutoGUI library is used to control the user's mouse to click on the piece to move it to the correct position.

![image](https://github.com/Ibrahimango02/OpenCV-Chess-Bot/assets/86329820/c98be7e8-d2d5-424a-b922-a97f29c43825)



