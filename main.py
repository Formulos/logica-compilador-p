import sys

class token():
    def __init__(self, stamp, value):
        self.stamp = stamp
        self.value = value

class PrePro():
    
    @staticmethod
    def filter3(code):
        code = code.replace('\\n', '\n')
        size = len(code)
        for i in range(size):
            if code[i] == "'":
                start = i
                for j in range(len(code[start:])):
                    if code[j+start] == "\n":
                        code = code[:start] + code[j+start:]
                        return code
        return code

    @staticmethod
    def filter(code):
        code = code.replace('\\n', '\n')
        size = len(code)
        i = 0
        c_start = None #start of coment
        in_coment = False
        while i < (size):
            if code[i] == "'" and in_coment == False:
                c_start = i
                in_coment = True
            
            if code[i] == "\n" and in_coment == True:
                code = code[:c_start] + code[i+1:]
                size = len(code)
                i = 0
                in_coment = False
            i+= 1
            
        return code
            

class tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = token("FIN", "FIN")

    def selectNext(self):
        while (self.position < len(self.origin)) and (self.origin[self.position] == " "):
            self.position += 1

        if self.origin[self.position] == "=":
            self.actual = token("EQUAL", "=")
            self.position += 1

        elif self.origin[self.position] == "\n":
            self.actual = token("LBREAK", "n") #Line Break
            self.position += 1

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

        elif self.origin[self.position].isalpha():
            string = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isalpha()):
                string += self.origin[self.position]
                self.position += 1
            if string == "print":
                self.actual = token("S_STR", string) # s = special
            elif string == "Begin":
                self.actual = token("BEGIN", string) # s = special
            elif string == "End":
                self.actual = token("FIN", string) # s = special
            else:
                self.actual = token("ID", string)

        elif self.origin[self.position].isdigit():
            number = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                number += self.origin[self.position]
                self.position += 1
            self.actual = token("INT", int(number))

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

class VarStr(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    def evaluate(self,table):
        return table.getter(self.value)

class Assigmen(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in BinOp, BinOp needs two children, children: ",self.children)
    def evaluate(self,table):
        var_key = self.children[0].value
        table.setter(var_key,self.children[1].evaluate())

class Print(Node): # reserved string
    def __init__(self,value):
        self.value = value
        self.children = []
    def evaluate(self,table):
        print(self.children[0].evaluate())

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []
    def evaluate(self):
        pass
    
class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self,key):
        return self.table[key]

    def setter(self,key,value):
        self.table[key] = value

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

            elif parser.token.actual.stamp == "DIVI":
                parser.token.selectNext()
                result = BinOp("/",[result, parser.factor()])
                continue

            parser.token.selectNext()
        return result
    

    @staticmethod
    def parseExpresion():
        parser.token.actual.stamp == "PLUS"
        
        while parser.token.actual.stamp in {"PLUS","MINUS"}:

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
    def Statement():
        if parser.token.actual.stamp == "BEGIN":
            pass

        elif parser.token.actual.stamp == "ID":
            parser.token.selectNext()
            if parser.token.actual.stamp == "EQUAL":
                parser.token.selectNext()
                parser.parseExpresion()


    @staticmethod
    def Statements():
        if parser.token.actual.stamp == "BEGIN":
            parser.token.selectNext()
            if parser.token.actual.stamp == "LBREAK":
                parser.token.selectNext()
                while parser.token.actual.stamp != "FIN":
                    parser.Statement()

        else:
            raise Exception("Error - Dosent start with Begin, recived ", parser.token.actual.stamp)


    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        print(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        ast = parser.Statements()
        if parser.token.actual.stamp != "FIN":
            raise Exception("Error - ast finished without flag FIN, flag returned: ", parser.token.actual.value)
        return ast 

if __name__ == '__main__':
    #sys.argv[1]
    with open("code.vbs", "r") as in_file:
            code = in_file.read()

    code += "\n"

    print("result:",parser.run(code).evaluate())
