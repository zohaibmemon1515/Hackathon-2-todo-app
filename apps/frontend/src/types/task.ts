// Task type definitions for frontend

export interface Task {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  due_date?: string; // ISO date string
  priority: 'low' | 'medium' | 'high';
  tags?: string[]; // Array of tag names
  recurrence_rule?: {
    frequency: 'daily' | 'weekly' | 'monthly';
    interval: number;
    end_condition: {
      type: 'on_date' | 'after_occurrences';
      value: string | number; // date string or occurrence count
    };
  }; // Recurrence configuration
  reminder_config?: {
    offset_minutes: number;
    notification_method: 'email' | 'push';
  }; // Reminder configuration
  user_id: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
  tags?: string[]; // Array of tag names
  recurrence_rule?: {
    frequency: 'daily' | 'weekly' | 'monthly';
    interval: number;
    end_condition: {
      type: 'on_date' | 'after_occurrences';
      value: string | number; // date string or occurrence count
    };
  }; // Recurrence configuration
  reminder_config?: {
    offset_minutes: number;
    notification_method: 'email' | 'push';
  }; // Reminder configuration
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
  tags?: string[]; // Array of tag names
  recurrence_rule?: {
    frequency: 'daily' | 'weekly' | 'monthly';
    interval: number;
    end_condition: {
      type: 'on_date' | 'after_occurrences';
      value: string | number; // date string or occurrence count
    };
  }; // Recurrence configuration
  reminder_config?: {
    offset_minutes: number;
    notification_method: 'email' | 'push';
  }; // Reminder configuration
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  limit: number;
  offset: number;
}