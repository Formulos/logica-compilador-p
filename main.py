class token():
    def __init__(self, stamp, value):
        self.stamp = stamp
        self.value = value

class PrePro():
    
    @staticmethod
    def filter(code):
        for i in range(len(code)):
            if code[i] == "'":
                start = i
                for j in range(len(code[start:])):
                    if code[j+start] == "\n":
                        code = code[:start] + code[j+start:]
                        return code
        return code
        
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
            
        elif self.origin[self.position] == "*":
            self.actual = token("MULTI", "*")
            self.position += 1

        elif self.origin[self.position] == "/":
            self.actual = token("DIVI", "/")
            self.position += 1

        elif self.origin[self.position] == "(":
            self.actual = token("OPEN", "(")
            self.position += 1

        elif self.origin[self.position] == ")":
            self.actual = token("CLOSE", ")")
            self.position += 1

        elif self.origin[self.position] == " " or self.origin[self.position] == "\n":
            self.position += 1

        elif self.origin[self.position].isdigit():
            number = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                number += self.origin[self.position]
                self.position += 1
            self.actual = token("INT", int(number))
        else:
            raise Exception("Error - Unknow string: ", self.origin[self.position])
            

class parser:

    @staticmethod
    def factor():
        result = parser.token.actual.value
        
        if parser.token.actual.stamp == "PLUS":
            parser.token.selectNext()
            result = parser.factor()
            
        if parser.token.actual.stamp == "MINUS":
            parser.token.selectNext()
            result = parser.factor() * -1

        if parser.token.actual.stamp == "INT":
            return result

        elif parser.token.actual.stamp == "OPEN":
            parser.token.selectNext()
            result = parser.parseExpresion()
            if parser.token.actual.stamp != "CLOSE":
                raise Exception("Error - Should have been a ), received: ", parser.token.actual.value)
            parser.token.selectNext()
            return result
        

    @staticmethod
    def term():
        result = parser.factor()

        while parser.token.actual.stamp in {"MULTI","INT","DIVI"}:

            if parser.token.actual.stamp == "MULTI":
                parser.token.selectNext()
                result *= parser.factor()
                continue

            elif parser.token.actual.stamp == "DIVI":
                parser.token.selectNext()
                result /= parser.factor()
                continue

            parser.token.selectNext()
        return result
    

    @staticmethod
    def parseExpresion():
        result = parser.term()
        
        while parser.token.actual.stamp in {"PLUS","INT","MINUS"}:

            if parser.token.actual.stamp == "PLUS":
                parser.token.selectNext()
                result += parser.term()
                continue

            elif parser.token.actual.stamp == "MINUS":
                parser.token.selectNext()
                result -= parser.term()
                continue

            parser.token.selectNext()
            print(parser.token.actual.stamp)
        return result

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        return parser.parseExpresion()

if __name__ == '__main__':
    code = " -2+4/(1+1)*2*(1+3+--9-9)'  bla"
    print("Your input: ")
    #code = input()
    code +="\n"
    print("result:",parser.run(code))
