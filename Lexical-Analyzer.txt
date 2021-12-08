#Final Assessment - Created by Nathan Heckman

#Import regex and string matching module
import re             

#Define main execution method
def main():
    global_declaration()                         #Declare the global variables
    index = 0                                    #Track index throughout analysis
    tokens = []                                  #Array to store the computed tokens. Add initial program token
    nextToken = tokens[0]                        #Start analysis at beginning of token list
    
    #Java defined regex rules. Based on assessment requirements
    rules = [  
    ('//[^\n]*',                          'SINGLE LINE COMMENT'),
    ('(\d*)\.\d+f?',                      'FLOAT LITERAL'),
    ('"[^\n]*"',                          'STRING LITERAL'),
    ('if{.*}',                            'IF STATEMENT'),
    ('else{.*}',                          'ELSE STATEMENT'),
    ('while{.*}',                         'WHILE LOOP'),
    ('do{.*}',                            'DO STATEMENT'),
    ('switch{.*}',                        'SWITCH STATEMENT'),
    ('for{.*}',                           'FOR LOOP'),
    ('\d+',                               'INTEGER LITERAL'),
    ('[a-zA-Z_]\w*',                      'IDENTIFIER'),
    ('\+\+',                              'INCREMENT'),
    ('\-\-',                              'DECREMENT'),
    ('\+',                                'PLUS'),
    ('\-',                                'MINUS'),
    ('\*',                                'MULTIPLY'),
    ('\/',                                'DIVIDE'),
    ('\(',                                'LEFT PARENTHESIS'),
    ('\)',                                'RIGHT PARENTHESIS'),
    ('\{',                                'LEFT CURLY'),
    ('\}',                                'RIGHT CURLY'),
    ('\[',                                'LEFT BRACKET'),
    ('\]',                                'RIGHT BRACKET'),
    ('<',                                 'LEFT WEDGE'),
    ('>',                                 'LEFT WEDGE'),
    (',',                                 'COMMA'),
    (';',                                 'SEMICOLON'),
    ('\.',                                'PERIOD'),
    ('=',                                 'EQUALS'),
    ('.',                                 'ERROR')  #if code gets here, the input is unknown. End analysis
    ]
    lexer = Lexer(rules, skip_whitespace=True)   #Create lexer object
    
    #run lexical analysis on input string. Below is a simple Java program to test
    lexer.input('''
    
    ''')
    try:
        for token in lexer.tokens():                    #Add each token to list and print with object format
            tokens.append(token.type)
            print(token)
    except LexerError as error:
        print('Error at position %s' % error.pos)       #Error checking for invalid or unrecognized token
    print(tokens)                                       #Print token list
    statement()                                         #Run the analysis after everything is defined

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
def switch_statement():
    x = 0
def foreach_loop
def if_statement():
    if(nextToken != 'IF STATEMENT'):            #Check for if keyword
        error()                                 #End analysis and error out if keyword not present
    else:
        index += 1                              #Increment token index
        nextToken = tokens[index]               #Grab next token
        nextToken, index, tokens = expression(nextToken, index, tokens)    #Run expression check with new information
        if(nextToken != 'RIGHT PARENTHESIS'):   #Check for right parenthesis
            error()                             #End analysis and error out if not present
        else:
            index += 1                          #Increment token index
            nextToken = tokens[index]           #Grab next token
            statement(nextToken, index, tokens) #Run statement check with new information
            if(nextToken == 'ELSE STATEMENT'):  #No error if else isn't present
                index += 1                      #Same as before
                nextToken = tokens[index]
                statement(nextToken, index, tokens) #Continue analysis
def while_loop():
    if(nextToken != 'WHILE LOOP'):
        error()                                 #End analysis and error out
    else:
        index += 1                              #Increment index to check next token
        nextToken = tokens[index]               #Process out next token and grab token after it
        if(nextToken != 'LEFT PARENTHESIS'):
            error()                             #End analysis and error out
        else:
            index += 1                                                          #Process out next token and grab token after it
            nextToken = tokens[index]                                           #Update nextToken
            nextToken, index, tokens = expression(nextToken, index, tokens)     #Run through expression and return needed values
            if(nextToken != 'RIGHT PARENTHESIS'):  #No error if else isn't present
                error()
            else:
                index += 1
                nextToken = tokens[index]
                statement(nextToken, index, tokens)                             #Return to statement when successful and continue analysis
def for_loop():
    if(nextToken != 'FOR LOOP'):
        error()                                 #End analysis and error out
    else:
        index += 1                              #Process out next token and grab token after it
        nextToken = tokens[index]               #Update nextToken
        if(nextToken != 'LEFT PARENTHESIS'):
            error()                             #End analysis and error out
        else:
            index += 1                          #Process out next token and grab token after it
            nextToken = tokens[index]
            nextToken, index, tokens = expression(nextToken, index, tokens)
            if(nextToken != 'SEMICOLON'):       #No error if else isn't present
                error()
            else:
                index += 1
                nextToken = tokens[index]
                nextToken, index, tokens = expression(nextToken, index, tokens)
                if(nextToken != 'SEMICOLON'):
                    error()
                else:
                    index += 1
                    nextToken = tokens[index]
                    nextToken, index, tokens = expression(nextToken, index, tokens)
                    if(nextToken != 'RIGHT PARENTHESIS'):
                        error()
                    else:
                        index += 1
                        nextToken = tokens[index]
                        statement(nextToken, index, tokens)

def expression():       #Question 2 code proof of concept
    if(nextToken != 'IDENTIFIER'):              #Beginning of expression should be some sort of identifier
        error()
    else:
        index += 1
        nextToken = tokens[index]
        #Check for valid operator
        if(nextToken != 'PLUS' and nextToken != 'MINUS' and nextToken != 'MULTIPLY' and nextToken != 'DIVIDE' and nextToken != 'EQUALS'):
            error()
        else:
            index += 1
            nextToken = tokens[index]
            #Check for valid data type
            if(nextToken != 'INTEGER LITERAL' and nextToken != 'FLOAT LITERAL' and nextToken != 'IDENTIFIER' and nextToken != 'STRING LITERAL'):
                error()
            else:
                index += 1
                nextToken = tokens[index]
    return nextToken, index, tokens         #Return values to be able to continue program
def statement():                        #Covers requirements for assignment
    if(nextToken == 'IF STATEMENT'):
        selection_statement(nextToken, index, tokens)
    elif(nextToken == 'WHILE LOOP'):
        while_loop(nextToken, index, tokens)
    elif(nextToken == 'FOR LOOP'):
        for_loop(nextToken, index, tokens)
    else:
        index += 1
        nextToken = tokens[index]
        statement(nextToken, index, tokens)
        
def error(wrong):                           #Programmatically show where the syntax analysis fails
    print('Failure: ' + wrong)              #Print failure statement plus additional information
def global_declaration():
    global index
    global nextToken
    global rules
    global lexer

if __name__=="__main__":                    #Begin the main method
     main()