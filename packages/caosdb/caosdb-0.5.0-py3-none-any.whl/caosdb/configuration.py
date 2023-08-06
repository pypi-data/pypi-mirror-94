# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#
try:
    # python2
    from ConfigParser import ConfigParser
except ImportError:
    # python3
    from configparser import ConfigParser


def _reset_config():
    global _pycaosdbconf
    _pycaosdbconf = ConfigParser(allow_no_value=False)


def configure(inifile):
    """read config from file.

    Return a list of files which have successfully been parsed.
    """
    global _pycaosdbconf
    if "_pycaosdbconf" not in globals():
        _pycaosdbconf = None
    if _pycaosdbconf is None:
        _reset_config()
    return _pycaosdbconf.read(inifile)


def get_config():
    return _pycaosdbconf
