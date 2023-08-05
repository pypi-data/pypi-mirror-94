import numpy as np
import math
def rand (lin,col):
    m = np.random.rand(lin,col)
    return m
def svd (M):
    Q, s, Vt = np.linalg.svd(M, full_matrices=False)
    S = np.diag(s)
    return Q,S
def diag (M):
    R = np.diag(M)
    return R
def eps (M):
    return np.finfo(M).eps
def size (M):
    [n,m]=np.matrix(M).shape
    return (n,m)
def double(text):
    R=[]
    for i in text:
        r = list(i.encode('ascii'))
        R.append(r)
    return np.array(R)
def repmat(M,m,n=1):
    return np.tile(M,(m,n))
def prod(A):
    R=np.prod(A,axis=0)
    return R
def find(a):
     return np.where(a)
def zeros(lin,col):
    M = np.zeros((lin,col))
    return M
def floor(n):
    r = math.floor(n)
    return r
def ones(lin,col):
    M = np.ones((lin,col))
    return M
def length(n):
    r = len (n)
    return r
def ceil(n):
    r = math.ceil(n)
    return r