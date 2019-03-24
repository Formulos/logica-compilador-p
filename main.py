
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
            
def funcname(self, parameter_list):
    raise NotImplementedError

"""This is a abstract class"""
class Node():
    def __init__(self, varient, list_children):
        self.value = varient
        self.children = list_children
    def evaluate(self, varient):
        raise Exception("Error - in abstract class, evaluate was not overwriten")

class BinOp(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in BinOp, BinOp needs two children, children: ",self.children)
    def evaluate(self):
        print(self.value)
        print(self.children)
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "/":
            return self.children[0].evaluate() / self.children[1].evaluate()

class UnOp(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 1: raise Exception("Error - in Unop, UnOp cant have more than one child, children: ",self.children)
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() * -1

class IntVal(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []
    def evaluate(self):
        pass
    

        

class parser:

    @staticmethod
    def factor():
        
        if parser.token.actual.stamp == "PLUS":
            parser.token.selectNext()
            return UnOp("+",[parser.factor()])
            
        if parser.token.actual.stamp == "MINUS":
            parser.token.selectNext()
            return UnOp("-",[parser.factor()])

        if parser.token.actual.stamp == "INT":
            return IntVal(parser.token.actual.value)

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
                result = BinOp("*",[result, parser.factor()])
                continue

            elif parser.token.actual.stamp == "DIVI": # error wrong children order
                parser.token.selectNext()
                result = BinOp("/",[result, parser.factor()])
                continue

            parser.token.selectNext()
        return result
    

    @staticmethod
    def parseExpresion():
        result = parser.term()
        
        while parser.token.actual.stamp in {"PLUS","INT","MINUS"}:

            if parser.token.actual.stamp == "PLUS":
                parser.token.selectNext()
                result = BinOp("+",[result,parser.term()])
                continue

            elif parser.token.actual.stamp == "MINUS":
                parser.token.selectNext()
                result = BinOp("-",[result,parser.term()])
                continue

            parser.token.selectNext()
        return result

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        return parser.parseExpresion().evaluate()

if __name__ == '__main__':
    code = " 4/(1+1)*2"
    #print("Your input: ")
    #a = BinOp("+",[IntVal(1),IntVal(1)])
    #print(a.evaluate(1))
    #code = str(input())
    code +="\n"
    print("result:",parser.run(code))
