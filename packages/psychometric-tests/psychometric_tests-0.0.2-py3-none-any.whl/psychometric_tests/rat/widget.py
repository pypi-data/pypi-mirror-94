import random
import time
from distutils.util import strtobool
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from psychometric_tests import defs
import psychometric_tests.shared.misc_funcs as mf

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class RAT_Widget(QtWidgets.QWidget):
    def __init__(self, setup_info):
        super().__init__()

        self.settings_file = str(defs.project_root() / 'rat.ini')
        self.title = 'Remote Associates Test'
        self.setWindowIcon(
            QtGui.QIcon(str(defs.project_root() / 'rat.svg')))

        self.setup_info = setup_info
        self.save_path = Path(
            setup_info['Save Directory']) / 'RAT_ID{}-s{}-{}.csv'.format(
            *setup_info.values())
        self.timeout = setup_info['Duration']  # minutes
        self.show_sol = setup_info['Show Solution']
        self.sol_shown = True

        self.questions = mf.read_csv(
            defs.remote_associates_dir() / setup_info['Test Questions'],
            encoding='utf-8')
        random.shuffle(self.questions)

        self.header = ['index', 'Q_num', 'item1', 'item2', 'item3', 'solution',
                       'input', 'duration',
                       'correct?']

        self.ques_count = 0
        self.record = []
        self.current_ques_num = None
        self.current_ques = None
        self.current_sol = None

        self.title_font = QtGui.QFont(defs.font, 30, QtGui.QFont.Bold)
        self.answer_font = QtGui.QFont(defs.font, 40, QtGui.QFont.Bold)
        self.ques_font = QtGui.QFont(defs.font, 30, QtGui.QFont.Normal)
        self.title_font.setStyleHint(QtGui.QFont.SansSerif)
        self.answer_font.setStyleHint(QtGui.QFont.SansSerif)
        self.ques_font.setStyleHint(QtGui.QFont.SansSerif)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.title_label = QtWidgets.QLabel(self)
        self.questions_labels = [QtWidgets.QLabel(self) for _ in range(3)]
        self.answer_edit = QtWidgets.QLineEdit(self)
        self.sol_label = QtWidgets.QLabel(self)
        self.ques_timer_label = QtWidgets.QLabel(self)
        self.glob_timer_label = QtWidgets.QLabel(self)

        self.setup_ui()

        self.refresh_clock_timer = QtCore.QTimer()
        self.refresh_clock_timer.timeout.connect(self.update_timer_labels)
        self.ques_start_time = time.time()
        self.end_timer = QtCore.QTimer()
        self.end_timer.timeout.connect(self.close)  # close programme at timeout

        self.answer_edit.returnPressed.connect(self.enter_pressed)

    def setup_ui(self):
        self.resize(650, 500)
        self.setWindowTitle(self.title)
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        self.title_label.setText('問題 {}'.format(self.ques_count))
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.title_font)
        main_layout.addWidget(self.title_label)
        main_layout.addStretch()

        questions_layout = QtWidgets.QHBoxLayout()
        questions_layout.addStretch()
        for label in self.questions_labels:
            label.setTextFormat(QtCore.Qt.PlainText)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFont(self.ques_font)
            questions_layout.addWidget(label)
            questions_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(questions_layout)
        main_layout.addStretch()

        answer_layout = QtWidgets.QHBoxLayout()
        answer_layout.addStretch()
        self.answer_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.answer_edit.setFont(self.answer_font)
        main_layout.addWidget(self.answer_edit)
        answer_layout.addWidget(self.answer_edit)
        answer_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(answer_layout)
        main_layout.addStretch()

        if self.show_sol:
            sol_layout = QtWidgets.QHBoxLayout()
            sol_layout.addStretch()
            sol_layout.addWidget(self.sol_label)
            self.sol_label.setFont(self.answer_font)
            sol_layout.addStretch()

            main_layout.addLayout(sol_layout)
        else:
            main_layout.addStretch()
        main_layout.addStretch()

        timer_layout = QtWidgets.QHBoxLayout()
        self.glob_timer_label.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        timer_layout.addWidget(self.glob_timer_label)
        timer_layout.addStretch()
        self.ques_timer_label.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        timer_layout.addWidget(self.ques_timer_label)

        main_layout.insertLayout(0, timer_layout)

        if Path(self.settings_file).is_file():
            settings = QtCore.QSettings(self.settings_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_restore(settings)

    def update_timer_labels(self):
        self.glob_timer_label.setText(
            'Time Remaining\n' + mf.convert_time(
                float(self.end_timer.remainingTime()) / 1000))
        self.ques_timer_label.setText(
            'Question Duration\n' + mf.convert_time(
                time.time() - self.ques_start_time))

    def next_question(self):
        self.ques_count += 1
        if self.ques_count > self.setup_info['No. of Questions'] \
                or self.ques_count > len(self.questions):
            self.close()
        else:
            ques_row = self.questions[self.ques_count - 1]
            self.current_ques_num = ques_row[0]
            self.current_ques = ques_row[1].split('/')
            self.current_sol = ques_row[2]

            self.title_label.setText('問題 {}'.format(self.ques_count))
            self.ques_start_time = time.time()  # restart duration 'timer'
            for label, q in zip(self.questions_labels, self.current_ques):
                if any(c in q for c in ['☐', '□']):
                    label.setText('\n'.join(q))
                else:
                    label.setText(q)
            self.answer_edit.clear()

    def record_answer(self):
        ans = self.answer_edit.text()
        duration = time.time() - self.ques_start_time
        correct = True if ans == self.current_sol else False
        self.record.append([self.ques_count,
                            self.current_ques_num,
                            *self.current_ques,
                            self.current_sol,
                            ans, duration, correct])

    def enter_pressed(self):
        if self.ques_count > 0:
            self.record_answer()
        else:
            self.end_timer.start(int(self.timeout * 60 * 1000))
            self.refresh_clock_timer.start(30)

        if self.show_sol and not self.sol_shown:
            self.answer_edit.setReadOnly(True)
            if self.answer_edit.text() == self.current_sol:
                self.sol_label.setText('\u2713')
                self.sol_label.setStyleSheet('color: blue')
            else:
                self.sol_label.setText(self.current_sol)
                self.sol_label.setStyleSheet('color: red')
            self.sol_shown = True
        else:
            self.next_question()
            self.answer_edit.setReadOnly(False)
            self.sol_label.setText('')
            self.sol_shown = False

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
            fontsize_title = self.title_font.pointSize()
            fontsize_answer = self.answer_font.pointSize()
            fontsize_ques = self.ques_font.pointSize()
            if wheel_event.angleDelta().y() > 0:
                fontsize_title += 4
                fontsize_answer += 4
                fontsize_ques += 4
                self.title_font.setPointSize(fontsize_title)
                self.answer_font.setPointSize(fontsize_answer)
                self.ques_font.setPointSize(fontsize_ques)
            elif wheel_event.angleDelta().y() < 0:
                fontsize_title -= 4
                fontsize_answer -= 4
                fontsize_ques -= 4
                self.title_font.setPointSize(fontsize_title)
                self.answer_font.setPointSize(fontsize_answer)
                self.ques_font.setPointSize(fontsize_ques)

            self.title_label.setFont(self.title_font)
            self.answer_edit.setFont(self.answer_font)
            self.sol_label.setFont(self.answer_font)
            for label in self.questions_labels:
                label.setFont(self.ques_font)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        event.accept()

    def gui_save(self, settings):
        settings.setValue('Widget/geometry', self.saveGeometry())
        settings.setValue('Widget/maximized', self.isMaximized())
        settings.setValue('Widget/full_screen', self.isFullScreen())
        settings.setValue('Widget/title_font', self.title_font)
        settings.setValue('Widget/answer_font', self.answer_font)
        settings.setValue('Widget/ques_font', self.ques_font)

    def gui_restore(self, settings):
        if settings.value('Widget/geometry') is not None:
            self.restoreGeometry(settings.value('Widget/geometry'))
        if settings.value('Widget/maximized') is not None:
            if strtobool(settings.value('Widget/maximized')):
                self.showMaximized()
        if settings.value('Widget/full_screen') is not None:
            if strtobool(settings.value('Widget/full_screen')):
                self.showFullScreen()

        if settings.value('Widget/title_font') is not None and \
                settings.value('Widget/answer_font') is not None and \
                settings.value('Widget/ques_font') is not None:

            self.title_font = settings.value('Widget/title_font')
            self.answer_font = settings.value('Widget/answer_font')
            self.ques_font = settings.value('Widget/ques_font')

            self.title_label.setFont(self.title_font)
            self.answer_edit.setFont(self.answer_font)
            self.sol_label.setFont(self.answer_font)
            for label in self.questions_labels:
                label.setFont(self.ques_font)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    exp_setup = {'Participant ID': '1',
                 'Session': 'A',
                 'Date-Time': '',
                 'Duration': 5.0,
                 'No. of Questions': 6,
                 'Test Questions': 'japanese_all.csv',
                 'Save Encoding': 'utf-8',
                 'Save Directory': ''}

    widget = RAT_Widget(exp_setup)
    widget.show()

    widget.title_label.setText('')
    widget.questions_labels[0].setText('')
    widget.questions_labels[1].setText('Press Enter at Text Input to Start')
    widget.questions_labels[2].setText('')

    app.exec()
