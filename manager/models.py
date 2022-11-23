from django.db import models
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_404_NOT_FOUND


class BaseManager(models.Manager):
    def get(self, *args, **kwargs):
        queryset = super().get_queryset()
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise APIException(code=HTTP_404_NOT_FOUND, detail=f'{queryset.model._meta.object_name} Does Not Exist')


class App(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=100)
    envs = models.JSONField()
    command = models.CharField(max_length=100)
    objects = BaseManager()

    def __str__(self):
        return self.name


class Run(models.Model):
    choice_list = [('R', 'Running'), ('F', 'Finished')]
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now=True, blank=False)
    state = models.CharField(max_length=100, choices=choice_list)
    envs = models.JSONField()
    command = models.CharField(max_length=200)
    app_id = models.ForeignKey(App, on_delete=models.SET_NULL, null=True)
    container_id = models.CharField(max_length=200)

    def __str__(self):
        return self.app_id.name + " " + str(self.id)
