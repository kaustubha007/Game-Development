import sys
import os
import time
from Connect4GameSearch import *

def printGameDetails(currentGame):
    currentGame.countScore()
    print 'Game state after move:'
    currentGame.printGameBoard()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

def oneMoveGame(currentGame, outFile):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay() # Make a move 

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if currentGame.currentTurn == 2:
        currentGame.currentTurn = 1
    else:
        currentGame.currentTurn = 2
    currentGame.printGameBoardToFile(outFile)
    

def interactiveGame(currentGame, currentPlayer):
    while currentGame.pieceCount != 42:    # If the board is not full?
        
        if currentPlayer.upper() == 'COMPUTER-NEXT':
            startTime = time.time()
            currentGame.aiPlay()
            endTime = time.time()
            printGameDetails(currentGame)
            currentPlayer = 'HUMAN-NEXT'
            if currentGame.currentTurn == 1:
                currentGame.currentTurn = 2
            elif currentGame.currentTurn == 2:
                currentGame.currentTurn = 1
            currentGame.printGameBoardToFile('computer.txt')
            print 'Time: ' + str(endTime - startTime)
        elif currentPlayer.upper() == 'HUMAN-NEXT':
            column = int(input('Enter column (1 to 7) to insert next piece: ')) - 1
            if column >= 0 and column <= 7:
                if currentGame.playPiece(column):
                    print('\n\nMove %d: Player %d, Column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, column + 1))
                    printGameDetails(currentGame)
                    currentPlayer = 'COMPUTER-NEXT'
                    currentGame.printGameBoardToFile('human.txt')
                    if currentGame.currentTurn == 2:
                        currentGame.currentTurn = 1
                    else:
                        currentGame.currentTurn = 2
                else:
                    print 'Column full. Please enter another column.'
            else:
                print 'Invalid column.'
    
    print 'BOARD FULL\n\nGame Over!\n'
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    if currentGame.player1Score > currentGame.player2Score:
        print 'Player 1 Wins!'
    elif currentGame.player1Score < currentGame.player2Score:
        print 'Player 2 Wins!'
    else:
        print 'It\'s a Tie!'
    sys.exit(0)

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    if os.path.isfile(inFile):
        currentGame.gameFile = open(inFile, 'r')

        # Read the initial game state from the file and save in a 2D list
        file_lines = currentGame.gameFile.readlines()
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
        currentGame.gameFile.close()
    elif game_mode.upper() == 'ONE-MOVE':
        print 'File does not exist. Please check.'
        sys.exit(0)
        
    currentGame.maxDepth = argv[4]
    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode.upper() == 'INTERACTIVE':
        currentPlayer = argv[3]
        interactiveGame(currentGame, currentPlayer) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        oneMoveGame(currentGame, outFile) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
