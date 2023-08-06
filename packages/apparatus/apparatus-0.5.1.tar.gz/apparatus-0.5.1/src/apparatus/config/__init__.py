from typing import Optional, List

import yaml
from pydantic import Field

from apparatus.base import Command, read_config


class Config(Command):
    env: Optional[str] = Field(None, description="the environment")

    HELP = "Examine the configuration"

    def run(self, remainder: List[str]) -> None:
        config = read_config(self.env)
        print(yaml.dump(config))
