# Data Model: Microservices Event Consumers for Todo System

## Notification Service Data Model

### Notification Event
- **event_type**: String (constant: "reminder.set")
- **task_id**: String (UUID of the task with the reminder)
- **user_id**: String (UUID of the user who owns the task)
- **reminder_time**: DateTime (ISO 8601 formatted timestamp when reminder should trigger)
- **task_title**: String (title of the task being reminded)
- **timestamp**: DateTime (ISO 8601 formatted timestamp when event was created)
- **payload**: Dict (additional reminder-specific data)

### Notification Log Entry
- **log_id**: String (UUID for the log entry)
- **notification_event**: NotificationEvent (the event that triggered the notification)
- **delivery_status**: String (enum: "attempted", "failed", "delivered")
- **delivery_timestamp**: DateTime (ISO 8601 formatted timestamp when delivery was attempted)
- **error_message**: String (optional error message if delivery failed)

## Audit Service Data Model

### Task Event
- **event_type**: String (enum: "task.created", "task.updated", "task.completed", "task.deleted")
- **task_id**: String (UUID of the affected task)
- **user_id**: String (UUID of the user who initiated the action)
- **timestamp**: DateTime (ISO 8601 formatted timestamp when event occurred)
- **previous_state**: Dict (optional, state before the change)
- **new_state**: Dict (optional, state after the change)
- **payload**: Dict (additional event-specific data)

### Audit Record
- **record_id**: String (UUID for the audit record)
- **event_type**: String (enum: "task.created", "task.updated", "task.completed", "task.deleted")
- **task_id**: String (UUID of the affected task)
- **user_id**: String (UUID of the user who initiated the action)
- **timestamp**: DateTime (ISO 8601 formatted timestamp when event occurred)
- **payload**: Dict (full event payload)
- **correlation_id**: String (optional ID to correlate related events)

## Shared Data Models

### Kafka Message
- **key**: String (optional, used for partitioning)
- **value**: String (JSON-encoded message content)
- **topic**: String (name of the topic)
- **partition**: Integer (partition number)
- **offset**: Integer (offset within partition)
- **timestamp**: DateTime (timestamp when message was produced)

### Consumer Configuration
- **bootstrap_servers**: List[String] (list of Kafka broker addresses)
- **group_id**: String (consumer group identifier: "notification-service" or "audit-service")
- **auto_offset_reset**: String (enum: "earliest", "latest", "none")
- **enable_auto_commit**: Boolean (whether to auto-commit offsets)
- **max_poll_records**: Integer (max number of records to poll at once)
- **session_timeout_ms**: Integer (session timeout in milliseconds)
- **graceful_shutdown_timeout**: Integer (time in seconds to wait during graceful shutdown)

### Error Handling Data
- **exception_type**: String (type of exception that occurred)
- **error_message**: String (detailed error message)
- **event_payload**: String (original event that caused the error, for debugging)
- **processed_successfully**: Boolean (whether the event was processed successfully)