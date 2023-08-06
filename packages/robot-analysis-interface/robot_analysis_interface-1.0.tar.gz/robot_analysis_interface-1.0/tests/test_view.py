import json
from pathlib import Path
import tempfile

from PyQt5 import QtTest, QtWidgets

from RAI.main_window import CompositeWindow
from RAI.plotting import Plot
from RAI.view import View

from .fixtures import (
    WAIT_TIME,
    TestCaseDefault, PatchWrapper
)


class TestView(TestCaseDefault):
    """Class for testing the View."""

    def setUp(self):
        super().setUp()

        # Side effect for the QInputDialog
        def change_text_and_return():
            self.win.line_edit_view.setTextValue('Awesome view')
            return 1

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("serialize", Plot, prefix='plot'),
            PatchWrapper("_on_save_session_button_clicked", CompositeWindow),
            PatchWrapper("exec_", QtWidgets.QFileDialog, return_value=1),  # OK
            PatchWrapper("exec_", QtWidgets.QInputDialog, prefix='input',
                         side_effect=change_text_and_return),

        )

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Add view
        self.win._on_new_view_button_clicked()

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_add_view(self):
        """Test adding a new View."""

        # Initial number of views
        nviews = len(self.win.views)

        # Check the number of tabs
        self.assertEqual(nviews, self.win.tab_widget.count())

        # Add view
        self.win._on_new_view_button_clicked()
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that a view and a tab have been added
        self.assertEqual(len(self.win.views), nviews + 1)
        self.assertEqual(self.win.tab_widget.count(), nviews + 1)

        # Check that the names are different
        views = self.views.values()
        for i, view in enumerate(views):
            if i > 0:
                self.assertNotEqual(view.name, views[0].name)

    def test_serialize(self):
        """Test the serialization of a View."""

        from RAI.session import RAIEncoder

        view = self.win.get_current_view()
        dictionary = json.loads(json.dumps(view, sort_keys=True, indent=4, cls=RAIEncoder))
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the serialization of Plots has been called
        self.assertEqual(self.get_patch('plot_serialize').mock.call_count, len(view.plots))

        # Check that the dictionary is not empty
        self.assertGreater(len(dictionary), 0)

        # The dictionary should have at least some fundamental elements
        elements = ['name', 'plots', 'serial_version']

        for x in elements:
            self.assertIsNotNone(dictionary[x])

    def test_deserialize(self):
        """Test the deserialization of a View."""

        from RAI.session import RAIEncoder

        view = self.win.get_current_view()
        dictionary = json.loads(json.dumps(view, sort_keys=True, indent=4, cls=RAIEncoder))
        QtTest.QTest.qWait(WAIT_TIME)

        # Load plot
        loaded_view = View.deserialize(dictionary, view.plots)
        QtTest.QTest.qWait(WAIT_TIME)

        # The dictionary should have at least some fundamental elements
        elements = ['name', 'plots']

        for elem in elements:
            a = getattr(view, elem)
            b = getattr(loaded_view, elem)
            self.assertEqual(a, b)

    def test_save_view(self):
        """Test saving a View."""

        # Save view
        self.win._on_save_view_button_clicked()
        QtTest.QTest.qWait(WAIT_TIME)

        # Check calls
        self.assertEqual(self.get_patch('_on_save_session_button_clicked').mock.call_count, 1)

    def test_remove_view(self):
        """Test removing a View."""

        # Initial configuration
        nviews = len(self.win.views)

        # Current view (will be deleted)
        current_view = self.win.get_current_view()
        current_view_name = current_view.name
        current_view_index = self.win.get_current_view_index()

        # Remove first view
        self.win._remove_view(current_view_index)
        QtTest.QTest.qWait(WAIT_TIME)

        # Checks
        nviews2 = len(self.win.views)
        current_view2 = self.win.get_current_view()
        current_view_name2 = current_view2.name
        self.assertEqual(nviews2, nviews - 1)
        self.assertNotEqual(current_view_name, current_view_name2)

    def test_rename_view(self):
        """Test renaming current View."""

        # Current view
        current_view = self.win.get_current_view()
        current_view_name = current_view.name

        # Rename view
        self.win._on_rename_view_button_clicked()

        # Check that names has changed
        current_view2 = self.win.get_current_view()
        current_view_name2 = current_view2.name

        # Check names are different
        self.assertEqual(current_view, current_view2)
        self.assertNotEqual(current_view_name, current_view_name2)

    def test_load_view(self):
        """Test loading a View."""

        # Choose file to save to.
        with tempfile.NamedTemporaryFile(suffix='.json', dir='.') as tf:
            self.win.dlg_load.selectFile(tf.name)

            # Initial configuration
            nviews = len(self.win.views)

            # First, save session
            self.session.videos = self.videos
            self.session.window = self.win

            # We need to stop this patch to be able to save the session
            self.get_patch('plot_serialize').stop()
            self.session.save(tf.name)
            QtTest.QTest.qWait(WAIT_TIME)

            # Load view
            self.win._on_load_view_button_clicked()
            QtTest.QTest.qWait(WAIT_TIME)

            # Checks that the new number of views
            nviews2 = len(self.win.views)
            self.assertEqual(nviews2, 2 * nviews)

            # Check that the names are different
            views = self.views.values()
            for i, view in enumerate(views):
                if i > 0:
                    self.assertNotEqual(view.name, views[0].name)
