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
"""Module attribute provides class Attribute."""

from csv import reader as csv_reader

from ajsonapi.field import Field


class Attribute(Field):
    """Attributes are used to specify data members of object model classes
    (classes derived from JSON_API).
    """

    def __init__(self, type_, *, nullable=False, default=None):
        self.type_ = type_
        self.name = ''  # Overridden in JSON_API.__init_subclass__
        self.nullable = nullable
        self.default = default

    def filter_condition(self, values):
        sql_values = [
            self.type_.sql(value) for value in next(csv_reader([values]))
        ]
        return f"{self.name} IN ({','.join(sql_values)})"

    def sql(self):
        """Creates the SQL column definition for this attribute.

        Returns:
            A string containing the SQL column definition for this attribute.
        """

        if self.nullable:
            if self.default:
                return f'{self.name} {self.type_.name} DEFAULT {self.default}'
            return f'{self.name} {self.type_.name}'
        if self.default:
            return (f'{self.name} {self.type_.name} '
                    f'NOT NULL DEFAULT {self.default}')
        return f'{self.name} {self.type_.name} NOT NULL'

    def __str__(self):
        return self.name
