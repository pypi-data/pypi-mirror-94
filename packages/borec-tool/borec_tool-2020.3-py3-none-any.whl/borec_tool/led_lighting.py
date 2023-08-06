from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QPushButton, QWidget, QListWidget, \
    QListWidgetItem, QLineEdit, QFormLayout, QCheckBox, QAction, QStyle
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIntValidator
import PyQt5
import numpy as np
from borec_tool import processing as process_bezier_svg
import borec_tool.data_utilities.loader as loader
from pathlib import Path
from tkinter import Tk
import os
from tkinter.filedialog import askopenfilename
import webbrowser
from borec_tool.data_utilities.loader import get_name
from .led_spectra import LedSpectra
from pkg_resources import resource_filename
# from radiance import Radiance


class AddItem(QWidget):
    update = pyqtSignal(dict)

    def get_dir(self):
        root = Tk()
        root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
        self.dir = Path(askopenfilename())
        self.dir_lbl.setText(str(self.dir))
        self.dir_lbl.adjustSize()
        return self.dir

    @pyqtSlot()
    def conf(self):
        new_led = {}
        dict_data = {}
        x = []
        y = []
        x.append(int(self.x_scale_min.text()))
        x.append(int(self.x_scale_max.text()))
        y.append(int(self.y_scale_min.text()))
        y.append(int(self.y_scale_max.text()))
        dict_data['path'] = "./" + os.path.relpath(self.dir)
        dict_data['x_scale'] = x
        dict_data['y_scale'] = y
        dict_data['link'] = None
        new_led[str(get_name(self.dir))] = dict_data
        loader.save_graphs(new_led)
        self.update.emit(new_led)

    def __init__(self):
        super(AddItem, self).__init__()
        self.window = QWidget()
        self.add_layout = QFormLayout(self.window)

        self.dir_lbl = QLabel(self)
        self.dir = QPushButton("Choose", self)
        self.dir.clicked.connect(self.get_dir)

        self.x_scale_min = QLineEdit(self)
        self.x_scale_min.setMaxLength(5)
        self.x_scale_min.setValidator(QIntValidator())
        self.x_scale_max = QLineEdit(self)
        self.x_scale_max.setMaxLength(5)
        self.x_scale_max.setValidator(QIntValidator())

        self.y_scale_min = QLineEdit(self)
        self.y_scale_min.setMaxLength(5)
        self.y_scale_min.setValidator(QIntValidator())
        self.y_scale_max = QLineEdit(self)
        self.y_scale_max.setMaxLength(5)
        self.y_scale_max.setValidator(QIntValidator())

        self.accept = QPushButton("Confirm", self)
        self.accept.clicked.connect(self.conf)
        self.accept.clicked.connect(self.window.close)
        self.cancel = QPushButton("Cancel", self)
        self.cancel.clicked.connect(self.window.close)

        self.add_layout.addRow("File: ", self.dir)
        self.add_layout.addRow("Directory: ", self.dir_lbl)
        # self.add_layout.addRow(self.dir_lbl)
        self.add_layout.addRow("Minimum value of X scale: ", self.x_scale_min)
        self.add_layout.addRow("Maximum value of X scale: ", self.x_scale_max)
        self.add_layout.addRow("Minimum value of Y scale: ", self.y_scale_min)
        self.add_layout.addRow("Maximum value of Y scale: ", self.y_scale_max)
        self.add_layout.addRow(self.accept, self.cancel)

        # self.layout.addWidget(self.x_scale)
        # self.layout.addWidget(self.y_scale)
        self.window.setLayout(self.add_layout)

    def add_item(self):
        self.window.show()


class Led(QWidget):
    checked_items = []
    sig_radiance = pyqtSignal(dict)

    def update_checked_items(self):
        for index in range(self.listwidget.count()):
            if self.listwidget.item(index).checkState() == PyQt5.Checked:
                self.checked_items.append(self.listwidget.item(index))

    #        return checked_items

    def createLedDisplayActions(self):
        for i in range(len(self.graphs)):
            self.led_display_actions.append(
                QAction(self, visible=False,
                        triggered=self.display_svg))
        return self.led_display_actions

    def display_svg(self, name):
        x = range(self.graphs[name]['x_scale'][0], self.graphs[name]['x_scale'][1])
        toplot_f = process_bezier_svg.svg_to_function(self.graphs[name]['path'], self.graphs[name]['x_scale'],
                                                      self.graphs[name]['y_scale'])
        toplot = [(lambda x: toplot_f(v))(v) for v in x]
        self.ax.clear()
        self.ax.plot(x, toplot)
        self.ax.figure.canvas.draw()

    def __init__(self):
        super(Led, self).__init__()
        # init
        self.layout = QGridLayout()
        self.listwidget = QListWidget()
        self.canvas = FigureCanvas(Figure(figsize=(4, 2)))
        self.ax = self.canvas.figure.subplots()
        self.add = QPushButton("+ Add new", self)
        self.add_window = AddItem()
        self.add.clicked.connect(self.add_window.add_item)
        self.add_window.update.connect(self.update_led)
        # self.add.clicked.connect(self.add_item)
        # load
        self.graphs = loader.load_graphs()
        self.index = 0
        self.led_spectra = LedSpectra(self.graphs)
        self.led_spectra.sig_switch.connect(self.update_radiance)
        for name in self.graphs.keys():
            if os.path.exists(resource_filename('borec_tool.resources',self.graphs[name]['path'])):
                item = QListWidgetItem()
                widget = self.create_widget(name)
                item.setSizeHint(widget.sizeHint())
                self.listwidget.addItem(item)
                self.listwidget.setItemWidget(item, widget)
        self.layout.addWidget(self.listwidget, 0, 0)
        self.layout.addWidget(self.add, 1, 0)
        #        self.layout.addWidget(self.canvas, 0, 1, 1, 1)
        self.layout.addWidget(self.led_spectra, 0, 1, 1, 1)
        self.setLayout(self.layout)

    def create_widget(self, name):
        widget = QWidget()
        widgetCheck = QCheckBox(name)
        widgetCheck.stateChanged.connect(lambda state, x=name: self.led_spectra.display_svg(x))
        widgetButton = QPushButton("")
        widgetButton.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxInformation')))
        widgetButton.setMaximumWidth(30)
        if self.graphs[name]['link'] is not None:
            widgetButton.clicked.connect(lambda: webbrowser.open(self.graphs[name]['link']))
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(widgetCheck)
        widgetLayout.addWidget(widgetButton)
        widget.setLayout(widgetLayout)
        return widget

    def update_led(self, new_led):
        self.graphs = {**self.graphs, **new_led}
        item = QListWidgetItem()
        widget = QWidget()
        widgetCheck = QCheckBox(list(new_led.keys())[0])
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(widgetCheck)
        widget.setLayout(widgetLayout)
        item.setSizeHint(widget.sizeHint())

        self.listwidget.addItem(item)
        self.listwidget.setItemWidget(item, widget)
        self.layout.update()

    def update_radiance(self, spectra):
        min = 1000
        max = 0
        svg_all = []
        for key in spectra.keys():
            if spectra[key].status:
                if min > spectra[key].min:
                    min = spectra[key].min
                if max < spectra[key].max:
                    max = spectra[key].max
        for i in range(min, max):
            var = 0
            for key in spectra.keys():
                if spectra[key].status and spectra[key].x[0] <= i <= spectra[key].x[-1]:
                    var = var + spectra[key].y[i - spectra[key].x[0]]
            svg_all.append(var)
        svg_all = np.array(svg_all)
        if len(svg_all)>0:
            svg_all = svg_all/svg_all.max()
        spectra_all = {'x_scale': [min, max], 'y_scale': svg_all}
        if min < 720 and max > 400:
            self.sig_radiance.emit(spectra_all)
