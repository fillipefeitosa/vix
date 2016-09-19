"""Some aditional data that can be excluded.

Module that crates tables and consumes data from rest api.
table = TaskTable(Task.objects.all().filter(user=request.user))
RequestConfig(request).configure(table)
return render(request, 'vix/list.html', {'table': table})

"""
import django_tables2 as tables
from .models import Task


class MalScore(tables.Column):
    """Returns MalScore from API."""

    def render(self, value):
        """render the MalScore."""
        return '<%s>' % value


class TaskTable(tables.Table):
    """Creates the table for tasks."""

    malscore = MalScore('MalScore', '1')

    class Meta:
        model = Task
        attrs = {'class': 'paleblue'}




class UpperCollumn(tables.Column):
    def render(self, value):
        return value.upper()


class Example(tables.Table):
    normal = tables.Column()
    upper = UpperCollumn()


data = [{'normal': 'Hi There!', 'upper': 'Hi There"'}]

table2 = Example(data)
