Name: Kaustubh Sanjiv Agnihotri

Structure:
Code is developed in python 2.3.

The check_true_false.py program expects 3 commandline arguments:

i.e. wumpus_file knowledge_base_file statement_file
	
eg. python check_true_false.py wumpus_rules.txt kb.txt statement.txt
	
in the same order as mentioned respectively.
	

An additional logical_expressions.py file is used to implement all the 
internal functionality of the program.

A function check_true_false which takes knowledge_base and statement as argument, generates model from entire knowledge base and extracts all the symbols from the knowledge base and statement. Then TTCheckAll function is called which performs recursive checking on the knowledge base and statement using model and symbols and it returns the final truth value of the statement. Another call is mase to check_true_false function with negation of the statement and the result is decided from the truth values of both checks. The result is stored into a result.txt file. 


Note: Please make sure all the required files are in the same directory as the source code file.


PS: The files used for testing have been included
.
