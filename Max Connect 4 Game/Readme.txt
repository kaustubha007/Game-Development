Name: Kaustubh Sanjiv Agnihotri




Structure:

Code is developed in python 2.3.

The game works in 2 modes:

1) Interactive Mode
	
4 arguments are expected 
i.e. game_mode input_file.txt human-next/computer-next depth
	
eg. python Connect4Game.py interactive input_file.txt human-next 5
	
in the same order as mentioned respectively.
	
In case input file does not exist, game starts in default state with blank board.


2) One-Move Mode:
	
4 arguments are expected 
i.e. game_mode input_file.txt output_file.txt depth
	
eg. python Connect4Game.py interactive input_file.txt output_file.txt 5
	
in the same order as mentioned respectively.
	
Game does not start if input file is missing.


It starts with main function where the arguments and input file are read. 
The game board is created and displayed.
If the mode is interactive mode, 
user and computer play alternatively.
In one-move word the program reads 
the board state from the input file and decides the move to be made. 

Then it prints the new game after making the move and writes it to the output file.


Note: Please make sure the input file is in the same directory as the source code file.


