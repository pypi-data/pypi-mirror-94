import os

from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QFileDialog, QWidget

import numpy as np
import scipy.io
from pathlib import Path

folder = "output"

class Saver(QWidget):

    file_path = None

    def save_as_npz(self, data, file_path, directory=None):
        if directory is not None:
            self.create_directory(directory)
            self.update_manifest(file_path.name, file_path.parent, "npz")
        np.savez(file_path, data)

    def save_as_mat(self, data_dict, file_path, directory=None):
        if directory is not None:
            self.create_directory(directory)
            self.update_manifest(file_path.name, file_path.parent, "mat")
        scipy.io.savemat(file_path, data_dict)


    def create_directory(self, directory, name=folder):
        path = directory / name
        try:
            os.mkdir(path)
        except:
            print('Already exists')

    def save_as(self, data):
        path = self.file_path if self.file_path is not None else '.'
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Numpy data (*.npz)", "Matlab data (*.mat)"])
        dlg.selectNameFilter("Numpy data (*.npz)")
        dlg.setDefaultSuffix('npz')
        dlg.setDirectory(path)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        filenames = None
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.file_path = Path(filenames[0])
            return self.file_path.name
        else:
            return None

    def save(self, data):
        if self.file_path is None:
            self.save_as(data)
        file_path = self.file_path
        if file_path.suffix == '.npz':
            self.save_as_npz(data, file_path)
        elif file_path.suffix == '.mat':
            self.save_as_mat({'output': data}, file_path)


    def update_manifest(self, file_name, directory, data_type, folder_name=folder):
        manifest = directory / 'manifest.xml'

        with open(manifest, "r") as f_manifest:
            manifest_data = BeautifulSoup(f_manifest, "xml")
            # create a new tag
            new_tag = manifest_data.new_tag("file")
            new_tag['extension'] = 'raw'
            new_tag['type'] = data_type
            new_tag.string = folder_name + file_name
            manifest_data.manifest.insert(-1, new_tag)

        with open(manifest, "w") as f_manifest:
            f_manifest.write(str(manifest_data))
