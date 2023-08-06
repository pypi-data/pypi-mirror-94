class ScoreParam:
    """The parameters for an alignment scoring function"""
    def __init__(self, gap, match, mismatch):
        self.gap = gap
        self.match = match
        self.mismatch = mismatch
def blast(x,y):
    A = [[0]*(len(y)+1) for i in range(0,len(x)+1)]
    score=ScoreParam(-7, 10, -5)
    """Do a local alignment between x and y"""
    # create a zero-filled matrix
    best = 0
    optloc = (0,0)
    # fill in A in the right order
    for i in range(1, len(y)+1): # row
        for j in range(1, len(x)+1): # column
            # the local alignment recurrance rule:
            try:
                A[i][j] = max(A[i][j-1] + score.gap,# left
                              A[i-1][j] + score.gap,# bottom
                              A[i-1][j-1] + (score.match if x[j-1] == y[i-1] else score.mismatch),#left diagonal
                              0)
                # track the cell with the largest score
                if A[i][j] >= best:
                    best = A[i][j]
                    optloc = (i,j)
            except:
                print(i,j)
                e = None
    # return the opt score and the best location
    return best, optloc, A
class seq_node(object):
    def __init__(self,description, sequence, quality):
        self.description = description
        self.sequence = sequence
        self.quality = quality

class short_alignment(object):
    def __init__(self, sequence_files):
        import gzip
        self.forward = gzip.open(sequence_files[0],'rb').readlines()
        self.reverse = gzip.open(sequence_files[1],'rb').readlines()
    def add_node(self):
        print('this will be a function')
    def load(self):
        from holotools.progress import progress_bar
        self.fn = []
        p = progress_bar(len(self.forward))
        for i in range(0,len(self.forward)):
            p.update()
            if i%4 ==0:
                description = self.forward[i].decode('utf-8').replace('\n','')
            if i%4 ==1:
                sequence =self.forward[i].decode('utf-8').replace('\n','')
            if i%4 ==3:
                quality = self.forward[i].decode('utf-8').replace('\n','')
                self.fn.append(seq_node(description,sequence,quality))
                # use this time to do some work on the new node
        self.rn=[]
        p = progress_bar(len(self.reverse))
        for i in range(0,len(self.reverse)):
            p.update()
            if i%4 ==0:
                description = self.reverse[i].decode('utf-8').replace('\n','')
            if i%4 ==1:
                sequence =self.reverse[i].decode('utf-8').replace('\n','')
            if i%4 ==3:
                quality = self.reverse[i].decode('utf-8').replace('\n','')
                self.rn.append(seq_node(description,sequence,quality))
                # use this time to do some work on the new node
