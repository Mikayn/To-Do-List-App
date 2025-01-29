# To-Do List Application
#### Video Demo: https://youtu.be/HD_gfCh4FX8

### Description:
As a student, I found it challenging to keep track of assignments, projects, and personal tasks, especially those with distant deadlines. I chose this for my final CS50P project to help other students, or even professionals, manage their tasks effectively, ensuring nothing important is missed.
It is a to-do list application having the features of task addition, deletion and categorization which saves the tasks in a `json` file.

---

### Features:
- Through **Command Line Interface (CLI)**, the user is prompted to:
- **Add tasks** with description, and a deadline.
- **View tasks** in sorted, completed, or pending format.
- **Delete task** with complete, and incomplete tasks distinctly marked.
- **Save tasks** for further usage.
- **Reminder** for a task whose deadline is close.

---

### Technical Details:
- This app utilizes python's built in `datetime` module to handle deadlines, and timely reminders.
- Because of simplicity, task storage is done using `json`.
- Testing is done using `pytest` ensuring core functionalities work as expected.
- It utilizes interactive Command Line Interface (CLI).

The main code is in `project.py` and the testing is done in `test_project.py`. `requirements.txt` states the libraries in python that you should install to run the program. After adding at least one task, `Tasks.json` will be created, where all of the stored tasks are kept in systematic order. The format for `Tasks.json` is:
```json
[
    {
        "ID": 1,
        "Task": "Example task",
        "Completed": true/ false,
        "Deadline": YYYY-MM-DD HH:MM:SS
    }
]
```
### File Overview:
- **project.py**: The main code for the application.
- **test_project.py**: Contains unit tests to ensure the app works as intended.
- **requirements.txt**: Lists the Python libraries required to run the program.

After running the program with `python project.py`, it immediately lists out any deadlines within the next 3 days, followed by a table of commands that asks the user what to do (Add tasks, delete tasks, view tasks or change the status of an existing task)

### Future Improvements:
- Support for recurring tasks (like taking the trash out, or attending a weekly meeting) would be a good addition.
- A good improvement would be the addition of simple Graphical User Interface (GUI).

### Acknowledgements:
I would like to thank CS50P for teaching me the foundation to build this project. Furthermore, I thank the Python community for their resources and discussion which contributed to the improvement in my skills.
