# Copyright (c) 2017 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import print_function
from six.moves import input
from typing import Optional
import ctypes
import os
import platform
import subprocess
import re


class ExitCLI(Exception):
    """Custom Exception when exit with 1 should happen"""
    pass


def ask_question(question, accept_confirmation=False):
    """Method to ask the user a yes/no question

    Args:
        question(str): A question to ask the user
        accept_confirmation(bool): Optional flag, if True will automatically accept question

    Returns:
        bool: True if yes, False if no
    """
    if accept_confirmation:
        return True

    valid_response = {"yes": True, "y": True, "no": False, "n": False}

    while True:
        print("{} [y/n]: ".format(question), end="")
        choice = input().lower().strip()
        if choice in valid_response:
            return valid_response[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def is_running_as_admin():
    """Method to check if the python script is running as an administrator

    Returns:
        bool
    """
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()

    return is_admin


def get_nvidia_driver_version() -> Optional[str]:
    driver_version = None
    if platform.system() == 'Linux':
        try:
            bash_command = "nvidia-smi --query-gpu=driver_version --format=csv,noheader"
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if not error:
                m = re.match(r"([\d.]+)", output.decode())
                if m:
                    driver_version = m.group(0)

                # If driver has a build version, strip it because we don't match on that.
                parts = driver_version.split('.')
                driver_version = f"{parts[0]}.{parts[1]}"

        except FileNotFoundError:
            pass
    return driver_version
