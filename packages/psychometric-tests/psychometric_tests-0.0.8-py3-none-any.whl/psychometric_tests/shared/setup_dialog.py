from distutils.util import strtobool
from functools import partial
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from psychometric_tests import defs
import psychometric_tests.shared.misc_funcs as mf

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class SetupDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setup_info = {}
        self.init_file = str(defs.project_root() / 'setup.ini')
        self.setWindowIcon(QtGui.QIcon(str(defs.resource_dir() / 'setup.svg')))

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.user_inputs = {}
        self.save_dialog = QtWidgets.QFileDialog(self)

    def make(self):
        self.input_settings()
        self.setup_ui()

        if Path(self.init_file).is_file():
            settings = QtCore.QSettings(self.init_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_restore(settings)

        self.overwrite_restored_inputs()

    def input_settings(self):
        pass

    def overwrite_restored_inputs(self):
        pass

    def setup_ui(self):

        self.resize(450, 100)
        self.setWindowTitle('Test Setup')
        main_layout = QtWidgets.QVBoxLayout(self)

        for label, widget in self.user_inputs.items():
            row = self.setup_input_row(label, widget)
            main_layout.addLayout(row)

        finish_button = QtWidgets.QPushButton(self)
        finish_button.setText('Finish Setup')
        main_layout.addWidget(finish_button)
        finish_button.clicked.connect(self.finish_clicked)

    def setup_input_row(self, label_text, widget):
        h_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self)
        label.setText(label_text + ': ')
        label.setMinimumWidth(100)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Minimum)
        h_layout.addWidget(label)
        h_layout.addWidget(widget)

        if ('Directory' in label_text) and isinstance(widget,
                                                      QtWidgets.QComboBox):
            dir_button = QtWidgets.QPushButton(self)
            dir_button.setText('…')
            dir_button.setMaximumWidth(20)
            dir_button.setFocusPolicy(QtCore.Qt.NoFocus)
            dir_button.clicked.connect(partial(self.add_dir, widget))
            h_layout.addWidget(dir_button)

        return h_layout

    def add_dir(self, widget):
        items = [widget.itemText(i) for i in range(widget.count())]
        selected_dir = self.save_dialog.getExistingDirectory(directory=str(
            mf.get_desktop()))
        if selected_dir:
            new_dir = Path(selected_dir).absolute()
            if str(new_dir) in items:
                widget.setCurrentIndex(items.index(str(new_dir)))
            elif new_dir.is_dir():
                widget.insertItem(0, str(new_dir))
                widget.setCurrentIndex(0)

    def finish_clicked(self):
        for label, widget in self.user_inputs.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                if widget.text() == '':
                    QtWidgets.QMessageBox.critical(
                        self, 'Error', 'Please fill in {}'.format(label))
                    break
            elif isinstance(widget, QtWidgets.QComboBox):
                if widget.currentIndex == -1:
                    QtWidgets.QMessageBox.critical(
                        self, 'Error', 'Please fill in {}'.format(label))
                    break
                elif 'Directory' in label:
                    if not Path(widget.currentText()).is_dir():
                        QtWidgets.QMessageBox.critical(
                            self, 'Error', 'Invalid Directory')
                        break

        else:
            settings = QtCore.QSettings(self.init_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_save(settings)
            for label, widget in self.user_inputs.items():
                if isinstance(widget, QtWidgets.QLineEdit):
                    self.setup_info[label] = widget.text()
                elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                    self.setup_info[label] = widget.value()
                elif isinstance(widget, QtWidgets.QSpinBox):
                    self.setup_info[label] = widget.value()
                elif isinstance(widget, QtWidgets.QComboBox):
                    self.setup_info[label] = widget.currentText()
                elif isinstance(widget, QtWidgets.QCheckBox):
                    self.setup_info[label] = widget.isChecked()
            print(self.setup_info)
            self.accept()

    def gui_save(self, settings):
        for label, widget in self.user_inputs.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                value = widget.text()
                settings.setValue('Setup/' + label, value)
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                value = widget.value()
                settings.setValue('Setup/' + label, value)
            elif isinstance(widget, QtWidgets.QSpinBox):
                value = widget.value()
                settings.setValue('Setup/' + label, value)
            elif isinstance(widget, QtWidgets.QComboBox):
                if 'Directory' in label:
                    items = [widget.itemText(i) for i in range(widget.count())]
                    settings.setValue('Setup/' + label + '_items', items)
                    index = widget.currentIndex()
                    settings.setValue('Setup/' + label + '_index', index)
                else:
                    value = widget.currentText()
                    settings.setValue('Setup/' + label, value)
            elif isinstance(widget, QtWidgets.QCheckBox):
                state = widget.isChecked()
                settings.setValue('Setup/' + label, state)

    def gui_restore(self, settings):
        for label, widget in self.user_inputs.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                value = settings.value('Setup/' + label)
                if value is not None:
                    widget.setText(value)
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                value = float(settings.value('Setup/' + label))
                if value is not None:
                    widget.setValue(value)
            elif isinstance(widget, QtWidgets.QSpinBox):
                value = int(settings.value('Setup/' + label))
                if value is not None:
                    widget.setValue(value)
            elif isinstance(widget, QtWidgets.QComboBox):
                if 'Directory' in 'Setup/' + label:
                    items = settings.value('Setup/' + label + '_items')
                    if items:
                        widget.addItems(items)
                        index = int(settings.value('Setup/' + label + '_index'))
                        widget.setCurrentIndex(index)

                        for index, item in enumerate(
                                items):  # remove invalid dirs
                            if not Path(item).is_dir():
                                widget.removeItem(index)
                else:
                    value = settings.value('Setup/' + label)
                    items = [widget.itemText(i) for i in range(widget.count())]
                    if value in items:
                        widget.setCurrentIndex(items.index(value))
            elif isinstance(widget, QtWidgets.QCheckBox):
                value = settings.value('Setup/' + label)
                if value is not None:
                    widget.setChecked(strtobool(value))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    dialog = SetupDialog()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        setup_info = dialog.setup_info
