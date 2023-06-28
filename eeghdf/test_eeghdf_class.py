import os
import h5py
import numpy as np
from . import EEGHDFUpdater
fpath = "test.h5"

def test_add_eeglab():
    fs = 500
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    ehf.add_eeglab("./matlab/test.set")

    with h5py.File(fpath) as h5:
        assert h5["origin"].attrs["fs"] == fs
        assert h5["origin"].attrs["count"] == 80
        assert h5["origin/79"].shape == (64,500)
        assert h5["origin/79"].attrs["label"] == "right"
    ehf.remove_hdf()
    
def test_prepro():
    fs = 500
    group_name ="test2355"
    ehf = EEGHDFUpdater(fpath,fs=fs,lables=["left","right"])
    ehf.remove_hdf()
    
    def prepro_func(x:np.ndarray):
         return np.ones((2,x.shape[1]))
    ehf.add_eeglab("./matlab/test.set")
    ehf.preprocess(group_name,prepro_func)

    with h5py.File(fpath) as h5:
        assert h5[group_name].attrs["fs"] == fs
        assert h5[group_name].attrs["count"] == 80
        assert np.all(h5[f"{group_name}/79"][()] == np.ones((2,500)))
        assert h5[f"{group_name}/79"].attrs["label"] == "right"
    
    ehf.remove_hdf()