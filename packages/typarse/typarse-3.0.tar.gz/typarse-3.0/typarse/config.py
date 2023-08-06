from typing import Any
from inspect import isclass


class MetaConfig(type):
    """Takes care of printing the config like a dictionary"""
    def __repr__(cls) -> str:
        contents = dict(cls.__dict__)
        contents.pop('__module__')
        contents.pop('__annotations__')
        contents.pop('__doc__')
        return contents.__repr__()

    def __str__(cls) -> str:
        contents = dict(cls.__dict__)
        contents.pop('__module__')
        contents.pop('__annotations__')
        contents.pop('__doc__')
        return contents.__str__()


class BaseConfig(metaclass=MetaConfig):

    @classmethod
    def set(cls, key: str, value: Any):
        """Set a single key's vale"""
        if hasattr(cls, key):
            setattr(cls, key, value)

    @classmethod
    def get(cls, key: str) -> Any:
        """Get the key's value, defaulting to None."""
        return getattr(cls, key, None)

    @classmethod
    def to_dict(cls) -> dict:
        """Converts the config to a dictionary, removing the built-ins"""
        contents = dict(cls.__dict__)
        contents.pop('__module__')
        contents.pop('__annotations__')
        contents.pop('__doc__')
        return contents

    @classmethod
    def update(cls, config: dict):
        """Updates the config based on the values from a dictionary."""
        for key in config:
            value = config.get(key)
            d_value = cls.get(key)

            if isclass(d_value) and issubclass(d_value, BaseConfig):
                d_value.update(value)
            else:
                cls.set(key, value)