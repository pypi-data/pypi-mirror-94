'''
Demos
=====

This module provides demonstrations of the RAI capabilities.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

import pkg_resources
from .video import Video
from .session import Session
from .launcher import launcher
from . import utils


def _demo_plot():
    """Demo showing how to create a window with Plots only."""

    # Sensors files
    sensors_filename = pkg_resources.resource_filename('RAI', 'resources/d00300')

    # Create and launch session
    my_session = Session(sensors_filename)
    my_session.launch()


def _demo_video():
    """Demo showing how to load and display a single Video in an OpenCV window."""

    filename = pkg_resources.resource_filename('RAI', 'resources/solo.mp4')
    vid = Video(filename)
    utils.show_video(vid)


def _demo_session():
    """Demo showing how to create a Session."""

    # Sensors files
    sensors_filename = pkg_resources.resource_filename('RAI', 'resources/d00300')

    # Videos
    videos_list = []
    videos_list.append(pkg_resources.resource_filename('RAI', 'resources/bolt.mp4'))
    videos_list.append(pkg_resources.resource_filename('RAI', 'resources/solo.mp4'))

    # Set up views
    views_data = {}
    views_data['View1'] = {0: ['LF_z', 'momrate_ref__a'], 1: ['momrate_ref__a'], 2: []}
    views_data['View2'] = {0: ['momrate_ref__a']}
    views_data['Empty View'] = {0: []}

    # Create and launch session
    my_session = Session(sensors_filename, videos_list, views_data)
    my_session.launch()


def _demo_launcher():
    """Demo showing how to use the launcher."""

    # Sensors file
    sensors_filename = '--data=' + pkg_resources.resource_filename('RAI', 'resources/d00300')

    # Session file
    session_filename = '--session=' + \
        pkg_resources.resource_filename('RAI', 'resources/session_demo.json')

    # Start launcher
    launcher([sensors_filename, session_filename])


def _demo_hopper():
    """Demo showing how to create a Session using a Pickle file as Sensor."""

    # Sensors files
    sensors_filename = pkg_resources.resource_filename('RAI', 'resources/jviereck_hopper/traj.pkl')

    # Videos
    videos_list = []
    videos_list.append(pkg_resources.resource_filename(
        'RAI', 'resources/jviereck_hopper/recording.mp4'))

    # Set up views
    views_data = {}
    views_data['View1'] = {0: ['baze_z', 'hip'], 1: ['u_knee'], 2: []}
    views_data['View2'] = {0: ['baze_z']}

    # Create and launch session
    my_session = Session(sensors_filename, videos_list, views_data)
    my_session.launch()


def _demo_npzfile():
    """Demo creating a session from a compressed .npz file."""

    # Sensors files
    sensors_filename = pkg_resources.resource_filename('RAI', 'resources/demo_data.npz')

    # Set up views
    views_data = {}
    views_data['SingleView'] = {0: ['data0/y', 'data1/z'], 1: ['data1/y']}

    # Create and launch session
    my_session = Session(sensors_filename, views_data=views_data)
    my_session.launch()


def demo(which=None):
    """Caller for the different demos."""

    DEMOS = {
        'plot': _demo_plot,
        'video': _demo_video,
        'session': _demo_session,
        'launcher': _demo_launcher,
        'hopper': _demo_hopper,
        'npzfile': _demo_npzfile,
    }

    if which not in DEMOS:
        print("Please indicate which demo you want:")
        for key in DEMOS:
            print("\tdemo('%s')" % key)
    else:
        DEMOS[which]()
