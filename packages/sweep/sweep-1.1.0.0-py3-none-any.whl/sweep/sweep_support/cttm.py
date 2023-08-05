def cttm(fasta):
    A = []
    for i in fasta:
        A.append(len(i.seq))
    return A