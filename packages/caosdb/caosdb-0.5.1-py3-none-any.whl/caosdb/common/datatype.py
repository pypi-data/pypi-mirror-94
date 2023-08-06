# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 IndiScale GmbH
# Copyright (C) 2020 Henrik tom Wörden, IndiScale GmbH
# Copyright (C) 2020 Daniel Hornung (d.hornung@indiscale.com)
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

import re

from ..exceptions import EmptyUniqueQueryError, QueryNotUniqueError

DOUBLE = "DOUBLE"
REFERENCE = "REFERENCE"
TEXT = "TEXT"
DATETIME = "DATETIME"
INTEGER = "INTEGER"
FILE = "FILE"
BOOLEAN = "BOOLEAN"


def LIST(datatype):
    if hasattr(datatype, "name"):
        datatype = datatype.name

    return "LIST<" + str(datatype) + ">"


def get_list_datatype(datatype):
    """ returns the datatype of the elements in the list """
    match = re.match("LIST(<|&lt;)(?P<datatype>.*)(>|&gt;)", datatype)

    if match is not None:
        return match.group("datatype")
    else:
        return None


def is_list_datatype(datatype):
    """ returns whether the datatype is a list """

    return get_list_datatype(datatype) is not None


def is_reference(datatype):
    """ returns whether the value is a reference

    FILE and REFERENCE properties are examples, but also datatypes that are
    RecordTypes
    """

    if datatype in [DOUBLE, BOOLEAN, INTEGER, TEXT, DATETIME]:
        return False
    elif is_list_datatype(datatype):
        return is_reference(get_list_datatype(datatype))
    else:
        return True


def get_id_of_datatype(datatype):
    """ returns the id of a Record Type

    This is not trivial, as queries may also return children. A check comparing
    names is necessary.

    Parameters
    ----------
    datatype : string
        A datatype, e.g. DOUBLE, or LIST<Person>

    Returns
    -------
    The id of the RecordType with the same name as the datatype.

    Raises
    ------
    QueryNotUniqueError
        If there are more than one entities with the same name as the datatype.
    EmptyUniqueQueryError
        If there is no entity with the name of the datatype.
    """
    from caosdb import execute_query

    if is_list_datatype(datatype):
        datatype = get_list_datatype(datatype)
    q = "FIND RECORDTYPE {}".format(datatype)

    # we cannot use unique=True here, because there might be subtypes
    res = execute_query(q)
    res = [el for el in res if el.name.lower() == datatype.lower()]

    if len(res) > 1:
        raise QueryNotUniqueError(
            "Name {} did not lead to unique result; Missing "
            "implementation".format(datatype))
    elif len(res) != 1:
        raise EmptyUniqueQueryError(
            "No RecordType named {}".format(datatype))

    return res[0].id
