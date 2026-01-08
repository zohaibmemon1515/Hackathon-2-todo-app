"use client";

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Pencil, Trash2, Check, X, Clock, Zap } from 'lucide-react';
import { Task } from '@/types/task';
import TaskEditForm from './task-edit-form';

export default function TaskCard({ task, onTaskUpdated, onTaskDeleted }: { task: Task, onTaskUpdated: any, onTaskDeleted: any }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const themes = {
    high: { card: "border-l-rose-500", chip: "bg-rose-50 text-rose-600 border-rose-100", glow: "group-hover:border-rose-200" },
    medium: { card: "border-l-amber-500", chip: "bg-amber-50 text-amber-600 border-amber-100", glow: "group-hover:border-amber-200" },
    low: { card: "border-l-emerald-500", chip: "bg-emerald-50 text-emerald-600 border-emerald-100", glow: "group-hover:border-emerald-200" }
  };

  const style = themes[task.priority?.toLowerCase() as keyof typeof themes] || themes.low;

  // Priority ka pehla letter nikalne ke liye logic
  const priorityInitial = task.priority?.charAt(0).toUpperCase() || 'L';

  return (
    <>
      <motion.div
        layout
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className={`relative group bg-white rounded-2xl border border-slate-100 border-l-[5px] ${style.card} transition-all duration-300 hover:shadow-xl hover:shadow-slate-100 ${style.glow}`}
      >
        <div className={`p-4 sm:p-6 flex flex-col gap-4 ${task.is_completed ? 'bg-slate-50/40 opacity-75' : ''}`}>
          
          {/* TOP SECTION */}
          <div className="flex items-center justify-between">
            {/* Ab yahan sirf Initial (H/M/L) dikhayi dega */}
            <div 
              title={task.priority} // Hover karne par poora naam dikhega
              className={`w-6 h-6 rounded-md border text-[10px] font-black flex items-center justify-center shrink-0 ${style.chip}`}
            >
              {priorityInitial}
            </div>
            
            <div className="flex items-center gap-1 sm:opacity-0 group-hover:opacity-100 transition-all">
              <button 
                onClick={() => setIsModalOpen(true)} 
                className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:bg-slate-100 hover:text-indigo-600 transition-all"
              >
                <Pencil size={15} />
              </button>
              <button 
                onClick={() => onTaskDeleted(task.id)} 
                className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition-all"
              >
                <Trash2 size={15} />
              </button>
            </div>
          </div>

          {/* CONTENT SECTION */}
          <div className="flex items-start gap-3">
            <button
              onClick={() => onTaskUpdated({ ...task, is_completed: !task.is_completed })}
              className={`mt-1 w-5 h-5 shrink-0 rounded-md border-2 flex items-center justify-center transition-all 
              ${task.is_completed ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-200 hover:border-indigo-400'}`}
            >
              {task.is_completed && <Check size={12} strokeWidth={4} />}
            </button>
            <div className="min-w-0 flex-1">
              <h3 className={`text-base font-bold leading-tight ${task.is_completed ? 'text-slate-400 line-through' : 'text-slate-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="mt-1 text-sm text-slate-500 line-clamp-1 group-hover:line-clamp-none transition-all">
                  {task.description}
                </p>
              )}
            </div>
          </div>

          {/* FOOTER */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-50">
            <div className="flex items-center gap-2 text-slate-400">
              {task.due_date && (
                <div className="flex items-center gap-1 text-[11px] font-bold uppercase tracking-tight">
                  <Clock size={12} />
                  {new Date(task.due_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })}
                </div>
              )}
            </div>
            <div className={`h-1.5 w-1.5 rounded-full ${task.is_completed ? 'bg-emerald-500' : 'bg-slate-200'}`} />
          </div>
        </div>
      </motion.div>

      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-100 flex items-end sm:items-center justify-center p-0 sm:p-4">
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" 
            />
            
            <motion.div 
              initial={{ y: "100%" }} animate={{ y: 0 }} exit={{ y: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="relative w-full max-w-lg bg-white shadow-2xl overflow-hidden rounded-t-3xl sm:rounded-3xl"
            >
              <div className="p-6 sm:p-8">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-black text-slate-800 tracking-tight italic">Update Task</h2>
                  <button 
                    onClick={() => setIsModalOpen(false)} 
                    className="w-9 h-9 flex items-center justify-center rounded-full bg-slate-50 text-slate-400 hover:text-rose-500 transition-colors"
                  >
                    <X size={20} />
                  </button>
                </div>

                <TaskEditForm 
                  task={task} 
                  onClose={() => setIsModalOpen(false)} 
                  onTaskUpdated={onTaskUpdated} 
                />
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}