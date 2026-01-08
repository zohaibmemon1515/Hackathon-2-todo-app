from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple
from ..models.task import Task as TaskModel, TaskCreate, TaskUpdate, TaskPatch
from ..schemas.task import TaskRead
from ..utils.logging import get_security_logger
import uuid
import logging

# Initialize logger
logger = logging.getLogger(__name__)
security_logger = get_security_logger()


def get_user_tasks(
    db: Session,
    user_id: uuid.UUID,
    completed: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[TaskRead], int]:
    try:
        query = db.query(TaskModel).filter(TaskModel.user_id == user_id)

        if completed is not None:
            query = query.filter(TaskModel.is_completed == completed)

        total = query.count()
        tasks = query.offset(offset).limit(limit).all()

        task_list = [
            TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead.model_validate(task)
            for task in tasks
        ]

        security_logger.log_sensitive_operation(
            "GET_USER_TASKS",
            str(user_id),
            {"count": len(task_list), "filter_completed": completed}
        )

        return task_list, total

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving tasks for user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving tasks for user {user_id}: {str(e)}")
        raise


def get_task_by_id(db: Session, task_id: str, user_id: uuid.UUID) -> Optional[TaskRead]:
    try:
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            logger.warning(f"Invalid UUID format for task_id: {task_id}")
            return None

        task = db.query(TaskModel).filter(
            and_(TaskModel.id == uuid_task_id, TaskModel.user_id == user_id)
        ).first()

        if task:
            result = TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead.model_validate(task)
            security_logger.log_sensitive_operation(
                "GET_TASK_BY_ID",
                str(user_id),
                {"task_id": str(uuid_task_id)}
            )
            return result
        return None

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise


def create_task(db: Session, user_id: uuid.UUID, task_data: TaskCreate) -> TaskRead:
    try:
        db_task = TaskModel(**task_data.model_dump(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        result = TaskRead.from_orm(db_task) if hasattr(TaskRead, 'from_orm') else TaskRead.model_validate(db_task)

        security_logger.log_sensitive_operation(
            "CREATE_TASK",
            str(user_id),
            {"task_id": str(db_task.id), "title": task_data.title}
        )

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error creating task for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating task for user {user_id}: {str(e)}")
        db.rollback()
        raise


def update_task(db: Session, task_id: str, user_id: uuid.UUID, task_data: TaskUpdate) -> Optional[TaskRead]:
    try:
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            logger.warning(f"Invalid UUID format for task_id: {task_id}")
            return None

        task = db.query(TaskModel).filter(
            and_(TaskModel.id == uuid_task_id, TaskModel.user_id == user_id)
        ).first()

        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        result = TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead.model_validate(task)

        security_logger.log_sensitive_operation(
            "UPDATE_TASK",
            str(user_id),
            {"task_id": str(uuid_task_id), "updated_fields": list(update_data.keys())}
        )

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error updating task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise


def patch_task(db: Session, task_id: str, user_id: uuid.UUID, task_data: TaskPatch) -> Optional[TaskRead]:
    try:
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            logger.warning(f"Invalid UUID format for task_id: {task_id}")
            return None

        task = db.query(TaskModel).filter(
            and_(TaskModel.id == uuid_task_id, TaskModel.user_id == user_id)
        ).first()

        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)

        result = TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else TaskRead.model_validate(task)

        security_logger.log_sensitive_operation(
            "PATCH_TASK",
            str(user_id),
            {"task_id": str(uuid_task_id), "updated_fields": list(update_data.keys())}
        )

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error patching task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error patching task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise


def delete_task(db: Session, task_id: str, user_id: uuid.UUID) -> bool:
    try:
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            logger.warning(f"Invalid UUID format for task_id: {task_id}")
            return False

        task = db.query(TaskModel).filter(
            and_(TaskModel.id == uuid_task_id, TaskModel.user_id == user_id)
        ).first()

        if not task:
            return False

        db.delete(task)
        db.commit()

        security_logger.log_sensitive_operation(
            "DELETE_TASK",
            str(user_id),
            {"task_id": str(uuid_task_id)}
        )

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error deleting task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
