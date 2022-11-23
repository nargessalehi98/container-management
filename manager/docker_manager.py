from dataclasses import dataclass
import docker.errors
from config.settings import client
from config.logger import log_error
from config.exceptions import RunException, ImageException


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
        except docker.errors.APIError as e:
            log_error(e)
            raise ImageException

    def run(self):
        try:
            if self.get():
                res = client.containers.run(image=self.image, command=self.command, environment=self.envs, detach=True)
                if not res.id:
                    raise RunException
                return res.id
            else:
                raise RunException
        except docker.errors.APIError as e:
            log_error(e)
            raise RunException
