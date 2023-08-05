from .matlab_like import repmat,size
from .aa2int import aa2int
from .nt2int import nt2int
import numpy as np
def aa2idx(xseq, defSize):
    [n,m] = size(xseq)
    if defSize == 20:
        vls = (np.array(aa2int(xseq))-1).T
    elif defSize == 4:
        vls = (np.array(nt2int(xseq))-1).T
    pot = repmat(list(range(0,m)),n,1).T
    t=repmat(defSize,m,n)
    mret = np.sum((t**pot)*vls,axis=0)+1
    return mret