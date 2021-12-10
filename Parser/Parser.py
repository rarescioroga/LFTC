from copy import deepcopy


class Parser:

    def __init__(self, grammar):
        self.grammar = grammar
        self.firstSet = {i: set() for i in self.grammar.nonTerminals}
        self.followSet = {i: set() for i in self.grammar.nonTerminals}
        self.table = {}
        self.generateFirst()
        self.generateFollow()

    def innerLoop(self, initialSet, items, additionalSet):
        copySet = initialSet

        for i in range(len(items)):
            if self.grammar.isNonTerminal(items[i]):
                copySet = copySet.union(entry for entry in self.firstSet[items[i]] if entry != 'E')
                if 'E' in self.firstSet[items[i]]:
                    if i < len(items) - 1:
                        continue
                    copySet = copySet.union(additionalSet)
                    break
                else:
                    break
            else:
                copySet = copySet.union({items[i]})
                break

        return copySet

    def generateFirst(self):
        isSetChanged = False

        for key, value in self.grammar.productions.items():
            for v in value:
                items = v[0].split(' ')
                copySet = self.firstSet[key]
                copySet = copySet.union(self.innerLoop(copySet, items, ['E']))

                if len(self.firstSet[key]) != len(copySet):
                    self.firstSet[key] = copySet
                    isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for key, value in self.grammar.productions.items():
                for v in value:
                    terminalsArray = v[0].split(' ')
                    copySet = self.firstSet[key]
                    copySet = copySet.union(self.innerLoop(copySet, terminalsArray, ['E']))

                    if len(self.firstSet[key]) != len(copySet):
                        self.firstSet[key] = copySet
                        isSetChanged = True

    def generateFollow(self):
        self.followSet[self.grammar.startingSymbol].add('E')
        isSetChanged = False

        for key, value in self.grammar.productions.items():
            for v in value:
                terminalsArray = v[0].split(' ')
                for i in range(len(terminalsArray)):
                    if not self.grammar.isNonTerminal(terminalsArray[i]):
                        continue
                    copySet = self.followSet[terminalsArray[i]]
                    if i < len(terminalsArray) - 1:
                        copySet = copySet.union(self.innerLoop(copySet, terminalsArray[i + 1:], self.followSet[key]))
                    else:
                        copySet = copySet.union(self.followSet[key])

                    if len(self.followSet[terminalsArray[i]]) != len(copySet):
                        self.followSet[terminalsArray[i]] = copySet
                        isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for key, value in self.grammar.productions.items():
                for v in value:
                    terminalsArray = v[0].split(' ')
                    for i in range(len(terminalsArray)):
                        if not self.grammar.isNonTerminal(terminalsArray[i]):
                            continue
                        copySet = self.followSet[terminalsArray[i]]
                        if i < len(terminalsArray) - 1:
                            copySet = copySet.union(self.innerLoop(copySet, terminalsArray[i + 1:], self.followSet[key]))
                        else:
                            copySet = copySet.union(self.followSet[key])

                        if len(self.followSet[terminalsArray[i]]) != len(copySet):
                            self.followSet[terminalsArray[i]] = copySet
                            isSetChanged = True

    def evaluateSequence(self, sequence):
        w = sequence.split(' ')
        stack = [self.grammar.startingSymbol, '$']
        output = ""
        while stack[0] != '$' and w:
            print(w, stack)
            if w[0] == stack[0]:
                w = w[1:]
                stack.pop(0)
            else:
                x = w[0]
                a = stack[0]
                if (a, x) not in self.table.keys():
                    return None
                else:
                    stack.pop(0)
                    rightHandSide, index = self.table[(a, x)]
                    rightHandSide = rightHandSide.split(' ')
                    for i in range(len(rightHandSide) - 1, -1, -1):
                        if rightHandSide[i] != 'E':
                            stack.insert(0, rightHandSide[i])
                    output += str(index) + " "
            print(output)
        if stack[0] == '$' and w:
            return None
        elif not w:
            while stack[0] != '$':
                a = stack[0]
                if (a, '$') in self.table.keys():
                    output += str(self.table[(a, '$')][1]) + " "
                stack.pop(0)
            return output