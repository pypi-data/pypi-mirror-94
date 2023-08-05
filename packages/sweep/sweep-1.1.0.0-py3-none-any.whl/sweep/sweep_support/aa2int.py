import numpy as np
import pandas as pd
def aa2int(aa_list):
    aa_list=pd.DataFrame(np.char.lower(aa_list))
    map = { "a":1,
            "b":21,
            "c":5,
            "d":4,
            "e":7,
            "f":14,
            "g":8,
            "h":9,
            "i":10,
            "j":0,
            "k":12,
            "l":11,
            "m":13,
            "n":3,
            "o":0,
            "p":15,
            "q":6,
            "r":2,
            "s":16,
            "t":17,
            "u":0,
            "v":20,
            "w":18,
            "x":23,
            "y":19,
            "z":22,
            "*":24,
            "-": 25,
            "?": 0
            }
    aa_list=aa_list.replace(map)
    return aa_list