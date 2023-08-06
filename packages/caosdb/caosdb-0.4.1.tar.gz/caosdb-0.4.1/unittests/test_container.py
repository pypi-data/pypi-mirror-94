
# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
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
"""Tests for the Container class."""
from __future__ import absolute_import

import caosdb as c


def test_get_property_values():
    rt_house = c.RecordType("House")
    rt_window = c.RecordType("Window")
    rt_owner = c.RecordType("Owner")
    p_height = c.Property("Height", datatype=c.DOUBLE)

    window = c.Record().add_parent(rt_window)
    window.id = 1001
    window.add_property(p_height, 20.5, unit="m")

    owner = c.Record("The Queen").add_parent(rt_owner)

    house = c.Record("Buckingham Palace")
    house.add_parent(rt_house)
    house.add_property(rt_owner, owner)
    house.add_property(rt_window, window)
    house.add_property(p_height, 40.2, unit="ft")

    container = c.Container()
    container.extend([
        house,
        owner
    ])

    assert getattr(house.get_property(p_height), "unit") == "ft"
    assert getattr(window.get_property(p_height), "unit") == "m"

    table = container.get_property_values("naME",
                                          "height",
                                          ("height", "unit"),
                                          "window",
                                          ("window", "non-existing"),
                                          ("window", "non-existing", "unit"),
                                          ("window", "unit"),
                                          ("window", "heiGHT"),
                                          ("window", "heiGHT", "value"),
                                          ("window", "heiGHT", "unit"),
                                          "owner",
                                          )
    assert len(table) == 2
    house_row = table[0]
    assert house_row == (house.name, 40.2, "ft", window.id, None, None, None, 20.5, 20.5, "m", owner.name)

    owner_row = table[1]
    assert owner_row == (owner.name, None, None, None, None, None, None, None, None, None, None)

    assert container.get_property_values("non-existing") == [(None,), (None,)]
    assert container.get_property_values("name") == [(house.name,),
                                                     (owner.name,)]
