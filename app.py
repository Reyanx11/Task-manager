from flask import Flask, render_template, request, redirect, url_for
from manager.task_manager import TaskManger

app = Flask(__name__)

manager =TaskManger()

@app.route("/")
def home():
    return render_template("index.html", tasks=manager.tasks)

# Route to add a new task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")   # Get task title from form
    if title:
        manager.add_task(title)     # Add task to TaskManager
    return redirect(url_for("home"))   # Redirect to home after adding

# Route to toggle task completion status
@app.route("/toggle/<task_id>", methods=["POST"])
def toggle_task(task_id):
    manager.toggle_task_by_id(task_id)    # Toggle completion status
    return redirect(url_for("home"))

# Route to delete a task
@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    manager.delete_task_by_id(task_id)  # Delete task
    return redirect(url_for("home"))

#runs flask app
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)   #enables debug mode
