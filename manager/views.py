from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from config.celery_tasks import CeleryTasks
from manager.docker_manager import DockerManger
from manager.models import App
from manager.serializers import CreateAppSerializer, RunAppSerializer, AppSerializer, AppAndContainerSerializer
from config.logger import log_warning


class CreateAppAPIView(CreateAPIView):
    serializer_class = CreateAppSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        docker_manager = DockerManger(**serializer.validated_data)
        if not docker_manager.get():
            log_warning(f'---> Image {docker_manager.image} is pulling... ')
            CeleryTasks.pull_image.delay(docker_manager)
            image = serializer.validated_data['image']
            log_warning(f'---> image {image} is pulling ...')
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RunAppAPIView(CreateAPIView):
    serializer_class = RunAppSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['name'] = self.kwargs['name']
        return context


class AppListAPIView(ListAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()


class UpdateAppAPIView(UpdateAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()
    lookup_field = 'name'


class RemoveApiView(DestroyAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()
    lookup_field = 'name'


class GetAppAPIView(RetrieveAPIView):
    serializer_class = AppAndContainerSerializer
    queryset = App.objects.all()
    lookup_field = 'name'
