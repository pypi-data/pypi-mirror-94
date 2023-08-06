from datetime import datetime

from PyQt5 import QtCore, QtWidgets

import psychometric_tests.shared.misc_funcs as mf
from psychometric_tests import defs
from psychometric_tests.shared.setup_dialog import SetupDialog

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class ANT_Setup(SetupDialog):
    def __init__(self):
        super().__init__()
        self.init_file = str(defs.project_root() / 'ant.ini')
        self.settings = defs.settings()['ant']

        self.user_inputs = {
            'Participant ID': QtWidgets.QLineEdit(self),
            'Session': QtWidgets.QLineEdit(self),
            'Date-Time': QtWidgets.QLineEdit(self),
            'No. of Trials': QtWidgets.QSpinBox(self),
            'Save Encoding': QtWidgets.QComboBox(self),
            'Save Directory': QtWidgets.QComboBox(self),
            'Show Results': QtWidgets.QCheckBox(self),
        }

    def input_settings(self):
        self.user_inputs['No. of Trials'].setMinimum(1)
        self.user_inputs['No. of Trials'].setMaximum(9999)
        self.user_inputs['No. of Trials'].setValue(20)

        for enc in ['utf-8', 'shift-jis']:
            self.user_inputs['Save Encoding'].addItem(enc)

    def overwrite_restored_inputs(self):
        self.user_inputs['Date-Time'].setText(
            self.settings['datetime_format'].format(datetime.now()))

        if self.user_inputs['Save Directory'].count() == 0:
            self.user_inputs['Save Directory'].addItem(str(mf.get_desktop()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    dialog = ANT_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        setup_info = dialog.setup_info
