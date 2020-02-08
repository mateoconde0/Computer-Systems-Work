class SymbolTable:
    def __init__(self):
        self._data = {'name':[],'type':[],'kind':[],'number':[]}
        self._numStatic = 0
        self._numField = 0 

    def add_symbol(self,name,type,kind,number):
        pass 