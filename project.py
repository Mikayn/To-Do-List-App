import json, os, sys, re, time
from datetime import datetime
from tabulate import tabulate #type:ignore

if os.path.exists("Tasks.json") and os.path.getsize("Tasks.json") > 0:
    with open("Tasks.json", "r") as file:
        Tasks = json.load(file)
else:
    Tasks = []


def main():
    show_reminders()
    time.sleep(1)

    table = [
        ["1", "Add a new task"],
        ["2", "View current tasks"],
        ["3", "Delete existing tasks"],
        ["4", "Change the status of tasks"]
    ]

    Choice = int(input(tabulate(table, tablefmt = "pretty") + "\n"))

    match Choice:
        case 1:
            add_task()

        case 2:
            view_task()

        case 3:
            delete_task()

        case 4:
            status_task()

        case _:
            print("Choose from the available options please!")

def add_task():
    userInteraction = "y"
    highest_ID = 0
    for task in Tasks:
        if task["ID"] and task["ID"] > highest_ID:
            highest_ID = task["ID"]
    i = highest_ID + 1

    while userInteraction == "y":
        taskToAdd = input("What is the task you would like to add? ")
        matches = re.match(r"^[\w\s]+$", taskToAdd)

        if not matches:
            print("Please enter only alphabets, numbers and whitespaces! ")
            continue

        deadline = deadline_validation()

        Tasks.append({"ID": i, "Task": taskToAdd, "Completed": False, "Deadline": deadline})
        i += 1

        userInteraction = input("do you wish to add another task? (y/n)").lower()
        while userInteraction not in ["y", "n"]:
            print('Please enter "y" for yes and "n" for no only')
            userInteraction = input("do you wish to add another task? (y/n)").lower()

    writing_to_file(Tasks)

def view_task():
    newList = []

    check_for_tasks()

    Table = [
        ["1"," View all tasks"],
        ["2", "View incomplete tasks"],
        ["3", "View the tasks in terms of deadline"],
        ["4" , "Search for a particular task" ]
    ]

    Choice = int(input(tabulate(Table, tablefmt = "pretty") + "\n"))

    match Choice:
        case 1:
            print(tabulate(Tasks, headers="keys", tablefmt ="github"))

        case 2:
            for task in Tasks:
                if not task["Completed"]:
                    newList.append(task)
            print(tabulate(newList, headers = "keys", tablefmt = "github"))

        case 3:
            newList = sorted(Tasks, key = lambda x: datetime.strptime(x["Deadline"], "%Y-%m-%d %H:%M:%S"))
            print(tabulate(newList, headers = "keys", tablefmt = "github"))

        case 4:
            search = input("What is the task you are looking for? ").strip()
            if matches := re.search(r"^[\w\s]+$", search):
                for task in Tasks:
                    if search.lower() in task["Task"].lower():
                        newList.append(task)

                if newList:
                    print(tabulate(newList, headers = "keys", tablefmt = "github"))

                else:
                    userInteraction = input("Did not find your task :( \nWould you like to see all tasks? (y/n) ").lower()
                    while userInteraction not in ["y", "n"]:
                        print("Please enter 'y' for yes and 'n' for no only! ")
                        userInteraction = input("Would you like to see all tasks? (y/n) ").lower()

                    if userInteraction == "y":
                        print(tabulate(Tasks, headers = "keys", tablefmt = "github"))
                    else:
                        sys.exit()
            else:
                sys.exit("Invalid search term! Please only use letters, numbers, or spaces! ")

        case _:
            sys.exit("You didnt choose from the available options. ")

def delete_task():
    userInteraction = "y"
    IDsToRemove = []

    check_for_tasks()

    while userInteraction == "y":
        print(tabulate(Tasks, headers="keys", tablefmt = "github"))

        getID = int(input("What is the ID of the task you wish to remove? "))
        IDsToRemove.append(getID)

        userInteraction = input("Do you wish to remove other tasks? (y/n)").lower()
        while userInteraction not in ["y", "n"]:
            print('Please enter "y" for yes and "n" for no only! ')
            userInteraction = input("Do you wish to remove other tasks? (y/n)").lower()

    for task_id in IDsToRemove:
        task_found = False
        for task in Tasks:
            if task["ID"] == task_id:
                Tasks.remove(task)
                task_found = True
        if not task_found:
            print(f"The task with ID {task_id} does not exist!" )

    for index, task in enumerate(Tasks):
       task["ID"] = index + 1

    writing_to_file(Tasks)

def status_task():
    #GET ID FROM USER > CHANGE THE STATUS FROM COMPLETE=FALSE TO COMPLETE=TRUE AND VICE VERSA
    IDstoChange = []
    userInteraction = "y"

    check_for_tasks()

    while userInteraction == "y":
        getID = int(input("What is the ID of the task whose status you would like to change? "))
        IDstoChange.append(getID)
        userInteraction = input("Would you like to change the status of another task? (y/n) ").lower()

        while userInteraction not in ["y","n"]:
            print("Please enter 'y' for yes or 'n' for no only! ")
            userInteraction = input("Would you like to change the status of another task? (y/n) ").lower()

    for id in IDstoChange:
        task_found = False
        for task in Tasks:
            if task["ID"] == id:
                task["Completed"] = not task["Completed"]
                if task["Completed"] == True:
                    print("Congratulations on completing the task! ")
                else:
                    print("Oh no! Better finish it fast. ")
                task_found = True
        if not task_found:
            print(f"Task with ID {id} not found. ")

    writing_to_file(Tasks)


def deadline_validation():
    now = datetime.now()
    date_formats = ["%Y/%m/%d", "%d/%m/%Y"]
    time_formats = ["%H:%M", "%I:%M %p"]

    while True:
        try:
            deadline = input("ENTER DEADLINE WITH PROPER FORMAT (YYYY/MM/DD) ")
            parsedDate = None

            for format in date_formats:
                try:
                    parsedDate = datetime.strptime(deadline, format)
                    break
                except ValueError:
                    continue

            if parsedDate == None:
                print("Your format is incorrect! ")
                continue

            if parsedDate < now:
                print("The deadline has passed! ")
                continue

            userInteraction = input("Would you like to add a specific time?(y/n) If no, then the time will automatically be set at 6 PM. ").lower()
            while userInteraction not in ["y", "n"]:
                print("Please answer y for yes and n for no only! ")
                userInteraction = input("Would you like to add a specific time?(y/n) If no, then the time will automatically be set at 6 PM. ").lower()

            if userInteraction == "y":
                while True:
                    timeDeadline = input("What is the time of the deadline? (HH:MM or HH:MM AM/PM) ")
                    parsed_time = None

                    for format in time_formats:
                        try:
                            parsed_time = datetime.strptime(timeDeadline, format).time()
                            break
                        except ValueError:
                            continue

                    if parsed_time is None:
                        print("The time format is invalid! ")
                    else:
                        parsedDate = datetime.combine(parsedDate.date(), parsed_time)
                        break

            else:
                for format in time_formats:
                    try:
                        parsed_time = datetime.strptime("06:00 PM", format).time()
                        parsedDate = datetime.combine(parsedDate.date(), parsed_time)
                        break
                    except ValueError:
                        continue

            if (parsedDate - now).total_seconds() < 600:
                print("The deadline is too soon! Just finish the task. ")

            elif (parsedDate - now).total_seconds() < 0:
                print("The deadline has already passed! ")
                continue

            return parsedDate.isoformat().replace("T" , " ")

        except ValueError as e:
            print(f"An error occured unexpectedly: {e} ")

def show_reminders():
    now = datetime.now()
    newList = []

    for task in Tasks:
        if "Deadline" in task:
            try:
                deadline = datetime.strptime(task["Deadline"], "%Y-%m-%d %H:%M:%S")
                if (0 <= (deadline - now).days <= 3) and task["Completed"] == False:
                    newList.append(task)

            except ValueError:
                continue

    if newList:
        print("🔔 Upcoming Deadlines: ")
        print(tabulate(newList, tablefmt = "pretty", headers= "keys") + "\n")
    else:
        print("Hooray! No Upcoming Deadlines! \n")


def writing_to_file(Tasks):
    with open("Tasks.json", "w") as file:
        json.dump(Tasks, file, indent = 4)

    print(tabulate(Tasks, headers = "keys", tablefmt = "github"))

def check_for_tasks():
    if not Tasks:
        sys.exit("There are no tasks saved currently. ")

if __name__ == "__main__":
    main()
