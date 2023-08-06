#!/usr/bin/env python3
'''Opporations That Should Be Standard'''
#how often symbol occurs in string
def occurs(symbol, string):
    return [j for j, x in enumerate(string) if x == symbol]
#random id generator of 6 figures
def id_generator(string,size=10 ):
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
def getparent(p = True):
    import os
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    parent = os.path.abspath(os.path.join(this_dir, os.pardir))
    grandparent = os.path.abspath(os.path.join(parent, os.pardir))
    if p ==True:
        return parent
    else:
        return grandparent
        
class listranges(object):
    def __init__(self, lst ):
        self.lst = lst
        self.tmp = [self.lst[0]]
        self.lst.pop(0)
        self.ranges = []
        print(self.tmp)
        for i in self.lst:
            if i-1 != self.tmp[-1]:
                if len(self.tmp)>1:
                    self.ranges.append(str(self.tmp[0])+'-'+str(self.tmp[-1]))
                else:
                    self.ranges.append(self.tmp[0])
                self.tmp = [i]
            else:
                self.tmp.append(i)

        if self.lst[-1] in self.tmp:
            self.ranges.append(str(self.tmp[0])+'-'+str(self.tmp[-1]))
