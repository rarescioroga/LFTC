from Scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner()

    try:
        _, _, message = scanner.scanProgram("/Users/user/Desktop/Learning Journey/College/Fifth "
                                               "Semester/LFTC/LFTC-mini-language/Scanner/inputFiles/p1.txt")
        # print("st: ", st)
        # print("pif: ", pif)
        print(message)
    except ValueError as ve:
        print(ve)
