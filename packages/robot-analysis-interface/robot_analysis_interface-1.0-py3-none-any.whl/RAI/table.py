'''
Table
=====

This module provides classes for the user to choose streams to add/remove from Plots.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from PyQt5 import QtGui, QtCore, QtWidgets

from .utils import _build_common_widget


class SelectionTable(QtWidgets.QTableWidget):
    """
    This class implements a TableWidget used to select streams.

    :param list(str) headers: Headers of the TableWidget
    :param list(dict) data: Data to be shown on the TableWidget
    """

    update_plot_signal = QtCore.pyqtSignal(str, int, int)

    def __init__(self, headers, data, *args):
        super().__init__(*args)

        self.headers = headers
        self.data = data
        self.parent_window = self.parent()

        # Make cells read-only
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Set up headers
        self.setHorizontalHeaderLabels(self.headers)
        self.verticalHeader().setVisible(False)

        # Set up stream names
        for row, stream in enumerate(sorted(self.data.keys())):
            name_item = QtWidgets.QTableWidgetItem(stream)
            self.setItem(row, 0, name_item)

        # Add stream data
        self._setup_data()

        # Connect signal
        self.itemClicked.connect(self.item_clicked)

    def getIdealWidth(self):
        width = self.verticalHeader().width()
        width += self.horizontalHeader().length()
        if self.verticalScrollBar().isVisible():
            width += self.verticalScrollBar().width()
        width += self.frameWidth() * 2
        return width

    def _setup_data(self):

        for row in range(self.rowCount()):

            # Find item to update
            stream = str(self.item(row, 0).text())

            # Remove old widget
            self.removeCellWidget(row, 1)

            # Add new item
            val_str = "%6.6e" % self.data[stream]
            val_item = QtWidgets.QTableWidgetItem(str(val_str))
            self.setItem(row, 1, val_item)

        # Adjust table view
        self.setVisible(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setVisible(True)

    def item_clicked(self, item):

        # If not stream clicked (first column), return
        if self.column(item) != 0:
            return

        # Item clicked
        stream = str(item.text())

        # Build list window
        checked_plots = self.parent_window._get_plots_id_with_stream(stream)
        current_view = self.parent_window.get_current_view()
        init_states = [QtCore.Qt.Unchecked for _ in range(len(current_view.plots))]
        for i in checked_plots:
            init_states[i] = QtCore.Qt.Checked
        self.check_list = CheckableListWindowWithUpdate(init_states, stream, "Plot", self)

        # Connect signals
        self.check_list.item_changed_signal.connect(self._update_plot)

        # Show window
        self.check_list.show()

    def update_data(self, new_table):
        """
        Update displayed value for all streams.

        :param dict new_table: dictionary containing the current value for all streams.
        """

        self.data = new_table
        self._setup_data()

    def _update_plot(self, stream, plot_number, state):
        """
        Send signal to update plot.

        :param str stream: stream to add or remove
        :param int plot_number: plot number to update
        :param int state: state of the checkbox
        """

        # Send signal to the Main Window
        self.update_plot_signal.emit(stream, plot_number, state)

    def _select_streams_to_show(self, rexp):
        """
        Update table according to a regular expression

        :param QtCore.QRegExp rexp: regular expression to be matched
        """

        for row in range(self.rowCount()):
            name = self.item(row, 0).text()  # Stream name
            if rexp.isEmpty() or rexp.exactMatch(name):
                self.showRow(row)
            else:
                self.hideRow(row)


class CheckableListWindow(QtWidgets.QMainWindow):
    """
    This class implements a window showing a checkable list of the plots to clear.

    :param list(int) init_states: initial state of the checkboxes
    :param str title: title of the window
    :param str item_prefix: prefix to add to all items
    """

    DEFAULT_GEOMETRY = (500, 300, 300, 200)
    ok_signal = QtCore.pyqtSignal(list)

    def __init__(self, init_states, title='', item_prefix='', *args):

        super().__init__(*args)
        self.init_states = init_states
        self.item_prefix = item_prefix
        self.title = title
        self.n_states = len(init_states)

        self.setGeometry(*self.DEFAULT_GEOMETRY)
        self.setWindowModality(True)
        self.setWindowTitle(self.title)

        # Disable X to force the user to use the Cancel or OK buttons.
        flags = self.windowFlags()
        if QtCore.Qt.WindowCloseButtonHint == (flags & QtCore.Qt.WindowCloseButtonHint):
            flags = flags ^ QtCore.Qt.WindowCloseButtonHint
            self.setWindowFlags(flags)

        # Create widget
        self.widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(self.widget)
        self.layout.setHorizontalSpacing(1)
        self.layout.setVerticalSpacing(1)

        # Create list
        self.list_widget = QtWidgets.QListWidget(self)

        for i, state in enumerate(self.init_states):
            item = QtWidgets.QListWidgetItem(self.item_prefix + ' ' + str(i))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(state)
            self.list_widget.addItem(item)

        # Connect
        self.list_widget.itemChanged.connect(self.item_changed)

        # Add list widget
        self.layout.addWidget(self.list_widget, 0, 0)

        # Add buttons
        self.cancel_btn = QtWidgets.QPushButton("Cancel", self)
        self.ok_btn = QtWidgets.QPushButton("OK", self)
        self.ok_btn.setEnabled(False)
        self.buttons_widget = _build_common_widget(self, 1, 2, self.cancel_btn, self.ok_btn)

        # Connect
        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.ok_btn.clicked.connect(self.ok_clicked)

        # Add buttons widget
        self.layout.addWidget(self.buttons_widget, 1, 0)

        # Set to central widget and write message
        self.setCentralWidget(self.widget)

    def item_changed(self, _item):

        # Check if we should enable the OK button
        self.current_states = [self.list_widget.item(i).checkState() for i in range(self.n_states)]
        if self.current_states != self.init_states:
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def ok_clicked(self):
        plots_to_update = []
        for i, state in enumerate(self.current_states):
            if state == QtCore.Qt.Checked:
                plots_to_update.append(i)

        # Send signal to the window to update plots
        self.ok_signal.emit(plots_to_update)

        # Close
        self.close()

    def cancel_clicked(self):
        self.close()


class CheckableListWindowWithUpdate(CheckableListWindow):
    """
    This class inherits from CheckableListWindow
    and send a signal when an item state is changed.
    """

    item_changed_signal = QtCore.pyqtSignal(str, int, int)

    def item_changed(self, item):

        super().item_changed(item)

        # Send signal to update plot right away
        # Get plot number
        plot_str = item.text().replace(self.item_prefix + ' ', '', 1)
        plot_number = int(plot_str)

        # Send signal
        # The title is the stream name so we use this trick to send it to the Selection window
        self.item_changed_signal.emit(self.title, plot_number, item.checkState())

    def ok_clicked(self):
        self.close()

    def cancel_clicked(self):

        # Roll back to initial state
        for i, state in enumerate(self.init_states):
            item = self.list_widget.item(i)
            if item.checkState() != state:
                # Send signal
                # The title is the stream name so we use this trick to send it to the Selection window
                self.item_changed_signal.emit(self.title, i, state)

        super().cancel_clicked()


class LabelWithAdaptiveText(QtWidgets.QLabel):
    """A Label with text adapting to its size."""

    def paintEvent(self, *args, **kwargs):

        painter = QtGui.QPainter(self)
        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), QtCore.Qt.ElideLeft, self.width())

        painter.drawText(self.rect(), self.alignment(), elided)
