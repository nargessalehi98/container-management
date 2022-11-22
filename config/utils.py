from dataclasses import dataclass


@dataclass
class DockerInput:
    name: str
    image: str
    envs: dict
    command: str
