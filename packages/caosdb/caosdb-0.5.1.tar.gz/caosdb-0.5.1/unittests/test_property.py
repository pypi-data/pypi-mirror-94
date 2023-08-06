# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
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
"""Tests for the Property class."""
# pylint: disable=missing-docstring
from lxml import etree
from caosdb import Entity, Property, Record

parser = etree.XMLParser(remove_comments=True)
testrecord = Record._from_xml(Record(),
                              etree.parse("unittests/test_record.xml",
                                          parser).getroot())


def test_is_entity():
    prop = Property()
    assert isinstance(prop, Entity)


def test_instance_variables():
    prop = Property()
    assert hasattr(prop, "datatype")
    assert hasattr(prop, "unit")
    assert hasattr(prop, "value")


def test_null_empty_text_value_1():
    assert testrecord.get_property("LISTofTEXT").value == ["One", "Two", "Three", None, ""]


def test_null_empty_text_value_2():
    assert testrecord.get_property("NULLTEXT1").value is None


def test_null_empty_text_value_3():
    assert testrecord.get_property("NULLTEXT2").value is None


def test_null_empty_text_value_4():
    assert testrecord.get_property("EMPTYTEXT1").value == ""


def test_null_empty_text_value_5():
    assert testrecord.get_property("EMPTYTEXT2").value == ""


def test_list_of_references_with_null():
    assert testrecord.get_property("MultiRecRecording").value[0] is None
    assert testrecord.get_property("MultiRecRecording").value[1] == 170651


def test_role():
    prop = Property()
    assert prop.role == "Property"


def test_get_property_with_entity():
    p = Property(name="Prop")
    r = Record().add_property("Prop", "blub")
    assert r.get_property(p).value == "blub"

    p = Property(id=1234)
    r.add_property(id=1234, value="bla")
    assert r.get_property(p).value == "bla"


def test_selected_reference_list():
    assert len(testrecord.get_property("Conductor").value) == 1
    assert isinstance(testrecord.get_property("Conductor").value[0], Entity)
