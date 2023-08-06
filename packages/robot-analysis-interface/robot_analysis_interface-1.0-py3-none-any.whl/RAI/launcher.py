'''
LAUNCHER
========

This module provides a launcher to ease the creation of a :py:class:`Session`.

:author: Maximilien Naveau <mnaveau@tuebingen.mpg.de>
'''

import sys
import os
import re
import glob
import json
from RAI.session import Session
import argparse
import datetime


def manage_arguments(args):
    # reset variables
    session_filename = None
    sensors_filename = None

    # determine the session file name and path
    if args.session is not None:
        _, extension = os.path.splitext(args.session)
        if extension != '.json':
            print("session file", args.session, "is not a json file, it will be ignored.")
        elif not os.path.isfile(args.session):
            print("session file", args.session, "does not exist, it will be ignored.")
        else:
            session_filename = args.session
    if session_filename is not None:
        print("use this session:", session_filename)
    else:
        print("use a clean session")

    # determine the sensors file (d-file) name and path
    # if the sensors_filename is not found look in the current folder if any
    # and pick the one with highest number
    # if nothing is found kill the launcher
    if args.data is None:
        dg_dir = []
        for folder in glob.glob('*'):
            try:
                dg_dir.append(datetime.datetime.strptime(folder[-19:], '%Y-%m-%d_%H-%M-%S'))
            except:
                pass
        if dg_dir:
            dg_dir = max(dg_dir).strftime('%Y-%m-%d_%H-%M-%S')
            sensors_filename = os.path.join(os.getcwd(), dg_dir)
            print("open the last dg folder: ", sensors_filename)
        else:
            expr = re.compile("d(\d+)")
            all_names = [_ for _ in glob.glob('d*') if re.match(expr, _) is not None]
            if len(all_names) == 0:
                raise ValueError("There are no data file found in the current " +
                                 "folder. Please check if a d-file exist.")
            sensors_filename = max(all_names)
            print("open the last d* file: ", sensors_filename)
    else:
        if not os.path.isfile(args.data) and not os.path.isdir(args.data):
            raise ValueError("Data not found at: [" + args.data + "].")
        sensors_filename = args.data

    root_path, sensors_filename = os.path.split(os.path.abspath(sensors_filename))

    print("open the requested: ", sensors_filename)
    print("the root_path is: ", root_path)
    return sensors_filename, session_filename, root_path


def session_factory(sensors_filename, session_filename, root_path):

    # just load the data with a blank session
    if session_filename is None:
        my_session = Session(os.path.join(root_path, sensors_filename))
    else:
        # load the json file
        with open(session_filename, 'r') as inputfile:
            session_dict = json.load(inputfile)
        # change the sensors_filename in the json tree
        session_dict['root_path'] = root_path
        session_dict['sensors_data']['filename'] = sensors_filename
        # save back the session in a another file
        my_session = Session.deserialize(session_dict)
    return my_session


def launcher(sys_args):
    """Function to easily create and launch a Session.

    To open an SL generated d-file, you can use this script by doing:

    ``python launcher.py --data d00021 --session session_torques.json``

    where:
        - ``d00021`` is the d-file (optional)
        - ``session_torques.json`` is the file used to restore a RAI session (optional)

    | If ``--data`` is not specified, the launcher will select the d-file in the current directory with the highest number.
    | If ``--session`` is not specified, the launcher will create a default session.
    """

    parser = argparse.ArgumentParser(description="Open plotting GUI (RAI) " +
                                                 "to display graph from SL generated d-file")
    parser.add_argument('--data', metavar='d-file', type=str,
                        help='local path to the d-file you want to open')
    parser.add_argument('--session', metavar='session', type=str,
                        help='local path to the session file you want to open')
    parser.add_argument('--window', dest='window', action='store_true')
    parser.add_argument('--no-window', dest='window', action='store_false')
    parser.set_defaults(window=True)
    args = parser.parse_args(sys_args)

    # manage the argument
    sensors_filename, session_filename, root_path = manage_arguments(args)
    # load the amd plot without the video.
    my_session = session_factory(sensors_filename, session_filename, root_path)

    # launch the session
    if args.window:
        my_session.launch()
    else:
        my_session.window.close()
    return my_session
