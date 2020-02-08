from tokenizer import * 
from CompilationEngine import * 
from CompilationEngine import MissingSymbol,MissingIdentifier,MissingKeyword,MissingType

if __name__ == "__main__":
        infile_sys = sys.argv[1]
        path = infile_sys
        path = path.rstrip('/')
        tokens = Tokenizer(path)
        tokens.write_data()
        # print('Raw Data:')
        # print(tokens.data)
        # print('Tokens')
        # print(tokens.tokens)

        #we now how tokenized data --> lets gramatize it 
        compilation = CompilationEngine(path)
        compilation.write_data()

        print('Raw Data:')
        print(compilation.data)
        # print('Data written to file: ' + vm.get_outfile_name())
        # print(hack_data)