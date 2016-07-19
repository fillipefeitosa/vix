"""This module describes the basic models that consumes flask api."""
from django.contrib.auth.models import User
from django.db import models
import requests


class Task(models.Model):
    """Task class that consumes flask services."""

    def user_directory_path(instance, filename):
        """File will be uploaded to MEDIA_ROOT/user_id/<filename> ."""
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    task_id = models.IntegerField()
    task_submission_date = models.DateTimeField('Submission Date')
    task_description = models.CharField(max_length=1000)
    task_file = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Method to return description data."""
        return self.task_description


class Status(models.Model):
    """Status class to consume server Status."""

    def _get_data_status(attribute, attribute2=None):
        """Returns server status."""
        resp = requests.get('http://192.168.0.16:8090/cuckoo/status')
        resp_data = resp.json()

        if resp.status_code != 200:
            raise ApiError('GET /cuckoo/tasks {}'.format(resp.status_code))
        else:
            response = resp_data[attribute]
        return response

    hostname = _get_data_status('hostname')
    version = _get_data_status('version')
    total_of_vms = _get_data_status('machines', 'total')
    total_analisys = _get_data_status('tasks', 'total')


class Connect_to_flask(models.Model):

    """
    Class to make connections and retrieve data from flask restfull
    """

    def get_data_status(attribute):
        resp = requests.get('http://192.168.0.16:8090/cuckoo/status')
        resp_data = resp.json()

        if resp.status_code != 200:
            raise ApiError('GET /cuckoo/tasks {}'.format(resp.status_code))
        else:
            response = resp_data[attribute]
        return response
