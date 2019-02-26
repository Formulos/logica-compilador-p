class token():
    def __init__(self, stamp, value):
        self.stamp = stamp
        self.value = value


class tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = token("FIN", "FIN")

    def selectNext(self):
        while (self.position < len(self.origin)) and self.origin[self.position] == " ":
            self.position += 1

        if self.position >= len(self.origin):
            self.actual = token("FIN", "FIN")

        elif self.origin[self.position] == "+":
            self.actual = token("PLUS", "+")
            self.position += 1

        elif self.origin[self.position] == "-":
            self.actual = token("MINUS", "-")
            self.position += 1

        elif self.origin[self.position] == " ":
            self.position += 1

        elif self.origin[self.position].isdigit():
            number = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                number += self.origin[self.position]
                self.position += 1
            self.actual = token("INT", int(number))


        


class parser:

    @staticmethod
    def parseExpresion():
        result = None

        if parser.token.actual.stamp == "INT":
            
            result = parser.token.actual.value
            while parser.token.actual.stamp != "FIN":



                if parser.token.actual.stamp == "PLUS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "INT":
                        result += parser.token.actual.value
                    else:
                        raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value)

                elif parser.token.actual.stamp == "MINUS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "INT":
                        result -= parser.token.actual.value
                    else:
                        raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value)

                parser.token.selectNext()
        return result

    @staticmethod
    def run(code):
        parser.token = tokenizer(code)
        parser.token.selectNext()
        return parser.parseExpresion()

if __name__ == '__main__':
    print("Your input: ")

    code = input()
    print("result:",parser.run(code))