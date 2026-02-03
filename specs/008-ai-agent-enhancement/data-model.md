# Data Model: AI Agent Enhancement

## Overview
Data model extensions for AI agent enhancement while maintaining compatibility with existing structures.

## Enhanced Command Entity
**enhanced_command**
- id: UUID (primary key)
- command_pattern: String (regex pattern for the command)
- command_type: String (check_tasks, set_reminder, etc.)
- language_support: Array<String> (supported languages like ["en", "ur"])
- multi_step_sequence: String (sequence to execute like "create_schedule_notify")
- created_at: DateTime
- updated_at: DateTime

## Command Mapping Entity
**command_mapping**
- id: UUID (primary key)
- original_command: String (English command pattern)
- urdu_equivalent: String (Roman Urdu equivalent)
- agent_tool_id: UUID (foreign key to agent tool)
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime

## Enhanced Message Entity
**message** (extends existing message model)
- id: UUID (primary key, from existing model)
- conversation_id: UUID (foreign key to conversation)
- role: String (system, user, assistant)
- content: Text (message content)
- original_content: Text (original input before processing, e.g., Urdu)
- processed_content: Text (processed content, e.g., translated to English)
- language_detected: String (detected language like "en", "ur")
- command_metadata: JSON (command-specific metadata)
- timestamp: DateTime
- metadata: JSON (language, intent, entities extracted)

## Conversation Context Extension
**conversation** (extends existing conversation model)
- id: UUID (primary key, from existing model)
- user_id: UUID (foreign key to user)
- title: String (generated from first message or user-provided)
- created_at: DateTime
- updated_at: DateTime
- metadata: JSON (AI context, language preference, etc.)
- active_context: JSON (current conversation context with due dates, priorities)

## Validation Rules
- Enhanced command patterns must be valid regex expressions
- Command mapping must have either original_command or urdu_equivalent (or both)
- Message content must not exceed 10,000 characters
- Conversation context must be updated atomically to maintain consistency
- Language detection confidence must be >70% for reliable processing

## Relationships
- Enhanced Command has many Command Mappings (1 to many)
- Conversation has many Messages (1 to many)
- Command Mapping references Agent Tools (many to one)