import random
from collections import deque
from distutils.util import strtobool
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

import psychometric_tests.shared.misc_funcs as mf
from psychometric_tests import defs

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class nBack_Widget(QtWidgets.QWidget):
    def __init__(self, setup_info):
        super().__init__()

        self.init_file = str(defs.project_root() / 'nback.ini')
        self.settings = defs.settings()['nback']
        self.title = 'N-Back Test'
        self.setWindowIcon(
            QtGui.QIcon(str(defs.resource_dir() / 'nback.svg')))

        self.setup_info = setup_info
        self.save_path = Path(
            setup_info['Save Directory']) / self.settings['save_name'].format(
            **setup_info)

        self.all_ques = mf.read_csv(
            defs.nback_stimulus_dir() / setup_info['Test Keys'],
            encoding='utf-8',
            add_index=False)

        self.header = ['index', 'stimulus', 'sol', 'ans', 'completion_time',
                       'correct?']

        self.trial_count = 0

        self.record = []
        self.history = deque(maxlen=self.setup_info['N-Back'])
        self.ques_sol = []
        self.current_sol = ''
        self.input = ''
        self.completion_time = float('nan')
        self.correct = 'no_response'
        self.answered = True

        self.stimulus_font = QtGui.QFont(self.settings['stimulus_font'],
                                         self.settings['stimulus_font_size'],
                                         self.settings['stimulus_font_weight'])
        self.answer_font = QtGui.QFont(self.settings['answer_font'],
                                       self.settings['answer_font_size'],
                                       self.settings['answer_font_weight'])

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.stimulus_label = QtWidgets.QLabel(self)
        self.answer_label = QtWidgets.QLabel(self)

        self.neutral_palette = self.answer_label.palette()
        self.correct_palette = self.answer_label.palette()
        self.correct_palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)
        self.wrong_palette = self.answer_label.palette()
        self.wrong_palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        self.setup_ui()

        if Path(self.init_file).is_file():
            settings = QtCore.QSettings(self.init_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_restore(settings)

        self.show_mask_timer = QtCore.QTimer()
        self.show_mask_timer.timeout.connect(self.show_mask)

        self.show_stimulus_timer = QtCore.QTimer()
        self.show_stimulus_timer.timeout.connect(self.show_stimulus)

        self.initiate_stimulus_timer = QtCore.QTimer()
        self.initiate_stimulus_timer.timeout.connect(self.initiate_stimulus)
        self.initiate_stimulus_timer.setSingleShot(True)

    def setup_ui(self):
        self.resize(650, 500)
        self.setWindowTitle(self.title)
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.addStretch()

        main_layout.addWidget(self.stimulus_label)
        self.stimulus_label.setFont(self.stimulus_font)
        self.stimulus_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addStretch()

        main_layout.addWidget(self.answer_label)
        self.answer_label.setFont(self.answer_font)
        self.answer_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addStretch()

    def show_mask(self):
        self.stimulus_label.setText(' ')
        self.answer_label.setText(' ')
        self.record_response()
        self.reset_trial()
        self.prepare_next_ques()

    def prepare_next_ques(self):
        self.ques_sol = random.choice(self.all_ques)
        if self.trial_count >= self.setup_info['No. of Trials'] + \
                self.setup_info['N-Back']:
            self.close()
        elif self.trial_count >= self.setup_info['N-Back']:
            self.current_sol = self.history[- self.setup_info['N-Back']][1]
        else:
            self.answered = True
            self.completion_time = float('nan')
            self.correct = ''
        self.trial_count += 1

    def reset_trial(self):
        self.answered = False
        self.input = ''
        self.current_sol = ''
        self.answer_label.setPalette(self.neutral_palette)
        self.completion_time = float('nan')
        self.correct = 'no_response'

    def initiate_stimulus(self):
        self.show_stimulus_timer.start(
            self.setup_info['Mask Duration'] + self.setup_info[
                'Stimulus Duration'])
        self.show_stimulus()

    def show_stimulus(self):
        self.stimulus_label.setText(self.ques_sol[0])

    def record_response(self):
        self.record.append([self.trial_count,
                            self.ques_sol[0],  # ques
                            self.current_sol,  # sol
                            self.input,
                            self.completion_time,
                            self.correct,
                            ])
        self.history.append(self.ques_sol)

    def save_results(self):
        try:
            self.save_path.parent.mkdir(exist_ok=True)
            mf.save_csv(self.save_path, self.record, self.header,
                        encoding=self.setup_info['Save Encoding'])
        except Exception as error:
            QtWidgets.QMessageBox.critical(self, 'Error',
                                           'Could not save!\n{}'.format(error))

    def closeEvent(self, event):
        self.save_results()
        settings = QtCore.QSettings(self.init_file,
                                    QtCore.QSettings.IniFormat)
        self.gui_save(settings)
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            self.answered = False
            self.input = self.input[:-1]
            self.answer_label.setText(self.input)
            self.answer_label.setPalette(self.neutral_palette)
            self.completion_time = float('nan')
            self.correct = 'no_response'

        elif not self.answered:
            self.input += event.text()
            self.answer_label.setText(self.input)
            if len(self.input) == len(self.current_sol):
                self.answered = True
                self.completion_time = (self.setup_info['Mask Duration'] +
                                        self.setup_info['Stimulus Duration']
                                        ) - self.show_mask_timer.remainingTime()
                if self.input == self.current_sol:
                    self.correct = 'yes'
                    self.answer_label.setPalette(self.correct_palette)
                else:
                    self.correct = 'no'
                    self.answer_label.setPalette(self.wrong_palette)

        if event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        elif event.key() == QtCore.Qt.Key_Space or \
                event.key() == QtCore.Qt.Key_Return or \
                event.key() == QtCore.Qt.Key_Enter:
            if self.trial_count == 0:
                self.initiate_stimulus_timer.start(
                    self.setup_info['Mask Duration'])
                self.show_mask_timer.start(
                    self.setup_info['Mask Duration'] + self.setup_info[
                        'Stimulus Duration'])
                self.stimulus_label.setStyleSheet('')
                self.answer_label.setStyleSheet('')
                self.stimulus_label.setText(' ')
                self.answer_label.setText(' ')
                self.reset_trial()
                self.prepare_next_ques()

        event.accept()

    def wheelEvent(self, wheel_event):
        if QtWidgets.QApplication.keyboardModifiers() \
                == QtCore.Qt.ControlModifier:
            fontsize_stimulus = self.stimulus_font.pointSize()
            fontsize_answer = self.answer_font.pointSize()
            if wheel_event.angleDelta().y() > 0:
                fontsize_stimulus += 4
                fontsize_answer += 4
                self.stimulus_font.setPointSize(fontsize_stimulus)
                self.answer_font.setPointSize(fontsize_answer)
            elif wheel_event.angleDelta().y() < 0:
                fontsize_stimulus -= 4
                fontsize_answer -= 4
                self.stimulus_font.setPointSize(fontsize_stimulus)
                self.answer_font.setPointSize(fontsize_answer)

            self.stimulus_label.setFont(self.stimulus_font)
            self.answer_label.setFont(self.answer_font)

    def gui_save(self, settings):
        settings.setValue('Widget/geometry', self.saveGeometry())
        settings.setValue('Widget/maximized', self.isMaximized())
        settings.setValue('Widget/full_screen', self.isFullScreen())
        defs.update_settings('nback', 'stimulus_font_size',
                             self.stimulus_font.pointSize())
        defs.update_settings('nback', 'answer_font_size',
                             self.answer_font.pointSize())

    def gui_restore(self, settings):
        if settings.value('Widget/geometry') is not None:
            self.restoreGeometry(settings.value('Widget/geometry'))
        if settings.value('Widget/maximized') is not None:
            if strtobool(settings.value('Widget/maximized')):
                self.showMaximized()
        if settings.value('Widget/full_screen') is not None:
            if strtobool(settings.value('Widget/full_screen')):
                self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    exp_setup = {'Participant ID': '1',
                 'Session': 'A',
                 'Date-Time': '',
                 'Stimulus Duration': 300,
                 'Mask Duration': 50,
                 'N-Back': 2,
                 'No. of Trials': 5,
                 'Test Keys': 'words.csv',
                 'Save Encoding': 'utf-8',
                 'Save Directory': ''}

    widget = nBack_Widget(exp_setup)
    widget.show()

    widget.stimulus_label.setText('N-Back Test')
    widget.stimulus_label.setStyleSheet('font-weight: bold; font-size: 16pt')
    widget.answer_label.setText('Press Space Bar to Start')
    widget.answer_label.setStyleSheet('font-size: 12pt')

    app.exec()
