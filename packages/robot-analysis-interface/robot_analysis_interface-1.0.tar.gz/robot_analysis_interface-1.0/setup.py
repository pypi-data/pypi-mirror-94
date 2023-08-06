"""Script for packaging the project."""

from pathlib import Path
from setuptools import setup

# Different names because 'rai' is taken on PyPI
PROJECT_NAME = "robot_analysis_interface"
PACKAGE_NAME = "RAI"


def _get_version():
    """"Convenient function to get the version of this package."""

    ns = {}
    version_path = Path(PACKAGE_NAME) / "version.py"
    if not version_path.is_file():
        return
    with open(version_path) as version_file:
        exec(version_file.read(), ns)
    return ns["__version__"]


dependencies = (
    "numpy",
    "opencv-python==4.3.0.36",
    "packaging",
    "PyQt5",
    "pyqtgraph==0.11.0",
    "qimage2ndarray"
)

classifiers = [
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9"
]

project_urls = {
    'Documentation':
        ('https://machines-in-motion.github.io/code_documentation/'
         'amd-robot-plotting-framework/docs/sphinx/html/index.html'),
}

setup(name=PROJECT_NAME,
      version=_get_version(),
      packages=[PACKAGE_NAME],
      package_data={
          PACKAGE_NAME: [
              "./resources/d00300",
              "./resources/demo_data.npz",
              "./resources/session_demo.json",
              "./resources/solo.mp4",
              "./resources/bolt.mp4",
              "./resources/jviereck_hopper/traj.pkl",
              "./resources/jviereck_hopper/recording.mp4",
              "./static/icon.png"
          ]
      },
      scripts=["bin/rai"],
      install_requires=dependencies,
      url='https://gitlab.tuebingen.mpg.de/SoW/amd-robot-plotting-framework',
      author="Jean-Claude Passy, Maximilien Naveau",
      author_email="jean-claude.passy@tuebingen.mpg.de, maximilien.naveau@tuebingen.mpg.de",
      description="Robot Analysis Infrastructure",
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      platforms=["Linux"],
      python_requires=">=3.6",
      license="BSD-3-Clause",
      project_urls=project_urls,
      classifiers=classifiers,
      )
