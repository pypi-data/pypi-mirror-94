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
"""Module query deals with everything related to query parameters."""

from re import compile as re_compile

from ajsonapi.errors import (
    FieldsInvalidFieldError,
    FieldsInvalidResourceError,
    QueryParameterUnsupportedError,
)
from ajsonapi.field import Field

RE_FIELDS = re_compile(r'fields\[([^\]]*)\]')
RE_PAGE = re_compile(r'page\[([^\]]*)\]')


def query_has_parameter(query, name):
    """Checks if a query parameter exists."""
    for parameter in query:
        if parameter.split('[')[0] == name:
            return True
    return False


def parse_fields(request_query, query, errors, *, allow=False):
    """Parses the request's fields query parameter."""

    if query_has_parameter(request_query, 'fields'):
        if allow:
            query['fields'] = fields_dict(request_query, errors)
        else:
            errors.append(QueryParameterUnsupportedError('fields'))
    else:
        query['fields'] = {}


def fields_dict(request_query, errors):
    """Helper function for parsing request query fields parameters."""

    # pylint: disable=import-outside-toplevel,cyclic-import
    from ajsonapi.uri.collection import Collection

    return_dict = {}
    for key, values in request_query.items():
        match = RE_FIELDS.match(key)
        if match:
            collection_name = match.group(1)
            try:
                collection = Collection.by_name[collection_name]
            except KeyError:
                errors.append(FieldsInvalidResourceError(collection_name))
                continue
            return_dict[collection] = []
            if values == '':
                continue
            for field_name in values.split(','):
                try:
                    field = getattr(collection.table.___, field_name)
                except AttributeError:
                    errors.append(
                        FieldsInvalidFieldError(collection_name, field_name))
                    continue
                if not isinstance(field, Field):
                    errors.append(
                        FieldsInvalidFieldError(collection_name, field_name))
                else:
                    return_dict[collection].append(field)
    return return_dict


def parse_page(request_query, query, errors, *, allow=False):
    """Parses the request's page query parameter."""
    if query_has_parameter(request_query, 'page'):
        if allow:
            query['page'] = page_dict(request_query, errors)
        else:
            errors.append(QueryParameterUnsupportedError('page'))
    else:
        query['page'] = {}


def page_dict(request_query, errors):
    """Helper function for parsing request query page parameters."""
    # pylint: disable=unused-argument

    return_dict = {}
    for key, value in request_query.items():
        match = RE_PAGE.match(key)
        if match:
            page_key = match.group(1)
            if page_key == 'number':
                return_dict['number'] = int(value)
            elif page_key == 'size':
                return_dict['size'] = int(value)
    return return_dict


def subquery(query, relationship):
    """Updates query when recursing down relationships."""

    return_query = {}
    for key, value in query.items():
        if key == 'fields':
            return_query['fields'] = value
        elif key in ('includes', 'filters'):
            if value and relationship in value:
                return_query[key] = value[relationship]
            else:
                return_query[key] = {}
        elif key in ('sort', 'page'):
            return_query[key] = value
    return return_query
