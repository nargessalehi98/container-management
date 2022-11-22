from config.celery import app
from config.settings import client
from celery.signals import celeryd_init

from manager.models import Run


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
        finish_statuses = ['die', 'destroy', 'kill', 'stop']
        for event in client.events(decode=True):
            if event.get('status') in finish_statuses:
                container_id = event.get('id')
                run = Run.objects.get(container_id=container_id)
                Run.objects.create(state='F', envs=run.envs, command=run.command ,app_id=run.app_id , container_id=container_id)



@celeryd_init.connect
def configure_workers(*args, **kwargs):
    CeleryTasks.docker_events.delay()
