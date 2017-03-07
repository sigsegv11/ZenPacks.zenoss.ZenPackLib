##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.Zuul.infos import ProxyProperty
from ..helpers.OrderAndValue import OrderAndValue
from .Spec import Spec, MethodInfoProperty, EnumInfoProperty
from DateTime import DateTime

class PropertySpec(Spec):
    """PropertySpec"""

    _property_map = {'string': {'default': '', 'class': str, 'type': 'str'},
                     'password': {'default': '', 'class': str, 'type': 'str'},
                     'boolean': {'default': False, 'class': bool, 'type': 'bool'},
                     'int': {'default': None, 'class': int, 'type': 'int'},
                     'float': {'default': None, 'class': float, 'type': 'float'},
                     'long': {'default': None, 'class': long, 'type': 'long'},
                     'date': {'default': DateTime('1970/01/01 00:00:00 UTC'), 'class': DateTime, 'type': 'date'},
                     'lines': {'default': [], 'class': list, 'type': 'list(str)'},
                     'text': {'default': None, 'class': str, 'type': 'str'},
                     }

    def __init__(
            self,
            class_spec,
            name,
            type_='string',
            default=None,
            _source_location=None,
            zplog=None,
            ):
        """
        Create a Property Specification
        """
        super(PropertySpec, self).__init__(_source_location=_source_location)
        if zplog:
            self.LOG = zplog
        self.class_spec = class_spec
        self.name = name
        self.type_ = type_
        self.default = default

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if value is not None:
            try:
                self._default = self.property_class(value)
            except Exception as e:
                # This appears to be occurring for int properties since they seem to acquire '' for a default
                # probably from the Spec or SpecParam init_params
                if self.type_ != 'int':
                    LOG.warn('Error setting "{}" default ({}): {}'.format(self.name, value, e))
                self._default = self.default_value
        else:
            self._default = self.default_value

    @classmethod
    def get_properties_entry_type(cls, type_):
        """Return a corresponding 'type' entry from a _properties dictionary"""
        return cls._property_map.get(type_, {}).get('type', 'str')

    @property
    def properties_entry_type(self):
        """Return a corresponding 'type' for this instance from a _properties dictionary"""
        return self.get_properties_entry_type(self.type_)

    @classmethod
    def get_property_class(cls, type_):
        """Return the corresponding Python class given the type_ argument"""
        return cls._property_map.get(type_, {}).get('class', str)

    @property
    def property_class(self):
        """Return the corresponding Python class for this instance"""
        return self.get_property_class(self.type_)
