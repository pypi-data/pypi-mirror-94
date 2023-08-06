# -*- encoding: utf-8 -*-
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

import caosdb as db
from pytest import raises


def test_config_ini_via_envvar():
    from os import environ
    from os.path import expanduser

    with raises(KeyError):
        environ["PYCAOSDBINI"]

    environ["PYCAOSDBINI"] = "bla bla"
    assert environ["PYCAOSDBINI"] == "bla bla"
    assert db.configuration.configure(environ["PYCAOSDBINI"]) == []
    environ["PYCAOSDBINI"] = "~/.pycaosdb.ini"
    assert db.configuration.configure(expanduser(environ["PYCAOSDBINI"])) == [expanduser("~/.pycaosdb.ini")]
