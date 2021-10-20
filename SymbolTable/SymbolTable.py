def hashCode(element):
    characters = list(element)
    hash_code = 0

    for char in characters:
        hash_code += ord(char)

    return hash_code


class SymbolTable:
    def __init__(self, initialCapacity=37):
        self._capacity = initialCapacity
        self._size = 0
        self._table = []
        for i in range(initialCapacity):
            self._table.append([])

    def hashFunction(self, element):
        elementAsString = str(element)
        elementCode = hashCode(elementAsString)
        return elementCode % self._capacity

    def add(self, element):
        position = self.hashFunction(element)

        if element in self._table[position]:
            arrayLengthAtPosition = len(self._table[position])

            for i in range(arrayLengthAtPosition):
                if self._table[position][i] == element:
                    return position, i
            return None

        self._table[position].append(element)
        self._size += 1

        return position, len(self._table[position]) - 1

    def get(self, element):
        position = self.hashFunction(element)

        if len(self._table[position]) == 0:
            return None

        currentChain = self._table[position]
        currentChainLength = len(currentChain)

        for i in range(currentChainLength):
            if currentChain[i] == element:
                return position, i

        return None

    def __str__(self):
        result = ''
        for i in range(self._capacity):
            result = result + str(i) + " : "
            result = result + str(self._table[i])
            result += '\n'
        return result
