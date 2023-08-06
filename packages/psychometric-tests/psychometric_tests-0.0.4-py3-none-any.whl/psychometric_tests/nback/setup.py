from datetime import datetime

from PyQt5 import QtCore, QtWidgets

import psychometric_tests.shared.misc_funcs as mf
from psychometric_tests import defs
from psychometric_tests.shared.setup_dialog import SetupDialog

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class nBack_Setup(SetupDialog):
    def __init__(self):
        super().__init__()
        self.init_file = str(defs.project_root() / 'nback.ini')
        self.settings = defs.settings()['nback']

        self.user_inputs = {
            'Participant ID': QtWidgets.QLineEdit(self),
            'Session': QtWidgets.QLineEdit(self),
            'Date-Time': QtWidgets.QLineEdit(self),
            'Stimulus Duration': QtWidgets.QSpinBox(self),
            'Mask Duration': QtWidgets.QSpinBox(self),
            'N-Back': QtWidgets.QSpinBox(self),
            'No. of Trials': QtWidgets.QSpinBox(self),
            'Test Keys': QtWidgets.QComboBox(self),
            'Save Encoding': QtWidgets.QComboBox(self),
            'Save Directory': QtWidgets.QComboBox(self),
            'Show Results': QtWidgets.QCheckBox(self),
        }

    def input_settings(self):
        self.user_inputs['Stimulus Duration'].setSingleStep(10)
        self.user_inputs['Stimulus Duration'].setMinimum(300)
        self.user_inputs['Stimulus Duration'].setMaximum(99999)
        self.user_inputs['Stimulus Duration'].setValue(1000)
        self.user_inputs['Stimulus Duration'].setSuffix(' ms')

        self.user_inputs['Mask Duration'].setSingleStep(10)
        self.user_inputs['Mask Duration'].setMinimum(50)
        self.user_inputs['Mask Duration'].setMaximum(99999)
        self.user_inputs['Mask Duration'].setValue(300)
        self.user_inputs['Mask Duration'].setSuffix(' ms')

        self.user_inputs['N-Back'].setSingleStep(1)
        self.user_inputs['N-Back'].setMinimum(1)
        self.user_inputs['N-Back'].setValue(1)

        self.user_inputs['No. of Trials'].setMinimum(1)
        self.user_inputs['No. of Trials'].setMaximum(9999)
        self.user_inputs['No. of Trials'].setValue(20)

        for csv_files in defs.nback_stimulus_dir().glob('*.csv'):
            self.user_inputs['Test Keys'].addItem(csv_files.name)

        for enc in ['utf-8', 'shift-jis']:
            self.user_inputs['Save Encoding'].addItem(enc)

    def overwrite_restored_inputs(self):
        self.user_inputs['Date-Time'].setText(
            self.settings['datetime_format'].format(datetime.now()))

        if self.user_inputs['Save Directory'].count() == 0:
            self.user_inputs['Save Directory'].addItem(str(mf.get_desktop()))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    dialog = nBack_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        setup_info = dialog.setup_info
