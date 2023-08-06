#!/usr/bin/env python3
'''Tools For Trimming Sequences'''
def longest_contig(seq):
    if len(seq)>=600:
        #ideal scinario >500 bp between Ns
        Ns =  [j for j, x in enumerate(seq) if x == "N"]
        if len(Ns)>0:
            #if there are ns in the seq
            #if the first letter not an N add 0 to the array so that start is at 0
            if Ns[0]>0:
                Ns.insert(0,0)
            #if the last letter is not an N add the end to the array
            if Ns[-1]<(len(seq)-1):
                Ns.append(len(seq)-1)
            gaps = []
            for i in range(0, len(Ns)-1):
                gaps.append(Ns[i+1]-Ns[i])
            if max(gaps)>=600:
                loc = [i for i, j in enumerate(gaps) if j == max(gaps)]
                if len(loc)>2:
                    print('Error: got more than one contig over 600bp')
                elif max(gaps)> 1500:
                    #dont allow any more than 1000 bps (trimmed from the beginning of seq)
                    return seq[Ns[loc[0]]:Ns[loc[0]]+1500]
                else:
                    return seq[Ns[loc[0]]+1:Ns[loc[0]+1]]

            else:
                #ns in the seq and <600 bp between Ns --> find smallest number of gaps to get above 500bp
                bgap = []
                for i in range(0, len(gaps)):
                    ph = [i]
                    mysum = gaps[i]
                    j = i+1
                    while mysum<600 and j<len(gaps):
                        mysum += gaps[j]
                        ph.append(j)
                        j+=1
                    if mysum >=600 or len(bgap) == 0:
                        if len(bgap)==0:
                            bgap = ph
                        elif len(ph)<len(bgap):
                            bgap = ph
                tseq = seq[  Ns[bgap[0]]   :   Ns[bgap[-1]+1]  ]

                #clean the ends
                go = False
                while go ==False:
                    if  len(tseq)>400:
                        if tseq[0]=='N' or tseq[-1]=='N':
                            if tseq[0]=='N':
                                tseq = tseq[1:]
                            if tseq[-1]=='N':
                                tseq = tseq[:-1]
                        else:
                            go =True
                    else:
                        go = True
                return tseq
        else:
            if len(seq)>1000:
                return seq[:1000]
            else:
                return seq
    else:
        print('BadSeq')
        return seq
def pass_trim(seq, bp = 500):
    Ns = [i for i, j in enumerate(seq) if j == 'N']
    if len(Ns)>5 or len(seq)<bp:
        return False
    else:
        return True
def sliding_window(sequence,window_size = 20,max_number_ns = 2,max_ns_inarow = 2,min_len = 600,max_len = None,side = 'left',):
    '''Sliding Window With Specifications: Takes in Sequence as String'''
    sequence = str(sequence)
    start = 0
    good_left = []
    left_gaps = []
    while start <= len(sequence) - window_size:
        window = sequence[start:start+window_size]
        if window.count('N')/window_size < max_number_ns/window_size and max_ns_inarow*'N' not in window:
            good_left.append(start)
        start+=1
    for i in range(0,len(good_left)-1):
        if good_left[i+1]-good_left[i]>1:
            left_gaps.append([good_left[i+1]-good_left[i], good_left[i],good_left[i+1]])
    dist = []
    if len(left_gaps)>1:
        for i in range(0,len(left_gaps)-1):
            dist.append(left_gaps[i+1][2]-left_gaps[i][2])
        if max(dist)>600:
            qual = 'good'
        else:
            qual = 'bad'
        take = dist.index(max(dist))
        left = left_gaps[take][2]
        while sequence[left]=='N':
            left+=1
        try:
            if sequence[left:].index('N')<20:
                left += sequence[left:].index('N')+1
        except:
            placeholder = 'No index which is good'
        right = left_gaps[take+1][1]+sequence[left_gaps[take+1][1]:].index('N')
    else:
        left = 0
        while sequence[left]=='N':
            left+=1
        try:
            if sequence[left:].index('N')<20:
                left += sequence[left:].index('N')+1
        except:
                placeholder = 'No index which is good'
        right = len(sequence)-1
        while sequence[right]=='N':
            right-=1
        if right-left >600:
            qual = 'good'
        else:
            qual = 'bad'
    d =  {  'seq':sequence,
            'tseq':sequence[left:right],
            'length':right-left,
            'qual':qual,
            'left':left,
            'right':right,}
    return d
def window_many(file,to = True,side='both',window_size = 20,max_number_ns = 2,max_ns_inarow = 2,min_len = 600,max_len = None):
    '''dictionary output from a multifasta input'''
    import holotools.biop as hb
    d = hb.fdict(file)
    td = {}
    for k,v in d.items():
        print(k)
        td[k]=sliding_window(v,side=side,window_size=window_size,max_number_ns=max_number_ns,max_ns_inarow=max_ns_inarow,min_len=min_len,max_len=max_len)
        if side == 'left':
            td[k]['tseq']=td[k]['seq'][td[k]['left']:]
        if side == 'right':
            td[k]['tseq']=td[k]['seq'][:td[k]['right']]
        if to==True:
            td[k]=td[k]['tseq']
    return td
