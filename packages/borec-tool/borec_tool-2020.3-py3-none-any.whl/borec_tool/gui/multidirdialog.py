from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox


class MultiDirDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)

        self.setFileMode(QFileDialog.FileMode.ExistingFiles)
        self.setOption(QFileDialog.Option.DontUseNativeDialog)
        self.setOption(QFileDialog.Option.ShowDirsOnly)

        def accepted():
            self.close()
            self.accepted.emit()

        button_box = self.findChild(QDialogButtonBox, 'buttonBox')
        button = button_box.button(QDialogButtonBox.StandardButton.Open)
        button.clicked.disconnect()
        button.clicked.connect(accepted)