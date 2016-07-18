"""Module with the views and helpers for cuckoo-vix pages."""
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .models import Status
import datetime

from .models import Task
from .forms import SubmissionForm
import requests
import json
import shutil


def handle_uploaded_file(f):
    """Method that creates a temporary file to submission."""
    with open('media/temp/{}'.format(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def erase_temp_folder(f):
    """Method to erase the temp folder created for submission."""
    try:
        shutil.rmtree('media/temp/', ignore_errors=True)
    except Exception as e:
        print('%s (%s)' % (e.message, type(e)))


def submit_file(task):
    """Method to submit file to rest API."""
    REST_URL = "http://192.168.1.9:8090/tasks/create/file"
    handle_uploaded_file(task)
    SAMPLE_FILE = 'media/temp/{}'.format(task)
    try:
        with open(SAMPLE_FILE, "rb") as sample:
            multipart_file = {"file": ("temp_file_name", sample)}
            request = requests.post(REST_URL, files=multipart_file)

            json_decoder = json.JSONDecoder()
            task_id = json_decoder.decode(request.text)["task_ids"]

            return task_id

    except Exception as e:
        print('%s (%s)' % (e.message, type(e)))


def index(request):
    """Index page that shows the server status and a upload form."""
    server_hostname = Status.hostname
    server_version = Status.version
    server_vms = Status.total_of_vms
    server_total = Status.total_analisys

    context = RequestContext(request,
                            {'request': request,
                            'user': request.user,
                            'server_hostname': server_hostname,
                            'server_version': server_version,
                            'server_vms': server_vms,
                            'server_total': server_total,
                            },
                            )

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = Task(
                task_file=request.FILES['task_file'],
                task_id=1,
                task_description='from my email',
                user=request.user,
                task_submission_date=datetime.datetime.now()
            )
            if submit_file(request.FILES['task_file']) is not None:
                new_task.save()

            # Redirecting to index after POST request
            return render_to_response(
                'vix/index.html',
                context_instance=context
            )
        else:
            # If something fails, return an empty form
            form = SubmissionForm()
        return render_to_response(
            'vix/index.html',
            {'form': form},
            context_instance=context
        )

    return render_to_response('vix/index.html', context_instance=context)


def task_list(request):
    if request.user.is_authenticated():
        return render_to_response('vix/list.html')
    else:
        return render_to_response('vix/index.html')


def task_new(request):
    return true
