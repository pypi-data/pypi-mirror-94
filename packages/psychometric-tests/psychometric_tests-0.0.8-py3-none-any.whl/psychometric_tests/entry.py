from PyQt5 import QtCore, QtGui, QtWidgets

from psychometric_tests import defs
from psychometric_tests.ant.main import ant
from psychometric_tests.nback.main import nback
from psychometric_tests.rat.main import rat
from psychometric_tests.shared.misc_funcs import open_file

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class EntryDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.selected = None

        self.setWindowIcon(
            QtGui.QIcon(str(defs.resource_dir() / 'options.svg')))

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setWindowTitle('Tasks')
        main_layout = QtWidgets.QHBoxLayout(self)

        main_layout.addWidget(
            self.app_button('Attention Network Test (ANT)',
                            QtGui.QIcon(
                                str(defs.resource_dir() / 'ant.svg'))))
        main_layout.addWidget(
            self.app_button('Remote Associates Test (RAT)',
                            QtGui.QIcon(
                                str(defs.resource_dir() / 'rat.svg'))))
        main_layout.addWidget(
            self.app_button('N-Back Test',
                            QtGui.QIcon(
                                str(defs.resource_dir() / 'nback.svg'))))

        settings_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(settings_layout)

        settings_button = QtWidgets.QPushButton(self)
        settings_button.setIcon(QtGui.QIcon(
            str(defs.resource_dir() / 'settings.svg')))
        settings_button.setIconSize(QtCore.QSize(12, 12))
        settings_button.setFlat(True)
        settings_button.clicked.connect(self.open_settings_file)
        settings_layout.addWidget(settings_button)
        settings_layout.addStretch()

    def app_button(self, name, icon):
        button = QtWidgets.QToolButton(self)
        button.setIcon(icon)
        button.setText(name)
        button.setIconSize(QtCore.QSize(64, 64))
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.clicked.connect(self.set_selected)
        button.setMinimumWidth(200)
        return button

    def set_selected(self):
        self.selected = self.sender().text()
        self.accept()

    @staticmethod
    def open_settings_file():
        settings_file = defs.project_root() / 'settings.json'
        open_file(settings_file)


def run():
    app = QtWidgets.QApplication([])

    entry = EntryDialog()
    if entry.exec() == QtWidgets.QDialog.Accepted:
        print(entry.selected)
        if entry.selected == 'Attention Network Test (ANT)':
            ant()
        elif entry.selected == 'Remote Associates Test (RAT)':
            rat()
        elif entry.selected == 'N-Back Test':
            nback()


if __name__ == '__main__':
    run()
