from Parser import Parser
from Tree import Tree
from Grammar import Grammar

class UI:

    def __init__(self):
        self.g1 = Grammar('/Users/user/Desktop/Learning Journey/College/Fifth Semester/LFTC/LFTC-mini-language/Parser/G1.txt')
        self.grammar = None
        self.parser = None
        self.p1 = None

    def run(self):
        while True:
            print(">>")
            cmd = input()
            if cmd == "g1":
                self.evaluateG1()

    def readSequence(self, fname):
        sequence = ""
        with open(fname, 'r') as fin:
            for line in fin.readlines():
                sequence += line.strip() + " "
        return sequence.strip()

    def evaluateG1(self):
        self.p1 = Parser(self.g1)
        print(self.p1.firstSet)
        print(self.p1.followSet)
        # for k in self.p1.table.keys():
        #     print(k, '->', self.p1.table[k])
        # result = self.p1.evaluateSequence(self.readSequence('seq.txt'))
        # if result is None:
        #     print("Sequence not accepted")
        # else:
        #     print(result)
        #     t = Tree(self.g1)
        #     t.build(result.strip().split(' '))
        #     t.print_table()
