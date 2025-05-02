from flask import Flask, render_template, flash, abort, request, redirect

from db.tables import create_tables
from config import APP_KEY
from utils.helpers import get_task_list, get_task, create_todo_task, sidebar_content
from utils.custom_filters import formatted_string, time_difference
from utils.enums import STATUS_CHOICES, PRIORITY_CHOICES

app = Flask(__name__)
app.secret_key = APP_KEY
app.jinja_env.filters['formatted_string'] = formatted_string
app.jinja_env.filters['time_difference'] = time_difference

create_tables()

MAIN_PATH = "app/"

# --------------- Context procesors ---------------------
@app.context_processor
def inject_data():
    context_processor = sidebar_content()
    return context_processor

# ---------------- error handlers --------------
@app.errorhandler(404)
def not_found(error):
    """ Custom page for 404 error """
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ---------------- routes --------------------
@app.route("/")
def index():
    tasks = get_task_list()
    print("tasks =================", tasks)
    return render_template(f"{MAIN_PATH}index.html", tasks=tasks)


@app.route("/task/add", methods=['GET', 'POST'])
def add_task():
    if request.method == "POST":
        data = request.form
        # Extract form data
        data = {
            "task": request.form.get('task'),
            "due_date": request.form.get('due_date'),
            "description": request.form.get('description'),
            "status": request.form.get('status'),
            "priority": request.form.get('priority', 'medium')
        }

        # Validate data
        validation = True
        for key, value in data.items():
            if not value:
                validation = False
                flash(message=f"'{formatted_string(value=key)}' is required !", category="error")
        if validation is True:
            c = create_todo_task(data=data)
            print("c =========", c)
            flash(f'{data.get("task")} created successfully !', category="success")
            return redirect('/')
    return render_template(f"{MAIN_PATH}add_task.html", STATUS_CHOICES=STATUS_CHOICES, PRIORITY_CHOICES=PRIORITY_CHOICES)


@app.route("/task/<task_id>/edit-task")
def edit_task(task_id):
    task = get_task(field="id", value=task_id)
    print("task ======", task)
    if task is None:
        return abort(code=404)
    return render_template(f"{MAIN_PATH}edit_task.html", task=task, STATUS_CHOICES=STATUS_CHOICES, PRIORITY_CHOICES=PRIORITY_CHOICES)


if __name__=="__main__":
    app.run(debug=True)