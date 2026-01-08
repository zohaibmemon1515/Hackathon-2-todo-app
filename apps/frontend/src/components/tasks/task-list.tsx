"use client";

import { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import TaskCard from '@/components/tasks/task-card';
import { LayoutGrid, CheckCircle2, Clock3, BarChart3, Filter } from 'lucide-react';

interface TaskListProps {
  tasks: Task[];
  // Updates ko Partial<Task> kiya taake accuracy rahe
  onTaskUpdated: (id: string, updates: Partial<Task>) => void;
  onTaskDeleted: (id: string) => void;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.is_completed;
    if (filter === 'pending') return !task.is_completed;
    return true;
  });

  const totalPages = Math.ceil(filteredTasks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedTasks = filteredTasks.slice(startIndex, startIndex + itemsPerPage);

  useEffect(() => {
    setCurrentPage(1);
  }, [filter]);

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.is_completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  if (tasks.length === 0) {
    return (
      <div className="bg-white shadow sm:rounded-lg p-12 text-center border-2 border-dashed border-slate-200">
          <LayoutGrid className="mx-auto h-12 w-12 text-slate-300" />
          <h3 className="mt-4 text-sm font-bold text-slate-900">No tasks created</h3>
          <p className="mt-1 text-sm text-slate-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* --- STATS --- */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total', val: totalTasks, icon: LayoutGrid, color: 'text-indigo-600', bg: 'bg-indigo-50' },
          { label: 'Done', val: completedTasks, icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50' },
          { label: 'Pending', val: pendingTasks, icon: Clock3, color: 'text-amber-600', bg: 'bg-amber-50' },
          { label: 'Rate', val: `${completionRate}%`, icon: BarChart3, color: 'text-blue-600', bg: 'bg-blue-50' }
        ].map((stat, i) => (
          <div key={i} className="bg-white p-4 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-4 hover:shadow-md transition-all">
            <div className={`shrink-0 ${stat.bg} ${stat.color} p-3 rounded-2xl`}>
              <stat.icon size={20} />
            </div>
            <div>
              <p className="text-[10px] font-black uppercase tracking-wider text-slate-400">{stat.label}</p>
              <p className="text-xl font-black text-slate-900">{stat.val}</p>
            </div>
          </div>
        ))}
      </div>

      {/* --- FILTER BAR --- */}
      <div className="bg-white p-2 rounded-3xl border border-slate-100 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex bg-slate-50 p-1 rounded-2xl w-full sm:w-auto">
          {(['all', 'pending', 'completed'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setFilter(t)}
              className={`flex-1 sm:flex-none px-6 py-2 text-xs font-bold uppercase tracking-widest rounded-xl transition-all ${
                filter === t 
                  ? 'bg-white text-slate-900 shadow-sm border border-slate-200' 
                  : 'text-slate-400 hover:text-slate-600'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="px-4 text-[11px] font-bold text-slate-400 uppercase tracking-widest hidden sm:block">
           {filteredTasks.length} Tasks Filtered
        </div>
      </div>

      {/* --- TASK LIST AREA --- */}
      <div className="p-6 bg-linear-to-b from-slate-50/50 to-white rounded-3xl border border-slate-100">
        {paginatedTasks.length > 0 ? (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {paginatedTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                // FIX: Added (updatedTask: Task) to remove implicit 'any' error
                onTaskUpdated={(updatedTask: Task) => onTaskUpdated(updatedTask.id, {
                  title: updatedTask.title,
                  description: updatedTask.description,
                  is_completed: updatedTask.is_completed,
                  due_date: updatedTask.due_date,
                  priority: updatedTask.priority
                })}
                onTaskDeleted={onTaskDeleted}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Filter className="mx-auto h-12 w-12 text-slate-200" />
            <h3 className="mt-2 text-sm font-semibold text-slate-900">No tasks found</h3>
          </div>
        )}
      </div>

      {/* PAGINATION */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4">
           <button 
             onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
             disabled={currentPage === 1}
             className="text-xs font-bold uppercase tracking-widest text-slate-400 disabled:opacity-20"
           >
             &larr; Prev
           </button>
           <div className="flex gap-2">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                <button 
                  key={p} 
                  onClick={() => setCurrentPage(p)}
                  className={`w-8 h-8 rounded-lg text-xs font-bold ${currentPage === p ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-500'}`}
                >
                  {p}
                </button>
              ))}
           </div>
           <button 
             onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
             disabled={currentPage === totalPages}
             className="text-xs font-bold uppercase tracking-widest text-slate-400 disabled:opacity-20"
           >
             Next &rarr;
           </button>
        </div>
      )}
    </div>
  );
}