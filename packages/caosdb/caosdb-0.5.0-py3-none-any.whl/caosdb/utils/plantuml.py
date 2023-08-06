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

"""Utilities for work with PlantUML.

PlantUML (http://plantuml.com) is a converter from a simple
descriptive language to graphviz diagrams.

To convert the output, you can write it into FILENAME.pu and then
convert it with:

plantuml FILENAME.pu -> FILENAME.png
"""

import os

import caosdb as db

REFERENCE = "REFERENCE"


def get_description(description_str):
    words = description_str.split()
    lines = []
    lines.append("")

    for w in words:
        if len(lines[-1] + w) > 60:
            lines.append("")

        if len(lines[-1]) > 0:
            lines[-1] += " "
        lines[-1] += w
    description = "\n".join(lines)

    return description + "\n"


class Grouped(object):
    def __init__(self, name, parents):
        self.name = name
        self.parents = parents

    def get_parents(self):
        return self.parents


def recordtypes_to_plantuml_string(iterable):
    """Converts RecordTypes into a string for PlantUML.

    This function obtains an iterable and returns a string which can
    be input into PlantUML for a representation of all RecordTypes in
    the iterable.

    Current limitations
    -------------------

    - It is inherently hard to detect if an element should be rendered
      as a class/RecordType or not.  Currently it is rendered if
      either the "type" attribute is None or
      type(element) == RecordType.
    - Inheritance of Properties is not rendered nicely at the moment.
    """

    classes = [el for el in iterable
               if isinstance(el, db.RecordType)]
    dependencies = {}
    inheritances = {}
    properties = [p for p in iterable if isinstance(p, db.Property)]
    grouped = [g for g in iterable if isinstance(g, Grouped)]

    def _add_properties(c, importance=None):
        result = ""

        for p in c.get_properties():
            if importance is None or c.get_properties().get_importance(p) == importance:
                if importance is not None and len(result) == 0:
                    result += ".." + importance.lower() + "..\n"
                name = p.name
                p_type = p.datatype

                if p_type is None:
                    # get type from properties

                    for p2 in properties:
                        if p2.name == p.name:
                            p_type = p2.datatype

                if p_type is None:
                    # is reference?

                    for p2 in classes:
                        if p2.name == p.name:
                            p_type = p2

                if isinstance(p_type, db.Entity):
                    p_type = p_type.name
                    dependencies[c].append(p_type)
                elif p_type is not None:
                    for c2 in classes:
                        if c2.name == p_type or db.LIST(c2.name) == p_type:
                            dependencies[c].append(c2.name)
                result += '  {name} ({type})\n'.format(
                    name=name, type=p_type)

        return result

    result = "@startuml\n\n"
    result += "skinparam classAttributeIconSize 0\n"

    result += "package Properties #DDDDDD {\n"

    for p in properties:
        inheritances[p] = p.get_parents()
        dependencies[p] = []

        result += "class \"{klass}\" << (P,#008800) >> {{\n".format(klass=p.name)

        if p.description is not None:
            result += get_description(p.description)
        result += "\n..\n"

        if isinstance(p.datatype, str):
            result += "datatype: " + p.datatype + "\n"
        elif isinstance(p.datatype, db.Entity):
            result += "datatype: " + p.datatype.name + "\n"
        else:
            result += "datatype: " + str(p.datatype) + "\n"
        result += "}\n\n"
    result += "}\n\n"

    result += "package RecordTypes #DDDDDD {\n"

    for c in classes:
        inheritances[c] = c.get_parents()
        dependencies[c] = []
        result += "class \"{klass}\" << (C,#FF1111) >> {{\n".format(klass=c.name)

        if c.description is not None:
            result += get_description(c.description)

        props = ""
        props += _add_properties(c, importance=db.FIX)
        props += _add_properties(c, importance=db.OBLIGATORY)
        props += _add_properties(c, importance=db.RECOMMENDED)
        props += _add_properties(c, importance=db.SUGGESTED)

        if len(props) > 0:
            result += "__Properties__\n" + props
        else:
            result += "\n..\n"
        result += "}\n\n"

    for g in grouped:
        inheritances[g] = g.get_parents()
        result += "class \"{klass}\" << (G,#0000FF) >> {{\n".format(klass=g.name)
    result += "}\n\n"

    for c, parents in inheritances.items():
        for par in parents:
            result += "\"{par}\" <|-- \"{klass}\"\n".format(
                klass=c.name, par=par.name)

    for c, deps in dependencies.items():
        for dep in deps:
            result += "\"{klass}\" *-- \"{dep}\"\n".format(
                klass=c.name, dep=dep)

    result += """

package \"B is a subtype of A\" <<Rectangle>> {
 A <|-right- B
 note  "This determines what you find when you query for the RecordType.\\n'FIND RECORD A' will provide Records which have a parent\\nA or B, while 'FIND RECORD B' will provide only Records which have a parent B." as N1
}
"""
    result += """

package \"The property P references an instance of D\" <<Rectangle>> {
 class C {
    P(D)
 }
 C *-right- D
 note  "Employ this when searching for C: 'FIND RECORD C WITH D'\\nOr if the value of D is a Record: 'FIND RECORD C WHICH REFERENCES D' is possible.\\nEmploying this while searching for D: 'FIND RECORD D WHICH IS REFERENCED BY C" as N2
}

"""

    result += "\n@enduml\n"

    return result


def to_graphics(recordtypes, filename):
    """ calls recordtypes_to_plantuml_string(), saves result to file and
    creates an svg image

    plantuml needs to be installed
    @params:
    recordtypes: itrable with the record types to be displayed
    filname: filename of the image (e.g. data_structure; data_structure.pu and
    data_structure.svg will be created.
    """
    pu = recordtypes_to_plantuml_string(recordtypes)

    pu_filename = filename+".pu"
    with open(pu_filename, "w") as pu_file:
        pu_file.write(pu)

    cmd = "plantuml -tsvg %s" % pu_filename
    print("Executing:", cmd)

    if os.system(cmd) != 0:
        raise Exception("An error occured during the execution of plantuml. "
                        "Is plantuml installed?")
