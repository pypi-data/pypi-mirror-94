class progress_bar(object):
    def __init__(self, n, symbol="\U0001f4a9"):
        self.symbol = symbol
        self.count = 0
        self.n = n
    def update(self, memory = False):
        if memory ==True:
            self.memory_usage()
        else:
            import sys
            sys.stdout.write('\r')
            self.count+=1
            progress = (self.count) / self.n
            sys.stdout.write("%d%% \U0001f4a8%-20s" % (100*progress,self.symbol*int(20*progress)))
            sys.stdout.flush()
    def test(self):
        import time
        for i in range(0,100):
            time.sleep(0.1)
            self.update()
        self.count = 0
    def clear(self):
        self.count = 0
    def memory_usage(self, ram=16):
        import sys
        import os
        import psutil
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss/1e9
        sys.stdout.write('\r')
        self.count+=1
        progress = (self.count) / self.n
        sys.stdout.write("%d%% \U0001f4a8%-20s memory left %f%%" % (100*progress,self.symbol*int(20*progress),ram-mem))
        sys.stdout.flush()
