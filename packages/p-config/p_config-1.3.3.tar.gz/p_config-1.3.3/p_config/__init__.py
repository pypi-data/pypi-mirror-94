__version__ = '1.3.3'

from copy import deepcopy
from functools import partial
import json
import os

import yaml


class AttrDict(dict):
    def __getattr__(self, key):
        return self[key.upper()]


class Converter:
    def __call__(self, value):
        return value


class ConfigMeta(type):
    def __new__(cls, name, bases, attrs):
        converter_mapping = {}
        to_be_removed = []
        for key, value in attrs.items():
            if isinstance(value, (type, Converter)):
                converter_mapping[key.upper()] = value
                to_be_removed.append(key)
        for key in to_be_removed:
            attrs.pop(key)
        attrs['_converter'] = converter_mapping
        return super().__new__(cls, name, bases, attrs)


class Config(metaclass=ConfigMeta):
    def __init__(self, config_file=None, **defaults):
        self.__raw_config = AttrDict()
        self.__converter = deepcopy(self.__class__._converter)
        self.load_dict(defaults)
        if config_file:
            self.load_file(config_file)

    def load(self, file_obj):
        return self.load_file(file_obj)

    def load_env(self):
        self.load_dict(os.environ)

    def load_file(self, file_obj, format='yaml'):
        _format = format
        # json/yaml
        if not hasattr(file_obj, 'read') and \
                os.path.splitext(file_obj)[-1] == '.json':
            _format = 'json'
        load_func = json.load if _format == 'json' else yaml.safe_load
        if hasattr(file_obj, 'read'):
            config = load_func(f)
        else:
            with open(file_obj) as f:
                config = load_func(f)
        self.load_dict(config)

    def load_dict(self, d, prefix=''):
        for key, value in d.items():
            key = '{prefix}.{key}'.format(prefix=prefix, key=key)
            if isinstance(value, dict):
                self.load_dict(value, prefix=key)
            else:
                self.__set_config(key, value)

    def __set_config(self, key, value):
        key = key.upper()
        nested_key_lst = key.strip('.').split('.')
        config_dct = self.__raw_config
        for key in nested_key_lst[:-1]:
            if not isinstance(config_dct.get(key), dict):
                config_dct[key] = AttrDict()
            config_dct = config_dct[key]
        key = nested_key_lst[-1]
        config_dct[key] = self.__normalize_value(value)

    def __normalize_value(self, value):
        if isinstance(value, dict):
            return {
                key: self.__normalize_value(_value)
                for key, _value in value.items()
            }
        elif isinstance(value, (list, tuple)):
            return [self.__normalize_value(item) for item in value]
        else:
            return value

    def set_converter(self, key, convert_func):
        self.__converter[key.upper()] = convert_func

    def set_cast_func(self, key, cast_func):
        return self.set_converter(key, cast_func)

    def __getitem__(self, key):
        value = self.__raw_config
        for part_key in key.upper().split('.'):
            value = value[part_key]
        converter = self.__converter.get(key.upper())
        if converter:
            value = converter(value)
        return value

    def __setitem__(self, key, value):
        return self.__set_config(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getattr__(self, key):
        if not key.isupper():
            raise KeyError('{} does not exist'.format(key))
        return self.__getitem__(key)
