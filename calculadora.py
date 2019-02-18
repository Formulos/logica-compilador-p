class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class tokenizer:
    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = position
        self.actual

    @staticmethod
    def selectNext():
        pass


class parser:
    def __init__(self, tokens):
        self.tokens = tokens
    
    def parseExpresion():
        pass

    def run(code):
        parser.tokens = tokenizer(code)