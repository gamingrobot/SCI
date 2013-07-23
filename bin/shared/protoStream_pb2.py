# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='protoStream.proto',
  package='',
  serialized_pb='\n\x11protoStream.proto\"A\n\x11ProtoStreamHeader\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\x0e\n\x06module\x18\x02 \x02(\t\x12\x0f\n\x07message\x18\x03 \x02(\t\"w\n\x0fProtoStreamAuth\x12,\n\tauth_type\x18\x01 \x02(\x0e\x32\x19.ProtoStreamAuth.AuthType\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\t\"(\n\x08\x41uthType\x12\t\n\x05TOKEN\x10\x01\x12\x08\n\x04HASH\x10\x02\x12\x07\n\x03KEY\x10\x03')



_PROTOSTREAMAUTH_AUTHTYPE = descriptor.EnumDescriptor(
  name='AuthType',
  full_name='ProtoStreamAuth.AuthType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='TOKEN', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='HASH', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='KEY', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=167,
  serialized_end=207,
)


_PROTOSTREAMHEADER = descriptor.Descriptor(
  name='ProtoStreamHeader',
  full_name='ProtoStreamHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='ProtoStreamHeader.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='module', full_name='ProtoStreamHeader.module', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='ProtoStreamHeader.message', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=21,
  serialized_end=86,
)


_PROTOSTREAMAUTH = descriptor.Descriptor(
  name='ProtoStreamAuth',
  full_name='ProtoStreamAuth',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='auth_type', full_name='ProtoStreamAuth.auth_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='data', full_name='ProtoStreamAuth.data', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROTOSTREAMAUTH_AUTHTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=88,
  serialized_end=207,
)

_PROTOSTREAMAUTH.fields_by_name['auth_type'].enum_type = _PROTOSTREAMAUTH_AUTHTYPE
_PROTOSTREAMAUTH_AUTHTYPE.containing_type = _PROTOSTREAMAUTH;
DESCRIPTOR.message_types_by_name['ProtoStreamHeader'] = _PROTOSTREAMHEADER
DESCRIPTOR.message_types_by_name['ProtoStreamAuth'] = _PROTOSTREAMAUTH

class ProtoStreamHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PROTOSTREAMHEADER
  
  # @@protoc_insertion_point(class_scope:ProtoStreamHeader)

class ProtoStreamAuth(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PROTOSTREAMAUTH
  
  # @@protoc_insertion_point(class_scope:ProtoStreamAuth)

# @@protoc_insertion_point(module_scope)
