# Data Model for AI Powered Todo Chatbot

## Entities

### Conversation
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Foreign Key reference to user)
- **created_at**: DateTime (Timestamp when conversation started)
- **updated_at**: DateTime (Timestamp when conversation was last updated)
- **title**: String (Optional, auto-generated from first message or topic)

### Message
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Reference to user who sent the message)
- **conversation_id**: Integer (Foreign Key reference to Conversation)
- **role**: String (Enum: "user", "assistant", "system")
- **content**: Text (The actual message content)
- **timestamp**: DateTime (When the message was created)
- **metadata**: JSON (Additional data like tool calls, etc.)

## Relationships
- One Conversation to Many Messages (One-to-Many)
- One User to Many Conversations (One-to-Many)
- One User to Many Messages (One-to-Many)

## Validation Rules
- Conversation must have a valid user_id
- Message must belong to a valid conversation
- Message role must be one of the allowed values
- Message content must not be empty
- Conversation timestamps must be in chronological order

## State Transitions
- Conversation state managed implicitly through updated_at timestamp
- Messages are immutable once created