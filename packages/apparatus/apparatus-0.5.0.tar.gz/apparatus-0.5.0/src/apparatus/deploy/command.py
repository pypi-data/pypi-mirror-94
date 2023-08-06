import subprocess
from typing import List, Mapping

from pydantic import Field

from apparatus.base import Command
from apparatus.deploy.manifest import Manifest, read


class Deploy(Command):
    env: str = Field(..., description="the environment", required=True)
    global_: str = Field(
        ..., description="location of the global manifest", alias="global", required=True
    )
    local: str = Field(
        "manifest.yaml", description="location of the local manifest", required=False
    )
    nop: bool = Field(False, description="do not make any actual changes", required=False)

    def run(self, remainder: List[str]) -> None:
        manifest = read(self.global_, self.local)
        version = self._read_version()
        self._helm(manifest, version)

    def _read_version(self) -> str:
        with open("VERSION") as h:
            return h.read().strip()

    def _helm(self, manifest: Manifest, version: str) -> None:
        command = self._helm_command(self._helm_args(manifest, version))
        print(" ".join(command))
        if not self.nop:
            subprocess.run(command)

    def _helm_args(self, manifest: Manifest, version: str) -> Mapping[str, str]:
        return {
            "namespace": manifest.environments[self.env].kube.namespace,
            "kubeHostname": manifest.environments[self.env].kube.hostname,
            "serviceAccount": manifest.environments[self.env].kube.service_account,
            "appName": f"{manifest.app.qualified_name}-{self.env}",
            "env": self.env,
            "image": manifest.registry.image(version),
            "deployment": f"{manifest.app.qualified_name}-{self.env}",
        }

    def _helm_command(self, helm_args: Mapping[str, str]) -> List[str]:
        deployment = helm_args["deployment"]
        command = ["helm", "upgrade", deployment, "./helm", "--install"]
        for (name, value) in helm_args.items():
            if name != "deployment":
                command.extend(["--set", f"{name}={value}"])
        return command
