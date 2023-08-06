from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Any, List, Mapping, Optional

import miniscule
from pydantic import BaseModel
from pydantic.main import ModelMetaclass


class CommandMeta(ModelMetaclass):
    def __init__(cls, _name, _bases, _attrs):
        # pylint: disable=super-init-not-called
        if not hasattr(cls, "commands"):
            cls.commands = []
        else:
            cls.commands.append(cls)


class Command(ABC, BaseModel, metaclass=CommandMeta):

    _ARG_PARSERS: Mapping[str, Any] = {}

    @abstractmethod
    def run(self, remainder: List[str]) -> None:
        pass

    def help(self) -> Optional[str]:
        return None

    @classmethod
    def create_parser(cls, arg_parsers=None, **kwargs) -> ArgumentParser:
        arg_parsers = arg_parsers or cls._ARG_PARSERS
        parser = ArgumentParser(**kwargs)
        subparsers = parser.add_subparsers()
        for command in Command.commands:
            command.add_subparser(subparsers, arg_parsers)
        return parser

    @classmethod
    def add_subparser(cls, subparsers, arg_parsers: Mapping[str, Any]) -> None:
        parser = subparsers.add_parser(cls.__name__.lower())
        for (name, field) in cls.__fields__.items():
            kwargs = {}
            if hasattr(field, "field_info") and field.field_info.description:
                kwargs["help"] = field.field_info.description
            if field.type_ == bool:
                kwargs["required"] = False
                kwargs["action"] = "store_true"
            else:
                kwargs["type"] = arg_parsers.get(field.type_, field.type_)
                kwargs["required"] = field.required
                if field.default is not None:
                    kwargs["default"] = field.default
            parser.add_argument(f"--{field.alias or name}", **kwargs)
            parser.set_defaults(cls=cls)


def read_config(env: Optional[str]):
    if env is not None:
        return miniscule.read_config(f"env/{env}/config.yaml")
    return miniscule.read_config()
