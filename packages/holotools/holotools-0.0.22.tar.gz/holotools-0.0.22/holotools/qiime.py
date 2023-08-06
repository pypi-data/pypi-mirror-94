#!/usr/bin/env python3
'''Binders and Tools for Clustering of Bacterial Sequences'''
def qiime_format(fastafile):
    import re
    import holotools.biop as biop
    out = open('qiimenames_'+fastafile, 'w')
    d = biop.fdict(fastafile)
    for k,v in d.items():
        out.write('>%s\n%s\n'%(re.sub('[^a-zA-Z0-9\n\.]','.',str(k))+'_Holobiome',str(v).upper()))
    out.close()
    return 'qiimenames_'+fastafile
def clean_biom(tsv):
    import pandas as pd
    file = open(tsv, 'r').readlines()[1:]
    out = open(tsv,'w')
    [out.write(i) for i in file]
    out.close()
def biom_to_list(tsv, mastertable='MasterTable.tsv'):
    import os
    import pandas as pd
    df = pd.read_csv(tsv,sep = '\t')
    mastertable=pd.read_csv(mastertable,sep='\t')
    os.system('unzip rep-seqs.qza -d tmp')
    print('unzip rep-seqs')
    nxt = os.listdir('./tmp')
    from holotools.biop import fdict
    d = fdict('./tmp/%s/data/dna-sequences.fasta'%nxt[0])
    os.system('rm -r tmp')
    nd = {}
    for k,v in d.items():
        nd[k[:k.index(' ')]]=k[k.index(' ')+1:].replace('_Holobiome','')
    hbid=[nd[i] for i in df['#OTU ID']]

    #
    hbid2 = []
    otu=[]
    hb =[]
    sp=[]
    md = list(df)
    df = df.to_numpy()
    ts = []
    tss = []
    for i in range(0,len(df)):
        try:
            h = mastertable.loc[mastertable.hb==float(hbid[i])]
            if len(h)>0:
                    species = h.iloc[0].species_1
                    t = h.iloc[0].type
        except:

            m = mastertable.loc[mastertable.ministock_name==hbid[i].replace('.','_')]
            if len(m)>0:
                species = m.iloc[0].species_1
                t = m.iloc[0].type
        for j in range(0,len(df[i])):
            if df[i][j]==1:
                hbid2.append(hbid[i])
                otu.append(df[i][0])
                hb.append(md[j])
                sp.append(species)
                ts.append(t)
                # loc on to the hb
                try:
                    tss.append(mastertable.loc[mastertable.hb==float(md[j])].iloc[0].type)
                except:
                    tss.append(mastertable.loc[mastertable.ministock_name==md[j].replace('.','_')].iloc[0].type)

    df = pd.DataFrame([ts,tss,sp,hbid2,otu,hb]).transpose()
    df.columns = ['Centroid Type','Strain Type','Centroid Species*','Centroid HB ID', 'Centroid Qiime2 ID','Holobiome Strain in Centroid']
    df.to_csv('biom_list.tsv',sep='\t', index = False)
    return mastertable
def qiime2vsearch(clean_seqs = 'truncated.fna', pct = 0.987):
    import os
    import shutil
    try:
        os.mkdir('tmp')
    except:
        print('tmp directory already exists, will overwrite')
        shutil.rmtree('tmp')
        os.mkdir('tmp')
    # read in samps into qiimes frustrating archive format
    os.system("qiime tools import --input-path %s --output-path seqs.qza --type 'SampleData[Sequences]'"%(clean_seqs))
    print('read')
    # run vsearch
    os.system("qiime vsearch dereplicate-sequences --i-sequences seqs.qza --o-dereplicated-table table.qza --o-dereplicated-sequences rep-seqs.qza")
    print('derep')

    # get the actual info you want out of qiimes frustrating archive format output
    os.system("qiime vsearch cluster-features-de-novo --i-table table.qza --i-sequences rep-seqs.qza --p-perc-identity %f --o-clustered-table table-dn-%s.qza --o-clustered-sequences rep-seqs-dn-%s.qza"%(pct,str(pct),str(pct)))
    print('cluster')

    # unzip table-dn-0.987.qza to get at the biom file
    os.system('unzip table-dn-%s.qza -d tmp'%(str(pct)))
    print('unzip biom')



    # convert biom to tsv
    cwd = os.getcwd()
    oi = os.listdir(cwd+'/tmp')
    table_dir = cwd+'/tmp/'+oi[0]+'/data/feature-table.biom'
    os.system('biom convert -i %s -o %s.%s.table.from_biom.tsv --to-tsv'%(table_dir, clean_seqs,str(pct)))
    os.system('rm -r tmp')
    clean_biom('%s.%s.table.from_biom.tsv'%(clean_seqs,str(pct)))

    biom_to_list('%s.%s.table.from_biom.tsv'%(clean_seqs,str(pct)))
