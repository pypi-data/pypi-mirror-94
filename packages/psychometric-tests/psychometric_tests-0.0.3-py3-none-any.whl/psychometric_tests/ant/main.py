from PyQt5 import QtWidgets

from psychometric_tests.ant.setup import ANT_Setup
from psychometric_tests.ant.widget import ANT_Widget
from psychometric_tests.shared.results_dialog import ResultsDialog


def ant():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    dialog = ANT_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        exp_setup = dialog.setup_info
        widget = ANT_Widget(exp_setup)
        widget.show()

        # 'intro' page
        widget.labels[0][2].setText(widget.title)
        widget.labels[0][2].setStyleSheet('font-weight: bold; font-size: 16pt')
        widget.labels[2][2].setText('Press Space or Enter to Start')
        widget.labels[2][2].setStyleSheet('font-size: 12pt')

        app.exec()

        if exp_setup['Show Results']:
            results = ResultsDialog(widget.header, widget.record)
            results.setWindowTitle('Results ({})'.format(widget.title))
            results.exec()


if __name__ == "__main__":
    ant()
