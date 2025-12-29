"""
Unit tests for TaskRepository
"""
from src.models.task import Task
from src.repositories.task_repository import TaskRepository


def test_add_task_with_auto_generated_id():
    """Test adding a task with auto-generated ID"""
    repo = TaskRepository()
    task = Task(id=0, title="Test Task")
    task_id = repo.add_task(task)

    assert task_id == 1
    assert task.id == 1
    assert len(repo.get_all_tasks()) == 1
    assert repo.get_task_by_id(1).title == "Test Task"


def test_add_task_with_predefined_id():
    """Test adding a task with predefined ID"""
    repo = TaskRepository()
    task = Task(id=5, title="Test Task")
    task_id = repo.add_task(task)

    assert task_id == 5
    assert task.id == 5
    assert len(repo.get_all_tasks()) == 1
    assert repo.get_task_by_id(5).title == "Test Task"


def test_add_multiple_tasks():
    """Test adding multiple tasks with auto-generated IDs"""
    repo = TaskRepository()

    task1 = Task(id=0, title="Task 1")
    task2 = Task(id=0, title="Task 2")
    task3 = Task(id=0, title="Task 3")

    id1 = repo.add_task(task1)
    id2 = repo.add_task(task2)
    id3 = repo.add_task(task3)

    assert id1 == 1
    assert id2 == 2
    assert id3 == 3

    all_tasks = repo.get_all_tasks()
    assert len(all_tasks) == 3


def test_get_all_tasks_empty():
    """Test getting all tasks when repository is empty"""
    repo = TaskRepository()
    tasks = repo.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_with_tasks():
    """Test getting all tasks when repository has tasks"""
    repo = TaskRepository()

    task1 = Task(id=0, title="Task 1")
    task2 = Task(id=0, title="Task 2")

    repo.add_task(task1)
    repo.add_task(task2)

    tasks = repo.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_get_task_by_id_existing():
    """Test getting a task by existing ID"""
    repo = TaskRepository()
    task = Task(id=0, title="Test Task")
    task_id = repo.add_task(task)

    retrieved_task = repo.get_task_by_id(task_id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"


def test_get_task_by_id_non_existing():
    """Test getting a task by non-existing ID"""
    repo = TaskRepository()
    retrieved_task = repo.get_task_by_id(999)

    assert retrieved_task is None


def test_update_task_existing_fields():
    """Test updating existing task fields"""
    repo = TaskRepository()
    task = Task(id=0, title="Original Title", description="Original Description")
    task_id = repo.add_task(task)

    success = repo.update_task(task_id, title="New Title", description="New Description", completed=True)

    assert success is True
    updated_task = repo.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    assert updated_task.completed is True


def test_update_task_partial_fields():
    """Test updating only some task fields"""
    repo = TaskRepository()
    task = Task(id=0, title="Original Title", description="Original Description", completed=False)
    task_id = repo.add_task(task)

    success = repo.update_task(task_id, title="New Title")

    assert success is True
    updated_task = repo.get_task_by_id(task_id)
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged
    assert updated_task.completed is False  # Should remain unchanged


def test_update_task_non_existing():
    """Test updating a non-existing task"""
    repo = TaskRepository()
    success = repo.update_task(999, title="New Title")

    assert success is False


def test_delete_task_existing():
    """Test deleting an existing task"""
    repo = TaskRepository()
    task = Task(id=0, title="Test Task")
    task_id = repo.add_task(task)

    success = repo.delete_task(task_id)

    assert success is True
    assert repo.get_task_by_id(task_id) is None
    assert len(repo.get_all_tasks()) == 0


def test_delete_task_non_existing():
    """Test deleting a non-existing task"""
    repo = TaskRepository()
    success = repo.delete_task(999)

    assert success is False


def test_toggle_task_completion():
    """Test toggling task completion status"""
    repo = TaskRepository()
    task = Task(id=0, title="Test Task", completed=False)
    task_id = repo.add_task(task)

    # Toggle from False to True
    success = repo.toggle_task_completion(task_id)
    assert success is True
    toggled_task = repo.get_task_by_id(task_id)
    assert toggled_task.completed is True

    # Toggle from True to False
    success = repo.toggle_task_completion(task_id)
    assert success is True
    toggled_task = repo.get_task_by_id(task_id)
    assert toggled_task.completed is False


def test_toggle_task_completion_non_existing():
    """Test toggling completion status of non-existing task"""
    repo = TaskRepository()
    success = repo.toggle_task_completion(999)

    assert success is False