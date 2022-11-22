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
        except docker.errors.ImageNotFound:
            return False
        return True

    def pull(self):
        try:
            client.images.pull(self.image)
        except docker.errors.InvalidRepository:
            return False
        return True

    def run(self):
        try:
            res = client.containers.run(image=self.image, command=self.command, environment=self.envs, detach=True)
        except docker.errors.APIError:
            return False
        return res.id

