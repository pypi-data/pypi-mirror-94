#!/usr/bin/env python3
'''Just Make Biopython Work With Less Key Strokes'''
from Bio import SeqIO
def fdict(file):
    '''parse fasta file to dictionary'''
    d = {}
    with open(file,'r') as h:
        for r in SeqIO.parse(h,'fasta'):
            d[r.description]=str(r.seq)
    return d
def csv_to_fasta(file='MasterTable.tsv', outfile='fastafromcsv.fna', minsize = 300, maxsize=1000000, seqnamecol='sequence_name',seqcol='sequence', sep = '\t'):
    import pandas as pd
    df = pd.read_csv(file, sep=sep)
    #seq and name handle
    df = df.loc[df[seqcol]!='NONE'].reset_index()
    out = open(outfile,'w')
    for k,v in zip(df[seqnamecol],df[seqcol]):
        out.write('>%s\n%s\n'%(k,v))
    out.close()
    print('Your Fasta %s Has Been Created'%outfile)
    return outfile

def mastertable_to_fasta(file='MasterTable.tsv', outfile='MasterTable.fna', minsize = 300):
    import pandas as pd
    df = pd.read_csv(file, sep='\t').fillna('NONE')
    # Drop Nulls
    df = df.loc[df['sequence']!='NONE'].reset_index(drop=True)
    # Make the Outfile
    out = open(outfile,'w')
    # Loop to write
    for m, h, s in zip(df['ministock_name'],df['hb'], df['sequence']):
        if len(s)>minsize:
            if str(h) != 'NONE':
                out.write('>%s\n%s\n'%(h,s))
            elif str(m) != 'NONE':
                out.write('>%s\n%s\n'%(m,s))
            else:
                print('issue with %s'%str(s))
    out.close()
    print('Your Fasta %s Has Been Created'%outfile)
    return outfile

def genbank_to_json(file):
    locus = 1
    i = {}
    out = open('clean_'+file,'w')
    with open(file) as h:
        lines = h.readlines()
        for line in lines:
            if 'LOCUS       ' in line:
                out.write('LOCUS       %i\n'%locus)
                locus +=1
            else:
                out.write(line)
    from Bio import GenBank
    with open('clean_'+file) as h:
        for r in GenBank.parse(h):
            print(locus)
            lst = []
            for m in r.features:
                lst.append(m)
            i[r.locus]= lst
    # organize
    import pandas as pd
    d = {}
    dfs = pd.DataFrame()
    y = 50
    for k,v in i.items():
        f = 0
        r = 0
        # each locus (or segment)
        l = []
        for j in range(1,len(v)):
            location = i[k][j].location
            if 'complement' in location:
                direction = 'complement'
                start = location[location.index('(')+1:location.index('..')]
                end = location[location.index('..')+2:-1]
                if r%2==0:
                    c = "#d699ff"
                else:
                    c = "#9d1ef3"
                r+=1
                my = y+20
                text_y = y+80
            else:
                direction = 'forward'
                start = location[:location.index('..')]
                end = location[location.index('..')+2:]
                if f%2==0:
                    c = "#1ef3dc"
                else:
                    c = "#199b8d"
                f+=1
                my = y
                text_y = y-10
            # for each list of cds go through qualifiers get the ones we want
            gene = ''
            product = ''
            translation = ''
            locus_tag = ''
            for h in i[k][j].qualifiers:
                # get the qualifiers we want
                if h.key == '/gene=':
                    gene = h.value.replace('"', '').replace("'", '')
                if h.key == '/product=':
                    product = h.value.replace('"', '').replace("'", '')
                if h.key == '/translation=':
                    translation = h.value.replace('"', '').replace("'", '')
                if h.key == '/locus_tag=':
                    locus_tag = h.value.replace('"', '').replace("'", '')

            l.append([k, gene, product, start, end, int(end)-int(start), direction, locus_tag, translation, c, my, text_y])
        df = pd.DataFrame(l,columns = ['contig','gene','product','start','end','length','direction','locus_tag','translation', 'color', 'y','text_y'])
        if len(df)>0:
            d[k]=' "%s":'%str(k)+str(df.to_json(orient='records'))
            dfs = pd.concat([dfs,df])
        # row height
        y+=300
    # json for gene view
    json = '{'
    for k,v in d.items():
        json+=v+','
    json = json[:-1]+'}'
    return json, dfs.to_json(orient='records')
