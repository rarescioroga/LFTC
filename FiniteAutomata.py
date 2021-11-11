class FiniteAutomata:
    def __init__(self, conf_file):
        self._states = []
        self._alphabet = []
        self._initialStates = []
        self._finalStates = []
        self._transitions = {}

        self._loadData(conf_file)

    def _classifyToken(self, section, probe):
        if section == 'states':
            spec = probe.split(', ')
            self._states.extend(spec)
        elif section == 'alpha':
            spec = probe.split(', ')
            self._alphabet.extend(spec)
        elif section == 'initial':
            spec = probe.split(', ')
            self._initialStates.extend(spec)
        elif section == 'final':
            spec = probe.split(', ')
            self._finalStates.extend(spec)
        elif section == "transitions":
            values = probe.split(", ")

            if (values[0], values[1]) in self._transitions.keys():
                self._transitions[(values[0], values[1])].append(values[2])
            else:
                self._transitions[(values[0], values[1])] = [values[2]]

    def _loadData(self, conf_file):
        with open(conf_file, 'r') as file:
            lines = file.readlines()
            section = ''

            for line in lines:
                line = line.strip()
                if line[0] == '#':
                    section = line[1:]
                else:
                    self._classifyToken(section, line)

    def isDeterministic(self):
        for key in self._transitions.keys():
            if len(self._transitions[key]) > 1:
                return False
        return True

    def isAccepted(self, sequence):
        if self.isDeterministic():
            current = self._initialStates[0]  # initial state is unique

            for symbol in sequence:
                if (current, symbol) in self._transitions.keys():
                    current = self._transitions[(current, symbol)][0]
                else:
                    return False

            return current in self._finalStates
        return False

    def _printMenu(self):
        print("Display data regarding a finite automata")
        print("1: Display the states")
        print("2: Display the alphabet")
        print("3: Display the transitions")
        print("4: Display the final state")
        print("5: Check if given sequence is accepted")
        print("0: Exit")

    def displayData(self):
        while True:
            self._printMenu()
            user_input = input('>').strip()

            if user_input == '1':
                print('The states of the finite automata are: ', self._states)
            elif user_input == '2':
                print('The alphabet of the finite automata is: ', self._alphabet)
            elif user_input == '3':
                print('The transitions of the finite automata are: ', self._transitions)
            elif user_input == '4':
                print('The final state(s) of the finite automata are: ', self._finalStates)
            elif user_input == '5':
                isAccepted = self.isAccepted(input("Sequence: ").strip())
                if isAccepted:
                    print('Accepted')
                else:
                    print('Not accepted')
            elif user_input == '0':
                break
            else:
                print('Wrong command')