from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from config.logger import log_warning
from manager.docker_manager import DockerManger
from manager.models import App, Run


class CreateAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"

    def validate_name(self, name):
        if " " in name:
            raise NotAcceptable("name can not contain space")
        return name


class RunAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"
        extra_kwargs = {
            'state': {'required': False},
            'envs': {'required': False},
            'command': {'required': False},
            'container_id': {'required': False},
        }

    def create(self, validated_data):
        app = App.objects.get(name=self.context['name'])
        docker_manager = DockerManger(name=app.name, image=app.image, envs=app.envs, command=app.command)
        log_warning(f'---> Docker container {docker_manager.image} is running ... ')
        container_id = docker_manager.run()
        return Run.objects.create(
            state='R',
            envs=app.envs,
            command=app.command,
            app_id=app,
            container_id=container_id
        )


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"


class AppAndContainerSerializer(serializers.ModelSerializer):
    # run_set = RunSerializer(many=True)
    run_set = serializers.SerializerMethodField('get_containers')

    class Meta:
        model = App
        fields = ('id', 'name', 'image', 'envs', 'command', 'run_set')

    def get_containers(self, instance):
        run_queryset = Run.objects.filter(app_id=self.instance.id, state='F')
        serialized = RunSerializer(instance=run_queryset, many=True)
        return serialized.data
