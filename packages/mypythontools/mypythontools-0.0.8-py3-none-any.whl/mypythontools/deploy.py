"""
Allow to deploy project.
Possible destinations: PYPI.
"""
import subprocess
import os

from . import misc


def deploy_to_pypi(setup_path=None):
    """Publish python library to Pypi. Username and password are set
    with env vars `TWINE_USERNAME` and `TWINE_PASSWORD`.

    Args:
        setup_path((str, pathlib.Path)): Function suppose, that there is a setup.py in cwd. If not, pass path to setup.py.
        username
        password
    """
    setup_path = misc.root_path if not setup_path else setup_path

    subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], cwd=misc.root_path, shell=True, check=True)

    # TODO move to separate  folder (dist name conflict) and clean afterwards
    subprocess.run(['twine', 'upload', '-u', os.environ['TWINE_USERNAME'], '-p', os.environ['TWINE_PASSWORD'], 'dist/*'], cwd=misc.root_path, shell=True, check=True)
