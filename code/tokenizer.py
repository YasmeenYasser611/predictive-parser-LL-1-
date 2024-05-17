import re
from enum import Enum

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        res = 'Token({}, {})'.format(
            self.name, repr(self.value))
        return res
    def __repr__(self):
        return self.__str__()
    def is_identifier(self):
        return self.name == Tokenizer.identifier.name
    def is_number(self):
        return self.name == Tokenizer.number.name
    def is_operator(self):
        return hasattr(Operator, self.name)
    def is_new_line(self):
        return self.name == Tokenizer.new_line.name
    def is_eof(self):
        return self.name == Tokenizer.eof.name

class Operator(Enum):
    # 2 characters
    power = '**'
    less_equal = '<='
    greater_equal = '>='
    not_equal = '!='
    quest_equal = '=='
    # 1 character
    plus = '+'
    minus = '-'
    multiply = '*'
    divide = '/'
    equal = '='
    less_than = '<'
    greater_than = '>'
    left_curly = '{'
    left_paren = '('
    left_square = '['
    right_curly = '}'
    right_paren = ')'
    right_square = ']'
    comma = ','
    #semi_coloumn = ';'

class Tokenizer(Enum):
    #if_else_tsmt = r'if\s*\(.+?\)\s*{.+?}\s*(?:else\s*{.+?})?'
    #while_stmt = r'while\s*\(.+?\)\s*{.+?}'
    #assignment_stmt = r'[a-zA-Z_][a-zA-Z_0-9]*\s*=\s*.+?;'
    if_word = r'if\b'
    while_word = r'while\b'
    else_word = r'else\b'
    comment = r'#[^\r\n]*'
    space = r'[ \t]+'
    identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'
    #number = r'[0-9]+(?:\.[0-9]*)?'
    number = r'[0-9]'
    operator = r'\*\*|[<>!]=|[-+*/=<>()[\]{},]'
    new_line = r'[\r\n]'
    eof = r'$'
    semi_coloumn= r';'
    error = r'(.+?)'
    #semi_cloumn = ';'

    @classmethod
    def _build_pattern(cls):
        cls.names = [x.name for x in cls]
        cls.regex = '|'.join('({})'.format(x.value) for x in cls)
        cls.pattern = re.compile(cls.regex)
    @classmethod
    def token_iter(cls, text):
        ''' text to token iter.
        Args:
            text: string for tokenization.
        Returns:
            Iteration object of generated tokens.
        '''
        for match in cls.pattern.finditer(text):
            name = cls.names[match.lastindex-1]
            # skip space and comment
            if (name == cls.space.name
                or name == cls.comment.name
                or name == cls.new_line.name):
                continue
            # raise error
            elif name == cls.error.name:
                print(text[match.start():])
                raise Exception('Invalid Syntax.')
            value = match.group()
            # operator name
            if name == cls.operator.name:
                name = Operator(value).name
            token = Token(name, value)
            yield token
Tokenizer._build_pattern()
#print (Operator.divide.name)