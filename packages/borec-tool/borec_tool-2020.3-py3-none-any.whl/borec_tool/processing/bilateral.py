from skimage.restoration import denoise_bilateral
import numpy as np

def bilateral(data, **kwargs):
    nchanels = data.shape[2]
    output = np.moveaxis(np.array([denoise_bilateral(data[..., band], **kwargs) for band in range(nchanels)]), 0, -1)
    return output

