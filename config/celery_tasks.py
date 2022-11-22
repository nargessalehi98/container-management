from config.celery import app
from config.settings import client
from celery.signals import celeryd_init


class CeleryTasks:
    @staticmethod
    @app.task
    def pull_image(docker_manager):
        docker_manager.pull()

    @staticmethod
    @app.task
    def run_image(docker_manager):
        docker_manager.run()

    @staticmethod
    @app.task
    def docker_events():
        for event in client.events(decode=True):
            print(event)


@celeryd_init.connect
def configure_workers(*args, **kwargs):
    CeleryTasks.docker_events.delay()
