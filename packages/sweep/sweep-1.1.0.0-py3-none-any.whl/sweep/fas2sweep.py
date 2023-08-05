from .sweep_support import fastaread,mask2vec,generate_chunk,length,zeros,ceil,size
import scipy.io as sio
import hdf5storage
import re
import os
import numpy as np
import pandas as pd
from .getMatrixFile import getMatrixFile
import sys
from scipy.sparse import lil_matrix
import dask.dataframe as dd
from tqdm import tqdm

def print_error(text):
    sys.stderr.write('\x1b[1;31m' + 'SWEEP FAIL ALERT: ' + text.strip() + '\x1b[0m' + '\n')

def fas2sweep(xfas,out_mat_file=None,orth_mat=None,mask=None,verbose=False,
              chunk_size=2E+3,projection=True,fasta_type='AA'):
    if mask is None:
        mask = np.array([2,1,2])
    if fasta_type == 'AA':
        defSize = 20
    elif fasta_type == 'NT':
        defSize = 4
        
    mask_type = type(sum(list(mask)))
    mask_sum = sum([mask[0],mask[2]])
    if len(mask) != 3 or not (mask_type == int or mask_type == np.int32):
        message = 'Mask must be an array with 3 integer values.'
        print_error(message)
        return
    elif not (orth_mat is None) and not projection:
        print_error('The orth_mat parameter is unnecessary if projection=False.')
        return
    elif (mask_sum > 5 and fasta_type == 'AA') or (mask_sum > 8 and fasta_type == 'NT'):
        print_error('The size of the mask parts is too high.')
        return
    
    libLocal = re.sub('[\\\/][^\\\/]+$','',os.path.realpath(__file__))
    
    # Extracts the sequences from the fasta file
    if isinstance(xfas, str):
        fas_cell = fastaread(xfas)
    else:
        fas_cell = xfas
    headers=[]
    seqs=[]
    for i in fas_cell:
        seqs.append(str(i.seq))
        headers.append(str(i.description))
    seqs = np.array(seqs)
    headers = np.array(headers)

    # Checking if all sequences are bigger than de mask size
    vlen = np.vectorize(len)
    seq_size = np.array(vlen(seqs))
    headers_small = seq_size < sum(mask);
    if sum(headers_small.astype(int)) > 0:
        message = 'There are sequences smaller than the mask size.'
        print_error(message)
        return
        
    # Calculate chunks number
    chunks = ceil(len(seqs)/chunk_size)
    idx = generate_chunk(chunks, length(seqs))-1;

    rows_size = defSize**mask[0]*defSize**mask[2]
    if projection:
        if orth_mat is None:
            if rows_size != 160000:
                message = ('The default matrix is intended for the sweep of '
                           'amino acids with the default mask, for other '
                           'cases you can disable the projection or set the '
                           'orth_mat parameter.')
                print_error(message)
                return
            # Download default projection matrix if not available
            getMatrixFile(libLocal+'/orthMat_default600.mat')
            orth_mat = hdf5storage.loadmat(libLocal+
                                           '/orthMat_default600.mat')['orthMat_default600'].astype('float')
        else:
            if size(orth_mat)[0] != rows_size:
                message = ("The defined orth_mat does not have the "
                           "appropriate dimensions."
                           "\nThe number of lines must be:"
                           "\n(x**mask[0])*(x**mask[2]),"
                           "\nwhere x=20, if fasta_type==\'AA\',"
                           "\nand x=4, if fasta_type==\'NT\'.")
                print_error(message)
                return
        resultMat = zeros(len(seqs),size(orth_mat)[1])
    else:
        resultMat = lil_matrix((len(seqs), rows_size), dtype=np.int8)
        
    m2v = lambda a: mask2vec(a, mask, defSize)[0]
    
    if verbose:
        message = 'Running SWEEP transformation...'
        print(message, flush=True)
        
    # Run sweep on chunks
    with tqdm(total=chunks,desc="Progress", disable=(not verbose), position=0, leave=True) as pbar:
        for i in range(0,chunks):
            parcM = seqs[np.array(range(int(idx[i,0]),int(idx[i,1])+1))]
            parcM = pd.Series(parcM)
            parcM = dd.from_pandas(parcM, npartitions=1)
            
            if projection:
                W160k = np.array(parcM.apply(m2v,meta=object).compute().to_list())
                W160k = np.dot(W160k,orth_mat)
            else:
                W160k = parcM.apply(m2v,meta=object).compute()
                W160k = np.array(W160k.to_list())
            resultMat[int(idx[i,0]):int(idx[i,1])+1,:] = W160k
            pbar.update(1)
            
    if not (out_mat_file is None):
        sio.savemat(out_mat_file,{re.sub('\..+','',out_mat_file):resultMat})
    return resultMat