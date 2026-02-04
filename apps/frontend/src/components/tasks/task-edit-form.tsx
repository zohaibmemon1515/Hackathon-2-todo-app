"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Task } from "@/types/task";
import { useTaskState } from "@/lib/task-state";
import {
  Save, Calendar, Flag, AlignLeft, Sparkles,
  Tag, X, Loader2, Command, Clock
} from "lucide-react";

interface Props {
  task: Task; // ✅ Existing task data as prop
  onTaskUpdated: (data: Task) => Promise<void>;
  onClose: () => void;
}

export default function TaskEditForm({ task, onTaskUpdated, onClose }: Props) {
  const { loading: stateLoading } = useTaskState();
  const [isFocused, setIsFocused] = useState(false);
  const [internalLoading, setInternalLoading] = useState(false);
  const [newTag, setNewTag] = useState("");
  
  const today = new Date().toISOString().split('T')[0];
  const nowForReminder = new Date().toISOString().slice(0, 16);

  // ✅ Initialize state with existing task values
  const [formData, setFormData] = useState({
    title: task.title || "",
    description: task.description || "",
    priority: (task.priority as "low" | "medium" | "high") || "medium",
    due_date: task.due_date ? new Date(task.due_date).toISOString().split('T')[0] : "",
    reminder_at: task.reminder_at ? new Date(task.reminder_at).toISOString().slice(0, 16) : "",
    tags: task.tags || [],
  });

  // Shortcut key (Ctrl/Cmd + Enter)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && formData.title) {
        handleSubmit(e as any);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [formData.title]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleAddTag = () => {
    const tag = newTag.trim().toLowerCase();
    if (!tag || formData.tags.includes(tag)) return;
    setFormData(prev => ({ ...prev, tags: [...prev.tags, tag] }));
    setNewTag("");
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(t => t !== tagToRemove)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || stateLoading || internalLoading) return;
    
    setInternalLoading(true);
    try {
        // Merge old task data with new formData
        await onTaskUpdated({ ...task, ...formData });
        onClose();
    } catch (error) {
        console.error("Update failed", error);
    } finally {
        setInternalLoading(false);
    }
  };

  const priorityColors = {
    low: "bg-emerald-500",
    medium: "bg-amber-500",
    high: "bg-rose-500"
  };

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`w-full bg-white dark:bg-slate-950 border transition-all duration-500 sm:rounded-3xl shadow-2xl relative overflow-hidden ${
        isFocused ? "border-indigo-500 ring-4 ring-indigo-500/10" : "border-slate-200 dark:border-slate-800"
      }`}
    >
      {/* Top Animated Bar */}
      <div className="absolute top-0 left-0 w-full h-1 bg-slate-100 dark:bg-slate-800">
        <motion.div 
          className="h-full bg-indigo-600"
          initial={{ width: "100%" }}
          animate={{ width: formData.title ? "100%" : "0%" }}
        />
      </div>

      {/* Header */}
      <div className="px-6 py-5 flex items-center justify-between border-b border-slate-100 dark:border-slate-800 bg-slate-50/30 dark:bg-slate-900/30 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-600 rounded-xl shadow-lg">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white leading-none">Edit Task</h2>
            <p className="text-[10px] text-slate-500 uppercase tracking-tighter mt-1 font-medium">Workspace / Update Mode</p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 rounded-full text-[10px] font-bold text-slate-500">
          <Command className="w-3 h-3" /> <span className="opacity-50">+</span> ENTER TO SAVE
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-6 sm:p-8 space-y-3">
        <div className="space-y-4">
          <input
            name="title"
            required
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            value={formData.title}
            onChange={handleChange}
            placeholder="What needs to be done?"
            className="w-full text-3xl sm:text-4xl font-black bg-transparent border-none focus:outline-none text-slate-900 dark:text-white tracking-tight"
          />
          
          <div className="flex gap-3 items-start group">
            <AlignLeft className="w-5 h-5 mt-1 text-slate-300 group-focus-within:text-indigo-500 transition-colors" />
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Add some details..."
              className="w-full bg-transparent border-none focus:outline-none text-slate-600 dark:text-slate-400 text-lg resize-none min-h-[60px]"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Priority UI */}
          <div className="space-y-3">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Flag className="w-3 h-3" /> Priority Level
            </label>
            <div className="grid grid-cols-3 gap-2 p-1 bg-slate-100 dark:bg-slate-900 rounded-2xl">
              {(['low', 'medium', 'high'] as const).map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, priority: p }))}
                  className={`py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
                    formData.priority === p 
                      ? "bg-white dark:bg-slate-800 text-slate-900 dark:text-white shadow-sm scale-[1.02]" 
                      : "text-slate-500 opacity-60 hover:opacity-100"
                  }`}
                >
                  <div className={`w-1.5 h-1.5 rounded-full ${priorityColors[p]}`} />
                  {p.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          {/* Due Date */}
          <div className="space-y-3">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Calendar className="w-3 h-3" /> Due Date
            </label>
            <input
              type="date"
              name="due_date"
              min={today}
              value={formData.due_date}
              onChange={handleChange}
              className="w-full bg-slate-100 dark:bg-slate-900 text-slate-900 dark:text-slate-200 rounded-2xl p-3.5 text-sm outline-none border-2 border-transparent focus:border-indigo-500/20 transition-all cursor-pointer"
            />
          </div>

          {/* Reminder */}
          <div className="space-y-3">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Clock className="w-3 h-3" /> Set Reminder
            </label>
            <input
              type="datetime-local"
              name="reminder_at"
              min={nowForReminder}
              value={formData.reminder_at}
              onChange={handleChange}
              className="w-full bg-slate-100 dark:bg-slate-900 text-slate-900 dark:text-slate-200 rounded-2xl p-3.5 text-sm outline-none border-2 border-transparent focus:border-indigo-500/20 transition-all cursor-pointer"
            />
          </div>

          {/* Tags */}
          <div className="space-y-3">
            <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Tag className="w-3 h-3" /> Tags
            </label>
            <div className="flex flex-wrap items-center gap-2 bg-slate-100 dark:bg-slate-900 rounded-2xl p-2 min-h-[52px]">
              <AnimatePresence mode="popLayout">
                {formData.tags.map(tag => (
                  <motion.span
                    layout key={tag}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.8, opacity: 0 }}
                    className="flex items-center gap-1.5 bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 px-3 py-1.5 rounded-xl text-[11px] font-bold border border-indigo-100 dark:border-indigo-800/50 shadow-sm"
                  >
                    #{tag}
                    <X className="w-3 h-3 cursor-pointer hover:text-rose-500" onClick={() => handleRemoveTag(tag)} />
                  </motion.span>
                ))}
              </AnimatePresence>
              <input
                value={newTag}
                onChange={e => setNewTag(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') { e.preventDefault(); handleAddTag(); }
                }}
                placeholder="Add tag..."
                className="flex-1 bg-transparent border-none outline-none py-1.5 px-2 text-sm text-slate-700 dark:text-slate-200 min-w-[80px]"
              />
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-8 flex items-center gap-3 border-t border-slate-50 dark:border-slate-900">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-6 py-4 rounded-2xl font-bold text-[11px] uppercase tracking-widest text-slate-400 hover:text-slate-600 transition-all"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={stateLoading || internalLoading || !formData.title}
            className="flex-[2] relative group bg-indigo-600 hover:bg-indigo-700 text-white px-10 py-4 rounded-2xl font-black text-sm transition-all shadow-xl active:scale-95 flex items-center justify-center gap-3"
          >
            {internalLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
              <>Save Changes <Save className="w-5 h-5" /></>
            )}
          </button>
        </div>
      </form>
    </motion.div>
  );
}
