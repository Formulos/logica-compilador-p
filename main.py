import sys

class token():
    def __init__(self, stamp, value):
        self.stamp = stamp
        self.value = value

class PrePro():

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
            self.actual = token("LBREAK", "\n") #Line Break
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

        elif self.origin[self.position].isalpha():
            string = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isalpha()):
                string += self.origin[self.position]
                self.position += 1
            if string == "print":
                self.actual = token("PRINT", string) # s = special
            elif string == "Begin":
                self.actual = token("BEGIN", string) # s = special
            elif string == "End":
                self.actual = token("FIN", string) # s = special
            elif string == "if":
                self.actual = token("IF", string) # s = special
            elif string == "else":
                self.actual = token("ELSE", string) # s = special
            elif string == "while":
                self.actual = token("WHILE", string) # s = special
            elif string == "and":
                self.actual = token("AND", string) # s = special
            elif string == "or":
                self.actual = token("OR", string) # s = special
            elif string == "not":
                self.actual = token("NOT", string) # s = special
            elif string == "then":
                self.actual = token("THEN", string) # s = special
            else:
                self.actual = token("ID", string)

        elif self.origin[self.position].isdigit():
            number = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()):
                number += self.origin[self.position]
                self.position += 1
            self.actual = token("INT", int(number))

#-------- Nodes -----------

"""This is a abstract class"""
class Node():
    def __init__(self, varient, list_children):
        self.value = varient
        self.children = list_children
    def evaluate(self, table):
        raise Exception("Error - in abstract class, evaluate was not overwriten")

class BinOp(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in BinOp, BinOp needs two children, children: ",self.children)
    def evaluate(self,table):
        if self.value == "+":
            return self.children[0].evaluate(table) + self.children[1].evaluate(table)
        if self.value == "-":
            return self.children[0].evaluate(table) - self.children[1].evaluate(table)
        if self.value == "*":
            return self.children[0].evaluate(table) * self.children[1].evaluate(table)
        if self.value == "/":
            return self.children[0].evaluate(table) / self.children[1].evaluate(table)
        if self.value == "=":
            return (self.children[0].evaluate(table) == self.children[1].evaluate(table))
        if self.value == "or":
                    return (self.children[0].evaluate(table) or self.children[1].evaluate(table))
        if self.value == "and":
                    return (self.children[0].evaluate(table) and self.children[1].evaluate(table))

class UnOp(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 1: raise Exception("Error - in Unop, UnOp cant have more than one child, children: ",self.children)
    def evaluate(self,table):
        if self.value == "+":
            return self.children[0].evaluate(table)
        if self.value == "-":
            return self.children[0].evaluate(table) * -1
        if self.value == "not":
            return (not self.children[0].evaluate(table))

class IntVal(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    def evaluate(self,table):
        return self.value

class Identifier(Node):
    def __init__(self,value):
        self.value = value
    def evaluate(self,table):
        return table.getter(self.value)

class Assignment(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in Assignment, Assignment needs two children, children: ",self.children)
    def evaluate(self,table):
        table.setter(self.children[0].value,self.children[1].evaluate(table))

class Print(Node): # reserved string
    def __init__(self,list_children):
        self.children = list_children
    def evaluate(self,table):
        tmp = self.children[0].evaluate(table)
        print(tmp)

class Node_if(Node): # reserved string
    def __init__(self,list_children):
        self.children = list_children
    def evaluate(self,table):
        if self.children[0].evaluate(table):
            return self.children[1].evaluate(table)
        elif len(self.children) == 3: # this if contains a else
            return self.children[2].evaluate(table)
        return None

class Node_While(Node): # reserved string
    def __init__(self,list_children):
        self.children = list_children
    def evaluate(self,table):
        while self.children[0].evaluate(table):
            self.children[1].evaluate(table)


class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []
    def evaluate(self,table):
        pass
    
#-------------End of Nodes----------------

class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self,key):
        return self.table[key]

    def setter(self,key,value):
        self.table[key] = value

class Statements(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table):
        for e in self.children:
           e.evaluate(table)

class parser:

    @staticmethod
    def factor():
        
        if parser.token.actual.stamp == "PLUS":
            parser.token.selectNext()
            return UnOp("+",[parser.factor()])
            
        if parser.token.actual.stamp == "MINUS":
            parser.token.selectNext()
            return UnOp("-",[parser.factor()])

        if parser.token.actual.stamp == "NOT":
            parser.token.selectNext()
            return UnOp("not",[parser.factor()])


        if parser.token.actual.stamp == "INT":
            node = IntVal(parser.token.actual.value)
            parser.token.selectNext()
            return node

        if parser.token.actual.stamp == 'ID':
            node = Identifier(parser.token.actual.value)
            parser.token.selectNext()
            return node

        elif parser.token.actual.stamp == "OPEN":
            parser.token.selectNext()
            result = parser.parseExpression()
            if parser.token.actual.stamp != "CLOSE":
                raise Exception("Error - Should have been a ), received: ", parser.token.actual.value)
                
            parser.token.selectNext()
            return result
        

    @staticmethod
    def term():
        result = parser.factor()

        while parser.token.actual.stamp in {"MULTI","INT","DIVI","AND"}:
            if parser.token.actual.stamp == "MULTI":
                parser.token.selectNext()
                result = BinOp("*",[result, parser.factor()])
                continue

            elif parser.token.actual.stamp == "DIVI":
                parser.token.selectNext()
                result = BinOp("/",[result, parser.factor()])
                continue

            elif parser.token.actual.stamp == "AND":
                parser.token.selectNext()
                result = BinOp("and",[result,parser.factor()])
                continue

            parser.token.selectNext()
        return result
    

    @staticmethod
    def parseExpression():
        result = parser.term()
        
        while parser.token.actual.stamp in {"PLUS","MINUS","OR"}:

            if parser.token.actual.stamp == "PLUS":
                parser.token.selectNext()
                result = BinOp("+",[result,parser.term()])
                continue

            elif parser.token.actual.stamp == "MINUS":
                parser.token.selectNext()
                result = BinOp("-",[result,parser.term()])
                continue
            
            elif parser.token.actual.stamp == "OR":
                parser.token.selectNext()
                result = BinOp("or",[result,parser.term()])
                continue

            parser.token.selectNext()
        

        return result

    @staticmethod
    def RelExpression():
        result = parser.parseExpression()
        if parser.token.actual.value == "=":
            parser.token.selectNext()
            return BinOp("=",[result,parser.parseExpression()])

    @staticmethod
    def Statement():
        if parser.token.actual.stamp == "BEGIN":
            return parser.Statements()

        elif parser.token.actual.stamp == "ID":
            str_id = parser.token.actual.value
            parser.token.selectNext()
            if parser.token.actual.stamp == "EQUAL":
                parser.token.selectNext()
                return Assignment("=",[Identifier(str_id),parser.parseExpression()])
        
        elif parser.token.actual.stamp == "PRINT":
            parser.token.selectNext()
            return Print([parser.parseExpression()])

        
        elif parser.token.actual.stamp == "IF":
            parser.token.selectNext()
            exp = [parser.RelExpression()]
            if parser.token.actual.stamp == "THEN":
                parser.token.selectNext()
                exp.append(parser.Statements())
                if parser.token.actual.stamp == "ELSE":
                    parser.token.selectNext()
                    exp.append(parser.Statements())

                if parser.token.actual.stamp == "END":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "IF":
                        parser.token.selectNext()
                        return Node_if(exp)

                    raise Exception("Error - if expression did not enconter if after end, received: ", parser.token.actual.value)
                raise Exception("Error - if expression did not enconter end, received: ", parser.token.actual.value)
            raise Exception("Error - if expression did not enconter then, received: ", parser.token.actual.value)



        else:
            return NoOp()


    @staticmethod
    def Statements():
        state_children = []
        if parser.token.actual.stamp == "BEGIN":
            parser.token.selectNext()
            if parser.token.actual.stamp == "LBREAK":
                parser.token.selectNext()
                while parser.token.actual.stamp != "FIN":
                    state_children.append(parser.Statement())

                    if parser.token.actual.stamp != "LBREAK":
                        raise Exception("Error - No line break after expression, received: ", parser.token.actual.value)

                    parser.token.selectNext()
            
            else:
                raise Exception("Error - No line break after Begin, received: ", parser.token.actual.value)


        else:
            raise Exception("Error - Dosent start with Begin, recieved ", parser.token.actual.stamp)

        parser.token.selectNext()
        return Statements('statements', state_children)




    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        ast = parser.Statements()
        return ast 

if __name__ == '__main__':
    #code = sys.argv[1]
    code = "code.vbs"
    with open(code, "r") as in_file:
            code = in_file.read()

    code += "\n"
    table = SymbolTable()
    ast = parser.run(code)
    ast.evaluate(table)
