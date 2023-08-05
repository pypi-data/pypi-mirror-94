# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/statistics/v1/resource.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/statistics/v1/resource.proto',
  package='spaceone.api.statistics.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)spaceone/api/statistics/v1/resource.proto\x12\x1aspaceone.api.statistics.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\xa1\x02\n\tJoinQuery\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12<\n\x04type\x18\x02 \x01(\x0e\x32..spaceone.api.statistics.v1.JoinQuery.JoinType\x12\x16\n\x0e\x64\x61ta_source_id\x18\x03 \x01(\t\x12\x15\n\rresource_type\x18\x04 \x01(\t\x12\x34\n\x05query\x18\x05 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\"5\n\x08JoinType\x12\x08\n\x04LEFT\x10\x00\x12\t\n\x05RIGHT\x10\x01\x12\t\n\x05OUTER\x10\x02\x12\t\n\x05INNER\x10\x03\"\xa0\x01\n\x0b\x43oncatQuery\x12\x16\n\x0e\x64\x61ta_source_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x34\n\x05query\x18\x03 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\",\n\x07\x46ormula\x12\x0f\n\x07\x66ormula\x18\x01 \x01(\t\x12\x10\n\x08operator\x18\x02 \x01(\t\"\x8a\x03\n\x13ResourceStatRequest\x12\x16\n\x0e\x64\x61ta_source_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x34\n\x05query\x18\x03 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x33\n\x04join\x18\x04 \x03(\x0b\x32%.spaceone.api.statistics.v1.JoinQuery\x12\x35\n\x08\x66ormulas\x18\x05 \x03(\x0b\x32#.spaceone.api.statistics.v1.Formula\x12\x11\n\tdomain_id\x18\x06 \x01(\t\x12\x37\n\x06\x63oncat\x18\x07 \x03(\x0b\x32\'.spaceone.api.statistics.v1.ConcatQuery\x12,\n\x0b\x65xtend_data\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x07\x66ill_na\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct2\x83\x01\n\x08Resource\x12w\n\x04stat\x12/.spaceone.api.statistics.v1.ResourceStatRequest\x1a\x17.google.protobuf.Struct\"%\x82\xd3\xe4\x93\x02\x1f\"\x1d/statistics/v1/resources/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])



_JOINQUERY_JOINTYPE = _descriptor.EnumDescriptor(
  name='JoinType',
  full_name='spaceone.api.statistics.v1.JoinQuery.JoinType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OUTER', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INNER', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=404,
  serialized_end=457,
)
_sym_db.RegisterEnumDescriptor(_JOINQUERY_JOINTYPE)


_JOINQUERY = _descriptor.Descriptor(
  name='JoinQuery',
  full_name='spaceone.api.statistics.v1.JoinQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='keys', full_name='spaceone.api.statistics.v1.JoinQuery.keys', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='spaceone.api.statistics.v1.JoinQuery.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_source_id', full_name='spaceone.api.statistics.v1.JoinQuery.data_source_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.JoinQuery.resource_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.JoinQuery.query', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.JoinQuery.extend_data', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOINQUERY_JOINTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=457,
)


_CONCATQUERY = _descriptor.Descriptor(
  name='ConcatQuery',
  full_name='spaceone.api.statistics.v1.ConcatQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_source_id', full_name='spaceone.api.statistics.v1.ConcatQuery.data_source_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.ConcatQuery.resource_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.ConcatQuery.query', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.ConcatQuery.extend_data', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=460,
  serialized_end=620,
)


_FORMULA = _descriptor.Descriptor(
  name='Formula',
  full_name='spaceone.api.statistics.v1.Formula',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='formula', full_name='spaceone.api.statistics.v1.Formula.formula', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='operator', full_name='spaceone.api.statistics.v1.Formula.operator', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=622,
  serialized_end=666,
)


_RESOURCESTATREQUEST = _descriptor.Descriptor(
  name='ResourceStatRequest',
  full_name='spaceone.api.statistics.v1.ResourceStatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_source_id', full_name='spaceone.api.statistics.v1.ResourceStatRequest.data_source_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.ResourceStatRequest.resource_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.ResourceStatRequest.query', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='join', full_name='spaceone.api.statistics.v1.ResourceStatRequest.join', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='formulas', full_name='spaceone.api.statistics.v1.ResourceStatRequest.formulas', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.statistics.v1.ResourceStatRequest.domain_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='concat', full_name='spaceone.api.statistics.v1.ResourceStatRequest.concat', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.ResourceStatRequest.extend_data', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fill_na', full_name='spaceone.api.statistics.v1.ResourceStatRequest.fill_na', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=669,
  serialized_end=1063,
)

_JOINQUERY.fields_by_name['type'].enum_type = _JOINQUERY_JOINTYPE
_JOINQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_JOINQUERY.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_JOINQUERY_JOINTYPE.containing_type = _JOINQUERY
_CONCATQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_CONCATQUERY.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_RESOURCESTATREQUEST.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_RESOURCESTATREQUEST.fields_by_name['join'].message_type = _JOINQUERY
_RESOURCESTATREQUEST.fields_by_name['formulas'].message_type = _FORMULA
_RESOURCESTATREQUEST.fields_by_name['concat'].message_type = _CONCATQUERY
_RESOURCESTATREQUEST.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_RESOURCESTATREQUEST.fields_by_name['fill_na'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
DESCRIPTOR.message_types_by_name['JoinQuery'] = _JOINQUERY
DESCRIPTOR.message_types_by_name['ConcatQuery'] = _CONCATQUERY
DESCRIPTOR.message_types_by_name['Formula'] = _FORMULA
DESCRIPTOR.message_types_by_name['ResourceStatRequest'] = _RESOURCESTATREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JoinQuery = _reflection.GeneratedProtocolMessageType('JoinQuery', (_message.Message,), {
  'DESCRIPTOR' : _JOINQUERY,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.JoinQuery)
  })
_sym_db.RegisterMessage(JoinQuery)

ConcatQuery = _reflection.GeneratedProtocolMessageType('ConcatQuery', (_message.Message,), {
  'DESCRIPTOR' : _CONCATQUERY,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.ConcatQuery)
  })
_sym_db.RegisterMessage(ConcatQuery)

Formula = _reflection.GeneratedProtocolMessageType('Formula', (_message.Message,), {
  'DESCRIPTOR' : _FORMULA,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.Formula)
  })
_sym_db.RegisterMessage(Formula)

ResourceStatRequest = _reflection.GeneratedProtocolMessageType('ResourceStatRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCESTATREQUEST,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.ResourceStatRequest)
  })
_sym_db.RegisterMessage(ResourceStatRequest)



_RESOURCE = _descriptor.ServiceDescriptor(
  name='Resource',
  full_name='spaceone.api.statistics.v1.Resource',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1066,
  serialized_end=1197,
  methods=[
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.statistics.v1.Resource.stat',
    index=0,
    containing_service=None,
    input_type=_RESOURCESTATREQUEST,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\037\"\035/statistics/v1/resources/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RESOURCE)

DESCRIPTOR.services_by_name['Resource'] = _RESOURCE

# @@protoc_insertion_point(module_scope)
