# Copyright © 2018-2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module relationships provides relationship classes."""

from abc import abstractmethod

from asyncpg.exceptions import ForeignKeyViolationError

from ajsonapi.conversions import id_name_to_number, id_number_to_name
from ajsonapi.errors import (
    DocumentDataInvalidRelationshipTypeError,
    DocumentDataMalformedRelationshipDataError,
    DocumentDataMalformedRelationshipIdError,
    DocumentDataMissingRelationshipIdError,
    DocumentDataMissingRelationshipTypeError,
    DocumentDataNonexistentIdError,
)
from ajsonapi.exceptions import NonexistentRelationshipIdError
from ajsonapi.field import Field
from ajsonapi.id_value import IdValue
from ajsonapi.logging import log
from ajsonapi.uri.related import (
    ManyToManyRelatedResource,
    ManyToOneRelatedResource,
    OneToManyRelatedResource,
    OneToOneLocalRelatedResource,
    OneToOneRemoteRelatedResource,
)
from ajsonapi.uri.relationship import \
    ManyToManyRelationship as UriManyToManyRelationship
from ajsonapi.uri.relationship import \
    ManyToOneRelationship as UriManyToOneRelationship
from ajsonapi.uri.relationship import \
    OneToManyRelationship as UriOneToManyRelationship
from ajsonapi.uri.relationship import \
    OneToOneLocalRelationship as UriOneToOneLocalRelationship
from ajsonapi.uri.relationship import \
    OneToOneRemoteRelationship as UriOneToOneRemoteRelationship

# pylint: disable=too-many-lines


class Relationship(Field):
    """Abstract base class for all relationships between resources.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable):
        self.rtable = rtable
        self.table = None  # Overridden in Table.__init_subclass__
        self.name = None  # Overridden in Table.__init_subclass__
        self.reverse = None  # Overridden in Table.__init_subclass__
        self.collection = None  # Overriden in Table.__init_subclass__

    @abstractmethod
    def make_uri_relationship(self, collection, id_):
        """Creates a URI Relationship object."""

    @abstractmethod
    def make_uri_related_resource(self, name, collection, id_):
        """Creates a URI Relationship object."""

    @abstractmethod
    async def verify_data_ids_exist(self, env, data_ids):
        """Verifies that a document's data/id members exist."""

    @abstractmethod
    def is_reverse(self, other):
        """Detects whether relationships are each other's reverse.

        Args:
            other: A Relationship instance.

        Returns:
           True if self and other are each other's reverse relationship, False
           otherwise.
        """

    @abstractmethod
    def collection_remote_ids(self, query, local_ids=None):
        """Returns the SQL statement for the remote ids of a relationship's
        local collection.
        """

    @abstractmethod
    def object_remote_ids(self, local_ids=None):
        """Returns the SQL condition for an ?include parameter from an
        object.
        """


class LocalRelationship(Relationship):
    """A relationship with a local foreign key."""

    def __init__(self, rtable, lfkey):
        super().__init__(rtable)
        self.lfkey = lfkey

    def filter_condition(self, values):
        uuids = ','.join(
            f"'{id_name_to_number(uuid)}'" for uuid in values.split(','))
        return f'{self.lfkey} IN ({uuids})'

    @abstractmethod
    def is_reverse(self, other):
        pass

    def sql(self):
        """Produces the SQL column definition for the local foreign key of
        this object.

        Returns:
            A string containing the SQL column definition for the local
            foreign key of this object.
        """

        return f'{self.lfkey} UUID'

    def __str__(self):
        return self.lfkey


class ToOneRelationship(Relationship):
    """A to-one relationship."""

    @abstractmethod
    def is_reverse(self, other):
        pass

    def verify_data_rios(self, data_relationship_name, data_relationship_data,
                         errors):
        """Verifies the resource identifier object specified in a to-one
        relationship in the request document.
        """
        if data_relationship_data is None:
            return None
        relationship_type_name = self.rtable.collection.name

        # Relationship type
        try:
            data_rio_type_name = data_relationship_data['type']
            if data_rio_type_name != relationship_type_name:
                errors.append(
                    DocumentDataInvalidRelationshipTypeError(
                        f'/data/relationships/{data_relationship_name}/data/'
                        f'type/{data_rio_type_name}'))
        except TypeError:
            errors.append(
                DocumentDataMalformedRelationshipDataError(
                    f'/data/relationships/{data_relationship_name}/data'))
            return None
        except KeyError:
            errors.append(
                DocumentDataMissingRelationshipTypeError(
                    f'/data/relationships/{data_relationship_name}/data'))

        # Relationship id
        try:
            data_rio_id_name = data_relationship_data['id']
            try:
                return IdValue(data_rio_id_name)
            except ValueError:
                errors.append(
                    DocumentDataMalformedRelationshipIdError(
                        'Invalid resource identifier object.',
                        f'/data/relationships/{data_relationship_name}/data/'
                        f'id/{data_rio_id_name}'))
        except KeyError:
            errors.append(
                DocumentDataMissingRelationshipIdError(
                    f'/data/relationships/{data_relationship_name}/data'))

        return None

    async def verify_data_ids_exist(self, env, data_ids):
        data_id_number = data_ids.number
        stmt = f'SELECT FROM data.{self.rtable.name} WHERE id=$1'
        async with env.lock:
            log.debug(f'{stmt}: {data_id_number}')
            records = await env.connection.fetch(stmt, data_id_number)
        if records == []:
            data_id_name = data_ids.name
            env.errors.append(
                DocumentDataNonexistentIdError(
                    f'/data/relationships/{self.name}/data/id/{data_id_name}'))


class ToManyRelationship(Relationship):
    """A to-many relationship."""

    @abstractmethod
    def is_reverse(self, other):
        pass

    def verify_data_rios(self, data_relationship_name, data_relationship_data,
                         errors):
        """Verifies the resource identifier objects specified in a
        to-many relationship in the request document.
        """
        relationship_type_name = self.rtable.collection.name
        data_rio_ids = []
        for data_index, data_rio in enumerate(data_relationship_data):
            # Relationship type
            try:
                data_rio_type_name = data_rio['type']
                if data_rio_type_name != relationship_type_name:
                    errors.append(
                        DocumentDataInvalidRelationshipTypeError(
                            f'/data/relationships/{data_relationship_name}/'
                            f'data/{data_index}/type/{data_rio_type_name}'))
            except TypeError:
                errors.append(
                    DocumentDataMalformedRelationshipDataError(
                        f'/data/relationships/{data_relationship_name}/'
                        f'data/{data_index}'))
                continue
            except KeyError:
                errors.append(
                    DocumentDataMissingRelationshipTypeError(
                        f'/data/relationships/{data_relationship_name}/'
                        f'data/{data_index}'))

            # Relationship id
            try:
                data_rio_id_name = data_rio['id']
                try:
                    data_rio_id = IdValue(data_rio_id_name)
                    data_rio_ids.append(data_rio_id)
                except ValueError:
                    errors.append(
                        DocumentDataMalformedRelationshipIdError(
                            'Invalid resource identifier object.',
                            f'/data/relationships/{data_relationship_name}/'
                            f'data/{data_index}/id/{data_rio_id_name}'))
            except KeyError:
                errors.append(
                    DocumentDataMissingRelationshipIdError(
                        f'/data/relationships/{data_relationship_name}/'
                        f'data/{data_index}'))
        return data_rio_ids

    async def verify_data_ids_exist(self, env, data_ids):
        data_id_names = [data_id.name for data_id in data_ids]
        data_id_numbers = [data_id.number for data_id in data_ids]
        stmt = (f'SELECT id '
                f'FROM data.{self.rtable.name} '
                f'WHERE id=ANY($1::UUID[])')
        async with env.lock:
            log.debug(f'{stmt}: {data_id_numbers}')
            records = await env.connection.fetch(stmt, data_id_numbers)
        existing_id_names = {
            id_number_to_name(record['id']) for record in records
        }
        nonexistent_id_names = set(data_id_names) - existing_id_names
        env.errors.extend([
            DocumentDataNonexistentIdError(
                f'/data/relationships/{self.name}/data/id/{id_name}')
            for id_name in nonexistent_id_names
        ])


class OneToOneLocalRelationship(LocalRelationship, ToOneRelationship):
    """A one-to-one relationship between resources with a local foreign key.
    """

    def make_uri_relationship(self, collection, id_):
        return UriOneToOneLocalRelationship(collection, id_, self)

    def make_uri_related_resource(self, name, collection, id_):
        return OneToOneLocalRelatedResource(name, collection, id_, self)

    def is_reverse(self, other):
        return (isinstance(other, OneToOneRemoteRelationship) and
                other.table is self.rtable and other.rtable is self.table and
                other.rfkey == self.lfkey)

    def sql_constraints(self):
        """Returns the SQL unique and foreign key constraints for this
        OneToOneLocalRelationship.
        """

        return [
            f'UNIQUE ({self.lfkey})',
            f'FOREIGN KEY ({self.lfkey}) REFERENCES data.{self.rtable.name}(id)'
        ]

    def collection_remote_ids(self, query, local_ids=None):
        filters = query['filters']
        page = query['page']
        if local_ids is None and filters is None and page == {}:
            partial = ''
        else:
            if filters:
                where_clause = f' WHERE {" AND ".join(filters)}'
            else:
                where_clause = ''

            sort = query['sort']
            if sort:
                order_by_clause = f' ORDER BY {", ".join(sort)}'
            else:
                order_by_clause = ''

            if page:
                limit = page['size']
                offset = page['number'] * limit
                limit_offset_clause = f' LIMIT {limit} OFFSET {offset}'
            else:
                limit_offset_clause = ''

            stmt = (f'SELECT id FROM data.{self.table.name}'
                    f'{where_clause}{order_by_clause}{limit_offset_clause}')
            partial = f' WHERE id IN ({stmt})'
        return f'SELECT {self.lfkey} FROM data.{self.table.name}{partial}'

    def object_remote_ids(self, local_ids=None):
        if local_ids is None:
            partial = '=$1'
        else:
            partial = f' IN ({local_ids})'
        return (f'SELECT {self.lfkey} FROM data.{self.table.name} '
                f'WHERE id{partial}')


class OneToOneRemoteRelationship(ToOneRelationship):
    """A one-to-one relationship between resources with a remote foreign key.
    """

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def filter_condition(self, values):
        uuids = ','.join(
            f"'{id_name_to_number(uuid)}'" for uuid in values.split(','))
        return (f'id IN (SELECT {self.rfkey} from data.{self.rtable.name} '
                f'WHERE id IN ({uuids}))')

    def make_uri_relationship(self, collection, id_):
        return UriOneToOneRemoteRelationship(collection, id_, self)

    def make_uri_related_resource(self, name, collection, id_):
        return OneToOneRemoteRelatedResource(name, collection, id_, self)

    def is_reverse(self, other):
        return (isinstance(other, OneToOneLocalRelationship) and
                other.table is self.rtable and other.rtable is self.table and
                other.lfkey == self.rfkey)

    def collection_remote_ids(self, query, local_ids=None):
        filters = query['filters']
        page = query['page']
        if local_ids is None and filters is None and page == {}:
            where = f'WHERE {self.rfkey} IS NOT NULL'
        else:
            if filters:
                where_clause = f' WHERE {" AND ".join(filters)}'
            else:
                where_clause = ''

            sort = query['sort']
            if sort:
                order_by_clause = f' ORDER BY {", ".join(sort)}'
            else:
                order_by_clause = ''

            if page:
                limit = page['size']
                offset = page['number'] * limit
                limit_offset_clause = f' LIMIT {limit} OFFSET {offset}'
            else:
                limit_offset_clause = ''

            stmt = (f'SELECT id FROM data.{self.table.name}'
                    f'{where_clause}{order_by_clause}{limit_offset_clause}')
            where = f'WHERE {self.rfkey} IN ({stmt})'
        return f'SELECT id FROM data.{self.rtable.name} {where}'

    def object_remote_ids(self, local_ids=None):
        if local_ids is None:
            partial = '=$1'
        else:
            partial = f' IN ({local_ids})'
        return (f'SELECT id FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey}{partial}')

    async def get_collection_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'one_one_remote': {
                        'data': {
                            'type': 'one_one_remotes',
                            'id': UUID_21,
                        },
                        'links': {
                            'self': '/centers/1/relationships/one_one_remote',
                            'related': '/centers/1/one_one_remote',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IS NOT NULL')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rid_by_lid = {record[self.rfkey]: record['id'] for record in records}
        for lid, data in env.data_by_lid.items():
            if lid in rid_by_lid:
                relationship_data = {
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid_by_lid[lid]),
                }
            else:
                relationship_data = None
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }

    async def get_collection_included(self, env, ids):
        """Gets the remote objects of this one-to-one remote relationship that
        need to be included in a GET /{collection} response.
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IN ({ids})')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rid_by_lid = {record[self.rfkey]: record['id'] for record in records}
        for lid, data in env.included_by_id.items():
            if lid in rid_by_lid:
                relationship_data = {
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid_by_lid[lid])
                }
            else:
                relationship_data = None
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }

    async def post_collection_task(self, env):
        """Updates the database with the one-to-one (remote) relationship
        specified in a POST /{collection} request.
        """
        stmt = (f'UPDATE data.{self.rtable.name} '
                f'SET {self.rfkey} = $1 '
                f'WHERE id=$2')
        data_id = env.relationships[self.name]
        if data_id is None:
            return
        data_id_number = data_id.number
        await env.event.wait()
        async with env.lock:
            log.debug(f'{stmt}: {env.id_number}, {data_id_number}')
            result = await env.connection.execute(stmt, env.id_number,
                                                  data_id_number)
        if result == 'UPDATE 0':
            env.cancel()
            raise NonexistentRelationshipIdError()

    async def get_object_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                    },
                    'links': {
                        'self': '/centers/1/relationships/one_one_remote',
                        'related': '/centers/1/one_one_remote',
                    },
                },
            },
        }
        """
        stmt = (f"SELECT id "
                f"FROM data.{self.rtable.name} "
                f"WHERE {self.rfkey} = $1")
        async with env.lock:
            log.debug(f'{stmt}: {env.obj.id.number}')
            record = await env.connection.fetchrow(stmt, env.obj.id.number)
        await env.event.wait()
        if record:
            rel_data = {
                'type': self.rtable.collection.name,
                'id': id_number_to_name(record['id']),
            }
        else:
            rel_data = None
        env.data.setdefault('relationships', {})[self.name] = {
            'data': rel_data,
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_object_included(self, env, ids):
        """Gets the remote objects of this one-to-one remote relationship that
        need to be included in a GET response.
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IN ({ids})')
        async with env.lock:
            log.debug(f'{stmt}: {env.object_id}')
            records = await env.connection.fetch(stmt, env.object_id)
        await env.event.wait()
        rid_by_lid = {record[self.rfkey]: record['id'] for record in records}
        for lid, data in env.included_by_id.items():
            if lid in rid_by_lid:
                relationship_data = {
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid_by_lid[lid])
                }
            else:
                relationship_data = None
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                }
            }

    async def patch_object_task(self, env):
        """Updates the database with the one-to-one (remote) relationship
        specified in a PATCH /{collection} request.
        """
        stmt_remove = (f'UPDATE data.{self.rtable.name} '
                       f'SET {self.rfkey} = NULL '
                       f'WHERE {self.rfkey}=$1')
        stmt_add = (f'UPDATE data.{self.rtable.name} '
                    f'SET {self.rfkey} = $1 '
                    f'WHERE id=$2')
        object_id_number = env.obj.id.number
        data_id = env.relationships[self.name]
        async with env.lock:
            log.debug(f'{stmt_remove}: {object_id_number}')
            await env.connection.execute(stmt_remove, object_id_number)
            if data_id:
                data_id_number = data_id.number
                log.debug(f'{stmt_add}: {object_id_number}, {data_id_number}')
                result = await env.connection.execute(stmt_add,
                                                      object_id_number,
                                                      data_id_number)
                if result == 'UPDATE 0':
                    env.cancel()
                    raise NonexistentRelationshipIdError()

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    'links': {
                        'self': '/one_one_remotes/UUID_21',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneRelationship
            stmt = (f'SELECT id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM data.{env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {env.related.id.number}')
            record = await env.connection.fetchrow(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        if record:
            rel_data = {
                'type': self.rtable.collection.name,
                'id': id_number_to_name(record[0]),
            }
        else:
            rel_data = None
        env.data.setdefault('relationships', {})[self.name] = {
            'data': rel_data,
            'links': {
                'self': (f'/{env.related.relationship.collection.name}/'
                         f'{env.related.id.name}')
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    'links': {
                        'self': '/one_one_remotes/UUID_21',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM data.{env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {env.related.id.number}')
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                rids = rids_by_lid[lid]
                assert len(rids) == 1
                relationship_data = {
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rids[0]),
                }
            else:
                relationship_data = None
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{env.related.relationship.collection.name}/'
                             f'{env.related.id.name}')
                },
            }


class OneToManyRelationship(ToManyRelationship):
    """A one-to-many relationship between resources."""

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def filter_condition(self, values):
        uuids = ','.join(
            f"'{id_name_to_number(uuid)}'" for uuid in values.split(','))
        return (f'id IN (SELECT {self.rfkey} FROM data.{self.rtable.name} '
                f'WHERE id in ({uuids}))')

    def make_uri_relationship(self, collection, id_):
        return UriOneToManyRelationship(collection, id_, self)

    def make_uri_related_resource(self, name, collection, id_):
        return OneToManyRelatedResource(name, collection, id_, self)

    def is_reverse(self, other):
        return (isinstance(other, ManyToOneRelationship) and
                other.table is self.rtable and other.rtable is self.table and
                other.lfkey == self.rfkey)

    def collection_remote_ids(self, query, local_ids=None):
        filters = query['filters']
        page = query['page']
        if local_ids is None and filters is None and page == {}:
            where = f'WHERE {self.rfkey} IS NOT NULL'
        else:
            if filters:
                where_clause = f' WHERE {" AND ".join(filters)}'
            else:
                where_clause = ''

            sort = query['sort']
            if sort:
                order_by_clause = f' ORDER BY {", ".join(sort)}'
            else:
                order_by_clause = ''

            if page:
                limit = page['size']
                offset = page['number'] * limit
                limit_offset_clause = f' LIMIT {limit} OFFSET {offset}'
            else:
                limit_offset_clause = ''

            stmt = (f'SELECT id FROM data.{self.table.name}'
                    f'{where_clause}{order_by_clause}{limit_offset_clause}')
            where = f'WHERE {self.rfkey} IN ({stmt})'
        return f'SELECT id FROM data.{self.rtable.name} {where}'

    def object_remote_ids(self, local_ids=None):
        if local_ids is None:
            partial = '=$1'
        else:
            partial = f' IN ({local_ids})'
        return (f'SELECT id FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey}{partial}')

    async def get_collection_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'one_manys': {
                        'data': [
                            {
                                'type': 'one_manys',
                                'id': UUID_41,
                            },
                            ...
                        ],
                        'links': {
                            'self': '/centers/1/relationships/one_manys',
                            'related': '/centers/1/one_manys',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IS NOT NULL')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.rfkey], []).append(record['id'])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                }
            }

    async def get_collection_included(self, env, ids):
        """Gets the remote objects of this one-to-many relationship that need
        to be included in a GET /{collection} response.
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IN ({ids})')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.rfkey], []).append(record['id'])
        for lid, data in env.included_by_id.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                }
            }

    async def post_collection_task(self, env):
        """Updates the database with the one-to-many relationship specified in
        a POST /{collection} request.
        """
        stmt = (f'UPDATE data.{self.rtable.name} '
                f'SET {self.rfkey} = $1 '
                f'WHERE id=ANY($2::UUID[])')
        data_ids = env.relationships[self.name]
        data_id_numbers = [data_id.number for data_id in data_ids]
        await env.event.wait()
        async with env.lock:
            log.debug(f'{stmt}: {env.id_number}, {data_id_numbers}')
            result = await env.connection.execute(stmt, env.id_number,
                                                  data_id_numbers)
        count = int(result[len('UPDATE '):])
        if count != len(data_id_numbers):
            env.cancel()
            raise NonexistentRelationshipIdError()

    async def get_object_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [
                        {
                            'type': 'one_manys',
                            'id': UUID_41,
                        },
                        ...
                    ],
                    'links': {
                        'self': '/centers/1/relationships/one_manys',
                        'related': '/centers/1/one_manys',
                    },
                },
            },
        }
        """
        lfkey_name = self.rfkey
        stmt = (f"SELECT id "
                f"FROM data.{self.rtable.name} "
                f"WHERE {lfkey_name} = $1")
        async with env.lock:
            log.debug(f'{stmt}: {env.obj.id.number}')
            records = await env.connection.fetch(stmt, env.obj.id.number)
        await env.event.wait()
        rids = [record['id'] for record in records]
        env.data.setdefault('relationships', {})[self.name] = {
            'data': [{
                'type': self.rtable.collection.name,
                'id': id_number_to_name(rid),
            } for rid in rids],
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_object_included(self, env, ids):
        """Gets the remote objects of this one-to-many relationship that need
        to be included in a GET response.
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM data.{self.rtable.name} '
                f'WHERE {self.rfkey} IN ({ids})')
        async with env.lock:
            log.debug(f'{stmt}: {env.object_id}')
            records = await env.connection.fetch(stmt, env.object_id)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.rfkey], []).append(record['id'])
        for lid, data in env.included_by_id.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                }
            }

    async def patch_object_task(self, env):
        """Updates the database with the one-to-many relationship specified in
        a PATCH /{collection}/{id} request.
        """
        stmt_remove = (f'UPDATE data.{self.rtable.name} '
                       f'SET {self.rfkey} = NULL '
                       f'WHERE {self.rfkey} = $1')
        async with env.lock:
            log.debug(f'{stmt_remove}: {env.obj.id.number}')
            await env.connection.execute(stmt_remove, env.obj.id.number)
            data_ids = env.relationships[self.name]
            if data_ids:
                stmt_add = (f'UPDATE data.{self.rtable.name} '
                            f'SET {self.rfkey} = $1 '
                            f'WHERE id=ANY($2::UUID[])')
                data_id_numbers = [data_id.number for data_id in data_ids]
                log.debug(f'{stmt_add}: {env.obj.id.number}, {data_id_numbers}')
                result = await env.connection.execute(stmt_add,
                                                      env.obj.id.number,
                                                      data_id_numbers)
                count = int(result[len('UPDATE '):])
                if count != len(data_id_numbers):
                    env.cancel()
                    raise NonexistentRelationshipIdError()

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneRelationship
            stmt = (f'SELECT id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM data.{env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {env.related.id.number}')
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        rel_data = [{
            'type': self.rtable.collection.name,
            'id': id_number_to_name(record[0])
        } for record in records]
        env.data.setdefault('relationships', {})[self.name] = {
            'data': rel_data,
            'links': {
                'self': f'/{self.rtable.collection.name}/{env.related.id.name}'
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM data.{env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM data.{self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {env.related.id.number}')
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }


class ManyToOneRelationship(LocalRelationship, ToOneRelationship):
    """A many-to-one relationship between resources."""

    def make_uri_relationship(self, collection, id_):
        return UriManyToOneRelationship(collection, id_, self)

    def make_uri_related_resource(self, name, collection, id_):
        return ManyToOneRelatedResource(name, collection, id_, self)

    def is_reverse(self, other):
        return (isinstance(other, OneToManyRelationship) and
                other.rtable is self.table and other.rfkey == self.lfkey and
                other.rfkey == self.lfkey)

    def sql_constraints(self):
        """Returns the SQL foreign key constraint for this
        ManyToOneRelationship.
        """

        return [
            f'FOREIGN KEY ({self.lfkey}) REFERENCES data.{self.rtable.name}(id)'
        ]

    def collection_remote_ids(self, query, local_ids=None):
        filters = query['filters']
        page = query['page']
        if local_ids is None and filters is None and page == {}:
            where = ''
        else:
            if filters:
                where_clause = f' WHERE {" AND ".join(filters)}'
            else:
                where_clause = ''

            sort = query['sort']
            if sort:
                order_by_clause = f' ORDER BY {", ".join(sort)}'
            else:
                order_by_clause = ''

            if page:
                limit = page['size']
                offset = page['number'] * limit
                limit_offset_clause = f' LIMIT {limit} OFFSET {offset}'
            else:
                limit_offset_clause = ''

            stmt = (f'SELECT id FROM data.{self.table.name}'
                    f'{where_clause}{order_by_clause}{limit_offset_clause}')
            where = f' WHERE id IN ({stmt})'
        return f'SELECT {self.lfkey} FROM data.{self.table.name}{where}'

    def object_remote_ids(self, local_ids=None):
        if local_ids is None:
            partial = '=$1'
        else:
            partial = f' IN ({local_ids})'
        return (f'SELECT {self.lfkey} FROM data.{self.table.name} '
                f'WHERE id{partial}')


class ManyToManyRelationship(ToManyRelationship):
    """A many-to-many relationship between resources."""

    def __init__(self, rtable, atable, lafkey, rafkey):
        # pylint: disable=too-many-arguments
        super().__init__(rtable)
        self.atable = atable
        self.lafkey = lafkey
        self.rafkey = rafkey

    def filter_condition(self, values):
        uuids = ','.join(
            f"'{id_name_to_number(uuid)}'" for uuid in values.split(','))
        return (f'id IN (SELECT {self.lafkey} FROM data.{self.atable.name} '
                f'WHERE {self.rafkey} IN ({uuids}))')

    def make_uri_relationship(self, collection, id_):
        return UriManyToManyRelationship(collection, id_, self)

    def make_uri_related_resource(self, name, collection, id_):
        return ManyToManyRelatedResource(name, collection, id_, self)

    def is_reverse(self, other):
        return (isinstance(other, ManyToManyRelationship) and
                other.table is self.rtable and other.rtable is self.table and
                other.atable is self.atable and other.lafkey == self.rafkey and
                other.rafkey == self.lafkey)

    def collection_remote_ids(self, query, local_ids=None):
        filters = query['filters']
        page = query['page']
        if local_ids is None and filters is None and page == {}:
            where = f'WHERE {self.lafkey} IS NOT NULL'
        else:
            if filters:
                where_clause = f' WHERE {" AND ".join(filters)}'
            else:
                where_clause = ''

            sort = query['sort']
            if sort:
                order_by_clause = f' ORDER BY {", ".join(sort)}'
            else:
                order_by_clause = ''

            if page:
                limit = page['size']
                offset = page['number'] * limit
                limit_offset_clause = f' LIMIT {limit} OFFSET {offset}'
            else:
                limit_offset_clause = ''

            stmt = (f'SELECT id FROM data.{self.table.name}'
                    f'{where_clause}{order_by_clause}{limit_offset_clause}')
            where = f'WHERE {self.lafkey} IN ({stmt})'
        return f'SELECT {self.rafkey} FROM data.{self.atable.name} {where}'

    def object_remote_ids(self, local_ids=None):
        if local_ids is None:
            partial = '=$1'
        else:
            partial = f' IN ({local_ids})'
        return (f'SELECT {self.rafkey} FROM data.{self.atable.name} '
                f'WHERE {self.lafkey}{partial}')

    async def get_collection_data(self, env):
        """Creates the response data member for ManyToManyRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'many_manys': {
                        'data': [
                            {
                                'type': 'many_manys',
                                'id': UUID_51,
                            },
                            ...
                        ],
                        'links': {
                            'self': '/centers/1/relationships/many_manys',
                            'related': '/centers/1/many_manys',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                f'FROM data.{self.atable.name}')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.lafkey],
                                   []).append(record[self.rafkey])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }

    async def get_collection_included(self, env, ids):
        """Gets the remote objects of this many-to-many relationship that need
        to be included in a GET /{collection} response.
        """
        stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                f'FROM data.{self.atable.name} '
                f'WHERE {self.lafkey} IN ({ids})')
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.lafkey],
                                   []).append(record[self.rafkey])
        for lid, data in env.included_by_id.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }

    async def post_collection_task(self, env):
        """Updates the database with the many-to-many relationship specified
        in a POST /{collection} request.
        """
        stmt = (f'INSERT INTO data.{self.atable.name} '
                f'({self.lafkey}, {self.rafkey}) '
                f'VALUES ($1, $2)')
        data_ids = env.relationships[self.name]
        await env.event.wait()
        data = [(env.id_number, data_id.number) for data_id in data_ids]
        try:
            async with env.lock:
                async with env.connection.transaction():
                    log.debug(f'{stmt}: {data}')
                    await env.connection.executemany(stmt, data)
        except ForeignKeyViolationError as exc:
            env.cancel()
            raise NonexistentRelationshipIdError() from exc

    async def get_object_data(self, env):
        """Creates the response data member for ManyToManyRelationships.

        Specifically, after this call the environment's data is updated with
        something like the following:

        env.data = {
            'relationships': {
                'many_manys': {
                    'data': [
                        {
                            'type': 'many_manys',
                            'id': UUID_51,
                        },
                        ...
                    ],
                    'links': {
                        'self': '/centers/1/relationships/many_manys',
                        'related': '/centers/1/many_manys',
                    },
                },
            }
        }
        """
        stmt = (f"SELECT {self.rafkey} "
                f"FROM data.{self.atable.name} "
                f"WHERE {self.lafkey} = $1")
        async with env.lock:
            records = await env.connection.fetch(stmt, env.obj.id.number)
        await env.event.wait()
        rids = [record[self.rafkey] for record in records]
        rafkeys_by_lafkey = {}
        for record in records:
            rafkeys_by_lafkey.setdefault(env.obj.id.number,
                                         []).append(record[self.rafkey])
        env.data.setdefault('relationships', {})[self.name] = {
            'data': [{
                'type': self.rtable.collection.name,
                'id': id_number_to_name(rid),
            } for rid in rids],
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_object_included(self, env, ids):
        """Gets the remote objects of this many-to-many relationship that need
        to be included in a GET response.
        """
        stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                f'FROM data.{self.atable.name} '
                f'WHERE {self.lafkey} IN ({ids})')
        async with env.lock:
            records = await env.connection.fetch(stmt, env.object_id)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.lafkey],
                                   []).append(record[self.rafkey])
        for lid, data in env.included_by_id.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            lid_name = id_number_to_name(lid)
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid_name}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid_name}/'
                                f'{self.name}'),
                },
            }

    async def patch_object_task(self, env):
        """Updates the database with the many-to-many relationship specified
        in a PATCH /{collection}/{id} request.
        """
        stmt_remove = (f'DELETE FROM data.{self.atable.name} '
                       f'WHERE {self.lafkey}=$1')
        stmt_add = (f'INSERT INTO data.{self.atable.name} '
                    f'({self.lafkey}, {self.rafkey}) '
                    f'VALUES ($1, $2)')
        data_ids = env.relationships[self.name]
        data = [(env.obj.id.number, data_id.number) for data_id in data_ids]
        try:
            async with env.lock:
                async with env.connection.transaction():
                    log.debug(f'{stmt_remove}: {env.obj.id.number}')
                    await env.connection.execute(stmt_remove, env.obj.id.number)
                    log.debug(f'{stmt_add}: {data}')
                    await env.connection.executemany(stmt_add, data)
        except ForeignKeyViolationError as exc:
            env.cancel()
            raise NonexistentRelationshipIdError() from exc

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneRelationship
            stmt = (f'SELECT {self.rafkey} '
                    f'FROM data.{self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM data.{env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT {self.rafkey} '
                    f'FROM data.{self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}, {env.related.id.number}')
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        rids = [record[0] for record in records]
        relationship_data = [{
            'type': self.rtable.collection.name,
            'id': id_number_to_name(rid),
        } for rid in rids]
        env.data.setdefault('relationships', {})[self.name] = {
            'data': relationship_data,
            'links': {
                'self': f'/{env.related.collection.name}/{env.related.id.name}'
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                    f'FROM data.{self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM data.{env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                    f'FROM data.{self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT id'
                    f' FROM data.{env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {env.related.id.number}')
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.rtable.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self':
                        f'/{env.related.collection.name}/{env.related.id.name}'
                },
            }
