"""Module with the views and helpers for cuckoo-vix pages."""
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from .models import Task
from .models import Status
from .forms import SubmissionForm

import datetime
import requests
import json
import shutil
import os


def handle_uploaded_file(f):
    """Method that creates a temporary file and folder to submission."""
    if not os.path.exists('media/temp'):
        os.makedirs('media/temp')
    with open('media/temp/{}'.format(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def erase_temp_folder():
    """Method to erase the temp folder created for submission."""
    try:
        shutil.rmtree('media/temp/', ignore_errors=True)
    except Exception as e:
        print('%s (%s)' % (e.message, type(e)))


def submit_file(task):
    """Method to submit file to rest API."""
    REST_URL = "http://192.168.1.8:8090/tasks/create/file"
    handle_uploaded_file(task)
    SAMPLE_FILE = 'media/temp/{}'.format(task)
    try:
        with open(SAMPLE_FILE, "rb") as sample:
            multipart_file = {"file": ("temp_file_name", sample)}
            request = requests.post(REST_URL, files=multipart_file)

            json_decoder = json.JSONDecoder()
            task_id = json_decoder.decode(request.text)["task_ids"]

            erase_temp_folder()
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
            id_from_submission = submit_file(request.FILES['task_file'])

            if id_from_submission is not None:
                result = id_from_submission[0]
                new_task = Task(
                    task_file=request.FILES['task_file'],
                    task_id=result,
                    task_description=request.POST.get(
                        'task_description', None),
                    user=request.user,
                    task_submission_date=datetime.datetime.now()
                )
                new_task.save()

                context = RequestContext(request,
                                        {'request': request,
                                        'user': request.user,
                                        'server_hostname': server_hostname,
                                        'server_version': server_version,
                                        'server_vms': server_vms,
                                        'server_total': server_total,
                                        'task_id': id_from_submission
                                        },
                                        )

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
    """List with all user tasks."""
    tasks_from_user = Task.objects.all().filter(user=request.user)

    return render_to_response(
        'vix/list.html',
        RequestContext(request, {
            'request': request,
            'tasks_from_user': tasks_from_user,
        }))


def about(request):
    """about page to show details."""
    return render_to_response(
        'vix/about.html'
    )
