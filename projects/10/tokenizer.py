from os import listdir
from os.path import *
import sys 

class Tokenizer:
    def __init__(self,infile,files = None):
        assert infile != None, 'Please pass a file path to a vm file.'
        self.infile = infile + '.jack'
        self.files = files
        if(isdir(infile)):
            self.outfile = infile + '/'+ basename(infile) + '.xml'
        else: 
            self.outfile = infile.split('.')[0] + '_tokens.xml'
        self.block = False
        self.data = self._get_data() 
        self.keywords = ['class','constructor','function','method','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return','field']
        self.symbols = ['{', '}', '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' , '*' ,'/' , '&' , '|' , '<' , '>' , '=' , '~']
        self.symbols_unique = {'<':'&lt;','>':'&gt;','"':'&quot;','&':'&amp;'} 
        self.tokens = self.tokenizer()

    def get_data(self):
        return self.data
    def get_outfile_name(self):
        return self.outfile
    def _get_data(self):
        '''
        Reads in a file and stores all of the data into the data obj of the assembler  
        '''   
        #what to read each line by line --> clean --> partition by space 
        try: 
            data = [] 
            if(self.files != None):
                for i in self.files:
                    base = basename(self.infile)
                    name = self.infile + '/' + i 
                    file_object = open(name,'r')
                    temp_data = file_object.readlines()
                    file_object.close()
                    for line in range(len(temp_data)):
                        temp_string = self.cleanString(temp_data[line])
                        if(temp_string[0] != ''):
                            data.append(temp_string)
            else:
                file_object = open(self.infile,"r")
                temp_data = file_object.readlines()
                file_object.close()
                #lets clean the data 
                for line in range(len(temp_data)):
                    temp_string = self.cleanString(temp_data[line])
                    if(temp_string != ''):
                        #going to go through each character and build the tokens 
                        temp_line = [] 
                        temp_word = '' 
                        in_string = False
                        for i in temp_string:  
                            if (i is ''): continue 
                            if((i not in ['"','"','.','(',')','{','}',';','[',']',',',' ','-','~']) or in_string):
                                if i is '"':
                                    in_string = False
                                temp_word += i 
                            else: 
                                #we are no longer making a word 
                                if temp_word not in '': 
                                    temp_line.append(temp_word)
                                #clear the word 
                                temp_word = '' 
                                if(i is not ' '):
                                    if ((i is '"') and (not in_string)):
                                        temp_word += '"'
                                        in_string = True
                                    elif ((i is '"') and in_string):
                                        in_string = False
                                    else:  
                                        temp_line.append(i)
                        data.append(temp_line)
                        temp_line = []
                return data
            return data
        except IOError: 
            print("There was an error reading the file or files. Please make sure that your path is correct.")
            return -1
        finally: 
            file_object.close()

    def cleanString(self,string):
        #clean the line 
        string = string.strip()
        #split the line into the data and the comment 
        string = string.partition("//")[0]
        #going to need to get ride of block comments
        if(string.find('/**') != -1):
            #want to make sure that we have entered a block comment we stop appending to data 
            if(string.find('*/') != -1):
                self.block = False
            else: 
                self.block = True 
            return ''
        if(string.find('*/') != -1):
            #we are now leaving the block comment
            self.block = False 
            return ''
        if(self.block):
            return ''
        #if we are not in a block comment we can write     
        #strip the spaces from the end of the string
        string = string.strip(" ")
        string = string.strip("\t")
        #partition line based off of strings and store into an array
        #need to search for function declarations and calls, as well as string constants   
        #string = string.split(" ")
        return string

    def tokenizer(self):
        outstring = ['<tokens>'] 
        # blockComment = False
        for i in self.data: 
            #looping through lines 
            for x in i:
                #looping through objects in the line 
                if(x in self.keywords):
                    string = '<keyword> '
                    string += x 
                    string += ' </keyword>'
                    outstring.append(string)
                elif(x in self.symbols):
                    string = '<symbol> '
                    if(x in ['<','>','"',"&"]):
                        x = self.symbols_unique[x]
                    string += x 
                    string += ' </symbol>'
                    outstring.append(string)
                elif(x.isnumeric()):
                    string = '<integerConstant> '
                    string += x
                    string += ' </integerConstant>'
                    outstring.append(string)
                elif(x.find('"') != -1):
                    x = x.strip('"').strip('\n')
                    string = '<stringConstant> '
                    string += x
                    string += ' </stringConstant>'
                    outstring.append(string)
                else: 
                    string = '<identifier> '
                    string += x
                    string += ' </identifier>'
                    outstring.append(string)
        outstring.append('</tokens>')
        return outstring


    def write_data(self):
        #first get the binary data 
        token_data = self.tokenizer()
        with open(self.outfile,'w') as tokenFile: 
            #write it to the file 
            for binline in token_data:
                tokenFile.write('%s\n' % binline)
        return token_data