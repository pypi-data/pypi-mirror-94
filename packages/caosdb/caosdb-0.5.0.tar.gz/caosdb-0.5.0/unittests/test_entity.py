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
"""Tests for the Entity class."""
# pylint: disable=missing-docstring
import unittest

from caosdb import (INTEGER, Entity, Property, Record, RecordType,
                    configure_connection)
from caosdb.connection.mockup import MockUpServerConnection


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.assertIsNotNone(Entity)
        configure_connection(url="unittests", username="testuser",
                             password_method="plain",
                             password="testpassword", timeout=200,
                             implementation=MockUpServerConnection)

    def test_instance_variables(self):
        entity = Entity()
        self.assertTrue(hasattr(entity, "role"))
        self.assertTrue(hasattr(entity, "id"))
        self.assertTrue(hasattr(entity, "name"))
        self.assertTrue(hasattr(entity, "description"))
        self.assertTrue(hasattr(entity, "parents"))
        self.assertTrue(hasattr(entity, "properties"))

    def test_role(self):
        entity = Entity(role="TestRole")
        self.assertEqual(entity.role, "TestRole")
        entity.role = "TestRole2"
        self.assertEqual(entity.role, "TestRole2")

    def test_instanciation(self):
        self.assertRaises(Exception, Entity())
