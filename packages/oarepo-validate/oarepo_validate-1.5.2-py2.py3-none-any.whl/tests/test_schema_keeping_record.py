#
# Copyright (c) 2019 UCT Prague.
#
# test_schema_keeping_record.py is part of Invenio Explicit ACLs
# (see https://github.com/oarepo/invenio-explicit-acls).
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
import pytest

from oarepo_validate.record import SchemaEnforcingRecord
from .helpers import create_record


def test_constructor(app, db):
    rec = SchemaEnforcingRecord({})
    assert rec['$schema'] == SchemaEnforcingRecord.PREFERRED_SCHEMA


def test_schema_create(app, db):
    pid, rec = create_record({}, clz=SchemaEnforcingRecord)
    assert rec['$schema'] == SchemaEnforcingRecord.PREFERRED_SCHEMA

    with pytest.raises(AttributeError):
        create_record({'$schema': 'http://blah'}, clz=SchemaEnforcingRecord)


def test_clear(app, db):
    pid, rec = create_record({}, clz=SchemaEnforcingRecord)
    rec.clear()
    assert rec['$schema'] == SchemaEnforcingRecord.PREFERRED_SCHEMA


def test_update(app, db):
    pid, rec = create_record({}, clz=SchemaEnforcingRecord)
    with pytest.raises(AttributeError):
        rec.update({'$schema': 'http://blah'})

    rec.update({'title': 'blah'})
    assert rec['title'] == 'blah'


def test_set(app, db):
    pid, rec = create_record({}, clz=SchemaEnforcingRecord)
    with pytest.raises(AttributeError):
        rec['$schema'] = 'http://blah'

    # should pass as this is an allowed schema
    rec['$schema'] = 'records/record-v1.0.0.json'

    # should pass as absolute path is an allowed schema as well
    rec['$schema'] = 'https://localhost/schemas/records/record-v1.0.0.json'


def test_delete(app, db):
    pid, rec = create_record({'test': 'blah'}, clz=SchemaEnforcingRecord)
    with pytest.raises(AttributeError):
        del rec['$schema']

    del rec['test']
    assert dict(rec) == {
        'control_number': '1',
        '$schema': SchemaEnforcingRecord.PREFERRED_SCHEMA
    }


def test_patch(app, db):
    pid, rec = create_record({}, clz=SchemaEnforcingRecord)
    with pytest.raises(AttributeError):
        rec.patch([
            {
                'op': 'replace',
                'path': '/$schema',
                'value': 'invalid'
            }
        ])

    rec.patch([
        {
            'op': 'replace',
            'path': '/$schema',
            'value': 'records/record-v1.0.0.json'
        }
    ])


RECORD_SCHEMA = 'records/record-v1.0.0.json'
