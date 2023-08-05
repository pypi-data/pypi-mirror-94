# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/performance.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import account_pb2 as gm_dot_pb_dot_account__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from gm.pb import gogo_pb2 as gm_dot_pb_dot_gogo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/performance.proto',
  package='performance.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x17gm/pb/performance.proto\x12\x0fperformance.api\x1a\x13gm/pb/account.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x10gm/pb/gogo.proto\"\xf0\x02\n\tIndicator\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x11\n\tpnl_ratio\x18\x02 \x01(\x01\x12\x18\n\x10pnl_ratio_annual\x18\x03 \x01(\x01\x12\x13\n\x0bsharp_ratio\x18\x04 \x01(\x01\x12\x14\n\x0cmax_drawdown\x18\x05 \x01(\x01\x12\x12\n\nrisk_ratio\x18\x06 \x01(\x01\x12\x12\n\nopen_count\x18\x07 \x01(\x05\x12\x13\n\x0b\x63lose_count\x18\x08 \x01(\x05\x12\x11\n\twin_count\x18\t \x01(\x05\x12\x12\n\nlose_count\x18\n \x01(\x05\x12\x11\n\twin_ratio\x18\x0b \x01(\x01\x12\x14\n\x0c\x63\x61lmar_ratio\x18\x0c \x01(\x01\x12\x34\n\ncreated_at\x18\r \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\x12\x34\n\nupdated_at\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\"6\n\nIndicators\x12(\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1a.performance.api.Indicator\"\xa3\x03\n\x11IndicatorDuration\x12\x12\n\naccount_id\x18\x01 \x01(\t\x12\x11\n\tpnl_ratio\x18\x02 \x01(\x01\x12\x0b\n\x03pnl\x18\x03 \x01(\x01\x12\x0c\n\x04\x66pnl\x18\x04 \x01(\x01\x12\x0e\n\x06\x66rozen\x18\x05 \x01(\x01\x12\x0c\n\x04\x63\x61sh\x18\x06 \x01(\x01\x12\x0b\n\x03nav\x18\x07 \x01(\x01\x12\x36\n\tpositions\x18\x08 \x03(\x0b\x32\x12.core.api.PositionB\x0f\xf2\xde\x1f\x0bxorm:\"json\"\x12\x0f\n\x07\x63um_pnl\x18\t \x01(\x01\x12\x0f\n\x07\x63um_buy\x18\n \x01(\x01\x12\x10\n\x08\x63um_sell\x18\x0b \x01(\x01\x12\x16\n\x0e\x63um_commission\x18\x0c \x01(\x01\x12\x31\n\x08\x64uration\x18\r \x01(\x0b\x32\x19.google.protobuf.DurationB\x04\x98\xdf\x1f\x01\x12\x34\n\ncreated_at\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\x12\x34\n\nupdated_at\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\"F\n\x12IndicatorDurations\x12\x30\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\".performance.api.IndicatorDurationb\x06proto3'
  ,
  dependencies=[gm_dot_pb_dot_account__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,gm_dot_pb_dot_gogo__pb2.DESCRIPTOR,])




_INDICATOR = _descriptor.Descriptor(
  name='Indicator',
  full_name='performance.api.Indicator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='performance.api.Indicator.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pnl_ratio', full_name='performance.api.Indicator.pnl_ratio', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pnl_ratio_annual', full_name='performance.api.Indicator.pnl_ratio_annual', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sharp_ratio', full_name='performance.api.Indicator.sharp_ratio', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_drawdown', full_name='performance.api.Indicator.max_drawdown', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='risk_ratio', full_name='performance.api.Indicator.risk_ratio', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='open_count', full_name='performance.api.Indicator.open_count', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='close_count', full_name='performance.api.Indicator.close_count', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='win_count', full_name='performance.api.Indicator.win_count', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lose_count', full_name='performance.api.Indicator.lose_count', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='win_ratio', full_name='performance.api.Indicator.win_ratio', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='calmar_ratio', full_name='performance.api.Indicator.calmar_ratio', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='performance.api.Indicator.created_at', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\220\337\037\001', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='performance.api.Indicator.updated_at', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\220\337\037\001', file=DESCRIPTOR),
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
  serialized_start=149,
  serialized_end=517,
)


_INDICATORS = _descriptor.Descriptor(
  name='Indicators',
  full_name='performance.api.Indicators',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='performance.api.Indicators.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=519,
  serialized_end=573,
)


_INDICATORDURATION = _descriptor.Descriptor(
  name='IndicatorDuration',
  full_name='performance.api.IndicatorDuration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='performance.api.IndicatorDuration.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pnl_ratio', full_name='performance.api.IndicatorDuration.pnl_ratio', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pnl', full_name='performance.api.IndicatorDuration.pnl', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fpnl', full_name='performance.api.IndicatorDuration.fpnl', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frozen', full_name='performance.api.IndicatorDuration.frozen', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cash', full_name='performance.api.IndicatorDuration.cash', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nav', full_name='performance.api.IndicatorDuration.nav', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='positions', full_name='performance.api.IndicatorDuration.positions', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\362\336\037\013xorm:\"json\"', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cum_pnl', full_name='performance.api.IndicatorDuration.cum_pnl', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cum_buy', full_name='performance.api.IndicatorDuration.cum_buy', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cum_sell', full_name='performance.api.IndicatorDuration.cum_sell', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cum_commission', full_name='performance.api.IndicatorDuration.cum_commission', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration', full_name='performance.api.IndicatorDuration.duration', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\230\337\037\001', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='performance.api.IndicatorDuration.created_at', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\220\337\037\001', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='performance.api.IndicatorDuration.updated_at', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\220\337\037\001', file=DESCRIPTOR),
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
  serialized_start=576,
  serialized_end=995,
)


_INDICATORDURATIONS = _descriptor.Descriptor(
  name='IndicatorDurations',
  full_name='performance.api.IndicatorDurations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='performance.api.IndicatorDurations.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=997,
  serialized_end=1067,
)

_INDICATOR.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_INDICATOR.fields_by_name['updated_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_INDICATORS.fields_by_name['data'].message_type = _INDICATOR
_INDICATORDURATION.fields_by_name['positions'].message_type = gm_dot_pb_dot_account__pb2._POSITION
_INDICATORDURATION.fields_by_name['duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_INDICATORDURATION.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_INDICATORDURATION.fields_by_name['updated_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_INDICATORDURATIONS.fields_by_name['data'].message_type = _INDICATORDURATION
DESCRIPTOR.message_types_by_name['Indicator'] = _INDICATOR
DESCRIPTOR.message_types_by_name['Indicators'] = _INDICATORS
DESCRIPTOR.message_types_by_name['IndicatorDuration'] = _INDICATORDURATION
DESCRIPTOR.message_types_by_name['IndicatorDurations'] = _INDICATORDURATIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Indicator = _reflection.GeneratedProtocolMessageType('Indicator', (_message.Message,), {
  'DESCRIPTOR' : _INDICATOR,
  '__module__' : 'gm.pb.performance_pb2'
  # @@protoc_insertion_point(class_scope:performance.api.Indicator)
  })
_sym_db.RegisterMessage(Indicator)

Indicators = _reflection.GeneratedProtocolMessageType('Indicators', (_message.Message,), {
  'DESCRIPTOR' : _INDICATORS,
  '__module__' : 'gm.pb.performance_pb2'
  # @@protoc_insertion_point(class_scope:performance.api.Indicators)
  })
_sym_db.RegisterMessage(Indicators)

IndicatorDuration = _reflection.GeneratedProtocolMessageType('IndicatorDuration', (_message.Message,), {
  'DESCRIPTOR' : _INDICATORDURATION,
  '__module__' : 'gm.pb.performance_pb2'
  # @@protoc_insertion_point(class_scope:performance.api.IndicatorDuration)
  })
_sym_db.RegisterMessage(IndicatorDuration)

IndicatorDurations = _reflection.GeneratedProtocolMessageType('IndicatorDurations', (_message.Message,), {
  'DESCRIPTOR' : _INDICATORDURATIONS,
  '__module__' : 'gm.pb.performance_pb2'
  # @@protoc_insertion_point(class_scope:performance.api.IndicatorDurations)
  })
_sym_db.RegisterMessage(IndicatorDurations)


_INDICATOR.fields_by_name['created_at']._options = None
_INDICATOR.fields_by_name['updated_at']._options = None
_INDICATORDURATION.fields_by_name['positions']._options = None
_INDICATORDURATION.fields_by_name['duration']._options = None
_INDICATORDURATION.fields_by_name['created_at']._options = None
_INDICATORDURATION.fields_by_name['updated_at']._options = None
# @@protoc_insertion_point(module_scope)
