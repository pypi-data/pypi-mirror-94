import pandas as pd
import os
import re
from Bio.SeqUtils import *
class patentin:
    def __init__(self, patent):
        self.patent = patent

    def parse(self):
        #read data in as array
        data = open(str(self.patent),'r').readlines()
        self.txt = data
        #dataframe to be built
        p210 = []
        p211 = []
        p212 = []
        p213 = []
        p220 = []
        p221 = []
        p222 = []
        p223 = []
        n220 = []
        p400 = []
        c400 = []
        #start location defined by <210> tag
        start = [i for i in range(0,len(data)) if '<210>' in data[i]]
        self.header=(data[:start[0]])
        #get primary data
        #get each entry data block
        for i in range(0,len(start)):
            feature = False
            #if at the end just scoop the rest
            if i == len(start)-1:
                block = data[start[i]:]
            #otherwise be normal
            else:
                block = data[start[i]:start[i+1]]
            #parse info for bolck into csv acceptable format
            for j in range(0,len(block)):
                if '<210>' in block[j]:
                    p210.append(int(block[j].replace('\n','').replace('<210>','')))
                if '<211>' in block[j]:
                    p211.append(block[j].replace('\n','').replace('<211>  ',''))
                if '<212>' in block[j]:
                    p212.append(block[j].replace('\n','').replace('<212>  ',''))
                if '<213>' in block[j]:
                    p213.append(block[j].replace('\n','').replace('<213>  ',''))
                if '<220>' in block[j]:
                    if feature==False:
                        fs = j
                        feature = True
                if '<400>' in block[j]:
                    #clean p400 after the df is made
                    fe = j
                    p400.append(block[j:])
            try:
                if feature ==True:
                    ps221 = []
                    ps222 = []
                    ps223 = []
                    #clean the feature
                    f = list(block[fs:fe])
                    n220.append(f.count('<220>\n'))
                    b = False
                    t = []

                    for l in f:
                        if b == False:
                            if '<221>' in l:
                                ps221.append(l[7:-1])
                            if '<222>' in l:
                                ps222.append(l[7:-1])
                            if '<223>' in l:
                                b = True
                                t.append(l[7:-1])
                        elif b ==True:
                            if l == '\n':
                                b = False
                                t = ''.join(t).replace('       ','').replace('      ','').replace('<223>  ','').replace('\n','').replace('    ','')
                                ps223.append(t)
                                t = []
                            else:
                                t.append(l)
                    p220.append(f)
                    p221.append(ps221)
                    p222.append(ps222)
                    p223.append(ps223)
                else:
                    n220.append(0)
                    p220.append('')
                    p221.append('')
                    p222.append('')
                    p223.append('')
            except:
                print('issue at p220')
        df = pd.DataFrame([p210,p211,p212,p213,n220,p221,p222,p223,p400]).transpose()
        df.columns = ['p210','p211','p212','p213','n220','p221','p222','p223','p400']
        self.df = df
        self.species = self.df.p213

    def write_patentin(self, title = 'holobiome_patentin_output'):
        out = open(title+'.txt','w')
        for i in self.header:
            out.write(i)
        for i in range(0,len(self.df)):
            ip210 = self.df.p210[i]
            ip211 = self.df.p211[i]
            ip212 = self.df.p212[i]
            ip213 = self.df.p213[i]
            ip221 = self.df.p221[i]
            ip222 = self.df.p222[i]
            ip223 = self.df.p223[i]
            ip400 = self.df.p400[i]
            string = '<210>  '+str(ip210)+'\n<211>  '+str(ip211)+'\n<212>  '+str(ip212)+'\n<213>  '+str(ip213)+'\n\n'
            if len(ip221)>0:
                string+='\n'
                for j in range(0,len(ip221)):
                    string+='<220>\n<221>  '+ip221[j]+'\n<222>  '+ip222[j]
                    if len(ip223[j])>55:
                        s = ip223[j]
                        n = 55
                        chunks = [s[i:i+n] for i in range(0, len(s), n)]
                        string+='\n<223>  '+chunks[0]+'\n'
                        for m in range(1,len(chunks)):
                            string+='       '+chunks[m]+'\n'
                        string+='\n'
                    else:
                        string+='\n<223>  '+ip223[j]+'\n\n'
            string+=''.join(ip400)
            out.write(string)
        out.close()

    def patentin_entry_format(self, title = 'patentin_entry_format'):
        out = open(title+'.txt','w')
        for i in range(0,len(self.df)):
            name = self.df.p213[i]
            if 'PRT' in self.df.p212[i]:
                #get each amino acid
                aas = []
                for j in self.df.p400[i]:
                    if '<400>' not in j:
                        a = re.sub("^\d+\s|\s\d+\s|\s\d+$|\n|\t", " ",j )
                        a = a.split(' ')
                        for m in a:
                            if m != '' and m !='Xaa':
                                aas.append(IUPACData.protein_letters_3to1[m])
                            elif m=='Xaa':
                                aas.append('X')
                out.write('<'+str(self.df.p210[i])+';'+'Protein/1'+';'+name+'>\n')
                out.write(''.join(aas)+'\n')
            elif 'DNA' in self.df.p212[i]:
                fasta = self.df.p400[i]
                fastac = []
                for j in fasta:
                    if '<400>' not in j:
                        f = re.sub("^\d+\s|\s\d+\s|\s\d+$|\n|\t", " ", j)
                        f = f.replace(" ",'')
                        fastac.append(f)
                out.write('<'+str(self.df.p210[i])+';'+'DNA'+';'+name+'>\n')
                out.write(''.join(fastac)+'\n')
        out.close()

    def new_patent(self, main_csv, multi_fasta_file):
        r220 = []
        r400 = []
        with open(multi_fasta_file,'r') as h:
            for r in SeqIO.parse(h,'fasta'):
                seq.append(str(r.seq))
                des.append(str(r.description))
        mf = pd.DataFrame([r220,r400]).transpose()
        mf.columns = ['r220','r400']
        df = pd.DataFrame()
        self.df = df

    def change_header(self, tag, newtagline):
        header = []
        for i in self.header:
            if tag in i:
                header.append(tag+'  '+newtagline+'\n')
            else:
                header.append(i)
        self.header = header
    def iso_fasta(self,tp,seq_no):
        df = pd.DataFrame(self.df.loc[self.df.p210==seq_no].reset_index())
        fasta = df.p400[0]
        fastac = []
        for i in fasta:
            if '<400>' not in i:
                f = re.sub("^\d+\s|\s\d+\s|\s\d+$|\n|\t", " ", i)
                f = f.replace(" ",'')
                fastac.append(f)
        self.fasta = ''.join(fastac)
        self.fasta_pt = fasta
    def look(self, seq_id, txt_file = False):
        if txt_file == True:
            for i in range(0, len(self.txt)):
                if '<210>  '+str(seq_id)+'\n' in self.txt[i]:
                     c = i
            test = open('quick_look.txt','w')
            for i in range(c,c+1000):
                test.write(self.txt[i])
            test.close()
        seq_id-=1
        print(str(self.df.p223.iloc[seq_id]))
        print("________________________________________________\n"+str(self.df.iloc[seq_id]))
        self.looked = pd.DataFrame(self.df.iloc[seq_id]).transpose()
