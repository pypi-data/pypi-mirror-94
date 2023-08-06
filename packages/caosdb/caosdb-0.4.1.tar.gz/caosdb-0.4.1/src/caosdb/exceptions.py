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

from lxml import etree


class CaosDBException(Exception):
    """Base class of all CaosDB exceptions."""

    def __init__(self, msg=None, *args):
        Exception.__init__(self, msg, *args)
        self.msg = msg


class ConfigurationException(CaosDBException):
    """ConfigurationException.

    Indicates a misconfiguration.

    Parameters
    ----------
    msg : str
        A descriptin of the misconfiguration. The constructor adds
        a few lines with explainingg where to find the configuration.
    *args

    Attributes
    ----------
    msg : str
        A description of the misconfiguration.
    """

    def __init__(self, msg, *args):
        super(ConfigurationException, self).__init__(msg +
                                                     ConfigurationException._INFO,
                                                     *args)

    _INFO = ("\n\nPlease check your ~/.pycaosdb.ini and your $PWD/"
             ".pycaosdb.ini. Do at least one of them exist and are they correct?")


class ClientErrorException(CaosDBException):
    def __init__(self, msg, status, body):
        self.status = status
        self.body = body
        CaosDBException.__init__(self, msg)


class ServerErrorException(CaosDBException):
    def __init__(self, body):
        xml = etree.fromstring(body)
        error = xml.xpath('/Response/Error')[0]
        msg = error.get("description")

        if error.text is not None:
            msg = msg + "\n\n" + error.text
        CaosDBException.__init__(self, msg)


class ConnectionException(CaosDBException):
    """Connection is not configured or the network is down."""

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg)


class URITooLongException(CaosDBException):
    """The URI of the last request was too long."""

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg)


class AmbiguityException(CaosDBException):
    """A retrieval of an entity that was supposed to be uniquely identifiable
    returned two or more entities."""

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg)


class LoginFailedException(CaosDBException):
    """Login failed.

    Probably, your username/password pair is wrong.
    """

    def __init__(self, msg=None):
        CaosDBException.__init__(self, msg=msg)


class TransactionError(CaosDBException):

    def _calc_bases(self):
        types = dict()
        # collect each class once

        for err in self.errors:
            types[id(type(err))] = type(err)
        # delete redundant super classes

        if len(types.values()) > 1:
            # remove TransactionError
            try:
                del types[id(TransactionError)]
            except KeyError:
                pass

        if len(types.values()) > 1:
            # remove EntityError
            try:
                del types[id(EntityError)]
            except KeyError:
                pass

        ret = ()

        for t in types.values():
            ret += (t,)

        if ret == ():
            ret = (type(self),)

        return ret

    def __init__(self, container=None, error=None, msg=None):
        self.container = container
        self.errors = []
        self.msg = msg if msg is not None else str(error)
        self.error = error

    def print_errs(self):
        print(self)

        for err in self.errors:
            err.print_errs()

    def _convert(self):
        t = self._calc_bases()
        try:
            newtype = type('TransactionError', t, {})
        except BaseException:
            self.print_errs()
            raise
        newinstance = newtype(container=self.container, error=self.msg)
        newinstance.errors = self.errors
        newinstance.get_entities = self.get_entities

        return newinstance

    def get_container(self):
        '''
        @return: The container that raised this TransactionError during the last
        transaction.
        '''

        return self.container

    def add_error(self, error):
        """Add an error to this TransactionError.

        @param error: An EntityError or a list of EntityErrors.

        @raise TypeError: If and only if the 'error' parameter is not an
        instance of EntityError.

        @return: self.
        """

        if hasattr(error, "__iter__"):
            for e in error:
                self.add_error(e)

            return self
        elif isinstance(error, TransactionError):
            self.errors.append(error)

            return self
        else:
            raise TypeError(
                "Argument is to be an TransactionError or a list of TransactionErrors.")

    def get_errors(self):
        '''
        @return: A list of all EntityError objects.
        '''

        if hasattr(self, 'errors'):
            return self.errors

        return None

    def _repr_reasons(self, indent):
        if self.get_errors() is not None and len(self.get_errors()) > 0:
            ret = "\n" + indent + "    +--| REASONS |--"

            for c in self.get_errors():
                ret += '\n' + indent + '    |  -> ' + \
                    c.__str__(indent=indent + '    |')
            ret += "\n" + indent + "    +----------------"

            return ret
        else:
            return ''

    def _repr_head(self, indent):
        return str(type(self).__name__) + ((': ' + self.msg)
                                           if hasattr(self, 'msg') and self.msg is not None else '')

    def __str__(self, indent=''):
        ret = self._repr_head(indent=indent)
        ret += self._repr_reasons(indent=indent)

        return ret

    def __repr__(self):
        return self.__str__()

    def get_entities(self):
        '''
        @return: A list of all Entity objects with errors.
        '''
        ret = []

        if hasattr(self, 'get_entity') and self.get_entity() is not None:
            ret.append(self.get_entity())

        for error in self.errors:
            if hasattr(error, 'get_entity'):
                if error.get_entity() not in ret:
                    ret.append(error.get_entity())
#             if hasattr(error, 'get_entities'):
#                 for e in error.get_entities():
#                     if e not in ret:
#                         ret.append(e)
        return ret

    def get_error(self):
        return self.error


class EntityError(TransactionError):

    @staticmethod
    def _sort_t(t):
        if len(t) > 1:
            ret = ()
            '''remove EntityError'''

            for i in range(len(t)):
                if t[i] != EntityError:
                    ret += (t[i],)
            t = ret

        return t

    def _convert(self):
        t = self._calc_bases()
        # TODO is it really a good idea to create dynamically types here?
        newtype = type('EntityMultiError', t+(Exception,), {})
        newinstance = newtype(error=self.error, entity=self.entity)
        setattr(newinstance, 'msg', self.msg)
        setattr(newinstance, 'errors', self.errors)
        setattr(newinstance, 'container', self.container)

        return newinstance

    def __init__(self, error=None, container=None, entity=None):
        TransactionError.__init__(self, container=container)
        self.error = error
        self.entity = entity

        if error is not None and hasattr(error, "encode"):
            self.msg = error
        elif error is not None and hasattr(error, 'description'):
            self.msg = error.description
        elif error is None:
            self.msg = None
        else:
            self.msg = str(error)

    def get_entity(self):
        '''
        @return: The entity that caused this error.
        '''

        if hasattr(self, 'entity'):
            return self.entity

        return None

    @property
    def description(self):
        return self.error.description if self.error is not None else None

    def get_code(self):
        return self.error.code if self.error is not None else None

    def get_error(self):
        '''
        @return: Error Message object of this Error.
        '''

        return self.error

    def _repr_head(self, indent):
        if hasattr(self, 'entity') and self.entity is not None:
            return str(type(self.entity).__name__).upper() + " (" + str(self.entity.id) + (("," + "'" + str(self.entity.name) + "'")
                                                                                           if self.entity.name is not None else '') + ") CAUSED " + TransactionError._repr_head(self, indent)
        else:
            return TransactionError._repr_head(self, indent)


class UniqueNamesError(EntityError):
    """A name was supposed to be unique but was not."""


class UnqualifiedParentsError(EntityError):
    """This entity has unqualified parents (call 'get_errors()' for a list of
    errors of the parent entities or 'get_entities()' for a list of parent
    entities with errors)."""


class UnqualifiedPropertiesError(EntityError):
    """This entity has unqualified properties (call 'get_errors()' for a list
    of errors of the properties or 'get_entities()' for a list of properties
    with errors)."""


class EntityDoesNotExistError(EntityError):
    """This entity does not exist."""


class EntityHasNoDatatypeError(EntityError):
    """This has to have a data type."""


class ConsistencyError(EntityError):
    pass


class AuthorizationException(EntityError):
    """You are not allowed to do what ever you tried to do.

    Maybe you need more privileges or a user account at all.
    """
