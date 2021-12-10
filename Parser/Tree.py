class Node:
    def __init__(self, value, child, rightSibling):
        self.value = value
        self.child = child
        self.rightSibling = rightSibling

    def __str__(self):
        return "({}, {}, {})".format(self.value, self.child, self.rightSibling)


class Tree:
    def __init__(self, grammar):
        self.root = None
        self.grammar = grammar
        self.current = 1
        self.ws = ""
        self.indexInTreeSequence = 1

    def buildRecursive(self, currentTransition):
        if self.indexInTreeSequence == len(self.ws) and currentTransition == ['E']:
           pass
        elif len(currentTransition) == 0 or self.indexInTreeSequence >= len(self.ws):
            return None

        currentSymbol = currentTransition[0]
        if currentSymbol in self.grammar.terminals:
            node = Node(currentSymbol, None, None)
            print('Current value: ' + node.value)
            print('Finished terminal branch')
            
            node.rightSibling = self.buildRecursive(currentTransition[1:])
            return node
        elif currentSymbol in self.grammar.nonTerminals:
            transitionNumber = self.ws[self.indexInTreeSequence]
            _, production = self.grammar.getProductionForIndex(int(transitionNumber))
            node = Node(currentSymbol, None, None)
            print("current value: " + node.value)
            print("finished nonterminal branch")
            self.indexInTreeSequence += 1
            node.child = self.buildRecursive(production.split(' '))
            node.rightSibling = self.buildRecursive(currentTransition[1:])
            return node
        else:
            print('Epsilon branch')
            return Node('E', None, None)

    def print_table(self):
        self.breadthFirstSearch(self.root)
        
    def breadthFirstSearch(self, node, fatherCurrent=None, leftSiblingCurrent=None):
        if node is None:
            return []
        print("{} | {} | {} | {}".format(self.current, node.value, fatherCurrent, leftSiblingCurrent))

        crt = self.current
        self.current += 1

        if leftSiblingCurrent is not None:
            return [[node.child, crt, None]] + self.breadthFirstSearch(node.rightSibling, fatherCurrent, crt)
        else:
            children = [[node.child, crt, None]] + self.breadthFirstSearch(node.rightSibling, fatherCurrent, crt)
            for child in children:
                self.breadthFirstSearch(*child)

    def build(self, ws):
        print(ws)
        print(len(ws))
        self.ws = ws
        nonterminal, rightHandSide = self.grammar.getProductionForIndex(int(self.ws[0]))
        self.root = Node(nonterminal, None, None)
        self.root.child = self.buildRecursive(rightHandSide.split(' '))
        return self.root

    def __str__(self):
        string = ""
        node = self.root
        while node is not None:
            string += str(node)
            node = node.rightSibling
        return string
