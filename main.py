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
            
        return code.lower()
            

class tokenizer():
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        while (self.position < len(self.origin)) and (self.origin[self.position] == " "):
            self.position += 1

        if self.position >= len(self.origin):
            self.actual = token("EOF", "EOF")

        elif self.origin[self.position] == "=":
            self.actual = token("EQUAL", "=")
            self.position += 1

        elif self.origin[self.position] == "\n":
            self.actual = token("LBREAK", "\n") #Line Break
            self.position += 1

        elif self.origin[self.position] == ">":
            self.actual = token("BIGGER", ">")
            self.position += 1

        elif self.origin[self.position] == "<":
            self.actual = token("SMALER", "<")
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
        elif self.origin[self.position] == ",":
            self.actual = token("COMMA", ",")
            self.position += 1

        elif self.origin[self.position].isalpha():
            string = ""
            while (self.position < len(self.origin)) and ((self.origin[self.position].isalpha()) or (self.origin[self.position] == "_")):
                string += self.origin[self.position]
                self.position += 1
            if string == "print":
                self.actual = token("PRINT", string)
            elif string == "sub":
                self.actual = token("SUB", string)
            elif string == "end":
                self.actual = token("FIN", string)
            elif string == "wend":
                self.actual = token("WFIN", string)
            elif string == "if":
                self.actual = token("IF", string)
            elif string == "else":
                self.actual = token("ELSE", string)
            elif string == "while":
                self.actual = token("WHILE", string)
            elif string == "and":
                self.actual = token("AND", string)
            elif string == "or":
                self.actual = token("OR", string)
            elif string == "not":
                self.actual = token("NOT", string)
            elif string == "then":
                self.actual = token("THEN", string)
            elif string == "input":
                self.actual = token("INPUT", string)
            elif string == "dim":
                self.actual = token("DIM", string)
            elif string == "as":
                self.actual = token("AS", string)
            elif string == "integer":
                self.actual = token("TYPE", string)
            elif string == "boolean":
                self.actual = token("TYPE", string)
            elif string == "true":
                self.actual = token("TRUE", string)
            elif string == "false":
                self.actual = token("FALSE", string)
            elif string == "function":
                self.actual = token("FUNC", string)
            elif string == "call":
                self.actual = token("CALL", string)
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
        var1=self.children[0].evaluate(table)
        var2=self.children[1].evaluate(table)
        if type(var1) is tuple:#check if var type match
            vtype1 = var1[1]
            var1 = var1[0]
        else:
            vtype1 = type(var1)
            if vtype1 is int:
                vtype1 = 'integer'
            if vtype1 is bool:
                vtype1 = 'boolean'

        if type(var2) is tuple:
            vtype2 = var2[1]
            var2 = var2[0]
        else:
            vtype2 = type(var2)
            if vtype2 is int:
                vtype2 = 'integer'
            if vtype2 is bool:
                vtype2 = 'boolean'

        #if vtype1 != vtype2:
        #     raise Exception("Error - in BinOp, differente var types ",vtype1,vtype2)

        # integerer operetors
        if self.value == "+":
            return var1 + var2
        if self.value == "-":
            return var1 - var2
        if self.value == "*":
            return var1 * var2
        if self.value == "/":
            return var1 / var2
        if self.value == "=":
            return (var1 == var2)
        if self.value == ">":
            return (var1 > var2)
        if self.value == "<":
            return (var1 < var2)
        
        #bolean operators
        if self.value == "or":
                    return (var1 or var2)
        if self.value == "and":
                    return (var1 and var2)
        raise Exception("Error - in Binop, No operation possible (aka something went terible wrong), children: ",self.children," value: ",var1)

class UnOp(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 1: raise Exception("Error - in Unop, UnOp cant have more than one child, children: ",self.children)
    def evaluate(self,table):
        var1=self.children[0].evaluate(table)
        if type(var1) is tuple:#check if var type match
            vtype1 = var1[1]
            var1 = var1[0]
        else:
            vtype1 = type(var1)
            if vtype1 is int:
                vtype1 = 'integer'
            if vtype1 is bool:
                vtype1 = 'boolean'

        if vtype1 == 'integer':
            if self.value == "+":
                return var1
            if self.value == "-":
                return var1 * -1
        if vtype1 == 'boolean':
            if self.value == "not":
                return (not var1)
        raise Exception("Error - in Unop, No operation possible: children: ",self.children," value: ",var1)

class IntVal(Node):
    def __init__(self,value):
        self.value = value
    def evaluate(self,table):
        return self.value

class BoolVal(Node):
    def __init__(self,value):
        self.value = value
    def evaluate(self,table):
        return self.value

class Identifier(Node):
    def __init__(self,value):
        self.value = value
    def evaluate(self,table):
        return table.getter(self.value)

class Node_Input(Node):
    def __init__(self,value):
        self.value = value
    def evaluate(self,table):
        return int(input())

class Assignment(Node):
    def __init__(self,value,list_children):
        self.value = value
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in Node_while, Node_while cant have more than one child, children: ",self.children)
    def evaluate(self,table):
        table.setter(self.children[0].value,self.children[1].evaluate(table))

class Print(Node):
    def __init__(self,list_children):
        self.children = list_children
    def evaluate(self,table):
        var = self.children[0].evaluate(table)
        if type(var) is tuple:
            var = var[0]
        print(var)


class Node_if(Node): 
    def __init__(self,list_children):
        self.children = list_children
    def evaluate(self,table):
        if self.children[0].evaluate(table):
            return self.children[1].evaluate(table)
        elif len(self.children) == 3: # this if contains a else
            return self.children[2].evaluate(table)
        return None

class Node_While(Node):
    def __init__(self,list_children):
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in Node_While, Node_While cant have more than two child, children: ",self.children)
    def evaluate(self,table):
        while self.children[0].evaluate(table):
            self.children[1].evaluate(table)

class VarDec(Node):
    def __init__(self,list_children):
        self.children = list_children
        if len(self.children) != 2: raise Exception("Error - in VarDec, VarDec cant have more(or less) than two children, children: ",self.children)
    def evaluate(self,table):
        table.declare(self.children[0].value,[None,self.children[1].evaluate(table)])

class SubDec(Node):
    def __init__(self,value,list_children):
        self.children = list_children
        self.value = value
    def evaluate(self,table):
        table.declare(self.value,["SUB",[self.children[0],self.children[1]]])
        #for e in self.children:
        #   e.evaluate(table)

class FuncDec(Node):
    def __init__(self,value,list_children):
        self.children = list_children
        self.value = value
    def evaluate(self,table):
        table.declare(self.value,["FUNCTION",[self.children[0],self.children[1]]])

class FuncCall(Node):
    def __init__(self,value,list_children):
        self.children = list_children
        self.value = value
    def evaluate(self,table):
        func = table.getter(self.value)
        new_table = SymbolTable()
        new_table.clone(table)
        order = []
        for i in func[1][0][0:-1]: #put vars in the new table
            order.append(i.children[0].value)
            i.evaluate(new_table)

        for x in range(len(order)): # put list_children values in new_table
            value = self.children[x].evaluate(table)
            if self.children[x].value in table.table: #note: this is probably the worst way to do this
                value = table.getter(value)
            new_table.setter(order[x],value)

        for e in func[1][1]:
            e.evaluate(new_table)
        if func[0] != "SUB":
            return new_table.getter(self.value)

        #need to pass func as variable
class Node_type(Node):
    def __init__(self,value):
        self.value = value
        if value not in {"integer","boolean"}:
            raise Exception("Error - unreconized type: ",self.value)
    def evaluate(self,table):
        return self.value

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []
    def evaluate(self,table):
        return None
    
#-------------End of Nodes----------------

class SymbolTable():
    def __init__(self):
        self.table = {}
        self.reserved_set = {"call","sub","end","print","dim","if","else","then","while","end","wend"}

    def getter(self,key):
        if key in self.table:
            return tuple(self.table[key])
        raise Exception("Error - var: ",key,"was not declared using dim")
    
    def declare(self,key,value):
        if key in self.reserved_set:
            raise Exception("Error - in setter, the value: ",key,"is a reserved key")
        self.table[key] = value

    def setter(self,key,value):
        if key in self.table:
            if type(value) is tuple: value = value[0]
            self.table[key][0] = value
        else:
            raise Exception("Error - var: ",key,"was not declared using dim")
    def clone(self,over_table):
        self.table = over_table.table.copy()


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

        if parser.token.actual.stamp == "TRUE":
            node = BoolVal(True)
            parser.token.selectNext()
            return node

        if parser.token.actual.stamp == "FALSE":
            node = BoolVal(False)
            parser.token.selectNext()
            return node

        if parser.token.actual.stamp == 'ID':
            
            name = parser.token.actual.value
            parser.token.selectNext()

            if parser.token.actual.stamp == "OPEN":
                func_variables = []
                while parser.token.actual.stamp != "CLOSE":
                    parser.token.selectNext()
                    func_variables.append(parser.RelExpression()) 
                parser.token.selectNext()
                return FuncCall(name,func_variables)

            node = Identifier(name)
            return node

        if parser.token.actual.stamp == 'INPUT':
            node = Node_Input(parser.token.actual.value)
            parser.token.selectNext()
            return node


        elif parser.token.actual.stamp == "OPEN":
            parser.token.selectNext()
            result = parser.RelExpression()
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
        if parser.token.actual.value == ">":
            parser.token.selectNext()
            return BinOp(">",[result,parser.parseExpression()])
        if parser.token.actual.value == "<":
            parser.token.selectNext()
            return BinOp("<",[result,parser.parseExpression()])
        return result

    @staticmethod
    def Statement():

        if parser.token.actual.stamp == "ID":
            str_id = parser.token.actual.value
            parser.token.selectNext()
            if parser.token.actual.stamp == "EQUAL":
                parser.token.selectNext()                    
                return Assignment("=",[Identifier(str_id),parser.RelExpression()])
        
        elif parser.token.actual.stamp == "DIM":
            parser.token.selectNext()
            if parser.token.actual.stamp == "ID":
                var = Identifier(parser.token.actual.value)
                parser.token.selectNext()
                if parser.token.actual.stamp == "AS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "TYPE":
                        var_type = parser.token.actual.value
                        parser.token.selectNext()
                        return VarDec([var,Node_type(var_type)])
        
        elif parser.token.actual.stamp == "PRINT":
            parser.token.selectNext()
            return Print([parser.parseExpression()])

        elif parser.token.actual.stamp == "WHILE":
            parser.token.selectNext()
            exp = [parser.RelExpression()]
            if parser.token.actual.stamp != "LBREAK":
                raise Exception("Error - while requires line break after expression, received: ", parser.token.actual.value)


            exp.append(parser.Statment_loop())

            if parser.token.actual.stamp == "WFIN":
                parser.token.selectNext()
                return Node_While(exp)
            raise Exception("Error - while expression did not enconter wend, received: ", parser.token.actual.value)

        elif parser.token.actual.stamp == 'CALL': #sub call
            
            parser.token.selectNext()
            name = parser.token.actual.value
            parser.token.selectNext()

            if parser.token.actual.stamp == "OPEN":
                func_variables = []
                while parser.token.actual.stamp != "CLOSE":
                    parser.token.selectNext()
                    func_variables.append(parser.RelExpression()) 
                parser.token.selectNext()
                return FuncCall(name,func_variables)
            raise Exception("Error - wrong order at call")

        elif parser.token.actual.stamp == "IF":
            parser.token.selectNext()
            exp = [parser.RelExpression()]
            if parser.token.actual.stamp == "THEN":
                parser.token.selectNext()
                if parser.token.actual.stamp != "LBREAK":
                    raise Exception("Error - while requires line break after expression, received: ", parser.token.actual.value)
                parser.token.selectNext()
                exp.append(parser.Statment_loop())

                if parser.token.actual.stamp == "ELSE":
                    parser.token.selectNext()
                    if parser.token.actual.stamp != "LBREAK":
                        raise Exception("Error - while requires line break after expression, received: ", parser.token.actual.value)
                    parser.token.selectNext()
                    exp.append(parser.Statment_loop())

                parser.token.selectNext()

                if parser.token.actual.stamp == "IF":
                    parser.token.selectNext()
                    return Node_if(exp)

                raise Exception("Error - if expression did not enconter if after end, received: ", parser.token.actual.value)
            raise Exception("Error - if expression did not enconter then, received: ", parser.token.actual.value)



        else:
            return NoOp()

    @staticmethod
    def Statment_loop():
        statment_children = []
        statment_children.append(parser.Statement())
        while parser.token.actual.stamp == "LBREAK":
            parser.token.selectNext()
            statment_children.append(parser.Statement())
        return Statements('statements', statment_children)

    @staticmethod
    def Program():
        state_children = []
        has_main = False

        while parser.token.actual.stamp != "EOF":

            if parser.token.actual.stamp == "SUB":
                sub_vars = []
                sub_nodes = []

                for i in ["SUB","ID","OPEN"] : # better than 5 ifs ,"CLOSE","LBREAK"
                    if i == "ID": 
                        sub_name = parser.token.actual.value
                        if parser.token.actual.value == "main":
                            has_main = True
                    if parser.token.actual.stamp != i:
                        raise Exception("Error - wrong order at beginning expected:",i,"received:", parser.token.actual.value)
                    parser.token.selectNext()

                while parser.token.actual.stamp != "CLOSE":
                    if parser.token.actual.stamp == "ID":
                        var = Identifier(parser.token.actual.value)
                        parser.token.selectNext()
                        if parser.token.actual.stamp == "AS":
                            parser.token.selectNext()
                            if parser.token.actual.stamp == "TYPE":
                                var_type = parser.token.actual.value
                                parser.token.selectNext()
                                sub_vars.append(VarDec([var,Node_type(var_type)]))
                                if parser.token.actual.stamp == "COMMA":
                                    parser.token.selectNext()
                                elif parser.token.actual.stamp == "CLOSE":
                                    parser.token.selectNext()
                                    break
                                else:
                                    raise Exception("Error -  expected:","comma","received:", parser.token.actual.value)
                            else:
                                raise Exception("Error -  expected:","type","received:", parser.token.actual.value)
                        else:
                            raise Exception("Error -  expected:","as","received:", parser.token.actual.value)

                if parser.token.actual.stamp == "CLOSE":
                    parser.token.selectNext()
                if parser.token.actual.stamp != "LBREAK":
                    raise Exception("Error - wrong order at middle expected:","LBREAK","received:", parser.token.actual.stamp)

                while parser.token.actual.stamp == "LBREAK":
                    parser.token.selectNext()
                    sub_nodes.append(parser.Statement())

                if  parser.token.actual.stamp == "FIN":
                    parser.token.selectNext()
                    if  parser.token.actual.stamp == "SUB":
                        parser.token.selectNext()
                    else:
                        raise Exception("Error - wrong order at ending expected:","sub","received:", parser.token.actual.value)
                else:
                    raise Exception("Error - wrong order at ending expected:","end","received:", parser.token.actual.value)

                state_children.append(SubDec(sub_name,[sub_vars,sub_nodes]))
                # sub declaration ends here

            if parser.token.actual.stamp == "FUNC":
                func_vars = []
                func_nodes = []

                for i in ["FUNC","ID","OPEN"] : # better than 5 ifs ,"CLOSE","LBREAK"
                    if i == "ID": 
                        func_name = Identifier(parser.token.actual.value)
                    if parser.token.actual.stamp != i:
                        raise Exception("Error - wrong order at beginning expected:",i,"received:", parser.token.actual.value)
                    parser.token.selectNext()

                while parser.token.actual.stamp != "CLOSE":
                    if parser.token.actual.stamp == "ID":
                        var = Identifier(parser.token.actual.value)
                        parser.token.selectNext()
                        if parser.token.actual.stamp == "AS":
                            parser.token.selectNext()
                            if parser.token.actual.stamp == "TYPE":
                                var_type = parser.token.actual.value
                                parser.token.selectNext()
                                func_vars.append(VarDec([var,Node_type(var_type)]))
                                if parser.token.actual.stamp == "COMMA":
                                    parser.token.selectNext()
                                elif parser.token.actual.stamp == "CLOSE":
                                    parser.token.selectNext()
                                    break
                                else:
                                    raise Exception("Error -  expected:","comma","received:", parser.token.actual.value)
                            else:
                                raise Exception("Error -  expected:","type","received:", parser.token.actual.value)
                        else:
                            raise Exception("Error -  expected:","as","received:", parser.token.actual.value)

                if parser.token.actual.stamp == "CLOSE": #temp fix
                    parser.token.selectNext()
                
                if  parser.token.actual.stamp == "AS":
                    parser.token.selectNext()
                    if parser.token.actual.stamp == "TYPE":
                        var_type = parser.token.actual.value
                        parser.token.selectNext()
                        func_vars.append(VarDec([func_name,Node_type(var_type)]))
                    else:
                        raise Exception("Error -  expected:","type","received:", parser.token.actual.value)
                else:
                    raise Exception("Error -  expected:","as","received:", parser.token.actual.value)

                if parser.token.actual.stamp != "LBREAK":
                    raise Exception("Error - wrong order at middle expected:","LBREAK","received:", parser.token.actual.stamp)

                while parser.token.actual.stamp == "LBREAK":
                    parser.token.selectNext()
                    func_nodes.append(parser.Statement())

                if  parser.token.actual.stamp == "FIN":
                    parser.token.selectNext()
                    if  parser.token.actual.stamp == "FUNC":
                        parser.token.selectNext()
                    else:
                        raise Exception("Error - wrong order at ending expected:","FUNC","received:", parser.token.actual.value)
                else:
                    raise Exception("Error - wrong order at ending expected:","end","received:", parser.token.actual.value)

                state_children.append(FuncDec(func_name.value,[func_vars,func_nodes]))
                
                #func dec ends here
            elif parser.token.actual.stamp == "LBREAK":
                parser.token.selectNext()
        if has_main:
            state_children.append(FuncCall("main",[]))
        return Statements('statements', state_children)




    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        parser.token = tokenizer(code)
        parser.token.selectNext()
        ast = parser.Program()
        return ast 

if __name__ == '__main__':
    code = sys.argv[1]
    #code = "code.vbs"
    with open(code, "r") as in_file:
            code = in_file.read()

    code += "\n"
    table = SymbolTable()
    ast = parser.run(code)
    ast.evaluate(table)
