from project import add_task, view_task, delete_task, status_task
import pytest

Tasks= [
    {"ID": 1, "Task": "Finish CS50P", "Completed": True, "Deadline": "2025-02-01 00:00:00"},
    {"ID": 2, "Task": "Buy eggs, milk, and cereal", "Completed": False, "Deadline": "2025-01-28 18:00:00"}
]

def test_add_task():

    Tasks.append(
        {"ID": 3, "Task": "Buy birthday gift", "Completed": False, "Deadline": "2025-02-20 18:00:00"}
        )

    assert(len(Tasks)) == 3
    assert(Tasks[2]["Task"]) == "Buy birthday gift"

def test_view_task():
    sortedtasks = []
    sortedtasks = sorted(Tasks, key = lambda task: task["Deadline"])

    assert(sortedtasks[0]["Task"]) == "Buy eggs, milk, and cereal"

def test_delete_task():
    idtoremove = 2
    newList = []

    for task in Tasks:
        if task["ID"] == idtoremove:
            continue
        else:
            newList.append(task)

    assert(len(newList)) == 2
    assert(newList[1]["ID"]) == 3

def test_status_task():
    
