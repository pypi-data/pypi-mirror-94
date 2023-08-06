from PyQt5 import QtWidgets

from psychometric_tests import defs
from psychometric_tests.rat.setup import RAT_Setup
from psychometric_tests.rat.widget import RAT_Widget
from psychometric_tests.shared.results_dialog import ResultsDialog


def rat():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    settings = defs.settings()['rat']

    dialog = RAT_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        exp_setup = dialog.setup_info
        widget = RAT_Widget(exp_setup)
        widget.show()

        # 'intro' page
        widget.title_label.setText(settings['intro_text1'])
        widget.title_label.setStyleSheet(settings['intro_text1_style'])
        widget.questions_labels[0].setText('')
        widget.questions_labels[1].setText(settings['intro_text2'])
        widget.questions_labels[1].setStyleSheet(settings['intro_text2_style'])
        widget.questions_labels[2].setText('')

        app.exec()

        if exp_setup['Show Results']:
            results = ResultsDialog(widget.header, widget.record)
            results.setWindowTitle('Results ({})'.format(widget.title))
            results.exec()


if __name__ == "__main__":
    rat()
