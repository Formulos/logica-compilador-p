import sys #para debug
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
    def mult_div():
        result = parser.token.actual.value

        forbidden = ("FIN","PLUS","MINUS")
        while parser.token.actual.stamp not in forbidden:



            if parser.token.actual.stamp == "MULTI":
                parser.token.selectNext()
                #here
                if parser.token.actual.stamp == "INT":
                    result *= parser.token.actual.value
                else:
                    raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value)

            elif parser.token.actual.stamp == "DIVI":
                parser.token.selectNext()
                if parser.token.actual.stamp == "INT":
                    result /= parser.token.actual.value
                else:
                    raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value)

            parser.token.selectNext()
        return result

    @staticmethod
    def parseExpresion():
        result = None

        if parser.token.actual.stamp == "INT":
            result = 0
            
            while parser.token.actual.stamp != "FIN":

                
                result += parser.mult_div()

                if parser.token.actual.stamp == "PLUS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "INT":
                        result += parser.mult_div()
                    else:
                        raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value) 

                elif parser.token.actual.stamp == "MINUS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "INT":
                        result -= parser.mult_div()
                    else:
                        raise Exception("Error - Should have been a digit, error token: ", parser.token.actual.value)

                parser.token.selectNext()
        return result

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        return parser.parseExpresion()

if __name__ == '__main__':
    #code = "1-2 '  bla"
    print("Your input: ")

    code = input()
    code +="\n"
    print("result:",parser.run(code))
    #\n