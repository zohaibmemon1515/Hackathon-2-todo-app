from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple
from datetime import datetime
from ..models.task import Task as TaskModel, Tag, TaskTagLink as TaskTag, TaskCreate, TaskUpdate, TaskPatch
from ..schemas.task import TaskRead
from ..utils.logging import get_security_logger
from ..services.kafka_service import kafka_service
import uuid
import logging

# Initialize loggers
logger = logging.getLogger(__name__)
security_logger = get_security_logger()

# ------------------ TASK OPERATIONS ------------------

async def get_user_tasks(
    db: Session,
    user_id: uuid.UUID,
    completed: Optional[bool] = None,
    query_text: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[TaskRead], int]:
    """Get all tasks for a user with optional filters, search, and sorting."""
    try:
        query = db.query(TaskModel).filter(TaskModel.user_id == user_id)

        if completed is not None:
            query = query.filter(TaskModel.is_completed == completed)

        if query_text:
            search_filter = or_(
                TaskModel.title.ilike(f"%{query_text}%"),
                TaskModel.description.ilike(f"%{query_text}%") if TaskModel.description is not None else False
            )
            query = query.filter(search_filter)

        if due_date_from:
            query = query.filter(TaskModel.due_date >= due_date_from)
        if due_date_to:
            query = query.filter(TaskModel.due_date <= due_date_to)

        if tags:
            query = query.join(TaskTag).join(Tag).filter(
                and_(Tag.user_id == user_id, Tag.name.in_(tags))
            )

        sort_column = getattr(TaskModel, sort_by, TaskModel.created_at)
        query = query.order_by(sort_column.desc() if sort_order.lower() == "desc" else sort_column.asc())

        total = query.count()
        tasks = query.offset(offset).limit(limit).all()

        task_list = []
        for task in tasks:
            task_dict = task.to_dict()
            task_tags = db.query(Tag).join(TaskTag).filter(TaskTag.task_id == task.id).all()
            task_dict['tags'] = [tag.name for tag in task_tags]
            task_list.append(TaskRead.model_validate(task_dict))

        security_logger.log_sensitive_operation(
            "GET_USER_TASKS",
            str(user_id),
            {
                "count": len(task_list),
                "filter_completed": completed,
                "search_query": query_text,
                "filtered_tags": tags,
                "due_date_from": due_date_from,
                "due_date_to": due_date_to,
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        )

        return task_list, total

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving tasks for user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving tasks for user {user_id}: {str(e)}")
        raise


async def get_task_by_id(db: Session, task_id: int, user_id: uuid.UUID) -> Optional[TaskRead]:
    try:
        task = db.query(TaskModel).filter(and_(TaskModel.id == task_id, TaskModel.user_id == user_id)).first()
        if task:
            result = TaskRead.model_validate(task)
            security_logger.log_sensitive_operation("GET_TASK_BY_ID", str(user_id), {"task_id": task_id})
            return result
        return None

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise


async def create_task(db: Session, user_id: uuid.UUID, task_data: TaskCreate) -> TaskRead:
    try:
        tags = task_data.tags if hasattr(task_data, 'tags') else []

        # Create task
        task_dict = task_data.model_dump(exclude={'tags'}, exclude_unset=True)
        db_task = TaskModel(**task_dict, user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # Process tags
        tag_objs = []
        for tag_name in tags:
            tag = db.query(Tag).filter(and_(Tag.name == tag_name, Tag.user_id == user_id)).first()
            if not tag:
                tag = Tag(name=tag_name, user_id=user_id)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            tag_objs.append(tag)

            # Link task and tag if not already linked
            existing_link = db.query(TaskTag).filter(and_(TaskTag.task_id == db_task.id, TaskTag.tag_id == tag.id)).first()
            if not existing_link:
                db.add(TaskTag(task_id=db_task.id, tag_id=tag.id))
        db.commit()
        db.refresh(db_task)

        task_dict = db_task.to_dict()
        task_dict['tags'] = [tag.name for tag in tag_objs]
        result = TaskRead.model_validate(task_dict)

        security_logger.log_sensitive_operation(
            "CREATE_TASK",
            str(user_id),
            {"task_id": db_task.id, "title": task_data.title, "tags_count": len(tags)}
        )

        # Publish events after successful database commit
        try:
            # Publish task.created event
            await kafka_service.publish_task_event('task.created', task_dict)

            # Publish UI sync event
            await kafka_service.publish_ui_sync_event('created', task_dict)

            # Publish reminder event if reminder_at is set
            if task_dict.get('reminder_at'):
                await kafka_service.publish_reminder_event(task_dict)
        except Exception as e:
            logger.error(f"Error publishing events after task creation: {str(e)}")
            # Don't raise - event publishing shouldn't break the main operation

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error creating task for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating task for user {user_id}: {str(e)}")
        db.rollback()
        raise


async def update_task(db: Session, task_id: int, user_id: uuid.UUID, task_data: TaskUpdate) -> Optional[TaskRead]:
    try:
        task = db.query(TaskModel).filter(and_(TaskModel.id == task_id, TaskModel.user_id == user_id)).first()
        if not task:
            return None

        tags = task_data.tags if hasattr(task_data, 'tags') else None
        update_data = task_data.model_dump(exclude={'tags'}, exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        if tags is not None:
            # Remove existing links
            db.query(TaskTag).filter(TaskTag.task_id == task_id).delete()
            db.commit()

            # Add new tags
            for tag_name in tags:
                tag = db.query(Tag).filter(and_(Tag.name == tag_name, Tag.user_id == user_id)).first()
                if not tag:
                    tag = Tag(name=tag_name, user_id=user_id)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                existing_link = db.query(TaskTag).filter(and_(TaskTag.task_id == task.id, TaskTag.tag_id == tag.id)).first()
                if not existing_link:
                    db.add(TaskTag(task_id=task.id, tag_id=tag.id))
            db.commit()

        db.commit()
        db.refresh(task)

        task_dict = task.to_dict()
        task_tags = db.query(Tag).join(TaskTag).filter(TaskTag.task_id == task.id).all()
        task_dict['tags'] = [tag.name for tag in task_tags]
        result = TaskRead.model_validate(task_dict)

        security_logger.log_sensitive_operation(
            "UPDATE_TASK",
            str(user_id),
            {"task_id": task_id, "updated_fields": list(update_data.keys()), "tags_updated": tags is not None}
        )

        # Publish events after successful database commit
        try:
            # Publish task.updated event
            await kafka_service.publish_task_event('task.updated', task_dict)

            # Publish UI sync event
            await kafka_service.publish_ui_sync_event('updated', task_dict)

            # Publish reminder event if reminder_at is set and changed
            if task_dict.get('reminder_at'):
                await kafka_service.publish_reminder_event(task_dict)
        except Exception as e:
            logger.error(f"Error publishing events after task update: {str(e)}")
            # Don't raise - event publishing shouldn't break the main operation

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error updating task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise


async def patch_task(db: Session, task_id: int, user_id: uuid.UUID, task_data: TaskPatch) -> Optional[TaskRead]:
    try:
        task = db.query(TaskModel).filter(and_(TaskModel.id == task_id, TaskModel.user_id == user_id)).first()
        if not task:
            return None

        tags = task_data.tags if hasattr(task_data, 'tags') else None
        update_data = task_data.model_dump(exclude={'tags'}, exclude_unset=True)

        # Track if completion status changed
        was_completed = task.is_completed
        for field, value in update_data.items():
            setattr(task, field, value)

        is_now_completed = task.is_completed

        if tags is not None:
            db.query(TaskTag).filter(TaskTag.task_id == task_id).delete()
            db.commit()
            for tag_name in tags:
                tag = db.query(Tag).filter(and_(Tag.name == tag_name, Tag.user_id == user_id)).first()
                if not tag:
                    tag = Tag(name=tag_name, user_id=user_id)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                existing_link = db.query(TaskTag).filter(and_(TaskTag.task_id == task.id, TaskTag.tag_id == tag.id)).first()
                if not existing_link:
                    db.add(TaskTag(task_id=task.id, tag_id=tag.id))
            db.commit()

        db.commit()
        db.refresh(task)

        task_dict = task.to_dict()
        task_tags = db.query(Tag).join(TaskTag).filter(TaskTag.task_id == task.id).all()
        task_dict['tags'] = [tag.name for tag in task_tags]
        result = TaskRead.model_validate(task_dict)

        security_logger.log_sensitive_operation(
            "PATCH_TASK",
            str(user_id),
            {"task_id": task_id, "updated_fields": list(update_data.keys()), "tags_updated": tags is not None}
        )

        # Publish events after successful database commit
        try:
            # Determine the appropriate event type
            event_type = 'task.completed' if is_now_completed and not was_completed else 'task.updated'

            # Publish the appropriate task event
            await kafka_service.publish_task_event(event_type, task_dict)

            # Publish UI sync event
            sync_action = 'completed' if is_now_completed and not was_completed else 'updated'
            await kafka_service.publish_ui_sync_event(sync_action, task_dict)

            # Publish reminder event if reminder_at is set and changed
            if task_dict.get('reminder_at'):
                await kafka_service.publish_reminder_event(task_dict)
        except Exception as e:
            logger.error(f"Error publishing events after task patch: {str(e)}")
            # Don't raise - event publishing shouldn't break the main operation

        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error patching task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error patching task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise


async def delete_task(db: Session, task_id: int, user_id: uuid.UUID) -> bool:
    try:
        task = db.query(TaskModel).filter(and_(TaskModel.id == task_id, TaskModel.user_id == user_id)).first()
        if not task:
            return False

        # Store task data before deletion for event publishing
        task_dict = task.to_dict()
        task_tags = db.query(Tag).join(TaskTag).filter(TaskTag.task_id == task.id).all()
        task_dict['tags'] = [tag.name for tag in task_tags]

        db.delete(task)
        db.commit()

        security_logger.log_sensitive_operation(
            "DELETE_TASK",
            str(user_id),
            {"task_id": task_id}
        )

        # Publish events after successful database commit
        try:
            # Publish task.deleted event
            await kafka_service.publish_task_event('task.deleted', task_dict)

            # Publish UI sync event
            await kafka_service.publish_ui_sync_event('deleted', task_dict)
        except Exception as e:
            logger.error(f"Error publishing events after task deletion: {str(e)}")
            # Don't raise - event publishing shouldn't break the main operation

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error deleting task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting task {task_id} for user {user_id}: {str(e)}")
        db.rollback()
        raise
