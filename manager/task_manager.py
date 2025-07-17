import json
from datetime import datetime

# Task class for individual task
class Task:
    def __init__(self,title,): 
        self.title = title
        self.completed=False
        self.created_at=datetime.now()   #captures time when task is created

    def mark_completed(self):
        self.completed =True
        print(f"{self.title} marked as completed")

    def mark_incomplete(self):
        self.completed=False
        print(f"{self.title} marked as incomplete")

# to toggle task (complete)
    def toggle(self):
        if self.completed:
            self.mark_incomplete()
        else:
            self.mark_completed()

# Convert task to dictionary to save in json
    def to_dict(self):
        return {
            "title" : self.title,
            "completed": self.completed,
            "created_at" : self.created_at.isoformat()
        }

# Recreate task from dictionary 
    @classmethod
    def from_dict(cls,data):
        task =cls(data['title'])
        task.completed = data['completed']
        task.created_at =datetime.fromisoformat(data['created_at'])
        return task

    def __str__(self):
        status = "✓" if self.completed else "○"
        date_str =self.created_at.strftime("%Y-%m-%d %H:%M")
        return(f"[{status}] {self.title} (created: {date_str})")


#TaskManager class to handle list of tasks
class TaskManger:
    def __init__(self,filename="tasks.json"):
        self.tasks =[]     # List to store all task objects
        self.filename = filename  #json file 
        self.load_task()          # loads task at startup

# Add a new task
    def add_task(self,title):
        new_task = Task(title)
        self.tasks.append(new_task)
        self.save_task()                    #saves the task in json file
        print(f"\nTask added: '{new_task}'")

# display task
    def display_task(self):
        if not self.tasks:
            print("\n Tasks not found")
        else:
            print("\n-----Your Tasks----")
            for idx,task in enumerate(self.tasks, start=1):  
                print(f"{idx}. {task}")

# Mark a specific task complete
    def mark_task_completed(self, task_id):
        if 1 <= task_id <= len(self.tasks):
            self.tasks[task_id - 1].mark_completed()
            self.save_task()
        else:
            print(f"Invalid task id {task_id}")
    
# delete a specific task
    def delete_task(self,task_id):
        if 1 <= task_id <= len(self.tasks):
            self.tasks.pop(task_id - 1)
            self.save_task()
        else:
            print(f"Invalid task id {task_id}")

# Saves tasks to json file
    def save_task(self):
        try:
            tasks_data=[task.to_dict() for task in self.tasks]
            with open("tasks.json","w") as f:
                json.dump(tasks_data, f, indent=2)
            print(f"\n tasks saved to {self.filename}")
        except Exception as e:
            print(f"error saving task: {e}")

# Loading tasks from json file
    def load_task(self):
        try:
            with open(self.filename,'r') as f:
                task_data =json.load(f)
            self.tasks = [Task.from_dict(task) for task in task_data]
            print(f"Loaded {len(self.tasks)} tasks from {self.filename}")
        except FileNotFoundError:
            print(f"No existing task file found. Starting fresh.")
        except Exception as e:
            print(f"Error loading tasks: {e}")

# returns a total number of task
    def get_task_count(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        return total, completed


def main():
    while True:
        manager = TaskManger()
        print("\n---TASK MANAGER---")
        print("\n 1. Add task"
              "\n 2. Display tasks"
              "\n 3. Mark as completed"
              "\n 4. Delete task"
              "\n 5. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input")
            continue

        if choice == 1:
            title=input("Enter a task to add:")
            manager.add_task(title)

        elif choice == 2:
            manager.display_task()

        elif choice == 3:
            manager.display_task()
            try:
                index = int(input("Enter index: "))
                manager.mark_task_completed(index)
            except ValueError:
                print("Invalid input")
        
        elif choice == 4:
            manager.display_task()
            try:
                index = int(input("Enter index: "))
                manager.delete_task(index)
            except ValueError:
                print("Invalid input")
        
        elif choice ==5:
            break

if __name__ =="__main__":
    main()
