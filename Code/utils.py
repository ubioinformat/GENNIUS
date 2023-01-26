import requests
from collections import Counter
from rdkit import Chem
from tqdm import tqdm
from time import sleep
import logging
import os

def seq2rat(sequence):

    # dict count stores information for each sequence

    dict_count = dict(Counter(sequence))
    len_seq = len(sequence)

    list_aminos = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 
                    'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 
                    'T', 'W', 'Y', 'V']

    list_aminos.sort()

    out = [round(dict_count.get(amino,0)/len_seq, 5) for amino in list_aminos]
    return out


def get_sequences(list_proteins):
    dict_protein_seq = {}

    # slice if large
    if len(list_proteins) > 500:
        n = 400
        list_proteins = [list_proteins[i:i + n] for i in range(0, len(list_proteins), n)]
    else:
        n = int(len(list_proteins)/2)
        list_proteins = [list_proteins[i:i + n] for i in range(0, len(list_proteins), n)]
    
    for lts in tqdm(list_proteins, desc='Retrieving uniprot sequence'):
        unilist = ','.join(lts)
        r = requests.get(f'https://rest.uniprot.org/uniprotkb/accessions?accessions={unilist}')
        jsons = r.json()['results']
        for data in tqdm(jsons, desc='saving to dict'):
            name = data.get('primaryAccession')
            res = data.get('sequence').get('value')
            dict_protein_seq[name] = res
        if len(list_proteins)>50:
            sleep(1)
    
    return dict_protein_seq


def pubchem2smiles_batch(drugs, size=500):

    pub2smiles = {}

    # split the list in chunks of 100 to make requests
    drugs = [str(drug) for drug in drugs]
    split_list = lambda big_list, x: [
        big_list[i : i + x] for i in range(0, len(big_list), x)
    ]

    drug_chunks = split_list(drugs, size)
    for chunk in tqdm(drug_chunks, desc='Requesting SMILES to PubChem'):
        chunk = ",".join(chunk)
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{chunk}/json"
        response = requests.get(url)
        if response.status_code == 200:
            jsons = response.json()
            for id in jsons.get("PC_Compounds"):
                cid, smile, inchikey = None, None, None
                cid = str(id.get('id').get('id').get('cid'))
                smile = [prop.get('value').get('sval') for prop in id.get('props') 
                        if prop.get('urn').get('label') == 'SMILES' 
                        and prop.get('urn').get('name') == 'Canonical'][0]
                
                if smile:
                    try:
                        mol1 = Chem.MolFromSmiles(str(smile))
                        fp1  = Chem.RDKFingerprint(mol1)
                    except:
                        logging.info(f'Error for pubchemid {cid}')
                        smile = None
                pub2smiles[cid] = smile

    return pub2smiles

