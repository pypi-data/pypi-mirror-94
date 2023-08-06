from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import imageio
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QListView, QTreeView, QFileSystemModel, QAbstractItemView
from bs4 import BeautifulSoup
import spectral.io.envi as envi
import yaml
from pathlib import Path
from pkg_resources import resource_filename
import os

from borec_tool.data_utilities.cube import Hyperspectral
from borec_tool.gui.ndarray2pixmap import ndarray2pixmap


def file_not_found(text=None):
    msg = QMessageBox()
    msg.setText(text)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec()


def load_history():
    try:
        cwd = os.getcwd()
        config_file = open(Path(cwd)/"configuration.yaml", "r")
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        return config
    except FileNotFoundError:
        return []

def save_history(files):
    # for backward compatibility, save file list as dictionary
    # config_dict = {}
    # for file in files:
    #     config_dict[Path(file).name] = str(file)
    cwd = os.getcwd()
    config_file = open(Path(cwd)/"configuration.yaml", "w")
    yaml.dump(files, config_file)
    config_file.close()


def get_name(dir):
    return dir.name


class Manifest():

    def __init__(self, directory):
        file = directory / 'manifest.xml'
        f_manifest = open(file, "r")
        self.manifest_data = BeautifulSoup(f_manifest, "lxml")

    def keys(self):
        return set([elem['type'] for elem in self.manifest_data.find_all('file')])

    def hdr_file(self, type):
        return [elem.string for elem in self.manifest_data.find_all('file') if
         (elem['type'] == type and elem['extension'] == 'hdr')][0]

    def data_file(self, type):
        return [elem.string for elem in self.manifest_data.find_all('file') if
         (elem['type'] == type and elem['extension'] in ['raw', 'dat'])][0]

    def preview_file(self):
        return [elem.string for elem in self.manifest_data.find_all('file') if
                (elem['type'] == 'preview')][0]


def get_manifest(directory, format):
    capt = directory / 'manifest.xml'
    f_manifest = open(capt, "r")
    manifest_data = BeautifulSoup(f_manifest, "lxml")
    b_files = manifest_data.find_all('file', {'type': format})
    f_manifest.close()
    return b_files # list of 2 elements, first is directory of header, second is directory of data


def get_hdr(directory):
    try:
        hdr = envi.open(directory)
    except Exception as e:
        if e.__class__.__name__ == 'FileNotFoundError':
            file_not_found(f'Error in manifest.xml: header {directory} not found')
        return None
    return hdr

def get_preview(path):
    image = imageio.imread(path, pilmode='RGB')
    return ndarray2pixmap(image)

def read_cube(directory):
    manifest = Manifest(directory)
    f_types = manifest.keys()
    # keys = ['raw', 'darkref', 'whiteref', 'whitedarkref']
    data = {}
    # raw, darkref, whiteref, whitedarkref
    if 'raw' in f_types:
        for type in f_types:
            if type in ['raw', 'darkref', 'whiteref', 'whitedarkref']:
                data[type] = open_file(directory, manifest, type)
    else:
        type = 'reflectance'
        if  type in f_types:
            data[type] = open_file(directory, manifest, type)
    data['preview'] = get_preview(Path(directory)/manifest.preview_file())
    return data


def open_file(directory, manifest, format):
    output = None
    lib = get_hdr(directory / manifest.hdr_file(format))
    if lib is not None:
        rawfile = directory / manifest.data_file(format)
        img = envi.open(directory / manifest.hdr_file(format), rawfile)
        im = np.fliplr(img.load().swapaxes(1, 0))
        output = {'data': im, 'header': lib}
    return output


def load_graphs():
    cwd = os.getcwd()
    try:
        with open(Path(cwd) / "graph.yaml", "r") as graph_file:
            return yaml.load(graph_file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        try:
            with open(resource_filename('borec_tool.resources', 'graph.yaml'), "r") as graph_file:
                graphs = yaml.load(graph_file, Loader=yaml.FullLoader)
            with open(Path(cwd) / "graph.yaml", "w") as save_file:
                yaml.dump(graphs, save_file)
            return graphs
        except FileNotFoundError:
            return None


def save_graphs(graph):
    try:
        graph_file = open(resource_filename('borec_tool.resources', 'graph.yaml'), "r")
        graph_dict = yaml.load(graph_file, Loader=yaml.FullLoader)
        graph_file.close()
    except FileNotFoundError:
        graph_dict = {}
    new_graph_dict = {**graph_dict, **graph}
    graph_file = open(resource_filename('borec_tool.resources','graph.yaml'), "w")
    yaml.dump(new_graph_dict, graph_file)
    graph_file.close()


def get_dir(text):
    file_dialog = QFileDialog(caption=text)
    file_dialog.setFileMode(QFileDialog.Directory)
    file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
    file_dialog.setOption(QFileDialog.DontUseNativeDialog)
    for view in file_dialog.findChildren((QListView, QTreeView)):
        if isinstance(view.model(), QFileSystemModel):
            view.setSelectionMode(QAbstractItemView.MultiSelection)
    if file_dialog.exec():
        paths = file_dialog.selectedFiles()
    return [Path(path) for path in paths]


def _file_error(message=None, e=None):
    if e is not None:
        if hasattr(e, 'message'):
            message=f"Error reading data: {e.message}"
        else:
            message=f"Error reading data: {e}"
    msg = QMessageBox()
    msg.setText(message)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec()


def open_folder(directory):
    output = None
    try:
        full_data_dict = read_cube(directory)
        output = Hyperspectral(**full_data_dict)
    except FileNotFoundError:
        if str(directory):
            text = f'Directory: {str(directory)} \nNo valid hyperspectral data.'
        else:
            text = 'Valid file not found!'
        _file_error(message=text)
    except TypeError:
        _file_error(message="Error - no file selected?")
    except EOFError:
        _file_error(message="Data corrupted\nor mismatch between data and header")
    except Exception as e:
        _file_error(e=e)
    return output