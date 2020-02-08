from os import listdir
from os.path import *
import time
import sys 

class CompilationEngine:
    def __init__(self,infile,files = None):
        assert infile != None, 'Please pass a file path to a jack file or directory.'
        self.infile = infile + '_tokens.xml'
        self.files = files
        if(isdir(infile)):
            self.outfile = infile + '/'+ basename(infile) + '_test.xml'
        else: 
            self.outfile = infile.split('.')[0] + '_test.xml'
        self.block = False
        self.data = self._get_data() 
        self.keywords = ['class','constructor','function','method','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
        self.symbols = ['{', '}', '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' , '*' ,'/' , '&amp;' , '|' , '&lt;' , '&gt;' , '=' , '~']
        self.ops = ['+','-','*','/','&amp;','|','&lt;','&gt;','=']
        self.compilation = self.compilation_engine()

    def get_data(self):
        return self.data
    def get_outfile_name(self):
        return self.outfile

    def _get_data(self):
        try: 
            data = [] 
            if(self.files != None):
                # for i in self.files:
                #     base = basename(self.infile)
                #     name = self.infile + '/' + i 
                #     file_object = open(name,'r')
                #     temp_data = file_object.readlines()
                #     file_object.close()
                #     for line in range(len(temp_data)):
                #         temp_string = self.cleanString(temp_data[line])
                #         if(temp_string[0] != ''):
                #             data.append(temp_string)
                pass
            else:
                file_object = open(self.infile,"r")
                data = file_object.readlines()
                file_object.close()
                #lets clean the data 
                for line in range(len(data)):
                    data[line] = self.cleanString(data[line])
            return data
        except IOError: 
            print("There was an error reading the file or files. Please make sure that your path is correct.")
            return -1
        finally: 
            file_object.close()

    def cleanString(self,string):
        #clean the line 
        string = string.strip()
        #strip the spaces from the end of the string
        string = string.strip(" ")
        string = string.strip("\t")
        return string

    def compilation_engine(self):
        outstring = []
        i = 0
        while( i < len(self.data)):
            datum = self.data[i]
            if(datum.find('<keyword>') != -1):
                if(datum.find('class') != -1):
                    outstring.append('<class>')
                    outstring.append(datum)
                    out = self.CompileClass(i+1)
                    outstring.extend(out[0]) 
                    i = out[1]
            i += 1
        
        return outstring

    def CompileClass(self,loc):
        outstring = [] 
        #need to make sure that we are following the grammar 
        if(self.data[loc].find('identifier') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingIdentifier(loc,'xxx (Identifier)',self.data[loc])
        #Check for Symbol 
        if(self.data[loc].find('{') != -1 ):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingSymbol(loc,'Symbol: {',self.data[loc])
        #now going to start writing the classVarDec 
        hasNext = True
        while(hasNext):
            currToken = self.data[loc].split(' ')
            if(currToken[1] == 'field' or currToken[1] == 'static'):
                out = self.CompileClassVarDec(loc)
                outstring.extend(out[0])
                loc = out[1]
            else: 
                hasNext = False
        # print('Finished ClassVarDec ... Moving onto subroutines')
        # print('Data @ ', loc , ' is: ', self.data[loc])
        hasNext = True
        while(hasNext):
            if(self.data[loc].find('}') != -1):
                hasNext = False 
                outstring.append(self.data[loc])
                loc += 1 
            else:
                currToken = self.data[loc].split(' ')
                if(currToken[1] in ['function','method','constructor']):
                    out = self.CompileSubroutineDec(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                else: 
                    raise MissingKeyword(loc,'Expected either } or a method/function declaration', self.data[loc],outstring)
        outstring.append('</class>')
        return (outstring,loc) 

    def CompileClassVarDec(self,loc):
        outstring = ['<classVarDec>'] 
        if(self.data[loc].find('static') != -1 or self.data[loc].find('field') != -1):
            outstring.append(self.data[loc])
            loc += 1 
            #check for identifier or keyword 
            currToken = self.data[loc].split(' ')
            if(currToken[0] in ['<keyword>','<identifier>']):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingIdentifier(loc,'Either a keyword or an identifer',self.data[loc])
            #check for the next things 
            hasNext = True 
            while(hasNext):
                if(self.data[loc].find(';') != -1):
                    outstring.append(self.data[loc])
                    loc += 1  
                    hasNext = False
                else: 
                    outstring.append(self.data[loc])
                    loc += 1 
        outstring.append('</classVarDec>')
        return (outstring,loc)
    
    def CompileSubroutineDec(self,loc):
        outstring = [] 
        if(self.data[loc].find('constructor') != -1  or self.data[loc].find('function') != -1 or self.data[loc].find('method') != -1):
            outstring.append('<subroutineDec>')
            outstring.append(self.data[loc])
            loc += 1 
            if(self.data[loc].find('void') != -1 or self.data[loc].find('identifier') != -1): 
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingType(loc,'(type)',self.data[loc])
            if(self.data[loc].find('identifier') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingIdentifier(loc,'xxx (Identifier)',self.data[loc])
            if(self.data[loc].find('symbol') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingSymbol(loc,'symbol',self.data[loc])

            out = self.CompileParameterList(loc)
            outstring.extend(out[0])
            loc = out[1]

            #symbol 
            if(self.data[loc].find(')') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingSymbol(loc,') (symbol)',self.data[loc],outstring)

            #need to do a subroutine body 
            out = self.CompileSubroutineBody(loc)
            outstring.extend(out[0])
            loc = out[1]

        outstring.append('</subroutineDec>')
        return (outstring,loc)
    
    def CompileParameterList(self,loc):
        outstring = ['<parameterList>']
        hasNext = True
        while hasNext:
            if(self.data[loc].find(')') != -1):
                hasNext = False
            else: 
                currToken = self.data[loc].split(' ')
                if(currToken[0] in ['<keyword>','identifier']):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingType(loc,'xxx (Type)', self.data[loc])

                #check for more 
                if(self.data[loc].find('<identifier>') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingIdentifier(loc,'xxx (Identifier)',self.data[loc])


                if(self.data[loc].find(',') != -1):
                    #has a list 
                    hasNext = True 
                    #write symbol
                    outstring.append(self.data[loc])
                    loc += 1 
                #if we dont have a comma --> we are expecting a close parenthesis --> raise an error? 

        outstring.append('</parameterList>')
        return (outstring,loc)

    def CompileSubroutineBody(self,loc):
        outstring = ['<subroutineBody>'] 
        if(self.data[loc].find('{') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingSymbol(loc,'{ symbol',self.data[loc],outstring)
        hasNext = True 
        while(hasNext):
            if(self.data[loc].find('}') != -1):
                outstring.append(self.data[loc])
                loc += 1 
                hasNext = False
            else: 
                if(self.data[loc].find('var') != -1):
                    #is a varDec 
                    out = self.CompileVarDec(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                else: 
                    #it is now a statement 
                    out = self.CompileStatements(loc)
                    outstring.extend(out[0])
                    loc = out[1]

        outstring.append('</subroutineBody>')
        return (outstring,loc)
        
    def CompileVarDec(self,loc):
        outstring =['<varDec>']
        #var 
        if(self.data[loc].find('var') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingKeyword(loc,'<keyword>let</keyword>',self.data[loc])
        #check for type 
        currToken = self.data[loc].split(' ')
        if(currToken[0] in ['<keyword>','<identifier>']):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingKeyword(loc,'<keyword>let</keyword>',self.data[loc])
        hasVars = True
        while hasVars:
            if(self.data[loc].find(';') != -1):
                outstring.append(self.data[loc])
                loc += 1 
                hasVars = False 
            else: 
                #check for more 
                if(self.data[loc].find(',') != -1):
                    #write symbol
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    #write symbol
                    outstring.append(self.data[loc])
                    loc += 1 
        outstring.append('</varDec>')
        return (outstring,loc)

    def CompileStatements(self,loc):
        outstring =['<statements>']
        hasNext = True 
        while hasNext: 
            if(self.data[loc].find('}') != -1):
                hasNext = False 
            else:
                #not the end of the statements --> lets find the statements   
                currToken = self.data[loc]
                if(currToken.find('let') != -1):
                    #its a let statement 
                    out = self.CompileLet(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                elif(currToken.find('while') != -1):
                    #its a while statement 
                    out = self.CompileWhile(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                elif(currToken.find('do') != -1):
                    out = self.CompileDo(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                elif(currToken.find('return') != -1):
                    out = self.CompileReturn(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                elif(currToken.find('if') != -1):
                    out = self.CompileIf(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                    # loc += 1
                else: 
                    raise UnknownError(self.data[loc],outstring)
        outstring.append('</statements>')
        return (outstring,loc)
    def CompileLet(self,loc):
        outstring = ['<letStatement>']
        #keyword 
        if(self.data[loc].find('let') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingKeyword(loc,'<keyword>let</keyword>',self.data[loc])
        #identifier
        # Note identifiers can have symbols following. 
        if(self.data[loc].find('identifier') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingIdentifier(loc,'<identifier> xxx </idenifier>',self.data[loc])
        #lets check to see if there is an expression before: 
        if(self.data[loc].find('[') != -1):
            # we have an expression 
            outstring.append(self.data[loc])
            loc += 1

            out = self.CompileExpression(loc)
            outstring.extend(out[0])
            loc = out[1]

            if(self.data[loc].find(']') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingSymbol(loc,'<symbol>]</symbol>',self.data[loc])
        # hasNext = True

        #symbol 
        if(self.data[loc].find('=') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingSymbol(loc,'<symbol>=</<symbol>',self.data[loc])

        out = self.CompileExpression(loc)
        outstring.extend(out[0])
        loc = out[1]

        #check for the return statement 
        if(self.data[loc].find(';') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingSymbol(loc,'Symbol: ;',self.data[loc])
        outstring.append('</letStatement>')
        return (outstring,loc)
    
    def CompileIf(self,loc):
        outstring = ['<ifStatement>']
        #keyword 
        if(self.data[loc].find('if') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingKeyword(loc,'Keyword: if',self.data[loc])
        #symbol 
        if(self.data[loc].find('(') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: (',self.data[loc])
        
        #expressions 
        out = self.CompileExpression(loc)
        outstring.extend(out[0])
        loc = out[1] 

        #symbol 
        if(self.data[loc].find(')') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: )',self.data[loc])
        #symbol 
        if(self.data[loc].find('{') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: {',self.data[loc])
        #statements 
        out = self.CompileStatements(loc)
        outstring.extend(out[0])
        loc = out[1]
        #symbol 
        if(self.data[loc].find('}') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: }',self.data[loc])
        #check if there is an else:
        if(self.data[loc].find('else') != -1):
            outstring.append(self.data[loc])
            loc += 1
            #open bracket 
            if(self.data[loc].find('{') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingSymbol(loc,'Symbol: {',self.data[loc])
            #statements 
            out = self.CompileStatements(loc)
            outstring.extend(out[0])
            loc = out[1]
            #closing bracket 
            if(self.data[loc].find('}') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingSymbol(loc,'<symbol>}</symbol>',self.data[loc])
        outstring.append('</ifStatement>')
        return (outstring,loc)

    def CompileWhile(self,loc):
        outstring = ['<whileStatement>'] 
        #check if there is a while statement 
        if(self.data[loc].find('while') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingKeyword(loc,'<keyword>while</keyword>',self.data[loc])
        #check if there is a symbol 
        if(self.data[loc].find('(') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: (',self.data[loc])
        #now lets get the expression 
        out = self.CompileExpression(loc)
        outstring.extend(out[0])
        loc = out[1]
        #check for a closing symbol 
        if(self.data[loc].find(')') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: )',self.data[loc])
        #check for open bracket 
        if(self.data[loc].find('{') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: {',self.data[loc])
        #get statements: 
        out = self.CompileStatements(loc)
        outstring.extend(out[0])
        loc = out[1]
        #check for closing bracket 
        if(self.data[loc].find('}') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingSymbol(loc,'Symbol: }',self.data[loc])
        outstring.append('</whileStatement>')
        return (outstring,loc)


    def CompileDo(self, loc):
        outstring = ['<doStatement>']
        #check for the do statement 
        if(self.data[loc].find('do') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingKeyword(loc,'<keyword>do</keyword>',self.data[loc])
        #check for an action ... this can be done as an identifier 
        if(self.data[loc].find('<identifier>') != -1):
            outstring.append(self.data[loc])
            loc += 1
        else: 
            raise MissingIdentifier(loc,'Identifier: xxx',self.data[loc])

        if(self.data[loc].find('.') != -1):
            outstring.append(self.data[loc])
            loc += 1
            if(self.data[loc].find('identifier') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingIdentifier(loc,'identifer',self.data[loc])
            if(self.data[loc].find('(') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingSymbol(loc,'(',self.data[loc])

            #this will be sent to expression list 
            out = self.CompileExpressionList(loc)
            outstring.extend(out[0])
            loc = out[1]

            if(self.data[loc].find(')') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingSymbol(loc,'Symbol: )',self.data[loc])  
    
        if(self.data[loc].find('(') != -1):
            #we have a subroutinecall 
            outstring.append(self.data[loc])
            loc += 1 
            #we want to send to expression list 
            out = self.CompileExpressionList(loc)
            outstring.extend(out[0])
            loc = out[1]
            #we need to check for a close parenthesis 
            if(self.data[loc].find(')') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingSymbol(loc,') (Symbol)',self.data[loc])

        if(self.data[loc].find(';') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingSymbol(loc,';',self.data[loc])

        outstring.append('</doStatement>')
        return (outstring,loc)

    def CompileReturn(self,loc):
        outstring = ['<returnStatement>']
        #check for return 
        if(self.data[loc].find('return') != -1):
            outstring.append(self.data[loc])
            loc += 1 
        else: 
            raise MissingKeyword(loc,'return',self.data[loc])
        #check to see if it has an expression 

        if(self.data[loc].find(';') == -1):
            #sending to expressions 
            out = self.CompileExpression(loc)
            outstring.extend(out[0])
            loc = out[1]
            if(self.data[loc].find(';') != -1):
                outstring.append(self.data[loc])
                loc += 1 
            else: 
                raise MissingSymbol(loc,'; (symbol)',self.data[loc])
        else:
            outstring.append(self.data[loc])
            loc += 1  

        outstring.append('</returnStatement>')
        return (outstring,loc)

    def CompileExpression(self,loc):
        outstring = ['<expression>'] 
        #we are going to compile a term on command and then continue 
        out = self.CompileTerm(loc)
        outstring.extend(out[0])
        loc = out[1]
        #need to look for term: 
        hasNext = True 
        while hasNext: 
            currToken = self.data[loc].split(' ')
            # print(currToken[1])
            if(self.data[loc].find(')') != -1 or self.data[loc].find(']') != -1 or currToken[1] == ';' and currToken[1] not in self.ops or currToken[1] == ','):
                # print('it thinks we are done')
                hasNext = False
            else: 
                #need to determine whether or not to send it to term or we write the op 
                currToken = self.data[loc].split(' ')
                # print('currToken')
                # print(currToken)
                if(currToken[1] in self.ops and currToken[1] != '('):
                    # print('op')
                    outstring.append(self.data[loc])
                    loc += 1
                else: 
                    # print('term')
                    # the current token is not an operator --> send to term 
                    out = self.CompileTerm(loc)
                    outstring.extend(out[0])
                    loc = out[1]
                    # print('We have exited')
                    # time.sleep(5)
        outstring.append('</expression>')
        return (outstring,loc)

    def CompileTerm(self,loc):
        '''
            Compiles a term in an expression or expressionlist. 
            A term can end with ;,),], or an op term. 
            Precondition: Assumes that pointer is at correct location, and that we are pointing to the start of a term 
            Postcondition: term is compiled, pointer is now located at either ;,),], or an op term or the parent function to handle. 
            returns: compiled term string, current pointer in document array 
        '''
        outstring = ['<term>']
        currToken = self.data[loc].split(' ')
        # print('\t¸currToken: ', currToken)
        #want to check for: integerConstant, stringConstant, keywordConstant, varName, varname'[expression]',subroutinecall,('expression'),'unaryOp term' 
        #integerConstant 
        if(currToken[0] == '<integerConstant>'):
            outstring.append(self.data[loc])
            loc += 1 
        #stringConstant
        elif(currToken[0] == '<stringConstant>'):
            outstring.append(self.data[loc])
            loc += 1
        #keywordConstant  
        elif(currToken[1] in ['false','true','null','this']):
            outstring.append(self.data[loc])
            loc += 1
        #unaryop   
        elif(currToken[1] in ['-','~']):
            outstring.append(self.data[loc])
            loc += 1 

            out = self.CompileTerm(loc)
            outstring.extend(out[0])
            loc = out[1]
        #(expression)
        elif(currToken[1] == '('):
            outstring.append(self.data[loc])
            loc += 1 

            #send to expressionlist 
            out = self.CompileExpression(loc)
            outstring.extend(out[0])
            loc = out[1]

            #check for ) 
            if(self.data[loc].find(')') != -1):
                outstring.append(self.data[loc])
                loc += 1
            else: 
                raise MissingSymbol(loc,') (symbol)',self.data[loc])
        #identifier 
        elif(currToken[0] == '<identifier>'):
            #check varName or varName[]
            nextToken = self.data[loc+1]
            # print('\t nextToken: ', nextToken)
            if(nextToken.find('[') != -1):
                #variable with expression list
                outstring.append(self.data[loc])
                loc += 1 
                #write [ 
                outstring.append(self.data[loc])
                loc += 1 

                #send to expression 
                out = self.CompileExpression(loc)
                outstring.extend(out[0])
                loc = out[1]

                if(self.data[loc].find(']') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else:
                    raise MissingSymbol(loc,'Symbol: ]',self.data[loc])
        
            elif(nextToken.find('(') != -1):
                #subRoutine with an expression/expression list 
                print('here')
                outstring.append(self.data[loc])
                loc += 1 
                #write (
                outstring.append(self.data[loc])
                loc += 1 

                #send to expression list
                out = self.CompileExpressionList(loc)
                outstring.extend(out[0])
                loc = out[1]

                if(self.data[loc].find(')') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else:
                    raise MissingSymbol(loc,'Symbol: )',self.data[loc])

            elif(nextToken.find('.') != -1 and nextToken.find('symbol') != -1):
                #classname or varname is the currToken 
                
                if(self.data[loc].find('<identifier>') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingIdentifier(loc,'Identifier: xxx',self.data[loc])
                #now write the . 
                if(self.data[loc].find('.') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingSymbol(loc,'Symbol: .',self.data[loc])
                #now subroutine name 
                if(self.data[loc].find('<identifier>') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingIdentifier(loc,'Identifier: xxx',self.data[loc])
                #now symbol (
                if(self.data[loc].find('(') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingSymbol(loc,'Symbol: (',self.data[loc])
                #now send to expression list 
                out = self.CompileExpressionList(loc)
                outstring.extend(out[0])
                loc = out[1]
                #check for close symbol 
                if(self.data[loc].find(')') != -1):
                    outstring.append(self.data[loc])
                    loc += 1 
                else: 
                    raise MissingSymbol(loc,"')' (Symbol)",self.data[loc])
            else: 
                #neither varName['expressionList'] or subroutine('expressionlist')
                outstring.append(self.data[loc])
                loc += 1 
            
        outstring.append('</term>')
        return (outstring,loc)

    def CompileExpressionList(self,loc):
        outstring = ['<expressionList>']
        hasNext = True  
        while(hasNext):
            if(self.data[loc].find(')') != -1):
                hasNext = False 
            else: 
                #we should have an expression here 
                out = self.CompileExpression(loc)
                outstring.extend(out[0])
                loc = out[1]
                #we are expecting a ,
                if(self.data[loc].find(',') != -1):
                    outstring.append(self.data[loc])
                    loc += 1
                else: 
                    #check that we dont have another expression 
                    if(self.data[loc].find(')') == -1):
                        raise MissingIdentifier(loc,'xxx (Identifier)', self.data[loc])
                    #if there is not another expression then we can set hasNext to false 
                    hasNext = False 

        outstring.append('</expressionList>')
        return (outstring,loc)

    def CompileSubroutineCall(self,loc):
        outstring = [] 

        return (outstring, loc)
    
    def write_data(self):
        #first get the binary data 
        compilation_data = self.compilation
        with open(self.outfile,'w') as compilationFile: 
            #write it to the file 
            for binline in compilation_data:
                compilationFile.write('%s\n' % binline)
        return compilation_data

class MissingIdentifier(Exception):
    def __init__(self, line, expected, actual,out=None):
        print('You are missing the identifier at line ' + str(line) + '. Expected: ' + expected + '. Got: ' + actual)
        if out: print(out)
class MissingSymbol(Exception):
    def __init__(self, line, expected, actual,out=None):
        print('You are missing a symbol at line ' + str(line) + '. Expected: ' + expected + '. Got: ' + actual)
        if out: print(out)
class MissingType(Exception):
    def __init__(self, line, expected, actual,out=None):
        print('You are missing a type at line ' + str(line) + '. Expected: ' + expected + '. Got: ' + actual)
        if out: print(out)
class MissingKeyword(Exception):
    def __init__(self, line, expected, actual,out = None):
        print('You are missing a keyword at line ' + str(line) + '. Expected: ' + expected + '. Got: ' + actual)
        if out: print(out)
class UnknownError(Exception):
    def __init__(self,got=None,out=None):
        if got: print(got)
        if out: print(out)
