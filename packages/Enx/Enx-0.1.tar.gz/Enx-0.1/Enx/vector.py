import random

class ListTypeNeeded(Exception):
    pass

class IndexNotFound(Exception):
    pass

class Vector(object):
    def __init__(self, arr: list, ranges: int=None):
        self.arr = arr
        self.start = 0
        if len(self.arr) == 1 and ranges != None:
            self.arr = [self.arr[0]] * ranges
        if type(self.arr) != list:
            raise ListTypeNeeded("Vector can contain only lists")

    def __str__(self):
        arrStr = "["
        lengthOfArr = len(self.arr)
        if len(self.arr) == 0:
            return "[]"
        for i in range(len(self.arr)):
            if i == lengthOfArr - 1:
                arrStr += f"{self.arr[i]}]"
            else:
                arrStr += f"{self.arr[i]}, "
        return arrStr
    
    def __getitem__(self, key):
        return self.arr[key]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __iter__(self):
        return self

    def __next__(self):
        if self.start < len(self.arr):
            ret = self.arr[self.start]
            self.start += 1
            return ret
        else:
            raise StopIteration
    
    def shuffle(self):
        random.shuffle(self.arr)
        return self.arr

    def sort(self, mode="normal"):
        if mode == "normal":
            for i in range(len(self.arr)):
                on = True
                for _ in range(len(self.arr) - 1):
                    if self.arr[_] > self.arr[_ + 1]:
                        self.arr[_], self.arr[_ + 1] = self.arr[_ + 1], self.arr[_]
                        on = False
                    else:
                        pass
                if on:
                    break
            return self.arr
        elif mode == "reverse":
            for i in range(len(self.arr)):
                on = True
                for _ in range(len(self.arr) - 1):
                    if self.arr[_] < self.arr[_ + 1]:
                        self.arr[_], self.arr[_ + 1] = self.arr[_ + 1], self.arr[_]
                        on = False
                    else:
                        pass
                if on:
                    break
            return self.arr

    
    def clear(self):
        self.arr = []
        return self.arr

    def set(self, value=0):
        for _ in range(len(self.arr)):
            self.arr[_] = value
        return self.arr

    def find(self, item):
        for i in range(len(self.arr)):
            if self.arr[i] == item:
                return i
            else:
                pass
        raise IndexNotFound("There is no index for the value")

    def append(self, value):
        length = len(self.arr)
        append_list = [None] * (length + 1)
        for _ in range(length):
            append_list[_] = self.arr[_]
        append_list[length] = value
        self.arr = append_list
        return self.arr
        
        
