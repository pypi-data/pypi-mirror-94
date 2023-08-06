# pylint: disable=no-member
import logging
from typing import Iterator, Mapping, Optional, Tuple

import miniscule
import smart_open as smart
from pydantic import BaseModel

log = logging.getLogger(__name__)


class Registry(BaseModel):
    host: str
    path: Optional[str]

    @property
    def tag(self) -> str:
        return f"{self.host}{self.path}"

    def image(self, version) -> str:
        return f"{self.tag}:{version}"


class App(BaseModel):
    namespace: str
    name: str

    @property
    def qualified_name(self) -> str:
        return f"{self.namespace}-{self.name}"


class Kube(BaseModel):
    namespace: str
    hostname: str
    service_account: str


class Environment(BaseModel):
    kube: Kube


class Manifest(BaseModel):
    app: App
    registry: Registry
    environments: Mapping[str, Environment]


def read(*paths: str) -> Manifest:
    acc: dict = {}
    for (path, piece) in fetch(*paths):
        try:
            acc = merge(acc, piece)
        except:
            log.error("Failed to merge file at %s", path)
            raise
    return Manifest(**acc)


def fetch(*paths: str) -> Iterator[Tuple[str, dict]]:
    for path in paths:
        with smart.open(path, "r") as handle:
            yield (path, miniscule.load_config(handle))


def merge(acc, piece):
    if not isinstance(acc, dict):
        return piece
    for (key, value) in piece.items():
        if key not in acc:
            acc[key] = value
        else:
            acc[key] = merge(acc[key], piece[key])
    return acc
