def getTokens(fileName):
    tokens = []
    with open(fileName, 'r') as file:
        lines = file.readlines()

        for line in lines:
            tokens.append(line.strip())

    return tokens
