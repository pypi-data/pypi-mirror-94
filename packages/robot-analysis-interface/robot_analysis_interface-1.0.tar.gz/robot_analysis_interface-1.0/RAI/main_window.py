'''
MainWindow
===========

This module provides a :py:class:`CompositeWindow` class to display Videos and Plots.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

import os
import json
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np

from .timers import DoubleTimer
from .plotting import Plot
from .serial import Serializable
from .utils import _build_common_widget, signals_blocked
from .table import SelectionTable, CheckableListWindow, LabelWithAdaptiveText
from .slider import FloatSlider
from .view import View


class CompositeWindow(QtWidgets.QMainWindow, Serializable):
    """ This class implements the composite window to be displayed.

    :param dict views_data: Data describing the Plots and the View
    :param videos: Videos to be displayed
    :type videos: list(:py:class:`Video<RAI.video.Video>`)
    :param str title: Window title
    :param int,int window_pos: position in pixels of the window
    :param int,int window_size: size in pixels of the window
    :param int,int plot_size: size in pixels of the plots
    """

    serial_version = '1.0'

    # Use dots instead of comma in float representations
    QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.C))

    def __init__(self, views_data=None, videos=None, title='Main Window',
                 window_pos=(100, 100), window_size=(2000, 800), plot_size=(400, 400),
                 parent=None, parent_session=None, **kwargs):

        super().__init__(parent)

        # Parent session
        self.parent_session = parent_session

        # Window geometry
        self.title = title
        self.setWindowTitle(self.title)
        self.left = window_pos[0]
        self.top = window_pos[1]
        self.width = window_size[0]
        self.height = window_size[1]
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Plots to be displayed
        self.plot_width = plot_size[0]
        self.plot_height = plot_size[1]

        # Videos to be displayed
        self.videos = videos or []
        use_videos = True if len(self.videos) > 0 else False

        # Initial starting time in seconds.
        self.current_time = 0.0

        # Minimum of all video durations and mean timeout in ms (needed for update_video_to_next_frame)
        if use_videos:
            self.mean_timeout = int(np.mean([1000.0 / video.fps for video in self.videos]))
            self._compute_video_playing_time()

        # Add buttons
        # Connection bindings
        self.button_bindings = {"New Session": self._on_new_session_button_clicked,
                                "Save Session": self._on_save_session_button_clicked,
                                "Load Session": self._on_load_session_button_clicked,
                                "New Plot": self._on_new_plot_button_clicked,
                                "Clear Plot": self._on_clear_plot_button_clicked,
                                "Remove Plot": self._on_remove_plot_button_clicked,
                                "New View": self._on_new_view_button_clicked,
                                "Rename View": self._on_rename_view_button_clicked,
                                "Save Views": self._on_save_view_button_clicked,
                                "Load Views": self._on_load_view_button_clicked,
                                "Copy Path": self._on_copy_btn_clicked,
                                "Refresh Data": self._on_refresh_btn_clicked
                                }

        # Add Videos buttons if necessary
        if len(self.videos) > 0:
            self.button_bindings["Play"] = self._on_play_button_clicked
            self.button_bindings["Stop"] = self._on_stop_button_clicked
            self.button_bindings["Reset"] = self._on_reset_button_clicked

        # Create buttons
        self.buttons = {name: QtWidgets.QPushButton(name, self) for name in self.button_bindings}

        # Connect buttons
        for name, button in self.buttons.items():
            button.clicked.connect(self.button_bindings[name])

        # Layout
        self.layout_horizontal_spacing = 3  # slider and video buttons dissociated for alignment
        if use_videos:
            self.layout_vertical_spacing = 3  # Table - Plots - Videos
        else:
            self.layout_vertical_spacing = 2  # Table - Plots

        # Set layout of the main widget
        self.main_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QGridLayout(self.main_widget)
        self.layout.setHorizontalSpacing(self.layout_horizontal_spacing)
        self.layout.setVerticalSpacing(self.layout_vertical_spacing)

        # Set stretch factors
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 2)
        if use_videos:
            self.layout.setColumnStretch(2, 1)

        # Selection Table to update plots
        headers = ['Stream', 'Value']
        init_table_data = self._get_all_streams_value(self.current_time)
        self.selection_table = SelectionTable(
            headers, init_table_data, len(init_table_data), 2, self)
        self.selection_table.update_plot_signal.connect(self._update_plot)

        # Search bar (with label)
        search_label = QtWidgets.QLabel("Regex Search: ", self)
        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_edit.setAlignment(QtCore.Qt.AlignRight)
        self.search_edit.setPlaceholderText("Stream name")
        # Validator
        self.search_edit.setValidator(QtGui.QRegExpValidator())
        # Connect QLineEdit
        self.search_edit.textChanged.connect(self._search_pattern_changed)
        # Put label and line_edit together
        self.search_bar = _build_common_widget(self, 1, 2, search_label, self.search_edit)

        # Table and search bar together
        self.table_and_searchbar = _build_common_widget(
            self, 2, 1, self.search_bar, self.selection_table)

        # Copy name to clipboard and refresh buttons together
        self.copy_and_refresh_widget = _build_common_widget(
            self, 1, 2, self.buttons["Copy Path"], self.buttons["Refresh Data"])

        # Label showing name of sensors file
        if self.parent_session.root_path is not None:
            self.text_label = os.path.join(self.parent_session.root_path,
                                           self.parent_session.sensors_file)
        else:
            self.text_label = self.parent_session.sensors_file
        self.sensors_label = LabelWithAdaptiveText(self)
        self.sensors_label.setText(self.text_label)
        self.sensors_label.setAlignment(QtCore.Qt.AlignCenter)

        # Label, copy, and refresh sensors together
        self.sensors_widget = _build_common_widget(
            self, 2, 1, self.sensors_label, self.copy_and_refresh_widget)

        # Plots are organized in views within a TabWidget
        self.tab_widget = QtWidgets.QTabWidget(self)
        # Make tabs closable
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._remove_view)
        # Make tabs movable
        self.tab_widget.tabBar().setMovable(True)
        # adding splitter to resize plot/video widgets
        self.main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)

        # Initialize views
        # TO THINK ABOUT
        # Currently, views are stored in a dictionary where the key is the view name
        # May be that would make more sense to just store them in a list...
        self.views = {}
        if views_data is not None:
            for name, view_data in views_data.items():
                self._create_view(name, view_data)

        # Build views
        for view in self.views.values():
            self._build_view(view, parent=self.tab_widget)

        # Build and add Videos widget if there are videos
        if use_videos:
            self._build_videos_widget(row=0, col=2)

        # Disable new session for the moment
        self.buttons["New Session"].setEnabled(False)

        # QLineEdit to specify time (with label)
        time_label = QtWidgets.QLabel("Current Time (s): ", self)
        self.time_line_edit = QtWidgets.QDoubleSpinBox(self)
        # Time Resolution is 10 ms and 3 digits
        self.time_line_edit.setSingleStep(0.01)
        self.time_line_edit.setDecimals(3)
        self.time_line_edit.setAlignment(QtCore.Qt.AlignRight)
        # Hold signal until return key is pressed
        self.time_line_edit.setKeyboardTracking(False)
        # Remove arrows
        self.time_line_edit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        # Connect signal
        self.time_line_edit.valueChanged.connect(self._on_time_line_edited)

        # Put Session buttons in a common widget
        self.session_buttons_widget = _build_common_widget(self, 1, 3,
                                                           self.buttons["New Session"],
                                                           self.buttons["Save Session"],
                                                           self.buttons["Load Session"])

        # Put Plots buttons in a common widget
        self.plots_buttons_widget = _build_common_widget(self, 1, 7,
                                                         self.buttons["New View"],
                                                         self.buttons["Rename View"],
                                                         self.buttons["Save Views"],
                                                         self.buttons["Load Views"],
                                                         self.buttons["New Plot"],
                                                         self.buttons["Remove Plot"],
                                                         self.buttons["Clear Plot"])
        self.layout.addWidget(self.plots_buttons_widget, self.layout_horizontal_spacing - 1, 1)

        # Put Videos buttons in a common widget and add slider
        null_widget = QtWidgets.QWidget(self)
        if use_videos:

            # Add Videos buttons
            self.videos_buttons_widget = _build_common_widget(self, 1, 3,
                                                              self.buttons["Play"],
                                                              self.buttons["Stop"],
                                                              self.buttons["Reset"])
            self.layout.addWidget(self.videos_buttons_widget, self.layout_horizontal_spacing - 1, 2)

            # Create slider
            # For abstraction, we give it only the duration of the videos
            # And it will decide which size to adopt
            self.msl = FloatSlider(self.min_duration, QtCore.Qt.Horizontal, self)

            # Connect slider
            self.msl.sliderPressed.connect(self._on_slider_press)
            self.msl.valueChanged.connect(self._on_slider_press)
            self.msl.sliderReleased.connect(self._on_slider_release)

            # Put slider, time_label, and time_line_edit together
            time_widget = _build_common_widget(self, 1, 4,
                                               self.msl, null_widget, time_label, self.time_line_edit,
                                               stretch_columns=[15, 1, 3, 3])

            # Initialize and connect timer
            self.timer = DoubleTimer(self.mean_timeout)
            self.timer.repeat_timer.timeout.connect(self._update_all_to_next_frame)

        else:

            # Add only time label widget
            time_widget = _build_common_widget(self, 1, 3,
                                               null_widget, time_label, self.time_line_edit,
                                               stretch_columns=[15, 1, 1])

        # Initialize QDialogs for saving/loading sessions
        self.dlg_save = QtWidgets.QFileDialog(self)
        self.dlg_load = QtWidgets.QFileDialog(self)

        # Initialize QInputDialog for changing the name of a view.
        self.line_edit_view = QtWidgets.QInputDialog(self)
        self.line_edit_view.setLabelText("Enter new View name")
        self.line_edit_view.setWindowTitle(' ')
        self.line_edit_view.setModal(True)

        # Add everything to the layout
        # Column 0
        self.layout.addWidget(self.table_and_searchbar, 0, 0,
                              alignment=QtCore.Qt.AlignHCenter)  # row 0
        self.layout.addWidget(self.sensors_widget, 1, 0)  # row 1
        self.layout.addWidget(self.session_buttons_widget,
                              self.layout_horizontal_spacing - 1, 0)  # row 2
        # Set widths of the widgets of the column
        table_ideal_width = self.selection_table.getIdealWidth()
        copy_and_refresh_width = self.copy_and_refresh_widget.width()
        session_buttons_width = 1.10 * (self.buttons["New Session"].width() +
                                        self.buttons["Save Session"].width() +
                                        self.buttons["Load Session"].width())  # + 10% to make some space

        optimal_width = max((table_ideal_width, copy_and_refresh_width, session_buttons_width))
        # for i in range(self.layout_horizontal_spacing):
        #    self.layout.itemAtPosition(i, 0).widget().setFixedWidth(optimal_width)
        self.sensors_widget.setFixedWidth(optimal_width)
        self.table_and_searchbar.setFixedWidth(optimal_width)

        # Column 1: Add plots with tab widget to main splitter & enable resizing
        self.main_splitter.insertWidget(0, self.tab_widget)
        self.layout.addWidget(self.session_buttons_widget,
                              self.layout_horizontal_spacing - 1, 0)  # row 2
        # Add splitter  to the layout at row 0, column 1, row span 1 and column span 2
        self.layout.addWidget(self.main_splitter, 0, 1, 1, 2)
        # Column 2
        if use_videos:
            self.layout.addWidget(time_widget, self.layout_horizontal_spacing - 2, 2)
        else:
            self.layout.addWidget(time_widget, self.layout_horizontal_spacing - 2, 1)

        # Set central widget and write message
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage('Starting new session.')

    def resizeEvent(self, event):
        """ Resize all the widgets when the window is resized. """

        super().resizeEvent(event)

#        # Repaint the videos widgets
#        video_layout = self.videos_widget.layout()
#        for video in self.videos:
#            geometry = video_layout.cellRect(video.id_number, 0)
#            new_width = geometry.width()
#            new_height = geometry.height()
#            if (new_width == 0) or (new_height == 0):  # true only at the window creation
#                new_width = self.geometry().width() / 3
#                new_height = self.geometry().height() / len(self.videos)
#
#            # One needs to leave a small padding between the frame size and the widget size,
#            # otherwise the framesself.assertEqual(self.mocked_update_data.call_count, 1) "collide" and cannot shrink. 5 pixels make things look good
#            video._resize_video(new_width - 5, new_height - 5)

    def _create_view(self, name, view_data):
        """Create the Plots and put them in a View.

        :param str name: View name
        :param dict view_data: data describing the Plots and the View
        """

        plots = []
        n_plots = len(view_data.keys())

        # Check that the plot numbers go from 0 to n_plots
        assert list(view_data) == list(range(n_plots)), \
            'Plots number should go from 0 to %s. Instead got %s' \
            % (n_plots - 1, sorted(view_data.keys()))

        # Prepare Plots
        iplot = 0
        while iplot < n_plots:
            x, y = {}, {}

            # Add streams at start-up if required
            streams_to_add = view_data[iplot]
            for stream in streams_to_add:
                x1, y1 = self.parent_session.sensors_data.get_streams(['time', stream])
                x[stream] = x1
                y[stream] = y1

            # Create plot
            plots.append(Plot(x, y, streams_to_add))
            iplot += 1

        # Make sure name is not taken
        view_name = self._check_and_update_view_name(name)

        # Create view
        self.views[view_name] = View(plots, name=view_name)

    def _build_new_view(self, view, parent=None):
        """Build the widgets for displaying a View and check for overlaping names.

        :param view: View to be displayed
        :type view: :py:class:`View<RAI.view.View>`
        """

        # Make sure name is not taken
        view.name = self._check_and_update_view_name(view.name)

        # Build view
        self._build_view(view, parent)

    def _build_view(self, view, parent=None):
        """Build the widgets for displaying a View.

        :param view: View to be displayed
        :type view: :py:class:`View<RAI.view.View>`
        """

        # First. prepare plots
        for i, plot in enumerate(view.plots):
            # Only prepare Plot if it has not been done before, i.e. if plot_widget1 does not exist.
            if not hasattr(plot, 'widget1'):
                plot.setParent(self)
                plot._prepare(self)
                plot.line_updated_signal.connect(self._sync_all_wrt_time)
            # Only set id_number if it has not been done before
            if plot.id_number is None:
                plot.id_number = i

        # Build and return View
        view.build(self.plot_width, self.plot_height, parent=parent)

        # Add to TabWidget
        self.views[view.name] = view
        self.tab_widget.addTab(view.vertical_widget_plots, view.name)

    def _modify_view(self, view):
        """Modify a view.
        :param view: View to be modified
        :type view: :py:class:`View<RAI.view.View>`
        """

        # Build new view
        for i, plot in enumerate(view.plots):
            # Only prepare Plot if it has not been done before, i.e. if plot_widget1 does not exist.
            if not hasattr(plot, 'widget1'):
                plot.setParent(self)
                plot._prepare(self)
                plot.line_updated_signal.connect(self._sync_all_wrt_time)
            # Only set id_number if it has not been done before
            if plot.id_number is None:
                plot.id_number = i

        # Build and return View
        new_view = View(view.plots, view.name)
        new_view.build(self.plot_width, self.plot_height, view.parent)

        # Remove old tab
        old_tab = self.tab_widget.currentWidget()
        old_tab_index = self.tab_widget.indexOf(old_tab)
        self.tab_widget.removeTab(old_tab_index)
        old_tab.setParent(None)
        old_tab.deleteLater()

        # Add new view to TabWidget
        self.tab_widget.insertTab(old_tab_index, new_view.vertical_widget_plots, new_view.name)
        self.views[new_view.name] = new_view

        # Return to the View that has been modified
        self.tab_widget.setCurrentWidget(self.tab_widget.widget(old_tab_index))

    def _build_offset_widget(self, video):
        """Generate a widget allowing the user to specify the offset of a given video.
        :param video: video to resize
        :type video: :py:class:`Video<RAI.video.Video>`
        :returns: offset widget
        :rtype: widget
        """

        # DoubleSpinBox to specify offset (by default, minimum is 0)
        offset_label = QtWidgets.QLabel("Offset (s): ", self)
        time_offset = QtWidgets.QDoubleSpinBox(self)
        # Min/Max values for offset
        # Min: video starts at the end of the sensors trace
        time_offset.setMinimum(-self.parent_session.sensors_data.max_time)
        # Max: sensors trace starts at the end of the video
        time_offset.setMaximum(video.duration)
        # Time resolution is such that one click changes by one frame
        time_offset.setValue(video.offset)
        time_offset.setSingleStep(1.0 / video.fps)
        time_offset.setDecimals(3)
        time_offset.setAlignment(QtCore.Qt.AlignRight)
        # Hold signal until return key is pressed
        time_offset.setKeyboardTracking(False)
        # Connect signal
        time_offset.valueChanged.connect(lambda x: self._on_offset_changed(x, video))
        # Save widget
        self.time_offset_boxes[video] = time_offset

        # Button to sync offset
        sync_button = QtWidgets.QPushButton('Apply to all', self)
        sync_button.clicked.connect(lambda _: self._on_sync_offset_button_clicked(video))
        # Save button
        self.sync_offset_buttons[video] = sync_button

        # Common widget
        return _build_common_widget(self, 1, 4,
                                    offset_label, time_offset, QtWidgets.QWidget(self), sync_button,
                                    stretch_columns=[1, 1, 3, 1])

    def _build_videos_widget(self, row, col):
        """Generate a widget with all videos.
        :param int row: widget row number
        :param int col: widget column number
        """

        # Prepare videos
        for i, video in enumerate(self.videos):
            video._prepare()
            self._resize_current_video(video)
            video.id_number = i

        # Build ScrollArea
        self.scroll_area_videos = QtWidgets.QScrollArea(self)
        self.scroll_area_videos.setWidgetResizable(True)
        self.scroll_area_videos_widget_contents = QtWidgets.QWidget(self.scroll_area_videos)
        self.scroll_area_videos_widget_contents.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.scroll_area_videos.setWidget(self.scroll_area_videos_widget_contents)

        self.vertical_widget_videos = QtWidgets.QWidget(self)
        self.vertical_layout_videos = QtWidgets.QVBoxLayout(self.vertical_widget_videos)
        self.vertical_layout_videos.addWidget(self.scroll_area_videos)
        self.vertical_layout_videos_scroll = QtWidgets.QVBoxLayout(
            self.scroll_area_videos_widget_contents)

        # Insert video widget
        self.time_offset_boxes = {}
        self.sync_offset_buttons = {}
        for video in self.videos:
            offset_widget = self._build_offset_widget(video)
            video_widget = _build_common_widget(self, 2, 1,
                                                offset_widget, video.image_widget,
                                                alignment=QtCore.Qt.AlignCenter)

            self.vertical_layout_videos_scroll.addWidget(video_widget)

        # Adding video widget to splitter to resize
        self.main_splitter.addWidget(self.vertical_widget_videos)

    def _update_all_to_next_frame(self):
        """Update all plots and videos to the next frame."""

        # Stop timer if we passed the end of the video
        if self.timer.elapse_timer.hasExpired(int(self.min_duration * 1000.0)):
            self._on_stop_button_clicked()

        # If timer is stopped, return
        if not self.timer.status_running:
            return

        # Otherwise, update plots, videos.
        elapsed_time = self.timer.elapse_timer.elapsed() / 1000.0 + self.current_time

        # Only update current view
        current_view = self.get_current_view()
        for plot in current_view.plots:
            plot._update_vertical_lines(elapsed_time)

        for video in self.videos:
            video.update_video_to_next_frame(elapsed_time)

        # Update master slider
        # Disabled for now. Will be reactivated when we find a better way to use the slider and its integer values.
        if False:
            self.msl.setValue(int(elapsed_time / self.min_duration * 100.0))

    def _on_slider_press(self):
        """Actions to perform when the slider is pressed."""

        # Stop the time
        if self.timer.status_running:
            self.timer.stop()

    def _on_slider_release(self):
        """Actions to perform when the slider is released."""

        # Slider value
        time = self.msl.value()

        # Update all
        self._sync_all_wrt_time(time)

    def _on_time_line_edited(self, *args, **kwargs):
        """Actions to perform when time has been specified by the user."""

        self._sync_all_wrt_time(self.time_line_edit.value())

    def _sync_all_wrt_time(self, time):
        """Synchronize Plots, Videos, Slider, and Table when the value of one of those has been modified by the user.

        :param float time: new value in seconds
        """

        # Stop the time for video timer
        if len(self.videos) > 0 and self.timer.status_running:
            self._on_stop_button_clicked()

        # First, make sure that we don't go below 0
        time = max(time, 0.0)

        # Sync Plots from all views
        for view in self.views.values():
            for plot in view.plots:
                plot._update_vertical_lines(time)

        # Sync videos
        for video in self.videos:
            video._update_video_to_given_time(time)

        # Sync slider
        if len(self.videos) > 0:
            self.msl.update_slider(time)

        # Sync table and window attribute
        new_table_data = self._get_all_streams_value(time)
        self.selection_table.update_data(new_table_data)
        self.current_time = time

        # Update time LineEdit
        with signals_blocked(self.time_line_edit):
            self.time_line_edit.setValue(time)

        # Update min_duration (necessary for the video timer)
        if len(self.videos) > 0:
            self._compute_video_playing_time()

    def _on_offset_changed(self, offset, video):
        """Actions to perform when the offset has been modified by the user on the SpinBox.

        :param float offset: offset value
        :param video: video whose offset will be modified
        :type video: :py:class:`Video<RAI.video.Video>`
        """

        # Stop if needed
        if self.timer.status_running:
            self._on_stop_button_clicked()

        # Update video offset
        video._update_offset(offset, self.current_time)

        # Update min_duration (necessary for the timer)
        self._compute_video_playing_time()

    def _compute_video_playing_time(self):
        """Compute the video playing time."""

        self.min_duration = np.min(
            [(video.duration - video.offset - self.current_time) for video in self.videos])
        self.min_duration = max(0.0, self.min_duration)  # Cannot be < 0

        if hasattr(self, 'buttons'):
            if self.min_duration < (self.mean_timeout / 1000.):
                self.buttons["Play"].setEnabled(False)
            else:
                self.buttons["Play"].setEnabled(True)

    def _on_sync_offset_button_clicked(self, source_video):
        """Synchronize the offset of all videos.

        :param source_video: video sending offset
        :type source_video: :py:class:`Video<RAI.video.Video>`
        """

        for video in self.videos:
            if video != source_video:
                self.time_offset_boxes[video].setValue(source_video.offset)

    def _resize_current_video(self, video, *args):
        """ Resize the video according to the layout geometry.

        :param video: video to resize
        :type video: :py:class:`Video<RAI.video.Video>`
        """

        # At start, the layout's geometry is not set.
        if (video.widget_width is None) or (video.widget_height is None):
            new_width = self.width / 3
            new_height = self.height / 3
        else:
            new_width = args[0]
            new_height = args[1]

        video._resize_video(new_width, new_height)

    def deleteLater(self):
        """Deleting views before closing to avoid Seg fault"""

        # Delete the views
        for view in self.views:
            self.views[view].deleteLater()
        super().deleteLater()

    def serialize(self):

        super().serialize()

        return {"views": self.views,
                "title": self.title,
                "window_size": (self.width, self.height),
                "plot_size": (self.plot_width, self.plot_height),
                "serial_version": self.serial_version
                }

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        assert(len(args) >= 2)  # we need the videos and the session
        videos = args[0]
        session = args[1]

        dictionary.pop("serial_version")
        views_dict = dictionary.pop("views")

        # Window without views
        window = CompositeWindow(None, videos=videos, parent_session=session, **dictionary)

        # Deserialize Views
        for name, view_dict in views_dict.items():

            # Deserialize Plots
            plots = []
            for plot_dict in view_dict['plots']:
                plots.append(Plot.deserialize(plot_dict, session.sensors_data))

            window.views[name] = View.deserialize(view_dict, plots)

        # Build views
        for view in window.views:
            window._build_view(window.views[view], parent=window.tab_widget)

        return window

    def _on_play_button_clicked(self):

        # Start timer
        self.timer.start()

        # Display status
        self.statusBar().showMessage('Playing videos.')

    def _on_stop_button_clicked(self):

        # If the timer was not running, do nothing
        if not self.timer.status_running:
            return

        # Stop timer if needed.
        self.timer.stop()

        # Update current_time
        self.current_time += self.timer.elapse_timer.elapsed() / 1000.0

        # Update table
        new_table_data = self._get_all_streams_value(self.current_time)
        self.selection_table.update_data(new_table_data)

        # Sync all views
        self._sync_all_wrt_time(self.current_time)

        # Update min_duration
        # self._compute_video_playing_time()

        # Display status
        self.statusBar().showMessage('Stopped videos playing.')

    def _on_reset_button_clicked(self):

        # Stop timer if needed.
        self.timer.stop()

        # Reset current_time
        self.current_time = 0.0

        # Sync all views
        self._sync_all_wrt_time(self.current_time)

        # Update min_duration
        self._compute_video_playing_time()

        # Display status
        self.statusBar().showMessage('Reset all videos.')

    def _on_new_session_button_clicked(self):

        # Not implemented yet
        self._buttonClicked()

    def _on_save_session_button_clicked(self):

        # Create Dialog with appropriate defaults
        self.dlg_save.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.dlg_save.setDirectory(".")

        # Confirm overwriting
        self.dlg_save.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        # Set JSON extension as filter
        self.dlg_save.setDefaultSuffix('json')
        self.dlg_save.setNameFilters(['JSON (*.json)'])
        self.dlg_save.setModal(True)

        # Launch dialog
        if self.dlg_save.exec_() == QtWidgets.QDialog.Accepted:

            # Get filename
            filenames = self.dlg_save.selectedFiles()
            save_name = os.path.abspath(filenames[0])

            # Save session if possible
            if self.parent_session is not None:
                self.parent_session.save(save_name)

                # Display status
                self.statusBar().showMessage('Session saved in %s' % save_name)
            else:
                self.statusBar().showMessage('Cannot save session: current session has not been initialized.')
        else:
            self.statusBar().showMessage('Cancelled saving session')

    def _on_load_session_button_clicked(self):

        from .session import Session

        # Create Dialog with appropriate defaults
        # Only show existing files
        self.dlg_load.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.dlg_load.setDirectory(".")

        # Set JSON extension as filter
        self.dlg_load.setDefaultSuffix('json')
        self.dlg_load.setNameFilters(['JSON (*.json)'])
        self.dlg_load.setModal(True)

        # Launch dialog
        if self.dlg_load.exec_() == QtWidgets.QDialog.Accepted:

            # Get filename
            filenames = self.dlg_load.selectedFiles()
            filename = os.path.abspath(filenames[0])

            # Load session
            new_session = Session.load(filename)
            new_session.launch(start_qt_loop=False)

            # Display status
            new_session.window.statusBar().showMessage('Session %s loaded' % new_session.ID)
        else:
            self.statusBar().showMessage('Cancelled loading session')

    def _update_plot(self, stream, plot_number, state):

        # Get current view
        current_view = self.get_current_view()

        # Transform stream from QString into string
        stream = str(stream)
        plot = current_view.plots[plot_number]

        if state == QtCore.Qt.Checked:  # add stream
            x, y = self.parent_session.sensors_data.get_streams(['time', stream])
            plot._add_stream(x, y, stream)
        elif state == QtCore.Qt.Unchecked:  # remove stream
            plot._remove_stream(stream)
        else:
            raise ValueError("State of item %s should be %s or %s, got %s instead."
                             % (stream, QtCore.Qt.Checked, QtCore.Qt.Unchecked, state))

    def _on_new_plot_button_clicked(self):

        # Get current view
        current_view = self.get_current_view()

        # Create and add empty plot
        empty_plot = Plot()
        current_view.plots.append(empty_plot)

        # Build and display new plot widget
        with signals_blocked(self.tab_widget):
            self._modify_view(current_view)

        # Display status
        self.statusBar().showMessage("Added new plot")

    def _on_clear_plot_button_clicked(self):

        # Display status
        self.statusBar().showMessage("Clearing plot")

        # Get current view
        current_view = self.get_current_view()

        # Build list window
        init_states = [QtCore.Qt.Unchecked for _ in range(len(current_view.plots))]
        self.check_list = CheckableListWindow(init_states, "Plots to clear", "Plot", self)
        self.check_list.ok_signal.connect(self._clear_plots)

        # Show window
        self.check_list.show()

    def _on_remove_plot_button_clicked(self):

        # Display status
        self.statusBar().showMessage("Removing plot")

        # Get current view
        current_view = self.get_current_view()

        # Build list window
        init_states = [QtCore.Qt.Unchecked for _ in range(len(current_view.plots))]
        self.check_list = CheckableListWindow(init_states, "Plots to delete", "Plot", self)
        self.check_list.ok_signal.connect(self._remove_plots)

        # Show window
        self.check_list.show()

    def _clear_plots(self, plots_to_clear):
        """ Clear plots.

        :param plots_to_clear: IDs of plots to clear
        :type plots_to_clear: list(int)
        """

        # Get current view
        current_view = self.get_current_view()

        # Delete streams
        for i in plots_to_clear:
            streams_copy = list(current_view.plots[i].streams)
            for stream in streams_copy:
                self._update_plot(stream, i, QtCore.Qt.Unchecked)

        # Display status
        self.statusBar().showMessage("Clearing plot confirmed")

    def _remove_plots(self, plots_to_delete):
        """ Remove plots.

        :param plots_to_delete: IDs of plots to delete
        :type plots_to_delete: list(int)
        """

        # Get current view
        current_view = self.get_current_view()

        # Delete streams first
        self._clear_plots(plots_to_delete)

        # Then remove plots
        plots_copy = list(current_view.plots)
        for i in plots_to_delete:
            current_view.plots.remove(plots_copy[i])

        # Build and display new plot widget
        self._modify_view(current_view)

        # Display status
        self.statusBar().showMessage("Removing plot confirmed")

    def _get_plots_id_with_stream(self, stream):
        """ Get the IDs of the plots displaying a strea.

        :param stream: name of the stream
        :type stream: str
        :returns: list of plot ID number
        :rtype: list(int)
        """

        # Get current view
        current_view = self.get_current_view()

        return [plot.id_number for plot in current_view.plots if stream in plot.streams]

    def _get_stream_value(self, stream, time):
        """ Get the linearly interpolated value of a stream at a given time.
        :param stream: stream name
        :type stream: str
        :param time: current time
        :type time: float
        :returns: interpolated value
        :rtype: float
        """

        x, y = self.parent_session.sensors_data.get_streams(['time', stream])
        return np.interp(time, x, y)

    def _get_all_streams_value(self, time):
        """ Get the linearly interpolated value of all streams at a given time.
        :param time: current time
        :type time: float
        :returns: interpolated value
        :rtype: dict
        """

        table_data = {}
        for stream in self.parent_session.sensors_data.fields:
            table_data[stream] = self._get_stream_value(stream, time)

        return table_data

    def _buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed.')

    def closeEvent(self, event):

        # Close tabs
        with signals_blocked(self.tab_widget):
            for i in range(self.tab_widget.count() - 1, -1, -1):
                tab = self.tab_widget.widget(i)
                self.tab_widget.removeTab(i)
                tab.setParent(None)
                tab.deleteLater()

            self.tab_widget.deleteLater()

        # Window
        self.deleteLater()
        super().closeEvent(event)

    def _remove_view(self, index):

        # Remove current view
        name = str(self.tab_widget.tabText(index))
        self.views.pop(name)
        tab = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        tab.setParent(None)
        tab.deleteLater()

        # Display status
        self.statusBar().showMessage("Removing view %s" % name)

    def _on_new_view_button_clicked(self):

        empty_plot = Plot()
        new_view = View([empty_plot])
        self._build_new_view(new_view, parent=self.tab_widget)

        # Emit signal to modify view displayed
        if hasattr(new_view, 'vertical_widget_plots'):
            self.tab_widget.setCurrentWidget(new_view.vertical_widget_plots)

        # Display status
        self.statusBar().showMessage("New view %s created" % new_view.name)

    def _on_rename_view_button_clicked(self):

        # Get current view
        current_view = self.get_current_view()
        old_name = current_view.name

        # Fill in with current name
        self.line_edit_view.setTextValue(old_name)

        # Launch dialog
        if self.line_edit_view.exec_() == QtWidgets.QDialog.Accepted:
            new_name = str(self.line_edit_view.textValue())
            if not new_name == '':
                current_view.name = new_name
                self.views[new_name] = self.views.pop(old_name)

                # Update tab bar
                self.tab_widget.tabBar().setTabText(self.get_current_view_index(), new_name)

                # Display status
                self.statusBar().showMessage("Current view name changed from %s to %s" % (old_name, new_name))
            else:
                self.statusBar().showMessage("View name cannot be empty")

    def _on_save_view_button_clicked(self):

        # For now, saving a view is the same as saving a session
        self._on_save_session_button_clicked()

        # Display status
        self.statusBar().showMessage("View saved")

    def _on_load_view_button_clicked(self):

        # Display status
        self.statusBar().showMessage("Loading view")

        # Create Dialog with appropriate defaults
        # Only show existing files
        self.dlg_load.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.dlg_load.setDirectory(".")

        # Set JSON extension as filter
        self.dlg_load.setDefaultSuffix('json')
        self.dlg_load.setNameFilters(['JSON (*.json)'])
        self.dlg_load.setModal(True)

        # Launch dialog
        if self.dlg_load.exec_() == QtWidgets.QDialog.Accepted:

            # Get filename
            filenames = self.dlg_load.selectedFiles()
            filename = os.path.abspath(str(filenames[0]))

            # Put information in a dictionary
            with open(filename) as data_file:
                dictionary = json.load(data_file)

            views_dict = dictionary['window']['views']

            # Deserialize Views
            for name, view_dict in views_dict.items():

                # Deserialize Plots
                plots = []
                for plot_dict in view_dict['plots']:
                    plots.append(Plot.deserialize(plot_dict, self.parent_session.sensors_data))

                # Make sure name is not taken
                name = self._check_and_update_view_name(name)
                view_dict['name'] = name
                self.views[name] = View.deserialize(view_dict, plots)

                # Build view
                self._build_view(self.views[name], parent=self.tab_widget)

            # Display status
            self.statusBar().showMessage('View loaded')
        else:
            self.statusBar().showMessage('Cancelled loading view')

    def _on_copy_btn_clicked(self):

        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.text_label)

        self.statusBar().showMessage('Path to sensors file copied to clipboard')

    def _on_refresh_btn_clicked(self):
        """Refresh the sensors data and views."""

        # Stop the time if necessary
        if len(self.videos) > 0:
            if self.timer.status_running:
                self.timer.stop()

        # Refresh data
        self.parent_session.refresh_sensors_data()

        # Refresh views
        for view in self.views.values():
            for plot in view.plots:
                for stream in plot.streams:
                    x, y = self.parent_session.sensors_data.get_streams(['time', stream])
                    plot._update_stream(x, y, stream)

        # SelectionTable: we should not have to do anything during refreshing
        # The streams are the same and current_time does not change

        # Message
        self.statusBar().showMessage('Sensors data, plots, and table refreshed.')

    def get_current_view(self):
        """ Get the View that is currently shown.

        :returns: Current view
        :rtype: :py:class:`View<RAI.view.View>`
        """

        current_widget = self.tab_widget.currentWidget()
        current_widget_index = self.tab_widget.indexOf(current_widget)
        current_widget_name = self.tab_widget.tabText(current_widget_index)

        return self.views[str(current_widget_name)]

    def get_current_view_index(self):
        """ Get the tab index of the View that is currently shown.

        :returns: Tab index of the current view.
        :rtype: int
        """

        current_widget = self.tab_widget.currentWidget()
        current_widget_index = self.tab_widget.indexOf(current_widget)

        return current_widget_index

    def _check_and_update_view_name(self, name):
        """ Check if a View name is already taken, and modify it if necessary.

        :param name: View name
        :type name: str
        """

        if name in self.views:
            i = 1
            while name + str(i) in self.views:
                i += 1
            name = name + str(i)

        return name

    def _search_pattern_changed(self, pattern):
        """ Method to update the table when a regular expression is entered in the search bar.
        :param pattern: pattern to be matched
        :type pattern: str
        """

        # Create regular expression
        rexp = QtCore.QRegExp(str(pattern) + '*')
        rexp.setPatternSyntax(QtCore.QRegExp.Wildcard)

        # Update Selection table
        self.selection_table._select_streams_to_show(rexp)
