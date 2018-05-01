#!/usr/bin/env python

import sys
from copy import copy
import copy
#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

#Function to return a list of symbols present in the knowledge base and statement.
def getSymbols(expr):
    symbols = []

    if expr.symbol[0]:
        symbols.append(expr.symbol[0])

    else:
        for subexpr in expr.subexpressions:
            for symbol in getSymbols(subexpr):
                if symbol not in symbols:
                    symbols.append(symbol)
    return symbols


#Function to generate a model from the knowledge base so as to reduce the computation time for entailment.
def getModel(statement):
    model = {};
    for expr in statement.subexpressions:
        if expr.symbol[0]:
            model[expr.symbol[0]] = True
        elif expr.connective[0].upper() == 'NOT':
            if expr.subexpressions[0].symbol[0]:
                model[expr.subexpressions[0].symbol[0]] = False
        
    return model


#Function to return the truth value of the statement. Works recursively and returns the final truth value.
def plTrue(statement, model):
    if statement.symbol[0]:
        return model[statement.symbol[0]]
    elif statement.connective[0].upper() == 'OR':
        result = False
        for expr in statement.subexpressions:
            result = result or plTrue(expr, model)
        return result
    elif statement.connective[0].upper() == 'AND':
        result = True
        for expr in statement.subexpressions:
            result = result and plTrue(expr, model)
        return result
    elif statement.connective[0].upper() == 'XOR':
        result = False
        for expr in statement.subexpressions:
            isExprTrue = plTrue(expr, model)
            result = (result and not isExprTrue) or (not result and isExprTrue)
        return result
    elif statement.connective[0].upper() == 'IF':
        leftExpr = statement.subexpressions[0]
        rightExpr = statement.subexpressions[1]
        isLeftExprTrue = plTrue(leftExpr, model)
        isRightExprTrue = plTrue(rightExpr, model)
        if( isLeftExprTrue and not isRightExprTrue ):
            return False
        else:
            return True
    elif statement.connective[0].upper() == 'IFF':
        leftExpr = statement.subexpressions[0]
        rightExpr = statement.subexpressions[1]
        isLeftExprTrue = plTrue(leftExpr, model)
        isRightExprTrue = plTrue(rightExpr, model)
        if( isLeftExprTrue == isRightExprTrue ):
            return True
        else:
            return False
    elif statement.connective[0].upper() == 'NOT':
        return not plTrue(statement.subexpressions[0],model)



#Function to call the TT-Entails algorithm. Symbols and model are generated here and redundant symbols are discarded.
def check_true_false(knowledgeBase, statement):
    model = getModel(knowledgeBase)
    symbols = getSymbols(knowledgeBase)
    
    for symbol in getSymbols(statement):
        symbols.append(symbol)

    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)

    for s in model:
        for symbol in getSymbols(statement):
            if symbol == s:
                symbols.remove(s)
    return TTCheckAll(knowledgeBase, statement, symbols, model)
    


#Function that implements TT Entails algorithm. Using recursion the truth value is found out and
#knowledge base is used to ensure the algorithm time is reasonable.
def TTCheckAll(knowledgeBase, statement, symbols, model):
    if not symbols:
        if plTrue(knowledgeBase, model):
            return plTrue(statement, model)
        else:
            return True
    else:
        symbols2 = copy.deepcopy(symbols)
        symbol = symbols.pop(0)
        symbol2 = symbols2.pop(0)
        return TTCheckAll(knowledgeBase, statement, symbols, extend(model, symbol, True)) and TTCheckAll(knowledgeBase, statement, symbols2, extend(model, symbol2, False))
        

#Function to add elements to the model which are not provided in the knowledge base.
def extend(model, symbol, val):
    model[symbol] = val
    return model

