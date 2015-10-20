__author__ = 'jiyue'

__author__ = 'jiyue'


class Stack:
    def __init__(self, size=2000):
        self.stack = []
        self.size = size
        self.top = -1

    def setSize(self, size):
        self.size = size

    def push(self, data):
        if self.isFull():
            raise Exception("stack is already full")
        else:
            self.stack.append(data)
            self.top = self.top + 1

    def pop(self):
        if self.isEmpty():
            raise Exception("stack is empty")
        else:
            self.top = self.top - 1
            return self.stack.pop()

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def isFull(self):
        if self.top == self.size - 1:
            return True
        else:
            return False
