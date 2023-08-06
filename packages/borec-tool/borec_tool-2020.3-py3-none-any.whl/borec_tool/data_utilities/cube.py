from dataclasses import dataclass, field
from numpy import ndarray
from spectral.io.bilfile import BilFile
import numpy as np
from PyQt5.QtGui import QPixmap

@dataclass
class DataHdr:
    data: ndarray
    header: BilFile

@dataclass
class Hyperspectral:
    preview: QPixmap
    raw: DataHdr = None
    darkref: DataHdr = None
    whiteref: DataHdr = None
    whitedarkref: DataHdr = None
    reflectance: ndarray = field(default=None, repr=True, init=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            value = v
            if k != 'preview' and isinstance(v, dict):
                value = DataHdr(**v)
            setattr(self, k, value)
        self.__post_init__()

    def __post_init__(self):
        if self.reflectance is None:
            raw = self.raw.data
            darkref = self.darkref.data
            whiteref = self.whiteref.data

            numerator = np.subtract(raw, darkref)
            denom = np.subtract(whiteref, darkref)
            hdr = self.raw.header
            hdr.dtype = np.dtype(np.float32).str
            self.reflectance = DataHdr(data=np.divide(numerator, denom), header=hdr)


