def datamine(query,
             email,
             api_key,
             retmax = 500,
             db = 'protein',
             rettype = 'fasta',
             retmode = 'text',
             idtype='acc'):

    import os
    from Bio import Entrez

    # let NCBI know who you are
    if api_key != 'None':
        Entrez.api_key = api_key
    Entrez.email = email

    # make a list of our data
    data = []
    handle = Entrez.esearch(db=db, retmax = retmax,term=query, idtype=idtype)
    record = Entrez.read(handle)
    search_results = record['IdList']

    # Fetch the data
    for i in search_results:
        fetch_handle = Entrez.efetch(
            db=db,
            rettype=rettype,
            retmode=retmode,
            id=i,
        )
        # this is our fasta as string
        fasta = fetch_handle.read()
        fetch_handle.close()
        data.append(fasta)
    return data

def occurs(symbol, string):
    return [j for j, x in enumerate(string) if x == symbol]

def multifasta_protein(csv, outfile, email, api_key):
    '''Takes CSV with Accession Numbers'''
    import pandas as pd
    #open the outfile to write
    out = open(outfile, 'w')
    # dataframe pandas
    df = pd.read_csv(csv)
    new_csv = []
    #make a list of accessions to loop through
    queries = list(df.accession.values)
    for query in queries:
        fasta = datamine(query, email, api_key)
        for i in fasta:
            char = occurs('\n',i)
            out.write(i[:char[1]]+i[char[1]+1:].replace('\n','')+'\n')
            new_csv.append([query,i[:char[0]],i[char[0]+1:].replace('\n','')])
    ndf = pd.DataFrame(new_csv, columns = ['accession','head','fasta'])
    ndf.to_csv(outfile+'.csv', index = False)
    out.close()
