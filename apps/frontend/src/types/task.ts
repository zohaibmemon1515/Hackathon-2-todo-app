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
  user_id: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  limit: number;
  offset: number;
}