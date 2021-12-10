# LL1

class Grammar:
    def __init__(self, file):
        self.nonTerminals = []
        self.productions = {}
        self.terminals = []
        self.startingSymbol = ''

        self._loadData(file)

    def _loadData(self, configurationFile):
        with open(configurationFile, 'r') as file:
            lines = file.readlines()
            firstLine = lines[0].strip()
            secondLine = lines[1].strip()
            thirdLine = lines[2].strip()
            productionsLines = lines[3:]

            self.nonTerminals = firstLine.split(',')
            self.terminals = secondLine.split(',')
            self.startingSymbol = thirdLine.split(',')[0]

            for productionLine in productionsLines:
                productionLine = productionLine.strip()
                parsedLine = productionLine.split(' -> ')
                startingPoint = parsedLine[0]
                endingPoints = parsedLine[1]
                endingPointsArray = endingPoints.split(' | ')

                existsKey = self.productions.get(startingPoint)
                if existsKey:
                    self.productions[startingPoint].append(endingPoints)
                else:
                    self.productions[startingPoint] = endingPointsArray

    def getProductionsByNonTerminal(self, nonTerminal):
        print(self.productions[nonTerminal])

    def getProductionForIndex(self, index):
        for key, value in self.productions.items():
            for v in value:
                if v[1] == index:
                    return key, v[0]

    def isNonTerminal(self, value):
        return value in self.nonTerminals

    def GFGCheck(self):
        nonTerminalsArray = self.productions.keys()

        for nonTerminal in nonTerminalsArray:
            if len(nonTerminal) != 1:
                return False
            if nonTerminal not in self.nonTerminals:
                return False
        return True

    def displayData(self):
        print('----- Non Terminals ----')
        print(self.nonTerminals)
        print('----- Productions ----')
        print(self.productions)
        print('----- Terminals ----')
        print(self.terminals)
        print('----- Starting Symbol ----')
        print(self.startingSymbol)
        print('--- Production by non terminal ---')
        self.getProductionsByNonTerminal('A')
        print('GFG Check: ', self.GFGCheck())

