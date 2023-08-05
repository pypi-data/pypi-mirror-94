# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='milvus.proto.common',
  syntax='proto3',
  serialized_options=_b('Z@github.com/zilliztech/milvus-distributed/internal/proto/commonpb'),
  serialized_pb=_b('\n\x0c\x63ommon.proto\x12\x13milvus.proto.common\"\x07\n\x05\x45mpty\"L\n\x06Status\x12\x32\n\nerror_code\x18\x01 \x01(\x0e\x32\x1e.milvus.proto.common.ErrorCode\x12\x0e\n\x06reason\x18\x02 \x01(\t\"*\n\x0cKeyValuePair\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x15\n\x04\x42lob\x12\r\n\x05value\x18\x01 \x01(\x0c\"#\n\x07\x41\x64\x64ress\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x03\"m\n\x07MsgBase\x12.\n\x08msg_type\x18\x01 \x01(\x0e\x32\x1c.milvus.proto.common.MsgType\x12\r\n\x05msgID\x18\x02 \x01(\x03\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\x12\x10\n\x08sourceID\x18\x04 \x01(\x03\"7\n\tMsgHeader\x12*\n\x04\x62\x61se\x18\x01 \x01(\x0b\x32\x1c.milvus.proto.common.MsgBase*\xb8\x04\n\tErrorCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x14\n\x10UNEXPECTED_ERROR\x10\x01\x12\x12\n\x0e\x43ONNECT_FAILED\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x19\n\x15\x43OLLECTION_NOT_EXISTS\x10\x04\x12\x14\n\x10ILLEGAL_ARGUMENT\x10\x05\x12\x15\n\x11ILLEGAL_DIMENSION\x10\x07\x12\x16\n\x12ILLEGAL_INDEX_TYPE\x10\x08\x12\x1b\n\x17ILLEGAL_COLLECTION_NAME\x10\t\x12\x10\n\x0cILLEGAL_TOPK\x10\n\x12\x15\n\x11ILLEGAL_ROWRECORD\x10\x0b\x12\x15\n\x11ILLEGAL_VECTOR_ID\x10\x0c\x12\x19\n\x15ILLEGAL_SEARCH_RESULT\x10\r\x12\x12\n\x0e\x46ILE_NOT_FOUND\x10\x0e\x12\x0f\n\x0bMETA_FAILED\x10\x0f\x12\x10\n\x0c\x43\x41\x43HE_FAILED\x10\x10\x12\x18\n\x14\x43\x41NNOT_CREATE_FOLDER\x10\x11\x12\x16\n\x12\x43\x41NNOT_CREATE_FILE\x10\x12\x12\x18\n\x14\x43\x41NNOT_DELETE_FOLDER\x10\x13\x12\x16\n\x12\x43\x41NNOT_DELETE_FILE\x10\x14\x12\x15\n\x11\x42UILD_INDEX_ERROR\x10\x15\x12\x11\n\rILLEGAL_NLIST\x10\x16\x12\x17\n\x13ILLEGAL_METRIC_TYPE\x10\x17\x12\x11\n\rOUT_OF_MEMORY\x10\x18\x12\x14\n\x0f\x44\x44_REQUEST_RACE\x10\xe8\x07*N\n\nIndexState\x12\x08\n\x04NONE\x10\x00\x12\x0c\n\x08UNISSUED\x10\x01\x12\x0e\n\nINPROGRESS\x10\x02\x12\x0c\n\x08\x46INISHED\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04*o\n\x0cSegmentState\x12\x0f\n\x0bSegmentNone\x10\x00\x12\x13\n\x0fSegmentNotExist\x10\x01\x12\x12\n\x0eSegmentGrowing\x10\x02\x12\x11\n\rSegmentSealed\x10\x03\x12\x12\n\x0eSegmentFlushed\x10\x04*\xaa\x05\n\x07MsgType\x12\t\n\x05kNone\x10\x00\x12\x15\n\x11kCreateCollection\x10\x64\x12\x13\n\x0fkDropCollection\x10\x65\x12\x12\n\x0ekHasCollection\x10\x66\x12\x17\n\x13kDescribeCollection\x10g\x12\x14\n\x10kShowCollections\x10h\x12\x12\n\x0ekGetSysConfigs\x10i\x12\x15\n\x10kCreatePartition\x10\xc8\x01\x12\x13\n\x0ekDropPartition\x10\xc9\x01\x12\x12\n\rkHasPartition\x10\xca\x01\x12\x17\n\x12kDescribePartition\x10\xcb\x01\x12\x14\n\x0fkShowPartitions\x10\xcc\x01\x12\x11\n\x0ckShowSegment\x10\xfa\x01\x12\x15\n\x10kDescribeSegment\x10\xfb\x01\x12\x11\n\x0ckCreateIndex\x10\xac\x02\x12\x13\n\x0ekDescribeIndex\x10\xad\x02\x12\x0c\n\x07kInsert\x10\x90\x03\x12\x0c\n\x07kDelete\x10\x91\x03\x12\x0b\n\x06kFlush\x10\x92\x03\x12\x0c\n\x07kSearch\x10\xf4\x03\x12\x12\n\rkSearchResult\x10\xf5\x03\x12\x13\n\x0ekGetIndexState\x10\xf6\x03\x12\x1d\n\x18kGetCollectionStatistics\x10\xf7\x03\x12\x1c\n\x17kGetPartitionStatistics\x10\xf8\x03\x12\x11\n\x0ckSegmentInfo\x10\xd8\x04\x12\x0e\n\tkTimeTick\x10\xb0\t\x12\x14\n\x0fkQueryNodeStats\x10\xb1\t\x12\x0f\n\nkLoadIndex\x10\xb2\t\x12\x0f\n\nkRequestID\x10\xb3\t\x12\x10\n\x0bkRequestTSO\x10\xb4\t\x12\x15\n\x10kAllocateSegment\x10\xb5\t\x12\x17\n\x12kSegmentStatistics\x10\xb6\t\x12\x16\n\x11kSegmentFlushDone\x10\xb7\tBBZ@github.com/zilliztech/milvus-distributed/internal/proto/commonpbb\x06proto3')
)

_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='milvus.proto.common.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNEXPECTED_ERROR', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONNECT_FAILED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COLLECTION_NOT_EXISTS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_ARGUMENT', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_DIMENSION', index=6, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_INDEX_TYPE', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_COLLECTION_NAME', index=8, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_TOPK', index=9, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_ROWRECORD', index=10, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_VECTOR_ID', index=11, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_SEARCH_RESULT', index=12, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILE_NOT_FOUND', index=13, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='META_FAILED', index=14, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CACHE_FAILED', index=15, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CREATE_FOLDER', index=16, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CREATE_FILE', index=17, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_DELETE_FOLDER', index=18, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_DELETE_FILE', index=19, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUILD_INDEX_ERROR', index=20, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_NLIST', index=21, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ILLEGAL_METRIC_TYPE', index=22, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OUT_OF_MEMORY', index=23, number=24,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DD_REQUEST_RACE', index=24, number=1000,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=397,
  serialized_end=965,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
_INDEXSTATE = _descriptor.EnumDescriptor(
  name='IndexState',
  full_name='milvus.proto.common.IndexState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNISSUED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPROGRESS', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINISHED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=967,
  serialized_end=1045,
)
_sym_db.RegisterEnumDescriptor(_INDEXSTATE)

IndexState = enum_type_wrapper.EnumTypeWrapper(_INDEXSTATE)
_SEGMENTSTATE = _descriptor.EnumDescriptor(
  name='SegmentState',
  full_name='milvus.proto.common.SegmentState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SegmentNone', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SegmentNotExist', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SegmentGrowing', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SegmentSealed', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SegmentFlushed', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1047,
  serialized_end=1158,
)
_sym_db.RegisterEnumDescriptor(_SEGMENTSTATE)

SegmentState = enum_type_wrapper.EnumTypeWrapper(_SEGMENTSTATE)
_MSGTYPE = _descriptor.EnumDescriptor(
  name='MsgType',
  full_name='milvus.proto.common.MsgType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='kNone', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kCreateCollection', index=1, number=100,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDropCollection', index=2, number=101,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kHasCollection', index=3, number=102,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDescribeCollection', index=4, number=103,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kShowCollections', index=5, number=104,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kGetSysConfigs', index=6, number=105,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kCreatePartition', index=7, number=200,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDropPartition', index=8, number=201,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kHasPartition', index=9, number=202,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDescribePartition', index=10, number=203,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kShowPartitions', index=11, number=204,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kShowSegment', index=12, number=250,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDescribeSegment', index=13, number=251,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kCreateIndex', index=14, number=300,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDescribeIndex', index=15, number=301,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kInsert', index=16, number=400,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kDelete', index=17, number=401,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kFlush', index=18, number=402,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kSearch', index=19, number=500,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kSearchResult', index=20, number=501,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kGetIndexState', index=21, number=502,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kGetCollectionStatistics', index=22, number=503,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kGetPartitionStatistics', index=23, number=504,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kSegmentInfo', index=24, number=600,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kTimeTick', index=25, number=1200,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kQueryNodeStats', index=26, number=1201,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kLoadIndex', index=27, number=1202,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kRequestID', index=28, number=1203,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kRequestTSO', index=29, number=1204,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kAllocateSegment', index=30, number=1205,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kSegmentStatistics', index=31, number=1206,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='kSegmentFlushDone', index=32, number=1207,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1161,
  serialized_end=1843,
)
_sym_db.RegisterEnumDescriptor(_MSGTYPE)

MsgType = enum_type_wrapper.EnumTypeWrapper(_MSGTYPE)
SUCCESS = 0
UNEXPECTED_ERROR = 1
CONNECT_FAILED = 2
PERMISSION_DENIED = 3
COLLECTION_NOT_EXISTS = 4
ILLEGAL_ARGUMENT = 5
ILLEGAL_DIMENSION = 7
ILLEGAL_INDEX_TYPE = 8
ILLEGAL_COLLECTION_NAME = 9
ILLEGAL_TOPK = 10
ILLEGAL_ROWRECORD = 11
ILLEGAL_VECTOR_ID = 12
ILLEGAL_SEARCH_RESULT = 13
FILE_NOT_FOUND = 14
META_FAILED = 15
CACHE_FAILED = 16
CANNOT_CREATE_FOLDER = 17
CANNOT_CREATE_FILE = 18
CANNOT_DELETE_FOLDER = 19
CANNOT_DELETE_FILE = 20
BUILD_INDEX_ERROR = 21
ILLEGAL_NLIST = 22
ILLEGAL_METRIC_TYPE = 23
OUT_OF_MEMORY = 24
DD_REQUEST_RACE = 1000
NONE = 0
UNISSUED = 1
INPROGRESS = 2
FINISHED = 3
FAILED = 4
SegmentNone = 0
SegmentNotExist = 1
SegmentGrowing = 2
SegmentSealed = 3
SegmentFlushed = 4
kNone = 0
kCreateCollection = 100
kDropCollection = 101
kHasCollection = 102
kDescribeCollection = 103
kShowCollections = 104
kGetSysConfigs = 105
kCreatePartition = 200
kDropPartition = 201
kHasPartition = 202
kDescribePartition = 203
kShowPartitions = 204
kShowSegment = 250
kDescribeSegment = 251
kCreateIndex = 300
kDescribeIndex = 301
kInsert = 400
kDelete = 401
kFlush = 402
kSearch = 500
kSearchResult = 501
kGetIndexState = 502
kGetCollectionStatistics = 503
kGetPartitionStatistics = 504
kSegmentInfo = 600
kTimeTick = 1200
kQueryNodeStats = 1201
kLoadIndex = 1202
kRequestID = 1203
kRequestTSO = 1204
kAllocateSegment = 1205
kSegmentStatistics = 1206
kSegmentFlushDone = 1207



_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='milvus.proto.common.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=37,
  serialized_end=44,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='milvus.proto.common.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_code', full_name='milvus.proto.common.Status.error_code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reason', full_name='milvus.proto.common.Status.reason', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=46,
  serialized_end=122,
)


_KEYVALUEPAIR = _descriptor.Descriptor(
  name='KeyValuePair',
  full_name='milvus.proto.common.KeyValuePair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='milvus.proto.common.KeyValuePair.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='milvus.proto.common.KeyValuePair.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=124,
  serialized_end=166,
)


_BLOB = _descriptor.Descriptor(
  name='Blob',
  full_name='milvus.proto.common.Blob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='milvus.proto.common.Blob.value', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=168,
  serialized_end=189,
)


_ADDRESS = _descriptor.Descriptor(
  name='Address',
  full_name='milvus.proto.common.Address',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='milvus.proto.common.Address.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='milvus.proto.common.Address.port', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=191,
  serialized_end=226,
)


_MSGBASE = _descriptor.Descriptor(
  name='MsgBase',
  full_name='milvus.proto.common.MsgBase',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg_type', full_name='milvus.proto.common.MsgBase.msg_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msgID', full_name='milvus.proto.common.MsgBase.msgID', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='milvus.proto.common.MsgBase.timestamp', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sourceID', full_name='milvus.proto.common.MsgBase.sourceID', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=228,
  serialized_end=337,
)


_MSGHEADER = _descriptor.Descriptor(
  name='MsgHeader',
  full_name='milvus.proto.common.MsgHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base', full_name='milvus.proto.common.MsgHeader.base', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=339,
  serialized_end=394,
)

_STATUS.fields_by_name['error_code'].enum_type = _ERRORCODE
_MSGBASE.fields_by_name['msg_type'].enum_type = _MSGTYPE
_MSGHEADER.fields_by_name['base'].message_type = _MSGBASE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['KeyValuePair'] = _KEYVALUEPAIR
DESCRIPTOR.message_types_by_name['Blob'] = _BLOB
DESCRIPTOR.message_types_by_name['Address'] = _ADDRESS
DESCRIPTOR.message_types_by_name['MsgBase'] = _MSGBASE
DESCRIPTOR.message_types_by_name['MsgHeader'] = _MSGHEADER
DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE
DESCRIPTOR.enum_types_by_name['IndexState'] = _INDEXSTATE
DESCRIPTOR.enum_types_by_name['SegmentState'] = _SEGMENTSTATE
DESCRIPTOR.enum_types_by_name['MsgType'] = _MSGTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.Empty)
  })
_sym_db.RegisterMessage(Empty)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.Status)
  })
_sym_db.RegisterMessage(Status)

KeyValuePair = _reflection.GeneratedProtocolMessageType('KeyValuePair', (_message.Message,), {
  'DESCRIPTOR' : _KEYVALUEPAIR,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.KeyValuePair)
  })
_sym_db.RegisterMessage(KeyValuePair)

Blob = _reflection.GeneratedProtocolMessageType('Blob', (_message.Message,), {
  'DESCRIPTOR' : _BLOB,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.Blob)
  })
_sym_db.RegisterMessage(Blob)

Address = _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.Address)
  })
_sym_db.RegisterMessage(Address)

MsgBase = _reflection.GeneratedProtocolMessageType('MsgBase', (_message.Message,), {
  'DESCRIPTOR' : _MSGBASE,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.MsgBase)
  })
_sym_db.RegisterMessage(MsgBase)

MsgHeader = _reflection.GeneratedProtocolMessageType('MsgHeader', (_message.Message,), {
  'DESCRIPTOR' : _MSGHEADER,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:milvus.proto.common.MsgHeader)
  })
_sym_db.RegisterMessage(MsgHeader)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
