import numpy as np
from borec_tool.data_utilities.cube import DataHdr

def reflectance(data):
    raw = data.raw.data
    darkref = data.darkref.data
    whiteref = data.whiteref.data

    header = data.raw.header

    numerator = np.subtract(raw, darkref)
    denom = np.subtract(whiteref, darkref)
    reflectance = data=np.divide(numerator, denom)
    header.dtype = np.dtype(np.float32).str
    return DataHdr(data=reflectance, header=header)