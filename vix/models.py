"""This module describes the basic models that consumes flask api."""
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import requests


class Task(models.Model):
    """Task generated to store data localy and identify users."""

    def user_directory_path(instance, filename):
        """File will be uploaded to MEDIA_ROOT/user_id/<filename> ."""
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    def check_if_finished(self,):
        """Check if cuckoo finished analisys."""
        resp = requests.get(
            settings.API_URL_TASK_VIEW.format(self.task_id))
        resp_data = resp.json()
        resp_finished = resp_data['task']['started_on']
        if resp_finished is None:
            return False
        else:
            return resp_finished

    def get_behavior_status(self):
        """Check if a behavior analisys exists. Returns true or false."""
        try:
            resp = requests.get(
                "http://192.168.0.107:8090/malheur/exists/{}".format(self.task_id)
            )
            resp_data = resp.json()
            resp_check_report = resp_data['exists']
            return resp_check_report
        except Exception:
            return 'Not able to check if a behavior analisys exists.'

    def get_malscore(self):
        """Get the malscore from the task analisys."""
        try:
            resp = requests.get(
                settings.API_URL_TASK_REPORT.format(self.task_id)
            )
            resp_data = resp.json()
            resp_malscore = resp_data['malscore']
            return resp_malscore
        except Exception:
            return 'Analisys Failed'

    def get_malfamily(self):
        """Get the mal-family from the task analisys."""
        try:
            resp = requests.get(
                settings.API_URL_TASK_REPORT.format(self.task_id)
            )
            resp_data = resp.json()
            resp_malfamily = resp_data['malfamily']
            return resp_malfamily
        except Exception:
            return 'Analisys Failed'

    def get_percent(self):
        """Get the percentage of positive analisys from virustotal."""
        try:
            resp = requests.get(
                settings.API_URL_TASK_REPORT.format(self.task_id)
            )
            resp_data = resp.json()
            resp_positives = resp_data['virustotal']['positives']
            resp_total = resp_data['virustotal']['total']
            return resp_positives/resp_total*100
        except Exception:
            return 'Analisys Failed'

    task_id = models.IntegerField()
    task_submission_date = models.DateTimeField('Submission Date')
    task_description = models.CharField(max_length=1000)
    task_file = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_finished = check_if_finished

    def __str__(self):
        """Method to return description data."""
        return str(self.task_id)


class TaskFinished(Task):
    """Class to get and parse data from rest api."""

    task_malscore = None
    task_malfamily = None
    task_permanlink = None
    task_positives = None
    task_total = None


class Status(models.Model):
    """Status class to consume server Status."""

    def _get_data_status(attribute, attribute2=None):
        """Returns server status."""
        resp = requests.get(settings.API_URL_STATUS)
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
    """Class to make connections and retrieve data from flask restfull."""

    def get_data_status(attribute):
        resp = requests.get('http://192.168.1.8:8090/cuckoo/status')
        resp_data = resp.json()

        if resp.status_code != 200:
            raise ApiError('GET /cuckoo/tasks {}'.format(resp.status_code))
        else:
            response = resp_data[attribute]
        return response
