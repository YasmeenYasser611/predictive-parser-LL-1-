from tokenizer import Operator, Tokenizer
from ParserError import ParserError
import networkx as nx

'''
CFG:

stmts→ stmt  stmts | ε
stmt → assign_stmt | while_stmt|if_else_stmt|{stmts}
assign_stmt → id = exp ;
while_stmt → while ( cond ) { stmts } 
if_else_stmt → if ( cond ) stmt  opt_stmt
opt_stmt → else stmt | ε 
cond → id op exp 
op→> | < | >= | <= | =|……. 
exp → term R 
R → + term R | - term R | ε 
term→ factor R1 
R1 → * factor R1 | / factor R1 | ε 
factor → id | digits | ( exp ) 
digits → digit digits | ε
id → a|……|z|A|……|Z
digit → 0|1|…..|9

'''

class Parser:
    def __init__(self, token_iter):
        '''Parser.
        Args:
            token_iter: token iterator returned by Tokenizer.
        '''
        self.tokenss = token_iter
        self.current_token = next(self.tokenss)
        print(self.current_token)
        #self.current_token = None
        self.parse_tree = nx.DiGraph()
        self.node_counter = 0
        #self.forward()

    def forward(self,text):
        '''Set current token by next(token_iter). '''

        if self.current_token.name == text:
            self.current_token = next(self.tokenss)
            print(self.current_token)

        else:
            self.error(self.current_token.name)

    def error(self,token):
        #Trigger by unexpected input. 
        raise ParserError(token=token, message="Invalid token encountered")
        #print ("invalid syntax")
        #print (self.current_token)
    
    def get_parse_tree(self):
        return self.parse_tree

    def add_node(self, label):
        node_id = str(self.node_counter)
        self.parse_tree.add_node(node_id, label=label)
        self.node_counter += 1
        return node_id
    
    def add_edge(self, source, target):
        self.parse_tree.add_edge(source, target)
    
    def parse(self):
        node_id = self.add_node("stmts")
        self.stmts(node_id)

    def stmts(self,parent_id):

        if (self.current_token.name == Tokenizer.identifier.name or
            self.current_token.name == Tokenizer.while_word.name or
            self.current_token.name == Tokenizer.if_word.name or 
            self.current_token.name == Operator.left_curly.name):

            #print("good")
            stmt_node = self.add_node("stmt")
            self.add_edge(parent_id, stmt_node)
            stmts_node = self.add_node("stmts")
            self.add_edge(parent_id, stmts_node)
            self.stmt(stmt_node)  #call stmt function to get what kind of statments
            self.stmts(stmts_node)
        else:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return

    def stmt(self,parent_id):

        if self.current_token.name == Tokenizer.identifier.name:

            assign_node= self.add_node("assign")
            self.add_edge(parent_id, assign_node)
            self.assign_stmt(assign_node)     #call assignment function

        elif self.current_token.name == Tokenizer.while_word.name:
            while_node = self.add_node("While_stmt")
            self.add_edge(parent_id, while_node)
            self.while_stmt(while_node)      #call while statment function

        elif self.current_token.name == Tokenizer.if_word.name:
            IF_node = self.add_node("IF_stmt")
            self.add_edge(parent_id, IF_node)
            self.if_else_stmt(IF_node)    #call if else statment function

        elif self.current_token.name == Operator.left_curly.name:  
            #it's mean that two statment compiled with each other 
            self.forward(Operator.left_curly.name)          #match('{')  to get next token iteration
            left_curly = self.add_node("{")
            self.add_edge(parent_id,left_curly)

            stmts_node = self.add_node("stmts")
            self.add_edge(parent_id,stmts_node)
            self.stmts(stmts_node)                  # identify what kind of the statment

            self.forward(Operator.right_curly.name)       #match (})  after that match the other curly and get the next token
            right_curly = self.add_node("}")
            self.add_edge(parent_id,right_curly)

        else:
            print ("Error in stmt function")
            self.error(self.current_token.name)

        
    def assign_stmt(self,parent_id):
        ID_value = self.add_node(self.current_token.value)
        if self.current_token.name == Tokenizer.identifier.name:
            self.forward(Tokenizer.identifier.name)             #match('id')
            ID_node = self.add_node("ID")
            self.add_edge(parent_id,ID_node)
            self.add_edge(ID_node,ID_value)

            self.forward(Operator.equal.name)             #match ('=')
            equal_node = self.add_node("=")
            self.add_edge(parent_id,equal_node)

            exp_node = self.add_node("exp")
            self.add_edge(parent_id,exp_node)
            self.exp(exp_node)

            self.forward(Tokenizer.semi_coloumn.name)              #match (;)
            semi = self.add_node(";")
            self.add_edge(parent_id,semi)
        else:
            print ("Error in assign_stmt function")
            self.error(self.current_token.name)

    def while_stmt(self,parent_id):
        if self.current_token.name == Tokenizer.while_word.name :
            self.forward(Tokenizer.while_word.name)     #match (while)
            while_word = self.add_node("while")
            self.add_edge(parent_id,while_word)

            self.forward(Operator.left_paren.name)     #match (()
            left_paren = self.add_node("(")
            self.add_edge(parent_id,left_paren)

            cond_stmt = self.add_node("cond")
            self.add_edge(parent_id,cond_stmt)
            self.cond(cond_stmt)
             
            self.forward(Operator.right_paren.name)     #match ())
            right_paren = self.add_node(")")
            self.add_edge(parent_id,right_paren)

            self.forward(Operator.left_curly.name)     #match ({)
            left_curly = self.add_node("{")
            self.add_edge(parent_id,left_curly)

            stmts_node= self.add_node("stmts")
            self.add_edge(parent_id,stmts_node)
            self.stmts(stmts_node)

            self.forward(Operator.right_curly.name)       #match (})
            right_curly = self.add_node("}")
            self.add_edge(parent_id,right_curly)
        else:
            print ("Error in while_stmt function")
            self.error(self.current_token.name)

    def if_else_stmt(self,parent_id):
        if self.current_token.name == Tokenizer.if_word.name:

            if_word = self.add_node("if")
            self.add_edge(parent_id,if_word)
            self.forward(Tokenizer.if_word.name)        #match(if)

            left_paren = self.add_node("(")
            self.add_edge(parent_id,left_paren)
            self.forward(Operator.left_paren.name)        #match ('(')

            cond_stmt = self.add_node("cond")
            self.add_edge(parent_id,cond_stmt)
            self.cond(cond_stmt)

            right_paren = self.add_node(")")
            self.add_edge(parent_id,right_paren)
            self.forward(Operator.right_paren._name_)       #match (')')

            stmt_node = self.add_node("stmt")
            self.add_edge(parent_id,stmt_node)
            opt_stmt_node = self.add_node("opt_stmt")
            self.add_edge(parent_id,opt_stmt_node)

            self.stmt(stmt_node)
            self.opt_stmt(opt_stmt_node)
        else:
            print ("Error in if_stmt function")
            self.error(self.current_token.name)

    def opt_stmt(self,parent_id):

        if self.current_token.name == Tokenizer.else_word.name:
            self.forward(Tokenizer.else_word.name)          #match (else)
            else_node = self.add_node("else")
            self.add_edge(parent_id,else_node)

            stmt_node = self.add_node("stmt")
            self.add_edge(parent_id,stmt_node)
            self.stmt(stmt_node)
        else:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return
        
    def cond(self,parent_id):
        Id_val = self.add_node(self.current_token.value)

        if self.current_token.name == Tokenizer.identifier.name:
            self.forward(Tokenizer.identifier.name)        #match ('id')
            node_ID = self.add_node("ID")
            self.add_edge(parent_id,node_ID)
            
            self.add_edge(node_ID,Id_val)

            Operator_node = self.add_node("OP")
            self.add_edge(parent_id,Operator_node)
            self.OP(Operator_node)

            Exp_node = self.add_node("exp")
            self.add_edge(parent_id,Exp_node)
            self.exp(Exp_node)
        else:
            print ("Error in cond function")
            self.error(self.current_token.name)

    def OP(self,parent_id):
        if  self.current_token.name == Operator.less_equal.name:
            self.forward(Operator.less_equal.name)         #match (relation)
            less_equal = self.add_node(Operator.less_equal.value)
            self.add_edge(parent_id,less_equal)

        elif self.current_token.name == Operator.greater_equal.name:
            self.forward(Operator.greater_equal.name)
            greater_equal = self.add_node(Operator.greater_equal.value)
            self.add_edge(parent_id,greater_equal)

        elif self.current_token.name == Operator.not_equal.name:
            self.forward(Operator.not_equal.name) 
            not_equal = self.add_node(Operator.not_equal.value)
            self.add_edge(parent_id,not_equal)

        elif self.current_token.name == Operator.equal.name :
            self.forward(Operator.equal.name) 
            equal = self.add_node(Operator.equal.value)
            self.add_edge(parent_id,equal)

        elif self.current_token.name == Operator.less_than.name:
            self.forward(Operator.less_than.name) 
            less_than = self.add_node(Operator.less_than.value)
            self.add_edge(parent_id,less_than)

        elif self.current_token.name == Operator.greater_than.name:
            self.forward(Operator.greater_than.name) 
            greater_than = self.add_node(Operator.greater_than.value)
            self.add_edge(parent_id,greater_than)

        else:
            print ("Error in OP function")
            self.error(self.current_token.name)

    def exp(self,parent_id):

        if (self.current_token.name == Tokenizer.identifier.name or 
            self.current_token.name == Tokenizer.number.name or
            self.current_token.name == Operator.left_paren.name):
            term_node = self.add_node("term")
            self.add_edge(parent_id,term_node)
            self.term(term_node)

            Rest_node = self.add_node("Rest")
            self.add_edge(parent_id,Rest_node)
            self.Rest(Rest_node)
        else:
            print ("Error in exp function")
            self.error(self.current_token.name)

    def Rest(self,parent_id):

        if self.current_token.name == Operator.plus.name:
            self.forward(Operator.plus.name)     #match(+)
            plus_node = self.add_node("+")
            self.add_edge(parent_id,plus_node)

            term_node = self.add_node("term")
            self.add_edge(parent_id,term_node)
            self.term(term_node)

            Rest_node = self.add_node("Rest")
            self.add_edge(parent_id,Rest_node)
            self.Rest(Rest_node)

        elif self.current_token.name == Operator.minus.name:
            self.forward(Operator.minus.name)     #match(-)
            minus_node = self.add_node("-")
            self.add_edge(parent_id,minus_node)

            term_node = self.add_node("term")
            self.add_edge(parent_id,term_node)
            self.term(term_node)

            Rest_node = self.add_node("Rest")
            self.add_edge(parent_id,Rest_node)
            self.Rest(Rest_node)
        else:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return
        
    def term(self,parent_id):

        if (self.current_token.name == Tokenizer.identifier.name or
            self.current_token.name == Tokenizer.number.name or 
            self.current_token.name == Operator.left_paren.name):

            factor_node = self.add_node("factor")
            self.add_edge(parent_id,factor_node)
            self.factor(factor_node)

            Rest1_node = self.add_node("Rest1")
            self.add_edge(parent_id,Rest1_node)
            self.Rest1(Rest1_node)
        else:
            print ("Error in term function")
            self.error(self.current_token.name)


    def Rest1(self,parent_id):

        if self.current_token.name == Operator.multiply.name:
            self.forward(Operator.multiply.name)     #match(*)
            multiply_node = self.add_node("*")
            self.add_edge(parent_id,multiply_node)

            factor_node = self.add_node("factor")
            self.add_edge(parent_id,factor_node)
            self.factor(factor_node)

            Rest1_node = self.add_node("Rest1")
            self.add_edge(parent_id,Rest1_node)
            self.Rest1(Rest1_node)

        elif self.current_token.name == Operator.divide.name:
            self.forward(Operator.divide.name)     #match(/)
            divide_node = self.add_node("/")
            self.add_edge(parent_id,divide_node)

            factor_node = self.add_node("factor")
            self.add_edge(parent_id,factor_node)
            self.factor(factor_node)

            Rest1_node = self.add_node("Rest1")
            self.add_edge(parent_id,Rest1_node)
            self.Rest1(Rest1_node)

        else:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return
        

    def factor(self,parent_id):
        Id_val = self.add_node(self.current_token.value)
        if self.current_token.name == Tokenizer.identifier.name:
            self.forward(Tokenizer.identifier.name)   #match(id)
            node_ID = self.add_node("ID")
            self.add_edge(parent_id,node_ID)
            self.add_edge(parent_id,Id_val)

        elif self.current_token.name == Tokenizer.number.name:

            digits_node= self.add_node("digits")
            self.add_edge(parent_id,digits_node)
            self.digits(digits_node)

        elif self.current_token.name == Operator.left_paren.name:

            self.forward(Operator.left_paren.name)         #match ('(')
            left_paren = self.add_node("(")
            self.add_edge(parent_id,left_paren)

            exp_stmt = self.add_node("exp")
            self.add_edge(parent_id,exp_stmt)
            self.exp(exp_stmt)

            self.forward(Operator.right_paren._name_)       #match (')')
            right_paren = self.add_node(")")
            self.add_edge(parent_id,right_paren)
        else:
            print ("Error in factor function")
            self.error(self.current_token.name)

    def digits(self,parent_id):

        if self.current_token.name != Tokenizer.number.name:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return
        else:
            digit_node = self.add_node("digit")
            self.add_edge(parent_id,digit_node)

            digit_val = self.add_node(self.current_token.value)
            self.add_edge(digit_node,digit_val)
            self.forward(Tokenizer.number.name)           #match (digit)

            digits_node= self.add_node("digits")
            self.add_edge(parent_id,digits_node)
            self.digits(digits_node)

        '''
        if self.current_token.name == Tokenizer.number.name:
            self.forward(Tokenizer.number.name)           #match (digit)

            digits_node= self.add_node("digits")
            self.add_edge(parent_id,digits_node)
            self.digits(digits_node)
        else:
            node_empty=self.add_node("E")
            self.add_edge(parent_id, node_empty)
            return'''