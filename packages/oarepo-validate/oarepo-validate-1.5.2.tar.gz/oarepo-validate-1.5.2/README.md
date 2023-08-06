# oarepo-validate



[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]
[![image][8]][9]

  [image]: https://img.shields.io/travis/oarepo/oarepo-validate.svg
  [1]: https://travis-ci.com/oarepo/oarepo-validate
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-validate.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-validate
  [4]: https://img.shields.io/github/tag/oarepo/oarepo-validate.svg
  [5]: https://github.com/oarepo/oarepo-validate/releases
  [6]: https://img.shields.io/pypi/dm/oarepo-validate.svg
  [7]: https://pypi.python.org/pypi/oarepo-validate
  [8]: https://img.shields.io/github/license/oarepo/oarepo-validate.svg
  [9]: https://github.com/oarepo/oarepo-validate/blob/master/LICENSE

OArepo Validate library for model-level matedata validation


## Table of Contents
* [Installation](#Installation)
* [Usage](#Usage)
	* [JSON schema validation](#JSON-schema-validation)
		* [Create record](#Create-record)
		* [PUT / PATCH record](#PUT-/-PATCH-record)
	* [Marshmallow validation](#Marshmallow-validation)
		* [Usage](#Usage)
		* [What about marshmallow in loader?](#What-about-marshmallow-in-loader?)
			* [record-files](#record-files)
		* [Context](#Context)
		* [Output of marshmallow validation](#Output-of-marshmallow-validation)
			* [Valid data](#Valid-data)
			* [Invalid data](#Invalid-data)
			* [Merging process](#Merging-process)
		* [Signals](#Signals)
		* [Serializers](#Serializers)

## Installation

```bash
    pip install oarepo-validate
```

## Usage

The library provides mixins for enforcing json schema and marshmallow validation.

### JSON schema validation

If ``$schema`` is present on metadata, invenio performs a json schema validation inside
the ``validate()`` method. The problem is that ``$schema`` can be set/removed via the REST
API. This means that an ill-written client can completely bypass the validation.

To mitigate this issue, create your own Record implementation:

```python
from oarepo_validate import SchemaKeepingRecordMixin
from invenio_records import Record

class MyRecord(SchemaKeepingRecordMixin, Record):
    ALLOWED_SCHEMAS = ('records/record-v1.0.0.json', 'records/record-v2.0.0.json')
    PREFERRED_SCHEMA = 'records/record-v2.0.0.json'
```

And register the record in REST endpoints in configuration:

```python
RECORD_PID = 'pid(recid,record_class="my:MyRecord")'

RECORDS_REST_ENDPOINTS = {
    'records': dict(
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        record_class='my:MyRecord',
        item_route='/records/<{0}:pid_value>'.format(RECORD_PID),
        # ...
    )
}
```

#### Create record

When creating a new record, if ``$schema`` is not set, ``MyRecord.PREFERRED_SCHEMA`` is added
automatically. If ``$schema`` is set, it is validated against ``MyRecord.ALLOWED_SCHEMAS``
and an exception is raised if the schema is not present in ``ALLOWED_SCHEMAS``.

#### PUT / PATCH record

Before the result of the operation is committed, ``$schema`` is checked again.

### Marshmallow validation

In invenio, REST create operation use the following sequence:

```
<flask>
<invenio_records_rest.views.RecordsListResource:post>
   <loader>
      <marshmallow>
   <permission factory>
   <pid minter>
   <record_class.create>
      <record.commit>
         <record.validate>
```

REST PUT operation then uses:

```
<flask>
<invenio_records_rest.views.RecordResource:put>
   <permission factory>
   <loader>
      <marshmallow>
   <record.update>
   <record.commit>
      <record.validate>
```

REST PATCH operation:

```
<flask>
<invenio_records_rest.views.RecordResource:put>
   <permission factory>
   <simple json loader>
   <record.patch>
   <record.commit>
      <record.validate>
```

As you can see, if you place any validation code in loader's marshmallow, it is not executed.
An alternative is to have the validation code in ``validate`` and handle all validations there.
This library does exactly this - it provides a record mixin that calls marshmallow schema's ``load``
method inside its ``validate`` method.

#### Usage

Create your own record and inherit from the mixin:

```python
from oarepo_validate import MarshmallowValidatedRecordMixin
from invenio_records import Record
from marshmallow import Schema, fields

class TestSchema(Schema):
    name = fields.Str(required=True)

class MyRecord(MarshmallowValidatedRecordMixin, Record):
    MARSHMALLOW_SCHEMA = TestSchema
```

Do not forget to register it as in the previous example.

Now marshmallow schema will be processed before each ``commit`` method.

#### What about marshmallow in loader?

In most cases, marshmallow schema in loader can be removed and a simple json loader used instead.
However, if you need a custom processing of input data that is independent of validation,
you can keep the two marshmallows. To remove marshmallow loader and use a simple one,
set ``oarepo_validate.json_loader`` as the record loader.

```python
RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        record_loaders={
            'application/json': 'oarepo_validate:json_loader',
        },
        # ...
    )
}
```

A special case is when the marshmallow in loader already includes validation marshmallow rules.
Then you would want to use loader's marshmallow for create / replace and marshmallow in validation
only for patch operation (so that the same marshmallow rules are not called twice). To accomplish
this, set:

```python
class MyRecord(MarshmallowValidatedRecordMixin, Record):
    MARSHMALLOW_SCHEMA = TestSchema

    VALIDATE_MARSHMALLOW = False
    VALIDATE_PATCH = True
```

``VALIDATE_MARSHMALLOW`` will switch off marshmallow validation in ``validate`` method and
``VALIDATE_PATCH`` will switch on marshmallow validation in ``patch`` method.

##### record-files

Be careful with removing the loader when you use ``invenio-record-files``. Just using plain
json loader makes it possible to set ``_bucket`` and ``_files`` directly which should be
disabled for security reasons (anyone might gain access to any file if he knows bucket and
object version of the file and has write access to any record).

To fix this, set:

```python
from oarepo_validate import FilesKeepingRecordMixin

RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        record_loaders={
            'application/json': 'oarepo_validate:json_loader',
        },
        # ...
    )
}

class MyRecord(FilesKeepingRecordMixin, ...):
    ...
```

The loader will strip ``_bucket`` and ``_files`` from the payload and the mixin
will make sure that the files can not be removed with ``put`` or replaced with ``patch``
operation.

#### Context

Marshmallow validation is called with a context, that is filled with:

  * ``record``
  * ``pid`` if it is known
  * Any ``**kwargs`` passed to ``Record.create`` or ``Record.commit``

#### Output of marshmallow validation

##### Valid data

The marshmallow loader produces validated data. Be default, the validated data are merged into
the record. The rationale for this is that the validation might be used to replace content
(include referenced content, etc). To have a consistent processing, the schema must be idempotent,
that is ``schema(schema(input)) == schema(input)``.

To prevent this behaviour, set ``MERGE_WITH_VALIDATED`` to ``False`` on your record class.

##### Invalid data

Even in the case the data are invalid, marshmallow validation might still return a partially
valid output (in ``ValidationError.valid_data``). This library merges the valid data into
the record's metadata. This behaviour can be switched off by setting
``MERGE_WITH_VALIDATED_ERROR = False``
on your record class.


##### Merging process

The merging process is recursive and is designed to preserve values in the record's metadata
if they are not present in the validated metadata. This means:

  * lists are merged item-wise. If the list in the record is longer than in validated data,
    extra items are kept.
  * dictionaries are merged based on the same key. If a key is both in the record and in validated
    data, the respective values are merged recursively and the result used. Extra keys from
    validated data are copied into the record's metadata and keys present in record's metadata
    and ommited from validated data are kept.

Sometimes it might be necessary to prevent this merging. The library provides:

  * ``Keep(value)`` - if an instance of ``Keep`` class is returned, no merging is performed
    and the value is used as is - that is, it will overwrite anything in the record
  * ``DELETED`` - if this constant is returned, the item will be deleted - if it is a part of
    an array, the corresponding array item in record's metadata is deleted. If it is a value
    of a key in the dictionary, the corresponding key in record's metadata is deleted.

#### Signals

The library provides the following signals:

```python
before_marshmallow_validate = signal('oarepo_before_marshmallow_validate')
"""
Signal invoked before record metadata are validated (loaded by marshmallow schema)
inside Record.validate

:param source:  the record being validated
:param record:  the record being validated
:param context: marshmallow context
:param **kwargs: kwargs passed to Record.create or Record.commit (or Record.validate)
"""

after_marshmallow_validate = signal('oarepo_after_marshmallow_validate')
"""
Signal invoked after record metadata are validated (loaded by marshmallow schema)
inside Record.validate

:param source:  the record being validated
:param record:  the record that was successfully validated
:param context: marshmallow context
:param result:  result of load that will be used to update record's metadata.
                Signal handler can modify it. In case of validation exception the result is None.
:param error:   Exception raised when validating. None if validation has been successful
:param **kwargs: kwargs passed to Record.create or Record.commit (or Record.validate)
"""
```

#### Serializers

If ``marhsmallow.dump`` is not required for metadata serialization,
``oarepo_validate.json_search, oarepo_validate.json_response``
are faster replacements for marshmallow-based serializers:

```python
RECORDS_REST_ENDPOINTS = {
    'recid': dict(
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        }
    )
}
```
