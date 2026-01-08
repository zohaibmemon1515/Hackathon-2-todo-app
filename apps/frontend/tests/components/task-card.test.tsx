import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import TaskCard from '@/components/tasks/task-card';
import { Task } from '@/types/task';

// Mock the api module
vi.mock('@/lib/api', () => ({
  api: {
    tasks: {
      patch: vi.fn(),
      delete: vi.fn(),
      update: vi.fn(),
    },
  },
}));

const mockTask: Task = {
  id: '1',
  title: 'Test Task',
  description: 'Test Description',
  is_completed: false,
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z',
  due_date: '2023-12-31T23:59:59Z',
  priority: 'medium',
  user_id: 'user-1',
};

const mockOnTaskUpdated = vi.fn();
const mockOnTaskDeleted = vi.fn();

describe('TaskCard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders task information correctly', () => {
    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('Medium')).toBeInTheDocument();
    expect(screen.getByText('Due: Dec 31, 2023')).toBeInTheDocument();
  });

  it('toggles task completion status when checkbox is clicked', async () => {
    const { api } = await import('@/lib/api');
    const updatedTask = { ...mockTask, is_completed: true };
    (api.tasks.patch as vi.Mock).mockResolvedValue(updatedTask);

    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(api.tasks.patch).toHaveBeenCalledWith(mockTask.id, {
        is_completed: true,
      });
      expect(mockOnTaskUpdated).toHaveBeenCalledWith(updatedTask);
    });
  });

  it('enters edit mode when edit button is clicked', () => {
    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test Description')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument();
  });

  it('updates task when save is clicked in edit mode', async () => {
    const { api } = await import('@/lib/api');
    const updatedTask = { ...mockTask, title: 'Updated Task' };
    (api.tasks.update as vi.Mock).mockResolvedValue(updatedTask);

    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    // Enter edit mode
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Change the title
    const titleInput = screen.getByDisplayValue('Test Task');
    fireEvent.change(titleInput, { target: { value: 'Updated Task' } });

    // Click save
    const saveButton = screen.getByRole('button', { name: 'Save' });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(api.tasks.update).toHaveBeenCalledWith(mockTask.id, expect.objectContaining({
        title: 'Updated Task',
      }));
      expect(mockOnTaskUpdated).toHaveBeenCalledWith(updatedTask);
    });
  });

  it('cancels edit mode when cancel is clicked', async () => {
    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    // Enter edit mode
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Change the title
    const titleInput = screen.getByDisplayValue('Test Task');
    fireEvent.change(titleInput, { target: { value: 'Updated Task' } });

    // Click cancel
    const cancelButton = screen.getByRole('button', { name: 'Cancel' });
    fireEvent.click(cancelButton);

    // Check that we're back in view mode
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Save' })).not.toBeInTheDocument();
  });

  it('deletes task when delete button is clicked', async () => {
    const { api } = await import('@/lib/api');
    (api.tasks.delete as vi.Mock).mockResolvedValue({});

    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    const deleteButton = screen.getByText('Del');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(api.tasks.delete).toHaveBeenCalledWith(mockTask.id);
      expect(mockOnTaskDeleted).toHaveBeenCalledWith(mockTask.id);
    });
  });

  it('shows error message when API call fails', async () => {
    const { api } = await import('@/lib/api');
    (api.tasks.patch as vi.Mock).mockRejectedValue(new Error('API Error'));

    render(
      <TaskCard
        task={mockTask}
        onTaskUpdated={mockOnTaskUpdated}
        onTaskDeleted={mockOnTaskDeleted}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(screen.getByText('API Error')).toBeInTheDocument();
    });
  });
});