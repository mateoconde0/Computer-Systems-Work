import sys 
infile_sys = sys.argv[1]

class vmToHack():
    def __init__(self,infile=infile_sys):
        assert infile != None, 'Please pass a file path to a vm file.'
        self.infile = infile
        self.outfile = infile.split('.')[0] + '.asm'
        self.data = self.get_data()
        self.count = 0 
        self.commands = {'StoreD':'@SP\nA=M\nM=D\n','IncSP':'@SP\nM=M+1','End':'(END)\n@END\n0;JMP\n'}

    def get_data(self):
        '''
        Reads in a file and stores all of the data into the data obj of the assembler  
        '''    
        try: 
            data = [] 
            file_object = open(self.infile,"r")
            temp_data = file_object.readlines()
            file_object.close()
            #lets clean the data 
            for line in range(len(temp_data)):
                temp_string = self.cleanString(temp_data[line])
                if(temp_string[0] != ''):
                    data.append(temp_string)
            return data
        except: 
            print("There was an error reading the file. Please make sure that your path is correct.")
            return -1

    def cleanString(self,string):
        #clean the line 
        string = string.strip()
        #split the line into the data and the comment 
        string = string.partition("//")[0]
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
            else: 
                continue
        #add
        outstring.append(self.commands['End'])
        return outstring

    def pop(self,dataloc = 'd',value=None):
        '''
            Precondition: The stack pointer is considered valid 
            Post Condition: The data at RAM[SP] was stored in D and SP-- 
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
            return '@SP\nM=M-1\nA=M\nD=M\n@'+ str(int(value) + 16) +'\nM=D'
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
            return '@' + str(int(value) + 16) + '\nD=M\n'
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
        + '@0\nA=A-1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 
    def lt(self):
        string = self.pop()  +  '@SP\nM=M-1\nA=M\nD=D-M\n' + '@true' + str(self.count) + '\n' + 'D;JGT\n'\
        + '@0\nD=A\n' + self.push('d') + '\n@endcomp' + str(self.count) + '\n' + '0;JMP\n' + '(true' + str(self.count) + ')\n'\
        + '@0\nA=A-1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 
    def Eq(self):
        string = self.pop()  +  '@SP\nM=M-1\nA=M\nD=D-M\n' + '@true' + str(self.count) + '\n' + 'D;JEQ\n'\
        + '@0\nD=A\n' + self.push('d') + '\n@endcomp' + str(self.count) + '\n' + '0;JMP\n' + '(true' + str(self.count) + ')\n'\
        + '@0\nA=A-1\nD=A\n' + self.push('d') + '\n(endcomp'+ str(self.count) + ')'
        self.count += 1 
        return string 
    def write_data(self):
        #first get the binary data 
        hack_data = self.vmCompiler()
        with open(self.outfile,'w') as hackFile: 
            #write it to the file 
            for binline in hack_data:
                hackFile.write('%s\n' % binline)
        return hack_data


if __name__ == "__main__":
    vm = vmToHack()
    hack_data = vm.write_data()
    print('Data written to file: ')
    print(hack_data)