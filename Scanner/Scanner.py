from SymbolTable.SymbolTable import SymbolTable
from ProgramInternalFrom import PIF
from regEx import INT_CONSTANT_REGEX, STRING_CONSTANT_REGEX, IDENTIFIER_REGEX
from FiniteAutomata import FiniteAutomata
import re


def isStringConstant(token):
    result = STRING_CONSTANT_REGEX.search(token)

    return result is not None

def isIdentifier(token):
    identifierFiniteAutomaton = FiniteAutomata('/Users/user/Desktop/Learning Journey/College/Fifth Semester/LFTC/LFTC-mini-language/Scanner/inputFiles/fa/identifier.in')

    return identifierFiniteAutomaton.isAccepted(token)

def isNumberConstant(token):
    integerFiniteAutomaton = FiniteAutomata('/Users/user/Desktop/Learning Journey/College/Fifth Semester/LFTC/LFTC-mini-language/Scanner/inputFiles/fa/integer.in')

    return integerFiniteAutomaton.isAccepted(token)


def needsLookAhead(token):
    return token in ['>', '<', '=', '!']


class Scanner:
    def __init__(self):
        self._operators = ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>", "==", "!="]
        self._separators = ["[", "]", "{", "}", ":", ";", "(", ")", '\'', '"']
        self._reservedWords = ["start", "finish", "var", "int", "char", "string", "read", "print", "if", "then", "else", "while", "execute", "break", "exit"]
        self._symbolTable = SymbolTable()
        self._PIF = PIF()

    def isReservedToken(self, token):
        return token in self._reservedWords or token in self._operators or token in self._separators

    def scanProgram(self, programFileName):
        # open file and read all lines
        programFile = open(programFileName, 'r')
        lines = programFile.readlines()

        lineCount = 0

        for line in lines:
            lineCount += 1
            # get all word from file
            lineData = re.split('("[^a-zA-Z0-9\"\']")|([^a-zA-Z0-9\"\'])', line)

            # filter words and eliminate spaces
            lineData = list(filter(None, lineData))
            lineData = map(lambda e: e.strip(), lineData)
            lineData = list(filter(None, lineData))

            omitNext = False

            for i in range(len(lineData)):
                token = lineData[i]
                if not omitNext:
                    if needsLookAhead(token) and lineData[i + 1] == '=':
                        self._PIF.add(token + lineData[i + 1], 0)
                        omitNext = True
                    elif self.isReservedToken(token):
                        self._PIF.add(token, 0)
                    elif isNumberConstant(token) or isStringConstant(token):
                        position = self._symbolTable.add(token)
                        self._PIF.add('CONST', position)
                    elif isIdentifier(token):
                        position = self._symbolTable.add(token)
                        self._PIF.add('IDENTIFIER', position)
                    else:
                        raise ValueError('Lexical error on token ' + token + ' at line: ' + str(lineCount))
                else:
                    omitNext = False

        with open('/Users/user/Desktop/Learning Journey/College/Fifth '
                  'Semester/LFTC/LFTC-mini-language/Scanner/outputFiles/ST.out', 'w') as file:
            file.write(str(self._symbolTable))

        with open("/Users/user/Desktop/Learning Journey/College/Fifth Semester/LFTC/LFTC-mini-language/Scanner/outputFiles/PIF.out", 'w') as file:
            file.write(str(self._PIF))

        return self._symbolTable, self._PIF, "Lexically correct"
