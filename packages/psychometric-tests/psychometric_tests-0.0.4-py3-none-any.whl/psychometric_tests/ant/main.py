from PyQt5 import QtWidgets

from psychometric_tests import defs
from psychometric_tests.ant.setup import ANT_Setup
from psychometric_tests.ant.widget import ANT_Widget
from psychometric_tests.shared.results_dialog import ResultsDialog


def ant():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    settings = defs.settings()['ant']

    dialog = ANT_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        exp_setup = dialog.setup_info
        widget = ANT_Widget(exp_setup)
        widget.show()

        # 'intro' page
        widget.labels[0][2].setText(settings['intro_text1'])
        widget.labels[0][2].setStyleSheet(settings['intro_text1_style'])
        widget.labels[2][2].setText(settings['intro_text2'])
        widget.labels[2][2].setStyleSheet(settings['intro_text2_style'])

        app.exec()

        if exp_setup['Show Results']:
            results = ResultsDialog(widget.header, widget.record)
            results.setWindowTitle('Results ({})'.format(widget.title))
            results.exec()


if __name__ == "__main__":
    ant()
