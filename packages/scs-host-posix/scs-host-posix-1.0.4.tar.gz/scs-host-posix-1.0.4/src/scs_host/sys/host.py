"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
http://code.activestate.com/recipes/577972-disk-usage/
"""

import os
import socket

from pathlib import Path

from scs_core.sys.ipv4_address import IPv4Address
from scs_core.sys.node import Node
from scs_core.sys.persistence_manager import FilesystemPersistenceManager


# --------------------------------------------------------------------------------------------------------------------

class Host(Node, FilesystemPersistenceManager):
    """
    Any Darwin Mac or Linux
    """

    # ----------------------------------------------------------------------------------------------------------------
    # directories and files...

    OS_ENV_PATH =           'SCS_ROOT_PATH'

    __SCS_DIR =             "SCS"                               # hard-coded rel path
    __LATEST_UPDATE =       "latest_update.txt"                 # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------
    # host acting as DHCP server...

    __SERVER_IPV4_ADDRESS =      None                           # had-coded abs path


    # ----------------------------------------------------------------------------------------------------------------
    # network identity...

    @classmethod
    def name(cls):
        full_name = socket.gethostname()
        full_names = full_name.split('.')

        return full_names[0]


    @classmethod
    def server_ipv4_address(cls):
        return IPv4Address.construct(cls.__SERVER_IPV4_ADDRESS)


    # ----------------------------------------------------------------------------------------------------------------
    # software update...

    @classmethod
    def software_update_report(cls):
        try:
            f = open(os.path.join(cls.scs_path(), cls.__LATEST_UPDATE))
            report = f.read().strip()
            f.close()

            return report

        except FileNotFoundError:
            return None


    # ----------------------------------------------------------------------------------------------------------------
    # filesystem paths...

    @classmethod
    def home_path(cls):
        return os.environ[cls.OS_ENV_PATH] if cls.OS_ENV_PATH in os.environ else str(Path.home())


    @classmethod
    def scs_path(cls):
        return os.path.join(cls.home_path(), cls.__SCS_DIR)
