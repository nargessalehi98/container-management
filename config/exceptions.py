from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class ImageException(APIException):
    default_detail = "repository does not exist or access to the resource is denied"
    status_code = status.HTTP_400_BAD_REQUEST


class RunException(APIException):
    default_detail = "Can not run this image"
    status_code = status.HTTP_400_BAD_REQUEST


class AppNotFoundException(NotFound):
    default_detail = "App not found"