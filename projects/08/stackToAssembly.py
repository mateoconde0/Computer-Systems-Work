from os import listdir
from os.path import *
from stack import Stack
import sys 

class vmToHack():
    def __init__(self,infile,files = None):
        assert infile != None, 'Please pass a file path to a vm file.'
        self.infile = infile
        self.files = files
        if(isdir(infile)):
            self.outfile = infile + '/'+ basename(infile) + '.asm'
        else: 
            self.outfile = infile.split('.')[0] + '.asm'
        self.data = self.__get_data()
        self.count = 0 
        self.commands = {'StoreD':'@SP\nA=M\nM=D\n','IncSP':'@SP\nM=M+1','End':'(END)\n@END\n0;JMP\n','uncondJMP':'0;JMP\n','GetSP':'@SP\nA=M\n'}
        self.functionDirectory = Stack()
        self.functionIndexes = {}
        self.currentFunction = ('',0)
        self.counter = 0 
        self.j = 0 

    def get_data(self):
        return self.data
    def get_outfile_name(self):
        return self.outfile
    def __get_data(self):
        '''
        Reads in a file and stores all of the data into the data obj of the assembler  
        '''    
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
                    if(temp_string[0] != ''):
                        data.append(temp_string)
                return data
            return data
        except IOError: 
            print("There was an error reading the file or files. Please make sure that your path is correct.")
            return -1
        
    def write_data(self):
        #first get the binary data 
        hack_data = self.vmCompiler()
        with open(self.outfile,'w') as hackFile: 
            #write it to the file 
            for binline in hack_data:
                hackFile.write('%s\n' % binline)
        return hack_data

    def cleanString(self,string):
        #clean the line 
        string = string.strip()
        #split the line into the data and the comment 
        string = string.partition("//")[0]
        #strip the spaces from the end of the string
        string = string.strip(" ")
        string = string.strip("\t")
        #partition line based off of strings and store into an array  
        string = string.split(" ")
        return string
        
    def vmCompiler(self):
        outstring = []
        for i in self.data:
            if(i[0] == 'push'):
                outstring.append(self.push(i[1],value=i[2]))
            elif(i[0] == 'pop'):
                outstring.append(self.pop(i[1],value=i[2]))
            elif(i[0] == 'add'):
                outstring.append(self.add())
            elif(i[0] == 'sub'):
                outstring.append(self.sub())
            elif(i[0] == 'and'):
                outstring.append(self.And())
            elif(i[0] == 'or'):
                outstring.append(self.Or())
            elif(i[0] == 'not'):
                outstring.append(self.Not())
            elif(i[0] == 'neg'):
                outstring.append(self.neg())
            elif(i[0] == 'gt'):
                outstring.append(self.gt())
            elif(i[0] == 'lt'):
                outstring.append(self.lt())
            elif(i[0] == 'eq'):
                outstring.append(self.Eq())
            elif(i[0] == 'label'):
                parentFunction = self.currentFunction
                outstring.append(self.label(i[1],parentFunction[0]))
            elif(i[0] == 'if-goto'):
                outstring.append(self.conditional('conditional',i[1],parentFunction[0]))
            elif(i[0] == 'goto'):
                outstring.append(self.conditional('unconditional',i[1],parentFunction[0]))
            elif(i[0] == 'function'):
                outstring.append(self.funct(i[1],i[2]))
            elif(i[0] == 'return'):
                outstring.append(self.ret())
            elif(i[0] == 'call'):
                outstring.append(self.call(i[1],i[2]))
            else: 
                continue
        #add
        outstring.append(self.commands['End'])
        return outstring

    def pop(self,dataloc = 'd',value=None):
        '''
            Precondition: The stack pointer is considered valid 
            Post Condition: The data at RAM[SP] was stored in D and SP-- 
            Returns the pop string if successful and -1 otherwise 
        '''
        if(dataloc == 'd'):
            return '@SP\nM=M-1\n@SP\nA=M\nD=M\n'
        elif(dataloc == 'argument'):
            return '@'+ str(value) + '\nD=A\n@R2\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif(dataloc == 'local'):
            return '@'+ str(value) + '\nD=A\n@R1\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif(dataloc == 'this'):
            return '@'+ str(value) + '\nD=A\n@R3\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif(dataloc == 'that'):
            return '@'+ str(value) + '\nD=A\n@R4\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif(dataloc == 'temp'):
            return '@'+ str(value) + '\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D'
        elif(dataloc == 'static'):
            fileName = self.currentFunction[0].partition('.')[0]
            return '@SP\nM=M-1\nA=M\nD=M\n@' + fileName + '.' + str(value) +'\nM=D'
            # Previous implementation 
            # return '@SP\nM=M-1\nA=M\nD=M\n@'+ str(int(value) + 16) +'\nM=D'
        elif(dataloc == 'pointer' and value == '0'):
            #popping into this 
            return '@SP\nM=M-1\nA=M\nD=M\n@R3\nM=D' 
        elif(dataloc == 'pointer' and value == '1'):
            #popping into that 
            return '@SP\nM=M-1\nA=M\nD=M\n@R4\nM=D' 
        else:
            return -1 

    def push(self,dataloc, value=None):
        '''
            Precondition: The stack is considered valid 
            Post Condition: The data from the data location is stored into D and pushed onto the stack. SP++ 
        '''
        string = '' 
        #general algorithm: 
        # - get and store the value in dataloc + i into d 
        # - push the value of D into the stack pointer 
        # - increment the SP
        string += self.get_value(dataloc,value)
        string += self.commands['StoreD']
        string += self.commands['IncSP']
        return string
    
    def get_value(self,dataloc,value):
        #get the dataloc pointer 
        #increment the dataloc pointer by I
        if(dataloc == 'constant'):
            return '@' + str(value) + '\nD=A\n' 
        elif(dataloc == 'local'):
            return '@' + str(value) + '\nD=A\n@R1\nA=D+M\nD=M\n' 
        elif(dataloc == 'argument'):
            return '@' + str(value) + '\nD=A\n@R2\nA=D+M\nD=M\n'
        elif(dataloc == 'this'):
            return '@' + str(value) + '\nD=A\n@R3\nA=D+M\nD=M\n'
        elif(dataloc == 'that'):
            return '@' + str(value) + '\nD=A\n@R4\nA=D+M\nD=M\n'
        elif(dataloc == 'temp'):
            return '@' + str(value) + '\nD=A\n@5\nA=D+A\nD=M\n'
        elif(dataloc == 'static'):
            fileName = self.currentFunction[0].partition('.')[0]
            return '@' + fileName +'.'+ str(value) +'\nD=M\n'
            # Previous implementation 
            # return '@' + str(int(value) + 16) + '\nD=M\n'
        elif(dataloc == 'pointer' and value == '0'):
            return '@R3\nD=M\n' 
        elif(dataloc == 'pointer' and value == '1'):
            return '@R4\nD=M\n'
        elif(dataloc == 'd'):
            return ''
        else: 
            return str(-1)

    def add(self):
        return self.pop() + '@SP\nM=M-1\nA=M\nM=D+M\n' + self.commands['IncSP']

    def sub(self):
        return self.pop() + '@SP\nM=M-1\nA=M\nM=M-D\n' + self.commands['IncSP']

    def And(self):
        return self.pop() + '@SP\nM=M-1\nA=M\nM=D&M\n' + self.commands['IncSP'] 

    def Or(self):
        return self.pop() + '@SP\nM=M-1\nA=M\nM=D|M\n' + self.commands['IncSP']

    def Not(self):
        return self.pop() + 'D=!D\n' + self.push('d')

    def neg(self):
        return self.pop() + 'D=-D\n' + self.push('d')

    def gt(self):
        string = self.pop()  +  '@SP\nM=M-1\nA=M\nD=D-M\n' + '@true' + str(self.count) + '\n' + 'D;JLT\n'\
        + '@0\nD=A\n' + self.push('d') + '\n@endcomp' + str(self.count) + '\n' + '0;JMP\n' + '(true' + str(self.count) + ')\n'\
        + '@1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 

    def lt(self):
        string = self.pop()  +  '@SP\nM=M-1\nA=M\nD=D-M\n' + '@true' + str(self.count) + '\n' + 'D;JGT\n'\
        + '@0\nD=A\n' + self.push('d') + '\n@endcomp' + str(self.count) + '\n' + '0;JMP\n' + '(true' + str(self.count) + ')\n'\
        + '@1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 

    def Eq(self):
        string = self.pop()  +  '@SP\nM=M-1\nA=M\nD=D-M\n' + '@true' + str(self.count) + '\n' + 'D;JEQ\n'\
        + '@0\nD=A\n' + self.push('d') + '\n@endcomp' + str(self.count) + '\n' + '0;JMP\n' + '(true' + str(self.count) + ')\n'\
        + '@1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 

    def label(self,lbl,funct=None):
        if(funct):
            #use if we are writing a label within a function 
            return '('+ funct + '$' + lbl + ')'
        else:
            #for use if we are writing a function label 
            return '(' + lbl + ')'

    def conditional(self,cond,lbl=None,funct=None):
        if(funct != None):
            lbl = self.currentFunction[0]+'$'+lbl
        if(cond == 'unconditional'):
            return '@'+ lbl +'\n'+ self.commands['uncondJMP']
        elif(cond == 'return'):
            return '@R14\nA=M\n' + self.commands['uncondJMP']
        else: 
            return self.pop() + '@' + lbl + '\nD;JGT'

    def funct(self,functName,nArgs):
        '''
        Takes a function call and conditions the stack to allow for the function to run. 
        @param functName: name of the function
        @param nArgs: number of arguments for the function
        '''
        self.currentFunction = (functName.strip(),nArgs)
        #psuedo algo: 
        #init local variables (these are going to be stored in sp+0 .. sp+n)
        #local variables are going to be stored with 0 in them. 
        string = self.label(functName)
        if(nArgs != 0):
            string += '\n'
            string1 = self.push('constant',0) + '\n'
            string1 *= int(nArgs) #store 0 nArg times to the stack --> stack pointer should now be at lcl + nArgs 
            string += string1
        return string 

    def ret(self):
        '''
        returns assembly code to return the stack machine back to its previous state. 
        '''
        #psuedo algo: 
        #store the return address into R14 
        string = '@R1\nA=M\nD=A\n@5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n'
        #pop stack to arg[0]
        string += self.pop('argument','0')
        #set sp to arg[0] and increment plus one 
        string += '\n@R2\nD=M\n@SP\nM=D\n' + self.commands['IncSP']
        #store endFrame - 1 to that
        string += '\n@R1\nM=M-1\nA=M\nD=M\n@R4\nM=D\n'
        #store endFrame - 2 to This
        string += '@R1\nM=M-1\nA=M\nD=M\n@R3\nM=D\n'
        #store endFrame - 3 to arg 
        string += '@R1\nM=M-1\nA=M\nD=M\n@R2\nM=D\n'
        #store endFrame - 4 to lcl
        string += '@R1\nM=M-1\nA=M\nD=M\n@R1\nM=D\n'  
        #goto retAddr 
        string += self.conditional('return')
        self.counter = 0
        return string

    def call(self,fName,nArgs):
        '''
        returns assembly code for calling a function
        '''
        parentFunction = self.currentFunction
        string = '@' + parentFunction[0] + '$ret.'+ str(self.counter) +'\nD=A\n'
        string += self.push('d') + '\n'
        string += '@R1\nA=M\nD=A\n' + self.push('d') + '\n'
        string += '@R2\nA=M\nD=A\n' + self.push('d') + '\n'
        string += '@R3\nA=M\nD=A\n' + self.push('d') + '\n'
        string += '@R4\nA=M\nD=A\n' + self.push('d') + '\n'
        n = 5 + int(nArgs)
        string += '@SP\nA=M\nD=A\n@' + str(n)+'\nD=D-A\n@R2\nM=D\n'
        string += '@SP\nA=M\nD=A\n@R1\nM=D\n'
        string += self.conditional('unconditional',fName)
        string += '(' + parentFunction[0] + '$ret.'+ str(self.counter) +')'
        self.counter += 1
        return string


if __name__ == "__main__":
    infile_sys = sys.argv[1]
    path = infile_sys
    path = path.rstrip('/')
    if(isdir(path)):
        #lets get the files 
        files = listdir(path)
        vmFiles =[]
        for i in files:
            if(i.find('.vm') != -1):
                vmFiles.append(i)
        #need to make sure that the sys file is at the start 
        try:
            #make sure that the sys file exists 
            if(vmFiles.index('Sys.vm') != 0):
                vmFiles.remove('Sys.vm')
                vmFiles.insert(0,'Sys.vm')
        except ValueError:
            print('Please make sure that you include Sys.vm file!')
            print('The current vm files in the directory are: ' + str(vmFiles))

        vm = vmToHack(path,files=vmFiles)
        hack_data = vm.write_data()
    else: 
        #the input is a file 
        vm = vmToHack(path)
        hack_data = vm.write_data()

    print('Raw Data:')
    print(vm.data)
    print('Data written to file: ' + vm.get_outfile_name())
    print(hack_data)