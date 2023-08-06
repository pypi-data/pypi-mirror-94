# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for airslate entities.

This module provides base entity class used by various entities
classes within airslate package.

Classes:

    BaseEntity

Functions:

    filter_includes

"""

from abc import ABCMeta, abstractmethod

from asdicts.dict import path

from ..exceptions import MissingData, TypeMismatch, RelationNotExist


class BaseEntity(metaclass=ABCMeta):
    """Base entity class."""

    # pylint: disable=too-many-instance-attributes
    # Nine is reasonable in this case.

    def __init__(self, uid):
        self._attributes = {'id': uid}
        self._relationships = {}
        self._included = []
        self._original_included = []
        self._meta = {}

    def __getitem__(self, item):
        """Getter for the attribute value."""
        return self._attributes[item]

    def __setitem__(self, key, value):
        """Setter for the attribute value."""
        self._attributes[key] = value

    def __contains__(self, item):
        """Attribute membership verification."""
        return item in self._attributes

    def __repr__(self):
        """String representation of the current entity."""
        return '<%s (%s): %s>' % (
            self.__class__.__name__,
            self.type,
            self['id']
        )

    def set_attributes(self, attributes):
        """Bulk setter for attributes."""
        for k in attributes:
            self[k] = attributes[k]

    def has_many(self, cls, relation):
        """Create a list of ``cls`` instances."""
        if relation not in self.relationships:
            raise RelationNotExist()

        data = path(self.relationships, f'{relation}.data')
        if data is None:
            return []

        ids = set((r['id'], r['type']) for r in data)
        relations = [e for e in self.included if (e['id'], e['type']) in ids]

        if len(relations) == 0:
            result = map(lambda r: cls(r[0]), ids)
            return list(result)

        return cls.from_collection({'data': relations})

    @property
    def relationships(self):
        """Getter for relationships dictionary."""
        return self._relationships

    @relationships.setter
    def relationships(self, data):
        """Setter for relationships dictionary."""
        self._relationships = data

    @property
    def included(self):
        """Getter for included list."""
        return self._included

    @included.setter
    def included(self, data):
        """Setter for included list."""
        self._included = data

    @property
    def meta(self):
        """Getter for meta dictionary."""
        return self._meta

    @meta.setter
    def meta(self, data):
        """Setter for meta dictionary."""
        self._meta = data

    @property
    def original_included(self):
        """Getter for original included list."""
        return self._original_included

    @original_included.setter
    def original_included(self, data):
        """Setter for original included list."""
        self._original_included = data

    @property
    @abstractmethod
    def type(self):
        """Get type name of the current entity."""

    @classmethod
    def from_collection(cls, response):
        """Create a list of ``cls`` instances from the given ``response``."""
        if 'data' not in response:
            raise MissingData()

        data = response['data']
        if len(data) == 0:
            return []

        entities = []
        for item in data:
            entity = cls(item['id'])

            if path(item, 'type', '') != entity.type:
                raise TypeMismatch()

            entity.set_attributes(item['attributes'])
            relationships = path(item, 'relationships', {})

            original_included = path(response, 'included', [])
            included = filter_included(relationships, original_included)

            entity.relationships = relationships
            entity.included = included
            entity.meta = path(item, 'meta', {})
            entity.original_included = original_included

            entities.append(entity)

        return entities


def filter_included(relationships, included):
    """Filer a list of ``included`` by nested id from ``relationships``."""
    def normalize(data):
        if data is None:
            return []
        return data if isinstance(data, list) else [data]

    def simplify(relation):
        return ((d['type'], d['id'])
                for i in relation for d in normalize(relation[i]['data']))

    r_set = set(simplify(relationships))

    return [e for e in included if (e['type'], e['id']) in r_set]
