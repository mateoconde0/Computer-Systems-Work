class Stack():
    def __init__(self):
        self.stack = []
        self.size = 0 
    def __len__(self):
        return self.size 
    def is_empty(self):
        return self.size == 0 
    def pop(self):
        if(not self.is_empty()):
            temp_item = self.stack.pop()
            self.size -= 1
            return temp_item 
        else: 
            return 
    def peek(self):
        if(not self.is_empty()):
            return self.stack[self.size - 1]
    def push(self,item):
        self.stack.append(item) 
        self.size += 1 
    def __str__(self):
        return str(self.stack)