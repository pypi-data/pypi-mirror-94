# -*- encoding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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
# Test apiutils
# A. Schlemmer, 02/2018

import caosdb as db
import pickle
import tempfile
from caosdb.apiutils import apply_to_ids
from .test_property import testrecord


def test_convert_object():
    r2 = db.apiutils.convert_to_python_object(testrecord)
    assert r2.species == "Rabbit"


def test_pickle_object():
    r2 = db.apiutils.convert_to_python_object(testrecord)
    with tempfile.TemporaryFile() as f:
        pickle.dump(r2, f)
        f.seek(0)
        rn2 = pickle.load(f)
    assert r2.date == rn2.date


def test_apply_to_ids():
    parent = db.RecordType(id=3456)
    rec = db.Record(id=23)
    p = db.Property(id=23345, datatype=db.INTEGER)
    rec.add_parent(parent)
    rec.add_property(p)

    def invert(id_):
        return id_ * -1
    apply_to_ids([rec], invert)

    assert invert(3456) == -3456
    assert rec.parents[0].id == -3456
    assert rec.properties[0].id == -23345
    assert rec.id == -23
