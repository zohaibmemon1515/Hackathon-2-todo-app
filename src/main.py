#!/usr/bin/env python3
"""
Menu-driven CLI interface for the todo application
"""
from typing import Optional
import sys
import os
# Add the src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


class TodoApp:
    """
    Main CLI application class
    """
    def __init__(self):
        self.repository = TaskRepository()
        self.service = TaskService(self.repository)

    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "="*50)
        print("                 TODO APPLICATION")
        print("="*50)
        print("1. Add Task        - Create a new task")
        print("2. View All Tasks  - Display all tasks")
        print("3. Update Task     - Modify existing task")
        print("4. Delete Task     - Remove a task (with confirmation)")
        print("5. Toggle Complete - Mark task as complete/incomplete")
        print("6. Help            - Show instructions")
        print("7. Exit            - Quit the application")
        print("-"*50)
        print("Instructions:")
        print("- Enter the number of your choice")
        print("- For task operations, you'll be prompted for task ID")
        print("- Empty titles are not allowed")
        print("- Use '0' to cancel operations when prompted")
        print("-"*50)

    def get_user_choice(self) -> str:
        """Get user's menu choice"""
        try:
            choice = input("Enter your choice (1-7): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return "7"

    def add_task(self):
        """Implement Add Task functionality"""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            task_id = self.service.add_task(title, description)
            print(f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_all_tasks(self):
        """Implement View All Tasks functionality"""
        print("\n--- All Tasks ---")
        try:
            tasks = self.service.get_all_tasks()

            if not tasks:
                print("No tasks found.")
                return

            print(f"{'ID':<4} {'Status':<10} {'Title':<20} {'Description'}")
            print("-" * 60)

            for task in tasks:
                status = "✓ Done" if task.completed else "○ Pending"
                print(f"{task.id:<4} {status:<10} {task.title:<20} {task.description}")
        except Exception as e:
            print(f"An error occurred while retrieving tasks: {e}")

    def update_task(self):
        """Implement Update Task functionality"""
        print("\n--- Update Task ---")
        try:
            task_id_str = input("Enter task ID to update: ").strip()
            if not task_id_str:
                print("Error: Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            # Check if task exists
            try:
                current_task = self.service.get_task_by_id(task_id)
            except ValueError:
                print(f"Error: Task with ID {task_id} does not exist.")
                return

            print(f"Current task: {current_task.title}")
            print(f"Current description: {current_task.description}")

            new_title = input(f"Enter new title (or press Enter to keep '{current_task.title}'): ").strip()
            new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

            # Prepare updates
            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_description:
                updates['description'] = new_description

            # If no updates were provided, keep the original values
            if not updates:
                print("No changes were made.")
                return

            # Perform update
            self.service.update_task(task_id, **updates)
            print("Task updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_task(self):
        """Implement Delete Task functionality"""
        print("\n--- Delete Task ---")
        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            if not task_id_str:
                print("Error: Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            # Confirm deletion
            try:
                task = self.service.get_task_by_id(task_id)
                confirm = input(f"Are you sure you want to delete task '{task.title}'? (yes/no): ").strip().lower()

                if confirm not in ['yes', 'y']:
                    print("Task deletion cancelled.")
                    return

                self.service.delete_task(task_id)
                print("Task deleted successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def toggle_task_completion(self):
        """Implement Mark Task as Complete/Incomplete functionality"""
        print("\n--- Toggle Task Completion ---")
        try:
            task_id_str = input("Enter task ID to toggle: ").strip()
            if not task_id_str:
                print("Error: Task ID cannot be empty.")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            try:
                # Get current task to show status before toggle
                current_task = self.service.get_task_by_id(task_id)
                current_status = "Complete" if current_task.completed else "Incomplete"

                self.service.toggle_task_completion(task_id)

                # Get updated task to show new status
                updated_task = self.service.get_task_by_id(task_id)
                new_status = "Complete" if updated_task.completed else "Incomplete"

                print(f"Task status changed from {current_status} to {new_status}.")
            except ValueError as e:
                print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def show_help(self):
        """Display help information"""
        print("\n" + "="*50)
        print("                    HELP")
        print("="*50)
        print("TASK ID EXPLANATION:")
        print("- Each task has a unique ID number")
        print("- You'll need this ID to update, delete, or toggle tasks")
        print("- Use the 'View All Tasks' option to see all task IDs")
        print()
        print("COMMAND EXPLANATIONS:")
        print("- Add Task: Creates a new task with a title and optional description")
        print("- View All Tasks: Shows all tasks with their status and details")
        print("- Update Task: Change the title or description of an existing task")
        print("- Delete Task: Remove a task permanently (with confirmation)")
        print("- Toggle Complete: Switch task status between complete/incomplete")
        print("- Help: Shows this help message")
        print("- Exit: Closes the application")
        print()
        print("VALIDATION RULES:")
        print("- Task titles cannot be empty")
        print("- Task IDs must be positive numbers")
        print("- All inputs are validated for correctness")
        print("="*50)

    def run(self):
        """Run the main application loop"""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_task_completion()
            elif choice == "6":
                self.show_help()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

            # Pause before showing menu again
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()