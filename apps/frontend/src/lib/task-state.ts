"use client";

import { useState, useCallback, useRef } from "react";
import { Task, TaskCreate, TaskUpdate } from "@/types/task";
import { taskAPI } from "@/lib/api";

export const useTaskState = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentTask, setCurrentTask] = useState<Task | null>(null);

  // 🔒 Prevent duplicate requests
  const inFlight = useRef<Set<string>>(new Set());

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await taskAPI.getAll();
      setTasks(res.tasks || []);
    } catch (e: any) {
      setError(e.message || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  }, []);

  const createTask = useCallback(async (data: Omit<TaskCreate, "user_id">) => {
    const key = JSON.stringify(data);
    if (inFlight.current.has(key)) return;

    inFlight.current.add(key);
    setLoading(true);
    setError(null);

    try {
      const task = await taskAPI.create(data); // ✅ ONLY API CALL
      setTasks(prev => [task, ...prev]);
    } catch (e: any) {
      setError(e.message || "Failed to create task");
    } finally {
      inFlight.current.delete(key);
      setLoading(false);
    }
  }, []);

  const updateTask = useCallback(async (id: string, data: TaskUpdate) => {
    if (inFlight.current.has(id)) return;
    inFlight.current.add(id);

    setLoading(true);
    setError(null);
    try {
      const updated = await taskAPI.update(id, data);
      setTasks(prev => prev.map(t => (t.id === id ? updated : t)));
      setCurrentTask(c => (c?.id === id ? updated : c));
    } catch (e: any) {
      setError(e.message || "Failed to update task");
    } finally {
      inFlight.current.delete(id);
      setLoading(false);
    }
  }, []);

  const deleteTask = useCallback(async (id: string) => {
    if (inFlight.current.has(id)) return;
    inFlight.current.add(id);

    setLoading(true);
    setError(null);
    try {
      await taskAPI.delete(id);
      setTasks(prev => prev.filter(t => t.id !== id));
    } catch (e: any) {
      setError(e.message || "Failed to delete task");
    } finally {
      inFlight.current.delete(id);
      setLoading(false);
    }
  }, []);

  return {
    tasks,
    loading,
    error,
    currentTask,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    setCurrentTask,
  };
};
