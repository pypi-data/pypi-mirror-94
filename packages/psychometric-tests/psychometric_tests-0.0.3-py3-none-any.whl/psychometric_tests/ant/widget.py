import random
from distutils.util import strtobool
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from psychometric_tests import defs
import psychometric_tests.shared.misc_funcs as mf

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class ANT_Widget(QtWidgets.QWidget):
    """
    Implementation of Attention Network Test Based on
    Fan, J., McCandliss, B.D., Sommer, T., Raz, A., et al. (2002)
    Testing the Efficiency and Independence of Attentional Networks.
    Journal of Cognitive Neuroscience. 14 (3), 340–347.
    Available from: doi:10.1162/089892902317361886.
    """

    def __init__(self, setup_info):
        super().__init__()

        self.settings_file = str(defs.project_root() / 'ant.ini')
        self.title = 'Attention Network Test'
        self.setWindowIcon(
            QtGui.QIcon(str(defs.resource_dir() / 'ant.svg')))

        self.setup_info = setup_info
        self.save_path = Path(
            setup_info['Save Directory']) / 'ANT_ID{}-s{}-{}.csv'.format(
            *setup_info.values())

        self.locations = ('up', 'down')
        self.cues = ('nocue', 'center', 'double', 'spatial')
        self.congruency = ('neutral', 'congruent', 'incongruent')
        self.direction = ('left', 'right')
        self.current_cond = []

        self.header = ['trial', 'D1', 'location', 'cue', 'direction',
                       'congruency', 'reaction_time',
                       'correct?']

        # experiment parameters
        self.d1_cond = 0
        self.location_cond = ''
        self.cue_cond = ''
        self.congruency_cond = ''
        self.direction_cond = ''
        self.answered = False

        self.trial_count = 0

        # results
        self.record = []
        self.reaction_time = float('nan')
        self.correct = 'no_response'

        self.stimulus = {
            'right': {'congruent': '\u2192\u2192\u2192\u2192\u2192',
                      'incongruent': '\u2190\u2190\u2192\u2190\u2190',
                      'neutral': '\u2015\u2015\u2192\u2015\u2015'},
            'left': {'congruent': '\u2190\u2190\u2190\u2190\u2190',
                     'incongruent': '\u2192\u2192\u2190\u2192\u2192',
                     'neutral': '\u2015\u2015\u2190\u2015\u2015'},
        }

        self.font = QtGui.QFont(defs.font, 64, QtGui.QFont.Normal)
        self.font.setStyleHint(QtGui.QFont.SansSerif)

        self.labels = []
        self.setup_ui()

        if Path(self.settings_file).is_file():
            settings = QtCore.QSettings(self.settings_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_restore(settings)

        self.timers = [QtCore.QTimer() for _ in range(5)]
        for timer in self.timers[:-1]:
            timer.setSingleShot(True)
        self.timers[0].timeout.connect(self.add_cue)
        self.timers[1].timeout.connect(self.remove_cue)
        self.timers[2].timeout.connect(self.add_target)
        self.timers[3].timeout.connect(self.end_target)
        self.timers[4].timeout.connect(self.next_trial)

    def setup_ui(self):
        self.resize(650, 500)
        self.setWindowTitle(self.title)
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        main_layout.addStretch()

        for _ in range(3):
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.addStretch()
            columns = []
            for _ in range(5):
                label = QtWidgets.QLabel(self)
                label.setFont(self.font)
                label.setText('')
                columns.append(label)
                h_layout.addWidget(label)
                h_layout.addStretch()

            self.labels.append(columns)
            main_layout.addLayout(h_layout)
            main_layout.addStretch()

    def next_trial(self):
        if self.trial_count < self.setup_info['No. of Trials']:
            self.timers[0].start(self.d1_cond)
            self.timers[1].start(self.d1_cond + 100)
            self.timers[2].start(self.d1_cond + 100 + 400)
            self.timers[3].start(self.d1_cond + 100 + 400 + 1700)
            self.trial_count += 1
        else:
            self.close()

    def add_target(self):
        stimulus = self.stimulus[self.direction_cond][self.congruency_cond]

        if self.location_cond == 'up':
            for i, label in enumerate(self.labels[0]):
                label.setText(stimulus[i])
        elif self.location_cond == 'down':
            for i, label in enumerate(self.labels[2]):
                label.setText(stimulus[i])

    def end_target(self):
        self.remove_target()
        self.record_response()
        self.new_trial_params()
        self.reset_trial()

    def record_response(self):
        self.record.append([self.trial_count,
                            self.d1_cond,
                            self.location_cond,
                            self.cue_cond,
                            self.direction_cond,
                            self.congruency_cond,
                            self.reaction_time,
                            self.correct,
                            ])

    def remove_target(self):
        if self.location_cond == 'up':
            for label in self.labels[0]:
                label.setText('')
        elif self.location_cond == 'down':
            for label in self.labels[2]:
                label.setText('')

    def add_cue(self):
        if self.cue_cond == 'spatial':
            if self.location_cond == 'up':
                self.labels[0][2].setText('∗')
            elif self.location_cond == 'down':
                self.labels[2][2].setText('∗')
        elif self.cue_cond == 'double':
            self.labels[0][2].setText('∗')
            self.labels[2][2].setText('∗')
        elif self.cue_cond == 'center':
            self.labels[1][2].setText('∗')
        elif self.cue_cond == 'nocue':
            pass

    def remove_cue(self):
        if self.cue_cond == 'spatial':
            if self.location_cond == 'up':
                self.labels[0][2].setText(' ')
            elif self.location_cond == 'down':
                self.labels[2][2].setText(' ')
        elif self.cue_cond == 'double':
            self.labels[0][2].setText(' ')
            self.labels[2][2].setText(' ')
        elif self.cue_cond == 'center':
            self.labels[1][2].setText('+')
        elif self.cue_cond == 'nocue':
            pass

    def reset_trial(self):
        for row in self.labels:
            for label in row:
                label.setText(' ')
        self.labels[1][2].setText('+')
        self.labels[0][2].setStyleSheet('')
        self.labels[2][2].setStyleSheet('')
        self.answered = False
        self.reaction_time = float('nan')
        self.correct = 'no_response'

    def new_trial_params(self):
        self.d1_cond = random.randrange(400, 1600)
        self.location_cond = random.choice(self.locations)
        self.cue_cond = random.choice(self.cues)
        self.direction_cond = random.choice(self.direction)
        self.congruency_cond = random.choice(self.congruency)

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
        settings = QtCore.QSettings(self.settings_file,
                                    QtCore.QSettings.IniFormat)
        self.gui_save(settings)
        event.accept()

    def wheelEvent(self, wheel_event):
        if QtWidgets.QApplication.keyboardModifiers() \
                == QtCore.Qt.ControlModifier:
            fontsize = self.font.pointSize()
            if wheel_event.angleDelta().y() > 0:
                fontsize += 4
                self.font.setPointSize(fontsize)
            elif wheel_event.angleDelta().y() < 0:
                fontsize -= 4
                self.font.setPointSize(fontsize)

            for col in self.labels:
                for label in col:
                    label.setFont(self.font)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            if not self.answered:
                if not self.timers[2].isActive() and self.timers[3].isActive():
                    self.answered = True
                    self.reaction_time = 1700 - self.timers[3].remainingTime()
                    if self.direction_cond == 'left':
                        self.correct = 'yes'
                        if self.location_cond == 'up':
                            self.labels[0][2].setStyleSheet('color: blue')
                        else:
                            self.labels[2][2].setStyleSheet('color: blue')

                    else:
                        self.correct = 'no'
                        if self.location_cond == 'up':
                            self.labels[0][2].setStyleSheet('color: red')
                        else:
                            self.labels[2][2].setStyleSheet('color: red')

        elif event.key() == QtCore.Qt.Key_Right:
            if not self.answered:
                if not self.timers[2].isActive() and self.timers[3].isActive():
                    self.answered = True
                    self.reaction_time = 1700 - self.timers[3].remainingTime()
                    if self.direction_cond == 'right':
                        self.correct = 'yes'
                        if self.location_cond == 'up':
                            self.labels[0][2].setStyleSheet('color: blue')
                        else:
                            self.labels[2][2].setStyleSheet('color: blue')
                    else:
                        self.correct = 'no'
                        if self.location_cond == 'up':
                            self.labels[0][2].setStyleSheet('color: red')
                        else:
                            self.labels[2][2].setStyleSheet('color: red')

        elif event.key() == QtCore.Qt.Key_Space or \
                event.key() == QtCore.Qt.Key_Return or \
                event.key() == QtCore.Qt.Key_Enter:
            if self.trial_count == 0:
                self.reset_trial()
                self.new_trial_params()
                self.next_trial()
                self.timers[4].start(3500 + 400 + 100)

        elif event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        event.accept()

    def gui_save(self, settings):
        settings.setValue('Widget/geometry', self.saveGeometry())
        settings.setValue('Widget/maximized', self.isMaximized())
        settings.setValue('Widget/full_screen', self.isFullScreen())
        settings.setValue('Widget/font', self.font)

    def gui_restore(self, settings):
        if settings.value('Widget/geometry') is not None:
            self.restoreGeometry(settings.value('Widget/geometry'))
        if settings.value('Widget/maximized') is not None:
            if strtobool(settings.value('Widget/maximized')):
                self.showMaximized()
        if settings.value('Widget/full_screen') is not None:
            if strtobool(settings.value('Widget/full_screen')):
                self.showFullScreen()
        if settings.value('Widget/font') is not None:
            self.font = settings.value('Widget/font')
            for col in self.labels:
                for label in col:
                    label.setFont(self.font)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    exp_setup = {'Participant ID': '1',
                 'Session': 'A',
                 'Date-Time': '',
                 'No. of Trials': 5,
                 'Save Encoding': 'utf-8',
                 'Save Directory': ''}

    widget = ANT_Widget(exp_setup)
    widget.show()

    widget.labels[0][2].setText('Attentional Networks Test')
    widget.labels[0][2].setStyleSheet('font-weight: bold; font-size: 16pt')
    widget.labels[2][2].setText('Press Space or Enter to Start')
    widget.labels[2][2].setStyleSheet('font-size: 12pt')

    app.exec()
