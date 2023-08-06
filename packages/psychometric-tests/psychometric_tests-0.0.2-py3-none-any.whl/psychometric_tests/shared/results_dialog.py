import csv
import io

from PyQt5 import QtCore, QtGui, QtWidgets

from psychometric_tests import defs

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class ResultsDialog(QtWidgets.QDialog):
    def __init__(self, header, results):
        super().__init__()
        self.setup_info = None

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(
            QtGui.QIcon(str(defs.resource_dir() / 'results.svg')))

        self.resize(450, 500)
        self.setWindowTitle('Results')
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setFrameStyle(scroll_area.NoFrame)
        main_layout.addWidget(scroll_area)

        scroll_contents = QtWidgets.QWidget(self)
        scroll_area.setWidget(scroll_contents)
        scroll_area.setWidgetResizable(True)

        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_contents.setLayout(scroll_layout)

        table_widget = QtWidgets.QTableWidget()
        scroll_layout.addWidget(table_widget)

        table_widget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        table_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        table_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
        table_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        table_widget.setStyleSheet("background:transparent;")
        font = QtGui.QFont('Yu Gothic', 10)
        table_widget.setFont(font)
        table_widget.setShowGrid(False)
        table_widget.verticalHeader().setVisible(False)
        table_widget.setColumnCount(len(header))
        table_widget.setHorizontalHeaderLabels(header)
        table_widget.setRowCount(len(results))

        for j, row in enumerate(results):
            for i, t in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(t))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(j, i, item)

        table_widget.resizeColumnsToContents()
        self.table_widget = table_widget

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.matches(QtGui.QKeySequence.Copy):
            self.copy_selection()
        event.accept()

    def copy_selection(self):
        selection = self.table_widget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            row_count = rows[-1] - rows[0] + 1
            col_count = columns[-1] - columns[0] + 1
            table = [[''] * col_count for _ in range(row_count)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, dialect='excel-tab').writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    dialog = ResultsDialog(['A', 'B', 'C'], [[1, 2, 3]] * 5)
    dialog.exec()
