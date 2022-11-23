from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from manager.docker_manager import DockerManger
from manager.models import App
from manager.serializers import CreateAppSerializer, RunAppSerializer, AppSerializer, AppAndContainerSerializer
from config.logger import log_info


class CreateAppAPIView(CreateAPIView):
    serializer_class = CreateAppSerializer

    def perform_create(self, serializer):
        docker_manager = DockerManger(**serializer.validated_data)
        if docker_manager.get():
            return Response(serializer.data, status=status.HTTP_200_OK)
        docker_manager.pull()
        image = serializer.validated_data['image']
        log_info(f'---> image {image} is pulling ...')
        serializer.save()


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
