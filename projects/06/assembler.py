class assembler():
    def __init__(self,infile):
        self.infile = infile
        self.outfile = infile.split('.')[0] + ".hack"
        self.data = []
        self.variables = {'SCREEN':'16384','KEYBOARD':'24576','KBD':'24576','R0':'0','R1':'1','R2':'2','R3':'3','R4':'4','R5':'5','R6':'6','R7':'7','R8':'8','R9':'9','R10':'10','R11':'11','R12':'12','R13':'13','R14':'14','R15':'15','SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4'}
        self.nextAvailable = 16 

    def get_data(self):
        '''
        Reads in a file and stores all of the data into the data obj of the assembler  
        '''    
        try:
            file_object = open(self.infile,"r")
            temp_data = file_object.readlines()
            file_object.close()
            #lets clean the data 
            for line in range(len(temp_data)):
                temp_string = self.cleanString(temp_data[line])
                if(temp_string != ''):
                    self.data.append(temp_string)
            return 1
        except: 
            print("There was an error reading the file.")
            return -1

    def cleanString(self,string):
        #clean the line 
        string = string.strip()
        #split the line into the data and the comment 
        string = string.partition("//")[0]
        #remove spaces 
        string = string.replace(" ", '')
        return string

    def get_variables(self):
        '''
         Looks through the file and gets all of the variables and stores into a dictionary 
        '''
        counter = 0
        for i,line in enumerate(self.data):
            #going to loop through and identify if it has a L command 
            if(line.find('(') != -1):
                #the line is a L command
                k = line[line.find('(')+1:line.find(')')]
                if(self.variables.get(k) == None):
                    #give the key the current line number 
                    self.variables[k] = i - counter 
                    counter += 1
                else: 
                    raise keyError(message="There is already and instance of this key")
        print(self.variables)

    def convert2hack(self):
        #determine if it is an a instruction or not 
        binary_strings = []
        #dictionaries for jump, dest, and comp
        jumpDictionary = {'null':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
        destDictionary = {'null':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
        compDictionary = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111','A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111','D&A':'0000000','D|A':'0010101','M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
        for string in self.data:
            binString = ''
            if(string.find('@') == 0):
                #check if we are simply dealing with a number 
                if(string[string.find('@')+1:len(string)].isnumeric()):
                    string = string[string.find('@')+1:len(string)]
                    #have a string in decimal. Lets put it into binary 
                    test_string = '{0:b}'.format(int(string))
                    #add remaining zeros 
                    binString = '0' * (16-len(test_string)) 
                    #add to current string 
                    binString += test_string
                    #append to the global list 
                    binary_strings.append(binString)
                #we are dealing with a variable or l command 
                else:
                    loc = string[string.find('@')+1:len(string)]
                    #check if this is a variable that needs to be defined 
                    if(self.variables.get(loc) == None):
                        self.variables[loc] = self.nextAvailable
                        self.nextAvailable += 1 
                    #get the line number 
                    string = self.variables[loc]
                    #convert it to binary 
                    test_string = '{0:b}'.format(int(string))
                    #fill with zeros 
                    binString = '0' * (16 - len(test_string)) 
                    #add it to the existing binary string 
                    binString += test_string
                    #append to the global binary string list 
                    binary_strings.append(binString)
            elif(string.find('(') != -1):
                #this section is not really needed 
                pass
            else:  
                #start the string with the binary represenation of a d instruction 
                binString = '111'
                if(string.find(';') != -1):
                    #this should be a jump instruction 
                    parts = string.split(';')
                    #add the comp to the bin string 
                    binString += compDictionary[parts[0]]
                    #we know that the dest is non existent so lets set all equal to 000
                    binString += destDictionary['null']
                    #we need to look up the jump
                    binString += jumpDictionary[parts[1]]       
                    binary_strings.append(binString)
                else: 
                    parts = string.split('=')
                    #need to add opperation first, then destination 
                    binString += compDictionary[parts[1]]
                    #then lets add the destination 
                    binString += destDictionary[parts[0]]
                    #now jump 
                    binString += jumpDictionary['null']
                    #append binary string to the global list 
                    binary_strings.append(binString)
        #return all of the strings 
        return binary_strings

    def write_data(self):
        #first get the binary data 
        binary_data = self.convert2hack()
        with open(self.outfile,'w') as hackFile: 
            #write it to the file 
            for binline in binary_data:
                hackFile.write('%s\n' % binline)
        


class keyError(Exception):
    def __init__(self,message="There was a key error"):
        print(message)

def main():
    asm = assembler("pong/Pong.asm")
    asm.get_data()
    asm.get_variables()
    asm.write_data()

main()
