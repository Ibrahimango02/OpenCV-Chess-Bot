# OpenCV Chess Bot

This project showcases the development of an advanced chess bot that can autonomously engage users in live chess matches online. It leverages the power of Python's OpenCV and PyAutoGUI libraries to fully analyze the state of a current chess game and make the best move on the board.

## How It Works

The OpenCV Chess Bot works by capturing screenshots of the user's current game and processes the image to identify and extract the positions of each piece on the board to generate an FEN string (a string used to denote the state of a chess board at any given time). Then using this string as input, the bot finds the best move in the current position using an imported chess engine (Stockfish). Finally, the PyAutoGUI library is used to control the user's mouse to click on the piece to move it to the correct position.

![image](https://github.com/Ibrahimango02/OpenCV-Chess-Bot/assets/86329820/ebc849ef-34d3-4b07-8fd9-76a6dcaccd95)

## Important Notes

This project was only created as a way to learn the basics of computer vision techniques so some features have not been created with ease of use in mind:
- Program only works on Lichess.com
- Screen layout must be pixel-perfect in order for piece detection to work properly
- Program cannot handle premoves



