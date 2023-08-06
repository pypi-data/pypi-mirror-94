from PyQt5 import QtWidgets

from psychometric_tests.nback.setup import nBack_Setup
from psychometric_tests.nback.widget import nBack_Widget
from psychometric_tests.shared.results_dialog import ResultsDialog


def nback():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    dialog = nBack_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        exp_setup = dialog.setup_info
        widget = nBack_Widget(exp_setup)
        widget.show()

        # 'intro' page
        widget.stimulus_label.setText('N-Back Test')
        widget.stimulus_label.setStyleSheet(
            'font-weight: bold; font-size: 16pt')
        widget.answer_label.setText('Press Space or Enter to Start')
        widget.answer_label.setStyleSheet('font-size: 12pt')

        app.exec()

        if exp_setup['Show Results']:
            results = ResultsDialog(widget.header, widget.record)
            results.setWindowTitle('Results ({})'.format(widget.title))
            results.exec()


if __name__ == "__main__":
    nback()
