from dataclasses import dataclass
import docker.errors
from config.settings import client


@dataclass
class DockerManger:
    name: str
    image: str
    envs: dict
    command: str

    def get(self):
        try:
            client.images.get(self.image)
            return True
        except docker.errors.ImageNotFound:
            return False

    def pull(self):
        try:
            client.images.pull(self.image)
            return True
        except docker.errors.InvalidRepository:
            return False

    def run(self):
        try:
            res = client.containers.run(image=self.image, command=self.command, environment=self.envs, detach=True)
            return res.id
        except docker.errors.APIError:
            return False
