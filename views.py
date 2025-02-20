from django.shortcuts import render
from .models import Tasks
from tabulate import tabulate
from django import forms
from django.core.validators import RegexValidator
from datetime import datetime
from django.http import HttpResponse

tasks_queryset = Tasks.objects.all().values()

class addnewtask(forms.Form):
    task = forms.CharField(
        validators= [RegexValidator(r"^[\w\s]+$", "Only alphabets are allowed")],
        label='Add a new task: '
    )
    
    deadline = forms.DateTimeField()

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < datetime.now(deadline.tzinfo):
            raise forms.ValidationError("The date and time cannot be in the past")
        return deadline
    
class deletetask(forms.Form):
    id = forms.IntegerField(label = "What is the ID of the task you want to delete: ")

class changestatus(forms.Form):
    id = forms.IntegerField(label="Enter the id of the task whose status you wish to change: ")

def tasklist(request):
    return render(request, 'todolist/tasklist.html', {
        "tasks_queryset": tasks_queryset
    })

def add(request):
    if request.method == "POST":
        form = addnewtask(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            deadline = form.cleaned_data["deadline"]
            Tasks.objects.create(
                task = task,
                deadline = deadline
            )

        else:
            return render(request, 'todolist/add.html', {
                "form": form
            })
    
    return render(request, 'todolist/add.html', {
        "form": addnewtask()
    })

def delete(request):
    if request.method == "POST":
        form = deletetask(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data["id"]
            try:
                tasktodelete = Tasks.objects.get(id = task_id)
                tasktodelete.delete()
                tasktodelete.save()
                return HttpResponse("Task was deleted successfully")
            except Tasks.DoesNotExist:
                return HttpResponse(f"Task with id {task_id} does not exist")
    
    return render (request, 'todolist/delete.html', {
        "tasks_queryset": tasks_queryset,
        "form": deletetask
    })

def status(request):
    if request.method == "POST":
        form = deletetask(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data["id"]
            try:
                tasktochange = Tasks.objects.get(id = task_id)
                tasktochange.status = True
                tasktochange.save()
                return HttpResponse("Status Changed")
            except Tasks.DoesNotExist:
                return HttpResponse(f"Task with id {task_id} does not exist")
    
    return render (request, 'todolist/status.html', {
        "tasks_queryset": tasks_queryset,
        "form": changestatus
    })
