#Final Assessment - Nathan Heckman

#Import regex and string matching module
import re             

#Simple Token object. Token type, value, and position
class Token(object):    
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos
        
    #define regulated print format for object
    def __str__(self):  
        return '%s(%s) at %s' % (self.type, self.val, self.pos)

#Define error handling in case no tokens are matched
class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos
        
#Define lexical analysis object
class Lexer(object):
    #Rules is essentially a regex and type pair. Type describes the token defined by the regex
    #Whitespace is skipped so errors can be avoided. Whitespace is also not necessary in Java.
    def __init__(self, rules, skip_whitespace=True):
        self.rules = []
        #add each element to the rules array
        for regex, type in rules:
            self.rules.append((re.compile(regex), type))
        self.skip_whitespace = skip_whitespace
        #Define a regex whitespace
        self.re_ws_skip = re.compile('\S')
    #Initialize lexer with buffer input
    def input(self, buf):
        self.buf = buf
        self.pos = 0
    #Return next token object found in the input. Error handling included
    def token(self):
        #Check for empty input string
        if self.pos >= len(self.buf):
            return None
        #Function to skip the whitespace present in the input string
        if self.skip_whitespace:
            m = self.re_ws_skip.search(self.buf, self.pos)
            if m:
                self.pos = m.start()
            #If only whitespace, return None
            else:
                return None
        #Create tokens for found regex matches in the input string, return the token if found
        for regex, type in self.rules:
            m = regex.match(self.buf, self.pos)
            if m:
                token = Token(type, m.group(), self.pos)
                self.pos = m.end()
                return token
        #If none of the above works, error
        raise LexerError(self.pos)
    def tokens(self):
        #Returns an iterator to the tokens found in the input. Allows token list to be created
        while 1:
            token = self.token()
            if token is None: break
            yield token
            
def increment_token():  #Used program wide to increment the global index and nextToken
    global index
    global nextToken
    global tokens
    index += 1
    nextToken = tokens[index]            
    
def switch_():
    global index                    #Declare global variables
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'switch'):  #Follow the syntax given in Lexer Syntax.txt
        error(tokens[index])        #Error when the token isn't valid
    else:
        increment_token()           #Program wide token incrementing function
        if(nextToken.val != '('):   #Continue for the whole syntax
            error(tokens[index])
        else:
            increment_token()
            if(nextToken.type != 'IDENTIFIER'):
                error(tokens[index])
            else:
                increment_token()
                if(nextToken.val != ')'):
                    error(tokens[index])
                else:
                    increment_token()
                    block()         #Go to block since switch needs one
def foreach():
    global index                    #Declare global variables
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.type != 'IDENTIFIER'): #Foreach spawns off of a normal for loop since both begin the same
        error(tokens[index])
    else:
        increment_token()
        if(nextToken.val != ':'):       #Now following the foreach syntax
            error(tokens[index])
        else:
            increment_token()
            if(nextToken.type != 'IDENTIFIER'):
                error(tokens[index])
            else:
                increment_token()
                if(nextToken.val != ')'):
                    error(tokens[index])
                else:
                    increment_token()
                    block() #Return to block because any loop or statement has one at the end
def for_():
    global index                #Declare global variables
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'for'): #Follow syntax sheet like the other ones
        error(tokens[index])
    else:
        increment_token()
        if(nextToken.val != '('):
            error(tokens[index])
        else:
            increment_token()
            if(nextToken.val == 'type'): #Branch that creates foreach loop
                increment_token()
                foreach()               #Jump to foreach
            else:
                expression()
                if(nextToken.val != ';'):
                    error(tokens[index])
                else:
                    increment_token()
                    expression()
                    if(nextToken.val != ';'):
                        error(tokens[index])
                    else:
                        incrementToken()
                        expression()
                        if(nextToken.val != ')'):
                            error(tokens[index])
                        else:
                            increment_token()
                            block()     #Create body for the for loop
def while_():
    global index                        #Same as before
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'while'):
        error(tokens[index])
    else:
        increment_token()
        if(nextToken.val != '('):
            error(tokens[index])
        else:
            increment_token()
            expression()
            if(nextToken.val != ')'):
                error(tokens[index])
            else:
                increment_token()
                block() #Same as before
def do_while():
    global index                    #Same as before
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'do'):
        error(tokens[index])
    else:
        increment_token()
        block()
        if(nextToken.val != 'while'):
            error(tokens[index])
        else:
            increment_token()
            if(nextToken.val != '('):
                error(tokens[index])
            else:
                increment_token()
                expression()
                if(nextToken.val != ')'):
                    error(tokens[index])
                else:
                    increment_token()
                    if(nextToken.val != ';'):
                        error(tokens[index])
                    else:
                        increment_token()
                        #No block, but program will continue where it left off before the do-while
def if_():
    global index                #Same as before
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'if'):
        error(tokens[index])
    else:
        increment_token()
        if(nextToken.val != '('):
            error(tokens[index])
        else:
            increment_token()
            expression()
            if(nextToken.val != ')'):               #Check for right parenthesis
                error(tokens[index])                #End analysis and error out if not present
            else:
                increment_token()
                block()
                if(nextToken.val == 'else'):            #No error if else isn't present
                    increment_token()
                    block() #Continue analysis
def assignment():
    global index                #Same as above
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.type != 'IDENTIFIER'): #Branches off from expression since they both can begin the same
        error(tokens[index])
    else:
        if(nextToken.val != ';'):
            error(tokens[index])
        else:
            increment_token()
            #No block but program continues where it left off
    print('Assignment Good')
def return_():
    global index            #Same as above
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'return'):  #Return can have an identifier with it or not
        error(tokens[index])
    else:
        if(nextToken.type == 'IDENTIFIER'):
            increment_token()
            if(nextToken.val != ';'):
                error(tokens[index])
        elif(nextToken.val != ';'):
            increment_token()
        else:
            error(tokens[index])
    print('Return Good')
def program():              #Beginning point for the entire analysis
    global index            #Declare global variables to be used throughout program
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != 'void'):
        error(tokens[index])                #Send token object to error message
    else:
        increment_token()
        if(nextToken.val != 'main'):
            error(tokens[index])
        else:
            increment_token()
            if(nextToken.val != '('):
                error(tokens[index])
            else:
                increment_token()
                if(nextToken.val != ')'):
                    error(tokens[index])
                else:
                    increment_token()
                    block()                 #Enter block that entire program will reside in
    print('\nProgram Good')                 #If program makes it back here, syntax analysis was successful
def block():
    global index
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val != '{'):
        error(tokens[index])
    else:
        increment_token()
        if(nextToken.val == '}'):
            increment_token()
        else:
            statement()                     #Block will always have some sort of statement in it (details in the syntax file)
            if(nextToken.val != '}'):
                error(tokens[index])
            else:
                if(nextGood()):             #Check for if the nextToken is within the bounds of the token array
                    increment_token()
def expression():
    global index
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.type == 'IDENTIFIER'):     #This verifies if the tokens need to branch into assignment or not
        t = tokens[index+1]
        if(t.val == '='):
            t = tokens[index+2]
            if(t.type == 'IDENTIFIER'):
                increment_token()
                increment_token()
                increment_token()
                assignment()
    #All the below are detailed in the syntax document
    elif(nextToken.type == 'INTEGER LITERAL' or nextToken.type == 'FLOAT LITERAL' or nextToken.type == 'STRING LITERAL' or nextToken.type =='IDENTIFIER'):
        increment_token()
        if(nextToken.val == '+' or nextToken.val == '-' or nextToken.val == '*' or nextToken.val == '/' or nextToken.val == '<' or nextToken.val == '>'):
            increment_token()
            if(nextToken.type == 'INTEGER LITERAL' or nextToken.type == 'FLOAT LITERAL' or nextToken.type == 'STRING LITERAL' or nextToken.type == 'IDENTIFIER'):
                increment_token()
            else:
                error(tokens[index])
        else:
            error(tokens[index])
    else:
        error(tokens[index])
def statement():
    global index
    global nextToken
    global rules
    global lexer
    global tokens
    if(nextToken.val == 'if'):      #Presents options for all the different kinds of statements that are possible
        if_()
        print('If Good')
        statement()
    elif(nextToken.val == 'while'):
        while_()
        print('While Good')
        statement()
    elif(nextToken.val == 'do'):
        do_while()
        print('Do-While Good')
        statement()
    elif(nextToken.val == 'for'):
        for_()
        print('For Good / For Each Good')
        statement()
    elif(nextToken.val == 'switch'):
        switch_()
        print('Switch Good')
        statement()
    elif(nextToken.val == 'return'):
        return_()
        print('Return Good')
        statement()
    elif(nextToken.val == '{'):
        block()
        print('Block Good')
        statement()
    elif(nextToken.type == 'SINGLE LINE COMMENT'):
        increment_token()
def error(wrong): #Programmatically show where the syntax analysis fails
    print('Invalid syntax (' + str(wrong.val) + ') at position ' + str(wrong.pos))  #Print failure statement with position and token
    exit()
def nextGood(): #verify if the new index will be valid or not
    global index
    global tokens
    if(index < len(tokens)-1):
        return True
    else:
        return False
if __name__=="__main__":                    #Begin the main method
    index = 0                               #Track index throughout analysis
    tokens = []                             #Array to store the computed tokens
    
    #Java defined regex rules. Based on assessment requirements
    rules = [  
    ('//[^\n]*',                          'SINGLE LINE COMMENT'),
    ('(\d*)\.\d+f?',                      'FLOAT LITERAL'),
    ('"[^\n]*"',                          'STRING LITERAL'),
    ('if',                                'IF'),
    ('else',                              'ELSE'),
    ('while',                             'WHILE'),
    ('do',                                'DO'),
    ('switch',                            'SWITCH'),
    ('for',                               'FOR'),
    ('\d+',                               'INTEGER LITERAL'),
    ('[a-zA-Z_]\w*',                      'IDENTIFIER'),
    ('\+\+',                              'INCREMENT'),
    ('\-\-',                              'DECREMENT'),
    ('\+',                                'PLUS'),
    ('\-',                                'MINUS'),
    ('\*',                                'MULTIPLY'),
    ('\/',                                'DIVIDE'),
    ('\(',                                'LEFT PAREN'),
    ('\)',                                'RIGHT PAREN'),
    ('\{',                                'LEFT CURLY'),
    ('\}',                                'RIGHT CURLY'),
    ('\[',                                'LEFT BRACKET'),
    ('\]',                                'RIGHT BRACKET'),
    ('\<',                                'LEFT WEDGE'),
    ('\>',                                'RIGHT WEDGE'),
    ('\,',                                'COMMA'),
    ('\;',                                'SEMICOLON'),
    ('\:',                                'COLON'),
    ('\.',                                'PERIOD'),
    ('\!\=',                              'NOT EQUALS'),
    ('\=',                                'EQUALS'),
    ('.',                                 'UNKNOWN')  #if code gets here, the input is unknown. End analysis
    ]
    
    lexer = Lexer(rules, skip_whitespace=True)   #Create lexer object
    
    #Sample Java Program. Used as a demonstration to show that code structure can be verified
    lexer.input('''
    void main(){
        switch(four){
            //Hello there
        }
        while(5.5 + 10){
            //General Kenobi
        }
        do{
            //Nothing
        } while(5 + 5);
        if(5+5){
            //This is a comment
        }
        for(type x : fourty){
            //Nothing
        }
    }
    ''')
    try:
        for token in lexer.tokens():                    #Add each token to list and print with object format
            tokens.append(token)
            #Tokens is now populated with token objects
    except LexerError as error:
        print('Error at position %s' % error.pos)       #Error checking for invalid or unrecognized token
    nextToken = tokens[index]                           #Start analysis at beginning of token list
    
    for token in tokens:
        print(token)
        
    print()
    program()                                           #Begin program